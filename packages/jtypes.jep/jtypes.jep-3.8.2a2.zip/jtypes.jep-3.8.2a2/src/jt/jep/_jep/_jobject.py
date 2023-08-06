# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from __future__ import absolute_import

import types

from ...jvm.lib.compat import *
from ...jvm.lib.compat import PY3
from ...jvm.lib import py2compatible
from ...jvm.lib import annotate, Optional
from ...jvm.lib import public

from ._constants import EJavaType
from ._constants import EJavaModifiers
from ._constants import EMatchType
from .           import _util as util

from .._java import java_lang_Comparable_compareTo


@public
class PyJType(type):

    # Equivalent of: jt.JavaClass

    @classmethod
    @annotate(jclass='jt.jvm.JClass')
    def _process_inner_classes(cls, jclass):

        from ._jclass import PyJClass

        classes = {}

        for inner_jclass in jclass.getDeclaredClasses():
            mods = inner_jclass.getModifiers()
            is_public = EJavaModifiers.PUBLIC in mods
            if is_public:
                inner_cname = inner_jclass.getSimpleName()
                classes[inner_cname] = PyJClass(inner_jclass)

        return classes

    @classmethod
    @annotate(jclass='jt.jvm.JClass')
    def _process_constructors(cls, jclass):

        from ._jmethod import PyJConstructor

        constructors = []

        for jconstructor in jclass.getConstructors():
            pyjconstructor = PyJConstructor(jconstructor)
            constructors.append(pyjconstructor)

        return constructors

    @classmethod
    @annotate(jclass='jt.jvm.JClass')
    def _process_methods(cls, jclass):

        from ._jmethod import PyJMethod, PyJMultiMethod

        methods = {}

        for jmethod in jclass.getMethods():

            # For every method of this name, check to see if a PyJMethod or
            # PyJMultiMethod is already in the cache with the same name. If
            # so, turn it into a PyJMultiMethod or add it to the existing
            # PyJMultiMethod.

            method_name = jmethod.getName()
            if method_name:
                try:
                    cached_method = methods[method_name]
                except KeyError:
                    methods[method_name] = PyJMethod(jmethod)
                else:
                    pyjmethod = PyJMethod(jmethod)
                    if isinstance(cached_method, PyJMethod):
                        methods[method_name] = PyJMultiMethod(pyjmethod, cached_method)
                    elif isinstance(cached_method, PyJMultiMethod):
                        cached_method._add_overload(pyjmethod)

        return methods

    @classmethod
    @annotate(jclass='jt.jvm.JClass')
    def _process_fields(cls, jclass):

        from ._jfield import PyJField

        fields = {}

        for jfield in jclass.getFields():
            field_name = jfield.getName()
            if field_name:
                fields[field_name] = PyJField(jfield)

        return fields


@public
@py2compatible
class PyJObject(obj):

    """jobject"""

    # "jep.PyJObject" # tp_name
    # Equivalent of: jt.JavaObject

    @annotate(jobject=Optional['jt.jvm.JObject'], jclass=Optional['jt.jvm.JClass'])
    def __new__(cls, jobject=None, jclass=None):

        # Create a new instance of PyJObject or one of it's subtypes that wraps
        # the object provided. If the class of the object is known it can be passed
        # in, or the final argument can be None and this function will figure it out.

        self = super(PyJObject, cls).__new__(cls)

        if jobject is None:
            # Special case for classes inherited from PyJObject
            pass
        else:

            if jclass is None:
                jclass = jobject.getClass()

            # There exist situations where a Java method signature has a return
            # type of Object but actually returns a Class or array.  Also if you
            # call Jep.set(String, Object[]) it should be treated as an array, not
            # an object.  Hence this check here to build the optimal Jep type in
            # the interpreter regardless of signature.

           #from ._jarray import PyJArray
           #from ._jarray import jndarray_check, jndarray_to_ndarray

           #jtype = util.get_jtype(jclass)

            #if jtype == EJavaType.CLASS:
           #if jtype == EJavaType.ARRAY:
           #    return PyJArray(jobject.asArray())
           #elif jndarray_check(jobject):
           #    # check for jep/NDArray and autoconvert to numpy.ndarray instead of PyJObject
           #    return jndarray_to_ndarray(jobject)

        self.__javaobject__ = jobject  # jt.jvm.JObject
        self.__javaclass__  = jclass   # jt.jvm.JClass
        self.__init()
        return self

    @classmethod
    @annotate(jobject='jt.jvm.JObject', jclass=Optional['jt.jvm.JClass'])
    def jobject_As_PyJObject(cls, jobject, jclass=None):

        from ._jcollection    import PyJIterable, PyJIterator
        from ._jcollection    import PyJCollection, PyJList, PyJMap
        from ._jautocloseable import PyJAutoCloseable
        from ._jclass         import PyJClass
        from ._jnumber        import PyJNumber

        if jclass is None:
            jclass = jobject.getClass()

        with jobject.jvm as (jvm, jenv):
            IterableClass      = jobject.jvm.JClass(None, jvm.Iterable.Class,                    borrowed=True)
            CollectionClass    = jobject.jvm.JClass(None, jobject.jvm.java_util.CollectionClass, borrowed=True)
            ListClass          = jobject.jvm.JClass(None, jobject.jvm.java_util.ListClass,       borrowed=True)
            MapClass           = jobject.jvm.JClass(None, jobject.jvm.java_util.MapClass,        borrowed=True)
            IteratorClass      = jobject.jvm.JClass(None, jobject.jvm.java_util.IteratorClass,   borrowed=True)
            AutoCloseableClass = jobject.jvm.JClass(None, jvm.AutoCloseable.Class,               borrowed=True)
            ClassClass         = jobject.jvm.JClass(None, jvm.Class.Class,                       borrowed=True)
            NumberClass        = jobject.jvm.JClass(None, jvm.Number.Class,                      borrowed=True)

            if IterableClass.isInstance(jobject):
                if not CollectionClass.isInstance(jobject):
                    self = PyJIterable(jobject)
                elif ListClass.isInstance(jobject):
                    self = PyJList(jobject)
                else:
                    self = PyJCollection(jobject)
            elif MapClass.isInstance(jobject):
                self = PyJMap(jobject)
            elif IteratorClass.isInstance(jobject):
                self = PyJIterator(jobject)
            elif AutoCloseableClass.isInstance(jobject):
                self = PyJAutoCloseable(jobject)
            elif jenv.IsSameObject(jclass.handle, ClassClass.handle):
                result = PyJClass(jobject.asClass())
            elif NumberClass.isInstance(jobject):
                self = PyJNumber(jobject)
            else:
                self = PyJObject(jobject)
            return self

    def __init(self):

        # Set the object attributes from the cache

        # the fully-qualified name of the object's Java class
        java_class_name = self.__javaclass__.getName()

        # Performance improvement.  The code below is very similar to previous
        # versions except methods and fields are now cached in memory.
        #
        # Previously every time you instantiate a PyJObject, Jep would get the
        # complete list of methods through reflection, turn them into PyJMethods,
        # and add them as attributes to the PyJObject.
        #
        # Now Jep retains a Python dictionary in memory with a key of the fully
        # qualified Java classname to a list of PyJMethods and PyJMultiMethods.
        # Since the Java methods will never change at runtime for a particular
        # Class, this is safe and drastically speeds up PyJObject instantiation
        # by reducing reflection calls. We continue to set and reuse the
        # PyJMethods and PyJMultiMethods attributes on the PyJObject instance,
        # but if __getattr__ sees a PyJMethod or PyJMultiMethod, it will
        # put it inside a PyMethod and return that, enabling the reuse of the
        # PyJMethod or PyJMultiMethod for this particular object instance.
        #
        # We have the GIL at this point, so we can safely assume we're
        # synchronized and multiple threads will not alter the dictionary at the
        # same time.

        # - GetMethodID fails when you pass the jclass object,
        #   it expects a java.lang.Class jobject.
        # - if you CallObjectMethod with the langClass jclass object,
        #   it'll return an array of methods, but they're methods of the
        #   java.lang.reflect.Method class -- not .__javaobject__.
        #
        # so what i did here was find the methodid using langClass,
        # but then i call the method using jclass. methodIds for java
        # classes are shared....

        from .._java import embed

        jep_thread = embed.get_jepthread()
        if not jep_thread:
            raise RuntimeError("Invalid JepThread pointer.")

        try:
            cached_attrs = jep_thread.fqnToPyJAttrs[java_class_name]
        except KeyError:

            methods = PyJType._process_methods(self.__javaclass__)
            fields  = PyJType._process_fields(self.__javaclass__)

            cached_attrs = {}
            cached_attrs.update(methods)
            cached_attrs.update(fields)

            # finalize cache update
            jep_thread.fqnToPyJAttrs[java_class_name] = cached_attrs

        if self.__javaobject__:
            self._attr_dict = cached_attrs  # dict for get/set attr
        else:
            # PyJClass may add additional attributes so use a copy
            self._attr_dict = cached_attrs.copy()  # dict for get/set attr

    # Attach the attribute java_name to the PyJObject instance to assist
    # developers with understanding the type at runtime.
    #
    java_name = property(lambda self: self.__javaclass__.getName())

    __dict__ = property(lambda self: self._attr_dict)

    def __getattr__(self, name):

        # uses obj._attr_dict dictionary for storage.

        #!!! print("@@@ PyJObject.__getattr__({}, '{}'):".format(type(self).__name__, name))
        #!!! print("@@@ PyJObject.dir(self):", dir(self))
        #!!! print("@@@ PyJObject.dir({}):".format(type(self).__name__), dir(type(self)))

        from ._jfield  import PyJField
        from ._jmethod import PyJMethod, PyJMultiMethod

        #attr = PyObject_GenericGetAttr(self, name)
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            try:
                attr = self._attr_dict[name]
            except KeyError:
                raise AttributeError("'{}' object has no attribute '{}'.".format(
                                     self.__javaclass__.getName(), name))

        if isinstance(attr, PyJField):
            return attr.__get__(self, type(self))
        elif isinstance(attr, (PyJMethod, PyJMultiMethod)):

            # TODO Should not bind non-static methods to PyJClass objects,
            # but not sure yet how to handle multimethods and static methods.

            # Bind the method to the jobject so that the jobject
            # will be the first arg when method is called.

            return (types.MethodType(attr, self) if PY3 else
                    types.MethodType(attr, self, type(self)))
        else:
            return attr

    def __setattr__(self, name, value):

        # uses obj._attr_dict dictionary for storage.

        from ._jfield  import PyJField
        from ._jmethod import PyJMethod, PyJMultiMethod

        if (name in ("__javaclass__","__javaobject__","_attr_dict", "__cache__") or
            name.startswith("_PyJObject__") or name.startswith("_PyJClass__")):
            super(PyJObject, self).__setattr__(name, value)
            return

        try:
            attr = self._attr_dict[name]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'.".format(
                                 self.__javaclass__.getName(), name))

        if isinstance(attr, PyJField):
            attr.__set__(self, value)
        else:
            raise AttributeError("'{}' object cannot assign to {} '{}'.".format(
                                 self.__javaclass__.getName(),
                                 "method" if isinstance(attr, (PyJMethod,
                                                               PyJMultiMethod)) else "attribute",
                                 name))

    def __delattr__(self, name):

        from ._exceptions import TypeError

        raise TypeError("Deleting attributes from PyJObjects is not allowed.")

    def __hash__(self):

        target = self.__javaobject__ or self.__javaclass__

        hash = int(target.hashCode())

        # This seems odd but Python expects -1 for error occurred.
        # Other Python built-in types then return -2 if the actual hash is -1.

        return -2 if hash == -1 else hash

    def __eq__(self, other):

        if self is other:
            return True

        if not isinstance(other, PyJObject):
            return NotImplemented

        self_target  = self.__javaobject__  or self.__javaclass__
        other_target = other.__javaobject__ or other.__javaclass__

        return self_target.equals(other_target)

    def __ne__(self, other):

        eq = self.__eq__(other)
        return NotImplemented if eq is NotImplemented else not eq

    def __lt__(self, other):

        compare = self.__compare_to(other)
        return NotImplemented if compare is NotImplemented else (compare == -1)

    def __gt__(self, other):

        compare = self.__compare_to(other)
        return NotImplemented if compare is NotImplemented else (compare == 1)

    def __le__(self, other):

        eq = self.__eq__(other)
        if eq is not NotImplemented and eq: return True
        lt = self.__lt__(other)
        return NotImplemented if lt is NotImplemented else lt

    def __ge__(self, other):

        eq = self.__eq__(other)
        if eq is not NotImplemented and eq: return True
        gt = self.__gt__(other)
        return NotImplemented if gt is NotImplemented else gt

    def __compare_to(self, other):

        if self is other:
            return 0

        if not isinstance(other, PyJObject):
            return NotImplemented

        self_target  = self.__javaobject__  or self.__javaclass__
        other_target = other.__javaobject__ or other.__javaclass__

        if self_target is other_target:
            return 0

        if self_target.handle == other_target.handle:
            return 0

        # All Java objects have equals, but we must rely on Comparable
        # for the more advanced operators.  Java generics cannot actually
        # enforce the type of other in self.compareTo(other) at runtime,
        # but for simplicity let's assume if they got it to compile, the
        # two types can be compared. If the types aren't comparable to
        # one another, a ClassCastException will be thrown.
        #
        # In Python 2 we will allow the ClassCastException to halt the
        # comparison, because it will most likely return
        # NotImplemented in both directions and Python 2 will devolve to
        # comparing the pointer address.
        #
        # In Python 3 we will catch the ClassCastException and return
        # NotImplemented, because there's a chance the reverse comparison
        # of other.compareTo(self) will work.  If both directions return
        # NotImplemented (due to ClassCastException), Python 3 will raise
        # a TypeError.

        jvm, _ = self_target.jvm

        ComparableClass = self_target.jvm.JClass(None, jvm.Comparable.Class, borrowed=True)
        #!!! bylo isInstance(self.__javaobject__). Chyba powinno byc (self_target) !!!
        if not ComparableClass.isInstance(self_target):
            raise TypeError("Invalid comparison operation for "
                            "Java type {}".format(self.__javaclass__.getName()))

        return java_lang_Comparable_compareTo(self_target, other_target)

    def __str__(self):

        target = self.__javaobject__ or self.__javaclass__

        result = target.toString() if target else None
        # python doesn't like None here...
        return result or u""

    def synchronized(self):

        """synchronized that emulates Java's synchronized { obj } and returns
        a Python ContextManager"""

        from ._jmonitor import PyJMonitor

        target = self.__javaobject__ or self.__javaclass__

        return PyJMonitor(target)
