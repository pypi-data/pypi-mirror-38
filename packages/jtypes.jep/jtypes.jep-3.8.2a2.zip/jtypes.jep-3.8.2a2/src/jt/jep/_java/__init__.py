# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from ...jvm.lib.compat import *
from ...jvm.lib.compat import PY3
from ...jvm.lib import annotate, Optional
from ...        import jni

from ...jvm.jframe      import JFrame
from ...jvm.jobjectbase import JObjectBase
from ...jvm.jobject     import JObject
from ...jvm.jclass      import JClass


# java.lang.AutoCloseable

@annotate(jobject=JObjectBase)
def AutoCloseable_close(jobject):

    with jobject.jvm as (jvm, jenv):
        jenv.CallVoidMethod(jobject.handle,
                            jvm.AutoCloseable.close)


# java.lang.Comparable

@annotate(int, jobject=JObjectBase, other=JObjectBase)
def java_lang_Comparable_compareTo(jobject, other):

    jvm, jenv = jobject.jvm
    try:
        jarg = jni.jvalue(l=other.handle)
        return jenv.CallIntMethod(jobject.handle,
                                  jvm.Comparable.compareTo, jarg)
    except jni.Throwable as exc:
       #if PY3 and jenv.IsInstanceOf(exc.getCause(), jvm.java_lang.ClassCastException): ???
        if PY3 and jenv.IsInstanceOf(exc, jvm.java_lang.ClassCastException):
            # To properly meet the richcompare docs we detect
            # ClassException and return NotImplemented, enabling Python
            # to try the reverse operation of other.compareTo(self).
            # Unfortunately this only safely works in Python 3.
            return NotImplemented
        else:
            jobject.jvm.handleException(exc)


# java.lang.Iterable

@annotate(JObject, iterable=JObject)
def java_lang_Iterable_iterator(iterable):

    with iterable.jvm as (jvm, jenv), JFrame(jenv, 1):
        jobj = jenv.CallObjectMethod(iterable.handle,
                                     jvm.Iterable.iterator)
        if not jobj:
            raise TypeError("java.lang.Iterable returned a null value from "
                            "iterator()")
        return iterable.jvm.JObject(jenv, jobj)


# java.util.Iterator

@annotate(bool, iterator=JObject)
def java_util_Iterator_hasNext(iterator):

    with iterator.jvm as (jvm, jenv):
        return jenv.CallBooleanMethod(iterator.handle,
                                      iterator.jvm.java_util.Iterator_hasNext)


@annotate(Optional[JObject], iterator=JObject)
def java_util_Iterator_next(iterator):

    with iterator.jvm as (jvm, jenv), JFrame(jenv, 1):
        jobj = jenv.CallObjectMethod(iterator.handle,
                                     iterator.jvm.java_util.Iterator_next)
        return iterator.jvm.JObject(jenv, jobj) if jobj else None


# java.util.Collections

@annotate(JObject, collection=JObject)
def java_util_Collections_unmodifiableList(collection):

    with collection.jvm as (jvm, jenv), JFrame(jenv, 1):
        jarg = jni.jvalue(l=collection.handle)
        jobj = jenv.CallStaticObjectMethod(collection.jvm.java_util.CollectionsClass,
                                           collection.jvm.java_util.Collections_unmodifiableList,
                                           jarg)
        if not jobj:
            raise Exception()
        return collection.jvm.JObject(jenv, jobj)


@annotate(int, collection=JObject)
def java_util_Collection_size(collection):

    with collection.jvm as (jvm, jenv):
        return jenv.CallIntMethod(collection.handle,
                                  collection.jvm.java_util.Collection_size)


@annotate(bool, collection=JObject, item=Optional[JObject])
def java_util_Collection_contains(collection, item):

    with collection.jvm as (jvm, jenv):
        jarg = jni.jvalue(l=item.handle if item is not None else 0)
        return jenv.CallBooleanMethod(collection.handle,
                                      collection.jvm.java_util.Collection_contains, jarg)


# java.util.List

@annotate(bool, list=JObject, value=Optional[JObjectBase])
def java_util_List_add(list, value):

    with list.jvm as (jvm, jenv):
        jarg = jni.jvalue(l=value.handle if value is not None else 0)
        return jenv.CallBooleanMethod(list.handle,
                                      list.jvm.java_util.List_add, jarg)


@annotate(bool, list=JObject, values=Optional[JObject])
def java_util_List_addAll(list, values):

    with list.jvm as (jvm, jenv):
        jarg = jni.jvalue(l=values.handle if values is not None else 0) # ???
        return jenv.CallBooleanMethod(list.handle,
                                      list.jvm.java_util.List_addAll, jarg)


@annotate(Optional[JObject], list=JObject, index=int)
def java_util_List_get(list, index):

    with list.jvm as (jvm, jenv), JFrame(jenv, 1):
        jarg = jni.jvalue(i=index)
        jobj = jenv.CallObjectMethod(list.handle,
                                     list.jvm.java_util.List_get, jarg)
        return list.jvm.JObject(jenv, jobj) if jobj else None


@annotate(jni.jobject, list=JObject, index=int, value=Optional[JObject])
def java_util_List_set(list, index, value):

    with list.jvm as (jvm, jenv), JFrame(jenv, 1): # !!! w orginale nie bylo Frame !!!
        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].i = index
        jargs[1].l = value.handle if value is not None else 0
        jobj = jenv.CallObjectMethod(list.handle,
                                     list.jvm.java_util.List_set, jargs)
        return list.jvm.JObject(jenv, jobj) if jobj else None


@annotate(list=JObject)
def java_util_List_clear(list):

    with list.jvm as (jvm, jenv):
        jenv.CallVoidMethod(list.handle,
                            list.jvm.java_util.List_clear)


@annotate(Optional[JObject], list=JObject, index=int)
def java_util_List_remove(list, index):

    with list.jvm as (jvm, jenv), JFrame(jenv, 1): # !!! w orginale nie bylo Frame !!!
        jarg = jni.jvalue(i=index)
        jobj = jenv.CallObjectMethod(list.handle,
                                     list.jvm.java_util.List_remove, jarg)
        return list.jvm.JObject(jenv, jobj) if jobj else None


@annotate(JObject, list=JObject, fromIndex=int, toIndex=int)
def java_util_List_subList(list, fromIndex, toIndex):

    with list.jvm as (jvm, jenv), JFrame(jenv, 1):
        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].i = fromIndex
        jargs[1].i = toIndex
        jobj = jenv.CallObjectMethod(list.handle,
                                     list.jvm.java_util.List_subList, jargs)
        return list.jvm.JObject(jenv, jobj)


# java.util.Map

@annotate(bool, map=JObject, key=Optional[JObject])
def java_util_Map_containsKey(map, key):

    with map.jvm as (jvm, jenv):
        jarg = jni.jvalue(l=key.handle if key is not None else 0)
        return jenv.CallBooleanMethod(map.handle,
                                      map.jvm.java_util.Map_containsKey, jarg)


@annotate(Optional[JObject], map=JObject, key=Optional[JObject])
def java_util_Map_get(map, key):

    with map.jvm as (jvm, jenv), JFrame(jenv, 1): # !!! w orginale nie bylo Frame !!!
        jarg = jni.jvalue(l=key.handle if key is not None else 0)
        jobj = jenv.CallObjectMethod(map.handle,
                                     map.jvm.java_util.Map_get, jarg)
        return map.jvm.JObject(jenv, jobj) if jobj else None


@annotate(JObject, map=JObject)
def java_util_Map_keySet(map):

    with map.jvm as (jvm, jenv), JFrame(jenv, 1):
        jobj = jenv.CallObjectMethod(map.handle,
                                     map.jvm.java_util.Map_keySet)
        if not jobj:
            raise Exception()
        return map.jvm.JObject(jenv, jobj)


@annotate(Optional[JObject], map=JObject, key=Optional[JObject], value=Optional[JObject])
def java_util_Map_put(map, key, value):

    with map.jvm as (jvm, jenv), JFrame(jenv, 1): # !!! w orginale nie bylo Frame !!!
        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].l = key.handle   if key   is not None else 0
        jargs[1].l = value.handle if value is not None else 0
        jobj = jenv.CallObjectMethod(map.handle,
                                     map.jvm.java_util.Map_put, jargs)
        return map.jvm.JObject(jenv, jobj) if jobj else None


@annotate(Optional[JObject], map=JObject, key=Optional[JObject])
def java_util_Map_remove(map, key):

    with map.jvm as (jvm, jenv), JFrame(jenv, 1): # !!! w orginale nie bylo Frame !!!
        jarg = jni.jvalue(l=key.handle if key is not None else 0)
        jobj = jenv.CallObjectMethod(map.handle,
                                     map.jvm.java_util.Map_remove, jarg)
        return map.jvm.JObject(jenv, jobj) if jobj else None


@annotate(int, map=JObject)
def java_util_Map_size(map):

    with map.jvm as (jvm, jenv):
        return jenv.CallIntMethod(map.handle,
                                  map.jvm.java_util.Map_size)


# jep.JepException

@annotate(type, jexc=JObject)
def jep_JepException_getPythonType(jexc):

    with jexc.jvm as (jvm, jenv):
        PyExc_id = jenv.CallLongMethod(jexc.handle,
                                       jexc.jvm.JepException.getPythonType)
        return jni.from_oid(PyExc_id) if PyExc_id else None
