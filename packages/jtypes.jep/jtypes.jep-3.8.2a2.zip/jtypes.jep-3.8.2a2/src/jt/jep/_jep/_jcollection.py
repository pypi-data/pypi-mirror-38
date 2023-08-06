# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from __future__ import absolute_import

import collections as abcoll

from ...jvm.lib.compat import *
from ...jvm.lib import py2compatible
from ...jvm.lib import annotate
from ...jvm.lib import public
from ...jvm.lib import cached
from ...jvm.lib import issequence
from ...        import jni

from ...jvm.jarray import JArray
from ._jobject     import PyJObject

from .._java import java_lang_Iterable_iterator
from .._java import java_util_Iterator_hasNext
from .._java import java_util_Iterator_next
from .._java import java_util_Collection_size
from .._java import java_util_Collection_contains
from .._java import java_util_List_addAll
from .._java import java_util_List_get
from .._java import java_util_List_subList
from .._java import java_util_List_set
from .._java import java_util_List_remove
from .._java import java_util_List_clear
from .._java import java_util_Map_size
from .._java import java_util_Map_containsKey
from .._java import java_util_Map_get
from .._java import java_util_Map_put
from .._java import java_util_Map_remove
from .._java import java_util_Map_keySet


@public
class PyJIterable(PyJObject):

    """jiterable"""

    # "jep.PyJIterable" # tp_name

    # A PyJIterable is a PyJObject that has __iter__ implemented to support
    # iteration. It should only be used where the underlying jobject of the
    # PyJObject is an implementation of java.lang.Iterable.

    def __iter__(self):

        iterator = java_lang_Iterable_iterator(self.__javaobject__)
        return PyJObject(iterator)


@public
@py2compatible
class PyJIterator(PyJObject):

    """jiterator"""

    # "jep.PyJIterator" # tp_name

    # A PyJIterator is a PyJObject that has __iter__ and __next__ implemented
    # to support iteration. It exists primarily to support PyJIterable.

    def __iter__(self):

        return self

    def __next__(self):

        has_next = java_util_Iterator_hasNext(self.__javaobject__)
        if not has_next:
            raise StopIteration

        item = java_util_Iterator_next(self.__javaobject__)
        if item is None:
            return None
        else:
            type_manager = self.__javaobject__.jvm.type_manager
            thandler = type_manager.get_handler(item.getClass())
            return thandler.toPython(item)


@public
class PyJCollection(PyJIterable):

    """jcollection"""

    # "jep.PyJCollection" # tp_name

    # A PyJCollection is a PyJIterable with the additional functionality
    # of the __contains__ and __len__ methods.
    # It should only be used where the underlying jobject of the PyJObject
    # is an implementation of java.util.Collection.

    def __len__(self):

        return java_util_Collection_size(self.__javaobject__)

    def __contains__(self, value):

        from . import _typehandler as thandler
        jitem = thandler.toJava(value) if value is not None else None

        if value is not None and jitem is None:
            # with the way toJava is currently implemented, shouldn't be able to get here
            raise TypeError("__contains__ received an incompatible type: {!s}".format(
                            value.__class__))

        return java_util_Collection_contains(self.__javaobject__, jitem)


@public
class PyJList(PyJCollection):

    """jlist"""

    # "jep.PyJList" # tp_name

    # A PyJList is a PyJCollection with some extra methods attached to meet
    # the Python Sequence protocol/interface.  It should only be used where the
    # underlying jobject of the PyJObject is an implementation of java.util.List.

    def __copy__(self):

        # Extended (as __copy__) against jep

        # Convenience method to copy a list's items into a new java.util.List
        # of the same type.

        new_list = self.__javaclass__.newInstance()
        java_util_List_addAll(new_list, self.__javaobject__)
        return PyJList(new_list)

    def __getitem__(self, idx):

        if isinstance(idx, slice):

            start, stop, step = idx.indices(len(self))
            return self._getslice(start, stop, step)

        elif isinstance(idx, (int, long)):

            if idx < 0: idx += len(self)
            return self._getitem(idx)

        else:
            raise TypeError("list indices must be integers, longs, or slices")

    def __setitem__(self, idx, value):

        if isinstance(idx, slice):

            start, stop, step = idx.indices(len(self))
            self._setslice(start, stop, step, value)

        elif isinstance(idx, (int, long)):

            if idx < 0: idx += len(self)
            self._setitem(idx, value)

        else:
            raise TypeError("list indices must be integers, longs, or slices")

    def __delitem__(self, idx):

        if isinstance(idx, slice):

            start, stop, step = idx.indices(len(self))
            self._delslice(start, stop, step)

        elif isinstance(idx, (int, long)):

            if idx < 0: idx += len(self)
            self._delitem(idx)

        else:
            raise TypeError("list indices must be integers, longs, or slices")

    def _getitem(self, idx):

        size = len(self)

        if not (0 <= idx < size):
            raise IndexError("list index {} out of range, size {}".format(idx, size))

        item = java_util_List_get(self.__javaobject__, idx)
        return PyJObject(item) if item is not None else None

    def _getslice(self, start, stop, step):

        size = JArray.size(start, stop, step)
        if size <= 0:
            start, stop, step = 0, 0, 1

        if step != 1:
            raise TypeError("pyjlist slices must have step of 1")

        sublist = java_util_List_subList(self.__javaobject__, start, stop)
        return PyJList(sublist)

    def _setitem(self, idx, value):

        from . import _typehandler as thandler
        jitem = thandler.toJava(value) if value is not None else None

        if value is not None and jitem is None:
            # with the way toJava is currently implemented, shouldn't be able to get here
            raise TypeError("__setitem__ received an incompatible type: {!s}".format(
                            value.__class__))

        java_util_List_set(self.__javaobject__, idx, jitem)

    def _setslice(self, start, stop, step, value):

        size = JArray.size(start, stop, step)
        if size <= 0:
            return

        if step != 1:
            raise TypeError("pyjlist slices must have step of 1")

        if not issequence(value):
            raise TypeError("PyJList can only slice assign a sequence")

        size = len(self)

        if start < 0:    start = 0
        if stop  > size: stop  = size
        if start >= stop:
            raise IndexError("invalid slice indices: {}:{}".format(start, stop))

        value_size = len(value)

        diff = stop - start
        if diff != value_size:
            # TODO: Python lists support slice assignment of a different length,
            # but that gets complicated, so not planning on supporting it until
            # requested.  For inspiration look at python's listobject.c's
            # list_ass_slice().
            raise IndexError("PyJList only supports assigning a sequence of the same size "
                             "as the slice, slice = [{}:{}], value size={}".format(
                             start, stop, value_size))

        for idx in range(start, stop, step):
            # TODO This is not transactional if it fails partially through.
            # Not sure how to make that safe short of making a copy of o
            # and then replacing o's underlying jobject on success.
            # That would slow it down though....
            self._setitem(idx, value[idx - start])

    def _delitem(self, idx):

        java_util_List_remove(self.__javaobject__, idx)

    def _delslice(self, start, stop, step):

        size = JArray.size(start, stop, step)
        if size <= 0:
            return

        if step != 1:
            raise TypeError("pyjlist slices must have step of 1")

        size = len(self)

        if start < 0:    start = 0
        if stop  > size: stop  = size
        if start >= stop:
            raise IndexError("invalid slice indices: {}:{}".format(start, stop))

        for idx in range(start, stop, step):
            # TODO This is not transactional if it fails partially through.
            # Not sure how to make that safe short of making a copy of o
            # and then replacing o's underlying jobject on success.
            # That would slow it down though....
            self._delitem(idx)

    def __add__(self, other):

        copy = self.__copy__()
        return copy.__iadd__(other)

    def __mul__(self, count):

        copy = self.__copy__()
        return copy.__imul__(count)

    def __iadd__(self, other):

        # TODO: To match Python behavior of += operator, we should really be
        # using jvm.Iterable.Class and ensuring its an instance of Iterable,
        # not Collection.

        from . import _typehandler as thandler
        other = (other.__javaobject__
                if isinstance(other, PyJList) else
                (thandler.toJava(other) if other is not None else None))
        #???CollectionClass = list.jvm.JClass(None, list.jvm.java_util.CollectionClass, borrowed=True)

        # it's a Collection so we need to simulate a python + and combine
        # the two collections
        java_util_List_addAll(self.__javaobject__, other)
        return self

    def __imul__(self, count):

        if count <= 0:

            java_util_List_clear(self.__javaobject__)

        elif count > 1:

            copy = self.__copy__()
            # TODO there's probably a better way to do this
            for i in range(1, count):
                self.__iadd__(copy)

        return self


@public
class PyJMap(PyJObject):

    """jmap"""

    # "jep.PyJMap" # tp_name

    # A PyJMap is a PyJObject with some extra methods attached to meet
    # the Python Mapping protocol/interface. It should only be used where the
    # underlying jobject of the PyJObject is an implementation of java.util.Map.

    def __len__(self):

        return java_util_Map_size(self.__javaobject__)

    def __contains__(self, key):

        from . import _typehandler as thandler
        jkey = thandler.toJava(key) if key is not None else None

        if key is not None and not jkey:
            # with the way toJava is currently implemented, shouldn't be able to get here
            raise TypeError("__contains__ received an incompatible type: {!s}".format(
                            key.__class__))

        return java_util_Map_containsKey(self.__javaobject__, jkey)

    def __getitem__(self, key):

        if not isinstance(key, PyJObject):
            # __check_match_pyarg will raise TypeError if we can't handle the key type
            PyJMap.__check_match_pyarg(self.__javaobject__.jvm, key)

        from . import _typehandler as thandler
        jkey = thandler.toJava(key) if key is not None else None

        item = java_util_Map_get(self.__javaobject__, jkey)

        if item is None and not self.__contains__(key):
            # Python docs indicate KeyError should be set if the key
            # is not in the container, but some Maps allow null values.
            # So we have to check.
            raise KeyError("KeyError: {!s}".format(key))

        if item is None:
            return None
        else:
            type_manager = self.__javaobject__.jvm.type_manager
            thandler = type_manager.get_handler(item.getClass())
            return thandler.toPython(item)

    def __setitem__(self, key, value):

        if not isinstance(key, PyJObject):
            # __check_match_pyarg will raise TypeError if we can't handle the key type,
            PyJMap.__check_match_pyarg(self.__javaobject__.jvm, key)

        from . import _typehandler as thandler
        jkey  = thandler.toJava(key)   if key   is not None else None
        jitem = thandler.toJava(value) if value is not None else None

        if value is not None and jitem is None:
            # with the way toJava is currently implemented, shouldn't be able to get here
            raise TypeError("__setitem__ received an incompatible type: {!s}".format(
                            value.__class__))

        java_util_Map_put(self.__javaobject__, jkey, jitem)

    def __delitem__(self, key):

        if not self.__contains__(key):
            raise KeyError("KeyError: {!s}".format(key))

        if not isinstance(key, PyJObject):
            # __check_match_pyarg will raise TypeError if we can't handle the key type
            PyJMap.__check_match_pyarg(self.__javaobject__.jvm, key)

        from . import _typehandler as thandler
        jkey = thandler.toJava(key) if key is not None else None

        java_util_Map_remove(self.__javaobject__, jkey)

    def __iter__(self):

        keySet   = java_util_Map_keySet(self.__javaobject__)
        iterator = java_lang_Iterable_iterator(keySet)
        return PyJIterator(iterator)

    @staticmethod
    @annotate(val=object, pos=int)
    def __check_match_pyarg(jvm, val, pos=1):

        # for parsing args.
        # takes a python object and sets the right jvalue member for the given java type.
        # returns uninitialized on error and raises a python exception.

        from ._constants import EMatchType

        from ._jobject import PyJObject
        from ._jarray  import ndarray_check

        str_types = (builtins.str, str)

        #case JOBJECT_ID:

        if val is None:
            return EMatchType.PERFECT
        elif isinstance(val, str_types):
            # strings count as objects here
            return EMatchType.PERFECT
        elif isinstance(val, PyJObject):
            Object = jvm.JClass(None, jvm._jvm.Object.Class, borrowed=True)
            # check object itself is assignable to that type.
            if Object.isAssignableFrom(val.__javaclass__):
                return EMatchType.PERFECT
            raise TypeError("Incorrect object type at {}.".format(pos + 1))
        elif ndarray_check(val):
            return EMatchType.PERFECT
        raise TypeError("Expected {} parameter at {}.".format("object", pos + 1))
