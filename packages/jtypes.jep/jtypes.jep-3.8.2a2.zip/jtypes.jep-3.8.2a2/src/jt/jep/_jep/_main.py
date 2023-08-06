# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from ...jvm.lib.compat import *
from ...jvm.lib import annotate
from ...jvm.lib import public
from ...        import jni

from ._constants import EJavaType
from ._jclass    import PyJClass
from ._jobject   import PyJObject
from ._jarray    import PyJArray
from .._java     import embed
from .           import _util as util


@public
def findClass(name):

    """Find and instantiate a system class, somewhat faster than forName."""

    if not isinstance(name, (builtins.str, str)):
        raise TypeError("argument should be a string")

    jep_thread = embed.get_jepthread()
    if not jep_thread:
        raise RuntimeError("Invalid JepThread pointer.")

    classloader = jep_thread.classloader

    try:
        jclass = classloader.jvm.JClass.forName(name.replace("/", "."))
    except:
        raise RuntimeError("Invalid class object.")

    return PyJClass(jclass)


@public
def forName(name):

    """Find and return a jclass object using the supplied ClassLoader."""

    if not isinstance(name, (builtins.str, str)):
        raise TypeError("argument should be a string")

    jep_thread = embed.get_jepthread()
    if not jep_thread:
        raise RuntimeError("Invalid JepThread pointer.")

    classloader = jep_thread.classloader

    try:
        jclass = classloader.loadClass(name)
    except:
        raise RuntimeError("Invalid class object.")

    return PyJClass(jclass)


@public
def jarray(size, two, value=None):

    """Create a new primitive array in Java.
    Accepts:
    (size, type_ID,  [0]) ||
    (size, JCHAR_ID, [string value]) ||
    (size, jobject) ||
    (size, str) ||
    (size, jarray)"""

    # called from module to create new arrays.
    # args are variable, should accept:
    # 1: (size, comp_jtype_id, [value])
    # 2: (size, PyJObject)
    # 3: (size, PyJArray)

    if not isinstance(size, (int, long)):
        raise ValueError("Unknown arg types.")

    if size < 0:
        raise ValueError("Invalid size {}".format(size))

    jep_thread = embed.get_jepthread() # <AK> added
    if not jep_thread:
        raise RuntimeError("Invalid JepThread pointer.")

    classloader = jep_thread.classloader

    jvm = classloader.jvm

    if isinstance(two, int):

        comp_jclass = None
        comp_jtype  = util.from_jep_jtype.get(two)

        # Blad w jep !!!. Tu bylo: if size < 0:

        # make a new primitive array

        if   comp_jtype == EJavaType.BOOLEAN: jarr = jvm.JArray.newBooleanArray(size)
        elif comp_jtype == EJavaType.CHAR:    jarr = jvm.JArray.newCharArray(size)
        elif comp_jtype == EJavaType.BYTE:    jarr = jvm.JArray.newByteArray(size)
        elif comp_jtype == EJavaType.SHORT:   jarr = jvm.JArray.newShortArray(size)
        elif comp_jtype == EJavaType.INT:     jarr = jvm.JArray.newIntArray(size)
        elif comp_jtype == EJavaType.LONG:    jarr = jvm.JArray.newLongArray(size)
        elif comp_jtype == EJavaType.FLOAT:   jarr = jvm.JArray.newFloatArray(size)
        elif comp_jtype == EJavaType.DOUBLE:  jarr = jvm.JArray.newDoubleArray(size)
        elif comp_jtype == EJavaType.STRING:  jarr = jvm.JArray.newStringArray(size)
        else:
            raise ValueError("Unknown type.")

    elif isinstance(two, PyJObject):

        comp_jclass = two.__javaclass__
        comp_jtype  = EJavaType.OBJECT

        jarr = jvm.JArray.newObjectArray(size, comp_jclass)

    elif isinstance(two, PyJArray):

        comp_jclass = two.__javaclass__
        comp_jtype  = EJavaType.ARRAY

        jarr = jvm.JArray.newObjectArray(size, comp_jclass)

    else:
        raise ValueError("Unknown arg type: expected one of: "
                         "J<foo>_ID, pyjobject, jarray")

    jarray = PyJArray()
    jarray.__javaarray__  = jarr
    jarray.__javaclass__  = jarr.getClass()
    jarray.componentClass = comp_jclass
    jarray.componentType  = comp_jtype
    jarray._pin()
    jarray._init(value)
    return jarray


@public
def jproxy(delegate, interfaces):

    """Create a Proxy class for a Python object.
    Accepts two arguments:
        ([a class object], [list of java interfaces to implement, string names])"""

    if not isinstance(interfaces, (tuple, list)):
        raise TypeError("argument 'interfaces' should be a tuple or list")

    if not interfaces:
        raise ValueError("Empty interface list.")

    for idx, itfname in enumerate(interfaces):
        if not isinstance(itfname, (builtins.str, str)):
            raise ValueError("Item {} not a string.".format(idx))

    jep_thread = embed.get_jepthread()
    if not jep_thread:
        raise RuntimeError("Invalid JepThread pointer.")

    classloader = jep_thread.classloader

    # try
    # {
    # itfname = jenv.NewStringUTF(itfname.encode("utf-8"))
    interfaces = tuple(classloader.loadClass(itfname) for itfname in interfaces)
    # }
    # catch ( ClassNotFoundException exc )
    # {
    #     throw new IllegalArgumentException(exc);
    # }

    class JProxy(classloader.jvm.JProxy):

        def newProxy(self, jep_thread, delegate):

            from ...jvm.jframe import JFrame

            with self.jvm as (jvm, jenv), JFrame(jenv, 4):
                # try
                # {
                jargs = jni.new_array(jni.jvalue, 4)
                jargs[0].j = id(jep_thread)
                jargs[1].j = id(delegate)
                jargs[2].l = jep_thread.caller.handle
                jargs[3].z = False
                ihandler = jenv.NewObject(self.jvm.JepProxyHandler.Class,
                                          self.jvm.JepProxyHandler.Constructor, jargs)
                # }
                # catch ( PyException exc )
                # {
                #     throw new IllegalArgumentException(exc);
                # }
                jargs = jni.new_array(jni.jvalue, 3)
                jargs[0].l = classloader.handle
                jargs[1].l = self._jitf_array
                jargs[2].l = ihandler
                jproxy = jenv.CallStaticObjectMethod(jvm.Proxy.Class,
                                                     jvm.Proxy.newProxyInstance, jargs)
                return self.jvm.JObject(jenv, jproxy) if jproxy else None

    proxy = JProxy(interfaces)
    proxy = proxy.newProxy(jep_thread, delegate)

    if proxy is None:
        raise RuntimeError("Unknown")

    return PyJObject(proxy)
