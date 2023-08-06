# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from __future__ import absolute_import

from itertools import count

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Union
from ...jvm.lib import public
from ...jvm.lib import cached

from ._constants import EJavaType
from ._constants import EJavaModifiers
from ._constants import EMatchType
from ._jobject   import PyJObject
from ._jarray    import PyJArray


@public
class PyJMethod(obj):

    """jmethod"""

    # "jep.PyJMethod" # tp_name
    # Equivalent of: jt.JavaMethodOverload

    # A callable python object which wraps a java method and is dynamically added
    # to a PyJObject using setattr. Most of the fields in this object are lazy
    # loaded and care should be taken to ensure they are populated before accessing
    # them. The only fields that are not lazily loaded are rmethod.

    class ParamInfo(object):

        __slots__ = ('thandler', 'is_mutable', 'is_output')

        def __init__(self, thandler):

            self.thandler   = thandler
            self.is_mutable = False
            self.is_output  = False

    class ReturnInfo(object):

        __slots__ = ('thandler',)

        def __init__(self, thandler):

            self.thandler = thandler

    @annotate(method=Union['jt.jvm.JConstructor', 'jt.jvm.JMethod'])
    def __new__(cls, method):

        self = super(PyJMethod, cls).__new__(cls)
        self._jmethod     = method  # Union[jt.jvm.JConstructor, jt.jvm.JMethod]
        self._params_info = None
        self._return_info = None
        self._is_static   = False
        return self

    @cached
    def _init(self):

        type_manager = self._jmethod.jvm.type_manager
        self._params_info = tuple(self.ParamInfo(type_manager.get_handler(jclass))
                                  for jclass in self._jmethod.getParameterTypes())
        jclass = self._jmethod.getReturnType()
        self._return_info = self.ReturnInfo(type_manager.get_handler(jclass))
        mods = self._jmethod.getModifiers()
        self._is_static = EJavaModifiers.STATIC in mods

    __name__ = property(lambda self: self._jmethod.getName(), doc="method name")

    def __call__(self, *args, **kwargs):

        from ._exceptions import TypeError

        if kwargs:
            raise TypeError("Keywords are not supported.")

        self._init()

        this = args[0]  # jep.PyJObject
        args = args[1:]

        arg_count  = len(args)
        par_count  = len(self._params_info)
        is_varargs = self._jmethod.isVarArgs()
        perm_count = (par_count - 1) if is_varargs else par_count

        if (arg_count < perm_count) if is_varargs else (arg_count != perm_count):
            raise RuntimeError("Invalid number of arguments: {}, expected {}.".format(
                               arg_count + 1, par_count + 1))

        if not isinstance(this, PyJObject):
            raise RuntimeError("First argument to a java method must be a java object.")

        if self._is_static:
            return self.__call_static(this, *args)
        else:
            return self.__call_instance(this, *args)

    def __call_static(self, this, *args):

        jclass = this.__javaclass__
        jargs = self._make_arguments(args)
        result = self._return_info.thandler.callStatic(self._jmethod, jclass, jargs)
        self._close_arguments(jargs, args)
        return result

    def __call_instance(self, this, *args):

        jthis = this.__javaobject__
        if jthis is None:
            raise RuntimeError("Instantiate this class before calling an object method.")
        jargs = self._make_arguments(args)
        result = self._return_info.thandler.callInstance(self._jmethod, jthis, jargs)
        self._close_arguments(jargs, args)
        return result

    def _make_arguments(self, args):

        from ..__config__ import config

        self._init()

        arg_count  = len(args)
        par_descrs = self._params_info
        par_count  = len(par_descrs)
        is_varargs = self._jmethod.isVarArgs()
        perm_count = (par_count - 1) if arg_count != par_count else par_count

        jargs = self._jmethod.jvm.JArguments(par_count)
        for pos, pdescr, arg in zip(count(), par_descrs, args):
            thandler = pdescr.thandler
            if config.getboolean("WITH_VALID", False) and not thandler.valid(arg):
                raise ValueError("Parameter value is not valid for required parameter type.")
            thandler.setArgument(pdescr, jargs, pos, arg)

        return jargs

    def _close_arguments(self, jargs, args):

        par_descrs = self._params_info
        par_count  = len(par_descrs)

        # re pin array objects if needed
        found_array = any((pd.thandler.javaType == EJavaType.ARRAY)
                          for pd in par_descrs)
        if found_array:
            for arg in args:
                if isinstance(arg, PyJArray):
                    arg._pin()

    def _match_args(self, args):

        # Check if a method is compatible with the types of a tuple of arguments.
        # This will return a 0 if the arguments are not valid for this method and a
        # positive integer if the arguments are valid. Larger numbers indicate a better
        # match between the arguments and the expected parameter types. This function
        # uses thandler.match to determine how well arguments match. This function
        # does not need to be called before using calling this method, it is only
        # necessary for resolving method overloading.

        self._init()

        arg_count  = len(args)
        par_descrs = self._params_info
        par_count  = len(par_descrs)
        is_varargs = self._jmethod.isVarArgs()
        perm_count = (par_count - 1) if is_varargs else par_count

        if arg_count != (par_count + 1):
            return EMatchType.NONE

        from . import _typehandler as thandler

        match_total = 1
        for pos, pdescr in enumerate(par_descrs):
            arg = args[pos + 1]
            par = pdescr.thandler._jclass
            try:
                match_level = thandler.match(arg, par)
            except:
                raise #!!! break
            if match_level == EMatchType.NONE:
                break
            match_total += match_level

        return match_total


@public
class PyJConstructor(PyJMethod):

    """jconstructor"""

    # "jep.PyJConstructor" # tp_name
    # Equivalent of: jt.JavaMethodOverload

    @annotate(constructor='jt.jvm.JConstructor')
    def __new__(cls, constructor):

        self = super(PyJConstructor, cls).__new__(cls, constructor)
        self._is_static = True

        # PyJConstructor does not currently initialize lazily because PyJMethod
        # does not provide a mechanism to override the lazy loading and
        # PyJMethod._init() does not work for a PyJConstructor. There isn't much
        # value in lazy loading anyway since constructors aren't created until
        # a class has been called.

        self._init()
        return self

    @cached
    def _init(self):

        type_manager = self._jmethod.jvm.type_manager
        self._params_info = tuple(self.ParamInfo(type_manager.get_handler(jclass))
                                  for jclass in self._jmethod.getParameterTypes())

    __name__ = property(lambda self: "<init>", doc="method name")

    def __call__(self, *args, **kwargs):

        from ._jclass     import PyJClass
        from ._exceptions import TypeError

        if kwargs:
            raise TypeError("Keywords are not supported.")

        self._init()

        jclass = args[0]  # jep.PyJClass
        args   = args[1:]

        arg_count = len(args)
        par_count = len(self._params_info)

        if arg_count != par_count:
            raise RuntimeError("Invalid number of arguments: {}, expected {}.".format(
                               arg_count + 1, par_count + 1))

        if not isinstance(jclass, PyJClass):
            raise RuntimeError("First argument to a java constructor must be a java class.")

        return self.__call_constructor(jclass, *args)

    def __call_constructor(self, jclass, *args):

        from ...jvm.jframe import JFrame
        from ...jvm.java.org.python.embed import ThreadState

        jclass = jclass.__javaclass__
        jargs = self._make_arguments(args)
        with self._jmethod.jvm as (jvm, jenv), JFrame(jenv, 1):
           #!!!with ThreadState(None):
            jobj = jenv.NewObject(jclass.handle, self._jmethod._jcid(jenv), jargs.arguments)
            jobj = self._jmethod.jvm.JObject(jenv, jobj)
        pyobj = PyJObject.jobject_As_PyJObject(jobj, jclass)
        self._close_arguments(jargs, args)  # tu byl blad. bylo args zamiast args[1:]
        return pyobj


@public
class PyJMultiMethod(object):

    """PyJMultiMethod wraps multiple java methods from the same class with the same
    name as a single callable python object."""

    # "jep.PyJMultiMethod" # tp_name
    # Equivalent of: jt.JavaMethod | jt.JavaConstructor

    @annotate(method1=PyJMethod, method2=PyJMethod)
    def __new__(cls, method1, method2):

        # Both args must be PyJMethods. A minimum of 2 methods is required
        # to make a PyJMultiMethod, after creation it is possible to add
        # more than two methods using PyJMultiMethod._add_overload.

        if not (isinstance(method1, PyJMethod) and isinstance(method2, PyJMethod)):
            raise TypeError("PyJMultiMethod can only hold PyJMethods")

        self = super(PyJMultiMethod, cls).__new__(cls)
        self.__jmethods = [method1, method2]
        return self

    __name__    = property(lambda self: self.__jmethods[0].__name__)
    __methods__ = property(lambda self: tuple(self.__jmethods))

    def _add_overload(self, method):

        if not isinstance(method, PyJMethod):
            raise TypeError("PyJMultiMethod can only hold PyJMethods")

        self.__jmethods.append(method)

    def __call__(self, *args, **kwargs):

        # If multiple methods have the same number of args then a complex check
        # is done to find the best match, in this case best_match has the current
        # match value for the current candidate method.

        from ._exceptions import TypeError

        if kwargs:
            raise TypeError("Keywords are not supported.")

        method_name = self.__name__

        best_ovr, best_match = self._match_overload(self.__jmethods, *args)

        if best_ovr is None:
            raise NameError("No such Method.")

        if isinstance(best_ovr, list):
            raise RuntimeError("More than one matching method found.")

        return best_ovr(*args)

    def _match_overload(self, overloads, *args):

        # best_ovrs is a candidate methods that passes the simple compatiblity check
        # but the complex check may not have been run.

        arg_count = len(args)

        best_match = EMatchType.NONE
        best_ovrs  = []  # List[jep.PyJMethod, ...]

        for ovr in overloads:
            ovr._init()

            par_count = len(ovr._params_info)

            if arg_count != (par_count + 1):
                continue

            if not best_ovrs:
                best_ovrs = [ovr]
                continue

            if best_match == EMatchType.NONE:
                best_match = best_ovrs[0]._match_args(args)

            if best_match == EMatchType.NONE:
                # best_ovrs was not compatible, replace it with ovr.
                best_ovrs = [ovr]
            else:
                match_level = ovr._match_args(args)
                if match_level > best_match:
                    best_match = match_level
                    best_ovrs  = [ovr]

        if len(best_ovrs) == 0:
            return None, EMatchType.NONE

        return best_ovrs[0] if len(best_ovrs) == 1 else best_ovrs, best_match
