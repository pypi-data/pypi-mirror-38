# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from __future__ import absolute_import

from ...jvm.lib.compat import *
from ...jvm.lib.compat import PY2, PY3
from ...jvm.lib import py2compatible
from ...jvm.lib import annotate, Optional, Tuple
from ...jvm.lib import public
from ...        import jni

from ...jvm.jframe  import JFrame
from ...jvm.jstring import JString
from ...jvm.jarray  import JArray

from ._constants import EJavaType
from ._jobject   import PyJObject
from .           import _util as util


@public
class PyJArray(obj):

    """jarray(size) -> new jarray of size"""

    # "jep.PyJArray" # tp_name
    # Equivalent of: jt.JavaArray

    @annotate(jarray=Optional['jt.jvm.JArray'])
    def __new__(cls, jarray=None):

        # called internally to make new PyJArray instances

        self = super(PyJArray, cls).__new__(cls)
        if jarray is None:
            # Special case
            self.__javaarray__  = None
            self.__javaclass__  = None
            self.componentClass = None
            self.componentType  = -1
            self.pinnedArray    = None
            return self

        self.__javaarray__  = jarray                 # jt.jvm.JArray
        self.__javaclass__  = jarray.getClass()      # jt.jvm.JClass # useful for later calls
        comp_jclass = self.__javaclass__.getComponentType()
        if comp_jclass is None:
            raise RuntimeError("Unknown")
        comp_jtype = util.get_jtype(comp_jclass)
        if comp_jtype < 0:
            raise RuntimeError("Unknown")
        self.componentClass = comp_jclass.getClass() # Optional[jt.jvm.JClass] # component type of object arrays, but not strings
        self.componentType  = comp_jtype             # EJavaType
        self.pinnedArray    = None                   # array elements buffer
        self._pin()
        return self

    def __del__(self):

        _, jenv = self.__javaarray__.jvm
        if jenv:
            # can't guarantee mode 0 will work in this case...
            self._release_pinned(False)

    def _init(self, value=None):

        if self.componentType == EJavaType.BOOLEAN:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jboolean, value if isinstance(value, (bool, int, long)) else False)
            for idx in range(len(self)):
                dst[idx] = val

        elif self.componentType == EJavaType.CHAR:

            if isinstance(value, (bytes, str)):
                dst = self.pinnedArray.buf
                # we won't throw an error for index, length problems. just deal...
                val = value
                for idx in range(min(len(self), len(val))):
                    dst[idx] = jni.obj(jni.jchar, val[idx])
                val = jni.obj(jni.jchar, u'\0')
                for idx in range(min(len(self), len(val)), len(self)):
                    dst[idx] = val
            else:
                dst = self.pinnedArray.buf
                val = jni.obj(jni.jchar, chr(value) if isinstance(value, int) else '\0')
                for idx in range(len(self)):
                    dst[idx] = val

        elif self.componentType == EJavaType.BYTE:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jbyte, value if isinstance(value, int) else 0)
            for idx in range(len(self)):
                dst[idx] = val

        elif self.componentType == EJavaType.SHORT:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jshort, value if isinstance(value, int) else 0)
            for idx in range(len(self)):
                dst[idx] = val

        elif self.componentType == EJavaType.INT:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jint, value if isinstance(value, int) else 0)
            for idx in range(len(self)):
                dst[idx] = val

        elif self.componentType == EJavaType.LONG:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jlong, value if isinstance(value, (int, long)) else 0)
            for idx in range(len(self)):
                dst[idx] = val

        elif self.componentType == EJavaType.FLOAT:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jfloat, value if isinstance(value, float) else 0.0)
            for idx in range(len(self)):
                dst[idx] = val

        elif self.componentType == EJavaType.DOUBLE:

            dst = self.pinnedArray.buf
            val = jni.obj(jni.jdouble, value if isinstance(value, float) else 0.0)
            for idx in range(len(self)):
                dst[idx] = val

    def _pin(self):

        # pin primitive array memory. NOOP for object arrays.

        if   self.componentType == EJavaType.BOOLEAN: self.pinnedArray = self.__javaarray__.getBooleanBuffer()
        elif self.componentType == EJavaType.CHAR:    self.pinnedArray = self.__javaarray__.getCharBuffer()
        elif self.componentType == EJavaType.BYTE:    self.pinnedArray = self.__javaarray__.getByteBuffer()
        elif self.componentType == EJavaType.SHORT:   self.pinnedArray = self.__javaarray__.getShortBuffer()
        elif self.componentType == EJavaType.INT:     self.pinnedArray = self.__javaarray__.getIntBuffer()
        elif self.componentType == EJavaType.LONG:    self.pinnedArray = self.__javaarray__.getLongBuffer()
        elif self.componentType == EJavaType.FLOAT:   self.pinnedArray = self.__javaarray__.getFloatBuffer()
        elif self.componentType == EJavaType.DOUBLE:  self.pinnedArray = self.__javaarray__.getDoubleBuffer()

    @annotate(mode=Optional[bool])
    def _release_pinned(self, mode=None):

        # used to either release pinned memory, commit, or abort.

        if not self.pinnedArray or (mode is False and not self.pinnedArray.is_copy):
            return

        if   self.componentType == EJavaType.BOOLEAN: self.__javaarray__.releaseBooleanBuffer(self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.CHAR:    self.__javaarray__.releaseCharBuffer   (self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.BYTE:    self.__javaarray__.releaseByteBuffer   (self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.SHORT:   self.__javaarray__.releaseShortBuffer  (self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.INT:     self.__javaarray__.releaseIntBuffer    (self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.LONG:    self.__javaarray__.releaseLongBuffer   (self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.FLOAT:   self.__javaarray__.releaseFloatBuffer  (self.pinnedArray.buf, mode)
        elif self.componentType == EJavaType.DOUBLE:  self.__javaarray__.releaseDoubleBuffer (self.pinnedArray.buf, mode)

    def commit(self):

        """arr.commit() -- commit pinned array to Java memory"""

        self._release_pinned(True)

    def __len__(self):

        return self.__javaarray__.getLength()

    def index(self, value):

        """arr.index(value) -> integer -- return first index of value"""

        pos = self.__index(value)
        if pos < 0:
            raise ValueError("list.index(x): x not in array")
        return pos

    def __contains__(self, value):

        return self.__index(value) >= 0

    def __getitem__(self, idx):

        """x.__getitem__(y) <==> x[y]"""

        if isinstance(idx, slice):

            start, stop, step = idx.indices(len(self))
            return self._getslice(start, stop, step)

        elif isinstance(idx, (int, long)):

            size = len(self)
            if idx < 0: idx += size
            if not (0 <= idx < size):
                raise IndexError("array index out of range: {}".format(idx))

            return self._getitem(idx)

        else:
            raise TypeError("array indices must be integers, longs, or slices")

    def __setitem__(self, idx, value):

        """x.__setitem__(y, v) <==> x[y] = v"""

        if isinstance(idx, slice):

            start, stop, step = idx.indices(len(self))
            self._setslice(start, stop, step, value)

        elif isinstance(idx, (int, long)):

            size = len(self)
            if idx < 0: idx += size
            if not (0 <= idx < size):
                raise IndexError("array index out of range: {}".format(idx))

            self._setitem(idx, value)

        else:
            raise TypeError("array indices must be integers, longs, or slices")

    def _getitem(self, idx):

        if self.componentType == EJavaType.BOOLEAN:

            return bool(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.CHAR:

            #!!! Sprawdzic czy dziala tak jak jchar_As_PyObject() (szczegolnie dla PY2) !!!
            ustr = self.pinnedArray.buf[idx]
            return ustr.encode("utf-8") if PY2 else ustr

        elif self.componentType == EJavaType.BYTE:

            return int(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.SHORT:

            return int(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.INT:

            return int(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.LONG:

            #!!! moze int? w orginale bylo long !!!
            return long(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.FLOAT:

            return float(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.DOUBLE:

            return float(self.pinnedArray.buf[idx])

        elif self.componentType == EJavaType.STRING:

            return self.__javaarray__.getString(idx)

        elif self.componentType == EJavaType.OBJECT:

            jobj = self.__javaarray__.getObject(idx)
            return PyJObject(jobj) if jobj is not None else None

        elif self.componentType == EJavaType.ARRAY:

            jobj = self.__javaarray__.getObject(idx)
            return PyJArray(jobj.asArray()) if jobj is not None else None

        else:
            raise TypeError("Unknown type {}.".format(self.componentType))

    def _setitem(self, idx, value):

        if self.componentType == EJavaType.BOOLEAN:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, (bool, int, long)):
                raise TypeError("Expected boolean.")

            self.pinnedArray.buf[idx] = jni.obj(jni.jboolean, value)

        elif self.componentType == EJavaType.CHAR:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if (not isinstance(value, int) and
                not (isinstance(value, (bytes, str)) and len(value) == 1)):
                raise TypeError("Expected char.")

            value = chr(value) if isinstance(value, int) else value

            self.pinnedArray.buf[idx] = jni.obj(jni.jchar, value)

        elif self.componentType == EJavaType.BYTE:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, int):
                raise TypeError("Expected byte.")

            print("=========")
            self.pinnedArray.buf[idx] = 12
            print("KK  12  KK {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = 13
            print("KK  13  KK {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = 111111
            print("K 111111 K {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = 13
            print("KK  13  KK {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = jni.obj(jni.jbyte, 111111)
            print("K(111111)K {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = 13
            print("KK  13  KK {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = value
            print("KK value K {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = 13
            print("KK  13  KK {}".format(self.pinnedArray.buf[idx]))
            self.pinnedArray.buf[idx] = jni.obj(jni.jbyte, value)
            print("KK(value)K {}".format(self.pinnedArray.buf[idx]))
            print("==== ====")

        elif self.componentType == EJavaType.SHORT:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, int):
                raise TypeError("Expected int.")

            self.pinnedArray.buf[idx] = jni.obj(jni.jshort, value)

        elif self.componentType == EJavaType.INT:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, int):
                raise TypeError("Expected int.")

            self.pinnedArray.buf[idx] = jni.obj(jni.jint, value)

        elif self.componentType == EJavaType.LONG:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, (int, long)):
                raise TypeError("Expected long.")

            self.pinnedArray.buf[idx] = jni.obj(jni.jlong, value)

        elif self.componentType == EJavaType.FLOAT:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, float):
                raise TypeError("Expected float.")

            self.pinnedArray.buf[idx] = jni.obj(jni.jfloat, value)

        elif self.componentType == EJavaType.DOUBLE:

            if not self.pinnedArray:
                raise RuntimeError("Pinned array shouldn't be null.")

            if not isinstance(value, float):
                raise TypeError("Expected float.")

            self.pinnedArray.buf[idx] = jni.obj(jni.jdouble, value)

        elif self.componentType == EJavaType.STRING:

            if value is None:
                with self.__javaarray__.jvm as (jvm, jenv):
                    jstr = jni.obj(jni.jstring)
                    jenv.SetObjectArrayElement(self.__javaarray__.handle, idx, jstr)
            else:
                if not isinstance(value, (bytes, str)):
                    raise TypeError("Expected string.")

                #!!! nie zrobic kodowania na byte? (const char *) value !!!
                with self.__javaarray__.jvm as (jvm, jenv), JFrame(jenv, 1):
                    jstr = jenv.NewStringUTF(value if isinstance(value, bytes) else value.encode("utf-8"))
                    jenv.SetObjectArrayElement(self.__javaarray__.handle, idx, jstr)

        elif self.componentType == EJavaType.OBJECT:

            if value is None:
                jobj = jni.NULL
            else:
                if not isinstance(value, PyJObject):
                    raise TypeError("Expected jobject.")

                if value.__javaobject__ is None:
                    raise TypeError("Expected instance, not class.")

                jobj = value.__javaobject__.handle

            with self.__javaarray__.jvm as (jvm, jenv):
                jenv.SetObjectArrayElement(self.__javaarray__.handle, idx, jobj)

        elif self.componentType == EJavaType.ARRAY:

            if value is None:
                jarr = jni.obj(jni.jobjectArray)
            else:
                if not isinstance(value, PyJArray):
                    raise TypeError("Expected jarray.")

                jarr = value.__javaarray__.handle

            with self.__javaarray__.jvm as (jvm, jenv):
                jenv.SetObjectArrayElement(self.__javaarray__.handle, idx, jarr)

        else:
            raise TypeError("Unknown type.")

    def _getslice(self, start, stop, step):

        if self.componentType == EJavaType.BOOLEAN:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newBooleanArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.CHAR:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newCharArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.BYTE:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newByteArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.SHORT:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newShortArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.INT:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newIntArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.LONG:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newLongArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.FLOAT:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newFloatArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.DOUBLE:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newDoubleArray(size))

            src = self.pinnedArray.buf
            dst = jarr.pinnedArray.buf
            for ix, idx in enumerate(range(start, stop, step)):
                dst[ix] = src[idx]

            return jarr

        elif self.componentType == EJavaType.STRING:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newStringArray(size))

            with self.__javaarray__.jvm as (jvm, jenv):
                src = self.__javaarray__.handle
                dst = jarr.__javaarray__.handle
                for ix, idx in enumerate(range(start, stop, step)):
                    with JFrame(jenv, 1):
                        jobj = jenv.GetObjectArrayElement(src, idx)
                        jenv.SetObjectArrayElement(dst, ix, jobj)

            return jarr

        elif self.componentType == EJavaType.OBJECT:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newObjectArray(size, self.componentClass))

            with self.__javaarray__.jvm as (jvm, jenv):
                src = self.__javaarray__.handle
                dst = jarr.__javaarray__.handle
                for ix, idx in enumerate(range(start, stop, step)):
                    with JFrame(jenv, 1):
                        jobj = jenv.GetObjectArrayElement(src, idx)
                        jenv.SetObjectArrayElement(dst, ix, jobj)

            return jarr

        elif self.componentType == EJavaType.ARRAY:

            size = JArray.size(start, stop, step)
            jarr = PyJArray(self.__javaarray__.jvm.JArray.newObjectArray(size, self.componentClass))

            with self.__javaarray__.jvm as (jvm, jenv):
                src = self.__javaarray__.handle
                dst = jarr.__javaarray__.handle
                for ix, idx in enumerate(range(start, stop, step)):
                    with JFrame(jenv, 1):
                        jobj = jenv.GetObjectArrayElement(src, idx)
                        jenv.SetObjectArrayElement(dst, ix, jobj)

            return jarr

        else:
            raise ValueError("Unsupported type.")

    def _setslice(self, start, stop, step, value):

        raise NotImplementedError()

    @annotate(int)
    def __index(self, value):

        if self.componentType == EJavaType.BOOLEAN:

            if not isinstance(value, (bool, int, long)):
                raise TypeError("Expected boolean.")

            value = bool(value)

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.CHAR:

            if (not isinstance(value, int) and
                not (isinstance(value, (bytes, str)) and len(value) == 1)):
                raise TypeError("Expected char.")

            value = chr(value) if isinstance(value, int) else value

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.BYTE:

            if not isinstance(value, int):
                raise TypeError("Expected byte.")

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.SHORT:

            if not isinstance(value, int):
                raise TypeError("Expected int (short).")

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.INT:

            if not isinstance(value, int):
                raise TypeError("Expected int.")

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.LONG:

            if not isinstance(value, (int, long)):
                raise TypeError("Expected long.")

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.FLOAT:

            if not isinstance(value, float):
                raise TypeError("Expected long.")

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.DOUBLE:

            if not isinstance(value, float):
                raise TypeError("Expected long.")

            for idx in range(len(self)):
                if self._getitem(idx) == value:
                    return idx
            else:
                return -1

        elif self.componentType == EJavaType.STRING:

            if value is not None and not isinstance(value, (bytes, str)):
                raise TypeError("Expected str.")

            jarr = self.__javaarray__.handle
            with self.__javaarray__.jvm as (jvm, jenv):
                for idx in range(len(self)):
                    with JFrame(jenv, 1):
                        jstr = jenv.GetObjectArrayElement(jarr, idx)
                        if jstr:
                            if (value is not None and
                                JString(jenv, jstr, borrowed=True).str == value):
                                return idx
                        elif value is None:
                            return idx
                else:
                    return -1

        elif self.componentType == EJavaType.OBJECT:

            if value is not None and not isinstance(value, PyJObject):
                raise TypeError("Expected jobject.")

            jarr = self.__javaarray__.handle
            with self.__javaarray__.jvm as (jvm, jenv):
                for idx in range(len(self)):
                    with JFrame(jenv, 1):
                        jobj = jenv.GetObjectArrayElement(jarr, idx)
                        if jobj:
                            if (value is not None and
                                jenv.IsSameObject(jobj, value.__javaobject__.handle)):
                                return idx
                        elif value is None:
                            return idx
                else:
                    return -1

        elif self.componentType == EJavaType.ARRAY:

            if value is not None and not isinstance(value, PyJArray):
                raise TypeError("Expected jarray.")

            jarr = self.__javaarray__.handle
            with self.__javaarray__.jvm as (jvm, jenv):
                for idx in range(len(self)):
                    with JFrame(jenv, 1):
                        jobj = jenv.GetObjectArrayElement(jarr, idx)
                        if jobj:
                            if (value is not None and
                                jenv.IsSameObject(jobj, value.__javaarray__.handle)):
                                return idx
                        elif value is None:
                            return idx
                else:
                    return -1

        else:
            raise RuntimeError("Unknown type {}.".format(self.componentType))

    def __str__(self):

        if PY3:
            jstr = self.__javaarray__.toString() if self.__javaarray__ is not None else None
            # python doesn't like None here...
            return jstr if jstr is not None else ""
        else:
            # retained to not break former behavior

            if not self.pinnedArray:
                raise RuntimeError("No pinned array.")

            if self.componentType == EJavaType.BYTE:
                #!!! !!! 
                return PyBytes_FromStringAndSize(self.pinnedArray.buf, len(self))
            else:
                raise TypeError("Unsupported type for str operation.")

    def __iter__(self):

        return PyJArrayIter(self)


@py2compatible
class PyJArrayIter(object):

    """jep.PyJArrayIter"""

    # "jep.PyJArrayIter" # tp_name

    def __new__(cls, arr):

        self = super(PyJArrayIter, cls).__new__(cls)
        #!!! moze raczej weak ? !!!
        self._arr = arr  # PyJArray - Set to None when iterator is exhausted
        self._idx = 0
        return self

    def __iter__(self):

        return self

    def __next__(self):

        if self._arr is None or self._idx >= len(self._arr):
            self._arr = None
            raise StopIteration

        item = self._arr._getitem(self._idx)
        self._idx += 1
        return item

    def __len__(self):

        if self._arr is None or self._idx >= len(self._arr):
            return 0

        return len(self._arr) - self._idx

    #(getattrofunc) pyjarrayiter.__del__, # tp_getattro !!! pomylka w orginale? !!!
    #
    #PyObject* pyjarrayiter_getattr(PyObject *one, PyObject *two):
    #
    #    return PyObject_GenericGetAttr(one, two)


@annotate(bool, obj=object)
def ndarray_check(obj):

    from ..__config__ import config

    if not config.getboolean("NUMPY_ENABLED", True):
        return False

    try:
        import numpy as np
    except ImportError:
        return False
    else:
        return isinstance(obj, np.ndarray)


@annotate(bool, jobj='jt.jvm.JObject')
def jndarray_check(jobj):

    # Checks if a jobject is an instance of a jep.NDArray
    #
    # @param jobj  the jobject to check
    #
    # @return true if it is an NDArray and jep was compiled with numpy support,
    #         otherwise false

    from ..__config__ import config

    if not config.getboolean("NUMPY_ENABLED", True):
        return False

    with jobj.jvm as (jvm, jenv):
        JepNDArray_Class = jobj.jvm.JClass(None, jobj.jvm.JepNDArray.Class, borrowed=True)
        return JepNDArray_Class.isInstance(jobj)


@annotate(bool, jobj='jt.jvm.JObject')
def jdndarray_check(jobj):

    # Checks if a jobject is an instance of a jep.DirectNDArray
    #
    # @param jobj  the jobject to check
    #
    # @return true if it is an DirectNDArray and jep was compiled with numpy
    #          support, otherwise false

    from ..__config__ import config

    if not config.getboolean("NUMPY_ENABLED", True):
        return False

    with jobj.jvm as (jvm, jenv):
        JepDNDArray_Class = jobj.jvm.JClass(None, jobj.jvm.JepDirectNDArray.Class, borrowed=True)
        return JepDNDArray_Class.isInstance(jobj)


#if NUMPY_ENABLED:

@annotate('jt.jvm.JObject', ndarr='np.ndarray')
def ndarray_to_jndarray(ndarr):

    # Convert a numpy ndarray to a jep.NDArray.
    #
    # @param ndarr  the numpy ndarray to convert
    #
    # @return a new jep.NDArray or NULL if errors are encountered

    import numpy as np

    from ...jvm.jframe import JFrame

    # setup the primitive array arg
    jarr = ndarray_to_jprimitivearray(ndarr)

    with jarr.jvm as (jvm, jenv), JFrame(jenv, 2):

        # setup the int[] constructor arg
        ndims = ndarr.ndim
        dims  = ndarr.shape
        jdims = jni.new_array(jni.jint, ndims)
        for i in range(ndims): jdims[i] = jni.obj(jni.jint, dims[i])
        jdimarr = jenv.NewIntArray(ndims)
        jenv.SetIntArrayRegion(jdimarr, 0, ndims, jdims)
        del jdims
        del dims

        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].l = jarr.handle
        jargs[1].l = jdimarr
        jobj = jenv.NewObject(jarr.jvm.JepNDArray.Class,
                              jarr.jvm.JepNDArray.Constructor, jargs)
        return jarr.jvm.JObject(jenv, jobj)


@annotate('jt.jvm.JArray', ndarr='np.ndarray', desired_type=Optional['jt.jvm.JClass'])
def ndarray_to_jprimitivearray(ndarr, desired_type=None):

    # Converts a numpy ndarray to a Java primitive array.
    #
    # @param ndarr         the ndarray to convert
    # @param desired_type  the desired type of the resulting primitive array,
    #                      or None if it should determine type based on the dtype
    #
    # @return a Java primitive array, or NULL if there were errors

    import numpy as np

    from ._jvm import JVM
    jt_jvm = JVM.jvm

    # determine what we can about the ndarray that is to be converted
    size  = ndarr.size
    dtype = ndarr.dtype

    with jt_jvm as (jvm, jenv):
        BooleanArray1Class = jt_jvm.JClass(None, jvm.java_array.BooleanArray1Class, borrowed=True)
        ByteArray1Class    = jt_jvm.JClass(None, jvm.java_array.ByteArray1Class,    borrowed=True)
        ShortArray1Class   = jt_jvm.JClass(None, jvm.java_array.ShortArray1Class,   borrowed=True)
        IntArray1Class     = jt_jvm.JClass(None, jvm.java_array.IntArray1Class,     borrowed=True)
        LongArray1Class    = jt_jvm.JClass(None, jvm.java_array.LongArray1Class,    borrowed=True)
        FloatArray1Class   = jt_jvm.JClass(None, jvm.java_array.FloatArray1Class,   borrowed=True)
        DoubleArray1Class  = jt_jvm.JClass(None, jvm.java_array.DoubleArray1Class,  borrowed=True)

    if desired_type is None:
        if   dtype == np.bool:    desired_type = BooleanArray1Class
        elif dtype == np.byte:    desired_type = ByteArray1Class
        elif dtype == np.int16:   desired_type = ShortArray1Class
        elif dtype == np.int32:   desired_type = IntArray1Class
        elif dtype == np.int64:   desired_type = LongArray1Class
        elif dtype == np.float32: desired_type = FloatArray1Class
        elif dtype == np.float64: desired_type = DoubleArray1Class
        else:
            raise TypeError("Unable to determine corresponding Java type for ndarray")

    if   desired_type == BooleanArray1Class and dtype == np.bool:    jarr = jt_jvm.JArray.newBooleanArray(size)
    elif desired_type == ByteArray1Class    and dtype == np.byte:    jarr = jt_jvm.JArray.newByteArray(size)
    elif desired_type == ShortArray1Class   and dtype == np.int16:   jarr = jt_jvm.JArray.newShortArray(size)
    elif desired_type == IntArray1Class     and dtype == np.int32:   jarr = jt_jvm.JArray.newIntArray(size)
    elif desired_type == LongArray1Class    and dtype == np.int64:   jarr = jt_jvm.JArray.newLongArray(size)
    elif desired_type == FloatArray1Class   and dtype == np.float32: jarr = jt_jvm.JArray.newFloatArray(size)
    elif desired_type == DoubleArray1Class  and dtype == np.float64: jarr = jt_jvm.JArray.newDoubleArray(size)
    else:
        raise RuntimeError("Error matching ndarray.dtype to Java primitive type")

    # TODO we could speed this up if we could skip the copy, but the copy makes
    # it safer by enforcing the correct length in bytes for the type

    cndarr = np.ascontiguousarray(ndarr, dtype)

    with jt_jvm as (jvm, jenv):
        try:
            # if jarr was allocated, we already know it matched the python array type
            if   dtype == np.bool:    jenv.SetBooleanArrayRegion(jarr.handle, 0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jboolean)))
            elif dtype == np.byte:    jenv.SetByteArrayRegion(jarr.handle,    0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jbyte)))
            elif dtype == np.int16:   jenv.SetShortArrayRegion(jarr.handle,   0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jshort)))
            elif dtype == np.int32:   jenv.SetIntArrayRegion(jarr.handle,     0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jint)))
            elif dtype == np.int64:   jenv.SetLongArrayRegion(jarr.handle,    0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jlong)))
            elif dtype == np.float32: jenv.SetFloatArrayRegion(jarr.handle,   0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jfloat)))
            elif dtype == np.float64: jenv.SetDoubleArrayRegion(jarr.handle,  0, size, cndarr.ctypes.data_as(jni.POINTER(jni.jdouble)))
        except jni.Throwable as exc:
            raise RuntimeError("Error setting Java primitive array region")

    return jarr


#PyObject* jdndarray_to_ndarray(JNIEnv *jenv, PyObject* jdndarr):
def jdndarray_to_ndarray(jenv, jdndarr):

    _init_numpy()

    from ...jvm.jframe import JFrame

    #obj = ((PyJObject*) jdndarr).__javaobject__
    obj = jdndarr.__javaobject__ # jni.jobject

    with jdndarr.jvm as (jvm, jenv), JFrame(jenv, 1 + 1):

        is_usigned = jenv.CallBooleanMethod(obj, JVM.JepDirectNDArray.isUnsigned)
        if handleException(jenv):
            return NULL;

        # set up the dimensions for conversion
        jdimarr = jenv.CallObjectMethod(obj, JVM.JepDirectNDArray.getDimensions)
        if handleException(jenv) or not jdimarr:
            return NULL;

        ndims = jenv.GetArrayLength(jdimarr)
        if ndims < 1:
            raise ValueError("ndarrays must have at least one dimension")

        jdims = jenv.GetIntArrayElements(jdimarr, None)
        if handleException(jenv) or not jdimarr:
            return NULL;
        try:
            dims = malloc(ndims * sizeof(npy_intp)) # npy_intp*
            for i in range(ndims): dims[i] = jdims[i]
        finally:
            jenv.ReleaseIntArrayElements(jdimarr, jdims, jni.JNI_ABORT)

        # get the primitive array and convert it
        jarr = jenv.CallObjectMethod(obj, JVM.JepDirectNDArray.getData)
        if handleException(jenv) or not jarr:
            return NULL;

        result = convert_jdirectbuffer_pyndarray(jenv, jarr, ndims, dims, is_usigned)
        if not result:
            free(dims);
            handleException(jenv)
            return NULL;

        if PyArray_SetBaseObject(ct.cast(result, ct.POINTER(PyArrayObject)), pyobj) == -1:
            Py_XDECREF(pyobj);
            Py_CLEAR(result);

        # primitive arrays can be large, encourage garbage collection
        free(dims);

    return result


@annotate(object, jndarr='jt.jvm.JObject')
def jndarray_to_ndarray(jndarr):

    # Converts a jep.NDArray to a numpy ndarray.
    #
    # @param jndarr  the jep.NDArray to convert
    #
    # @return  a numpy ndarray, or NULL if there were errors

    import numpy as np

    from ...jvm.jframe import JFrame

    with jndarr.jvm as (jvm, jenv), JFrame(jenv, 1 + 1):

        # set up the dimensions for conversion
        jdimarr = jenv.CallObjectMethod(jndarr.handle, jndarr.jvm.JepNDArray.getDimensions)
        ndims   = jenv.GetArrayLength(jdimarr)
        jdims   = jenv.GetIntArrayElements(jdimarr, None)
        try:
            dims = tuple(jdims[i] for i in range(ndims))
        finally:
            jenv.ReleaseIntArrayElements(jdimarr, jdims, jni.JNI_ABORT)

        if not dims:
            raise ValueError("ndarrays must have at least one dimension")

        # get the primitive array and convert it
        jarr = jenv.CallObjectMethod(jndarr.handle, jndarr.jvm.JepNDArray.getData)
        jarr = jndarr.jvm.JObject(jenv, jarr)

        return jprimitivearray_to_ndarray(jarr, dims)


@annotate('np.ndarray', jarr='jt.jvm.JObject', dims=Tuple[int])
def jprimitivearray_to_ndarray(jarr, dims):

    # Converts a Java primitive array to a numpy ndarray.
    #
    # @param jarr  the Java primitive array
    # @param dims  the dimensions of the output ndarray
    #
    # @return  an ndarray of matching dtype and dimensions

    import numpy as np

    jt_jvm = jarr.jvm

    with jarr.jvm as (jvm, jenv):
        BooleanArray1Class = jt_jvm.JClass(None, jvm.java_array.BooleanArray1Class, borrowed=True)
        ByteArray1Class    = jt_jvm.JClass(None, jvm.java_array.ByteArray1Class,    borrowed=True)
        ShortArray1Class   = jt_jvm.JClass(None, jvm.java_array.ShortArray1Class,   borrowed=True)
        IntArray1Class     = jt_jvm.JClass(None, jvm.java_array.IntArray1Class,     borrowed=True)
        LongArray1Class    = jt_jvm.JClass(None, jvm.java_array.LongArray1Class,    borrowed=True)
        FloatArray1Class   = jt_jvm.JClass(None, jvm.java_array.FloatArray1Class,   borrowed=True)
        DoubleArray1Class  = jt_jvm.JClass(None, jvm.java_array.DoubleArray1Class,  borrowed=True)

    nitems = 1
    for dim in dims:
        nitems *= dim

    ndarr = None

    if BooleanArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.bool)

        jarr = jarr.handle
        jels = jenv.GetBooleanArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseBooleanArrayElements(jarr, jels, jni.JNI_ABORT)

    elif ByteArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.byte)

        jarr = jarr.handle
        jels = jenv.GetByteArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseByteArrayElements(jarr, jels, jni.JNI_ABORT)

    elif ShortArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.int16)

        jarr = jarr.handle
        jels = jenv.GetShortArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseShortArrayElements(jarr, jels, jni.JNI_ABORT)

    elif IntArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.int32)

        jarr = jarr.handle
        jels = jenv.GetIntArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseIntArrayElements(jarr, jels, jni.JNI_ABORT)

    elif LongArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.int64)

        jarr = jarr.handle
        jels = jenv.GetLongArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseLongArrayElements(jarr, jels, jni.JNI_ABORT)

    elif FloatArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.float32)

        jarr = jarr.handle
        jels = jenv.GetFloatArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseFloatArrayElements(jarr, jels, jni.JNI_ABORT)

    elif DoubleArray1Class.isInstance(jarr):

        ndarr = np.empty(shape=dims, dtype=np.float64)

        jarr = jarr.handle
        jels = jenv.GetDoubleArrayElements(jarr, None)
        try:
            jni.memmove(ndarr.ctypes.data, jels, nitems * ndarr.itemsize)
        finally:
            jenv.ReleaseDoubleArrayElements(jarr, jels, jni.JNI_ABORT)

    return ndarr

#endif NUMPY_ENABLED
