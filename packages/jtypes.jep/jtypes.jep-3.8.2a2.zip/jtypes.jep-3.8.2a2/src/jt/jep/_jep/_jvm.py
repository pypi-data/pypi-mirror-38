# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Optional, Union, Tuple
from ...jvm.lib import public
from ...jvm.lib import classproperty
from ...        import jni

from ...jvm import JVM as _JVM


@public
@annotate(path=Optional[Union[builtins.str, str]], options=Optional[Tuple])
def start_jvm(path=None, options=None):

    # Extension against original jep

    """
    @annotate(jenv=Optional[jni.JNIEnv])
    def __init__(self, jenv=None):

    if jenv is None:
        from .jvm import JVM
        pjvm = jni.obj(jni.POINTER(jni.JavaVM))
        JVM.JNI.GetCreatedJavaVMs(pjvm, 1, None)
        penv = jni.obj(jni.POINTER(jni.JNIEnv))
        pjvm.AttachCurrentThread(penv)
        self.jvm  = pjvm  # jvm.JVM
        self.jenv = penv  # jni.JNIEnv
    else:
        pjvm = jni.obj(jni.POINTER(jni.JavaVM))
        jenv.GetJavaVM(pjvm)
        self.jvm  = pjvm  # jvm.JVM
        self.jenv = jenv  # jni.JNIEnv
    """

    if JVM.jvm is None:

        #pjvm = jni.obj(jni.POINTER(jni.JavaVM))
        #JNI.GetCreatedJavaVMs(pjvm, 1, None)
        #
        #penv = jni.obj(jni.POINTER(jni.JNIEnv))
        #pjvm.AttachCurrentThread(penv)
        #jenv = penv  # jni.JNIEnv
        #
        #JVM.jvm = JVM()  # jvm.JVM
        #JVM.jvm.jnijvm = pjvm
        #JVM.jvm        = pjvm

        jvm = JVM(path)
        _, jenv = jvm.start(*options, ignoreUnrecognized=False)

        ##########

        from ._jclass import PyJClass
        from .        import _util as util
        from .._java  import embed

        DICT_KEY = "jep"

        jep_thread = embed.JepThread()

        #!!!
        tdict = embed.PyThreadState_GetDict()
        if tdict is not None:
            tdict[DICT_KEY] = jep_thread
        #!!!

        #jep_thread.tstate = Py_NewInterpreter();

        #mod_main = PyImport_AddModule("__main__")
        #if (mod_main == NULL):
        #    throwJavaException(jenv, "jep.JepException", "Couldn't add module __main__.")
        #    return 0

        from ._jobject import PyJObject
        jclass = JVM.jvm.JClass.forName("org.python.util.PythonInterpreter")
        Jep = PyJClass(jclass)
        interp = Jep()

        # init static module
        jep_thread.modjep      = None # __import__("_jep",  None, None, [], 0)
       #jep_thread.modjep      = __import__("._jep", None, None, [], 1) # how to import relative ?
        jep_thread.globals     = {}
        jep_thread.env         = jenv
        jep_thread.caller      = interp.__javaobject__
    #!!!jep_thread.classloader = interp.cloader.__javaobject__
        jep_thread.classloader = JVM.jvm.JClassLoader.getSystemClassLoader()

        tdict = embed.PyThreadState_GetDict()
        if tdict is not None:
            tdict[DICT_KEY] = jep_thread

        #!!! print("@@@ embed.PyThreadState_GetDict() @@@: {}".format(tdict))

        ##########

    penv = jni.obj(jni.POINTER(jni.JNIEnv))
    JVM.jvm._jvm.jnijvm.AttachCurrentThread(penv)
    jenv = penv  # jni.JNIEnv


@public
def stop_jvm():

    # Extension against original jep

    if JVM.jvm is not None:
        JVM.jvm.shutdown()


@public
class JVM(_JVM):

    """JVM"""

    jvm  = classproperty(lambda cls: JVM._jvm)
    jenv = classproperty(lambda cls: JVM._jenv)

    _jvm  = None  # Optional[jt.jvm.JVM]
    _jenv = None  # Optional[jt.jvm.jni.JNIEnv]

    def __init__(self, dll_path=None):

        from ._typemanager import TypeManager

        super(JVM, self).__init__(dll_path)
        self._create()
        self.type_manager = TypeManager()

    def start(self, *jvmoptions, **jvmargs):

        _, jenv = result = super(JVM, self).start(*jvmoptions, **jvmargs)
        JVM._jvm, JVM._jenv = self, jenv
        try:
            self._initialize(jenv)
        except:
            raise RuntimeError("Failed to get primitive and frequent class types.")
        self.type_manager.start()
        return result

    def shutdown(self):

        self.type_manager.stop()
        _, jenv = self
        self._dispose(jenv)
        super(JVM, self).shutdown()
        JVM._jvm = JVM._jenv = None

    def _create(self):

        from .._java import jnijep

        self.java_util        = jnijep.java_util()
        self.JepException     = jnijep.jep_JepException()
        self.JepNDArray       = jnijep.jep_NDArray()
        self.JepDirectNDArray = jnijep.jep_DirectNDArray()
        self.Jep              = jnijep.jep_Jep()
        self.JepProxyHandler  = jnijep.jep_reflect_ProxyHandler()

    @annotate(jenv=jni.JNIEnv)
    def _initialize(self, jenv):

        self.java_util.initialize(jenv)
        self.JepException.initialize(jenv)
        self.JepNDArray.initialize(jenv)
        self.JepDirectNDArray.initialize(jenv)
        self.Jep.initialize(jenv)
        self.JepProxyHandler.initialize(jenv)

    @annotate(jenv=jni.JNIEnv)
    def _dispose(self, jenv):

        self.java_util.dispose(jenv)
        self.JepException.dispose(jenv)
        self.JepNDArray.dispose(jenv)
        self.JepDirectNDArray.dispose(jenv)
        self.Jep.dispose(jenv)
        self.JepProxyHandler.dispose(jenv)

    def handleException(self, exc):

        # Converts a Java exception to a Python Exception and raise it.
        # If an error was processed here, it can be caught in Python code
        # or if uncaught it will reach the method process_py_exception(...).

        from ._jobject import PyJObject
        from .._java   import embed

        try:
            raise exc
        except jni.Throwable as exc:

            jep_thread = embed.get_jepthread()
            if not jep_thread:
                msg = "Error while processing a Java exception, invalid JepThread."
                print(msg)
                raise RuntimeError(msg)

            jexc = self.JException(exc)

            jclass = jexc.getClass()
            #msg   = jexc.getMessage()

            try:
                # Java does not fill in a stack trace until getStackTrace() is
                # called. If it is not called now then the stack trace can be lost
                # so even though this looks like a no-op it is very important.
                jexc.getStackTrace()
            except: # jenv.ExceptionCheck()
                raise RuntimeError("wrapping java exception in pyjobject failed.")

            # turn the Java exception into a PyJObject so the interpreter
            # can handle it
            py_jexc = PyJObject(jexc.asObject())

            PyExc = self.__match_exception_type(jexc)
            raise PyExc(builtins.str(py_jexc))

        except:
            super(JVM, self).handleException(exc)

    @annotate(BaseException, jexc='jt.jvm.JException')
    def __match_exception_type(self, jexc):

        # Matches a jthrowable to an equivalent built-in Python exception type.
        # This is to enable more precise try: except: blocks in Python for Java
        # exceptions.

        from .._java import jep_JepException_getPythonType

        try:
            jvm, jenv = self
            if jenv.IsInstanceOf(jexc.handle, jvm.java_lang.NoClassDefFoundError):
                return ImportError  #*** added ***#
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.ClassNotFoundException):
                return ImportError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.IndexOutOfBoundsException):
                return IndexError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_io.IOException):
                return IOError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.ClassCastException):
                return TypeError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.IllegalArgumentException):
                return ValueError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.ArithmeticException):
                return ArithmeticError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.OutOfMemoryError):
                # honestly if you hit this you're probably screwed
                return MemoryError
            elif jenv.IsInstanceOf(jexc.handle, jvm.java_lang.AssertionError):
                return AssertionError
            elif jenv.IsInstanceOf(jexc.handle, jexc.jvm.JepException.Class):
                # Reuse the python type of the exception that caused
                # the JepException if it is available
                PyExc = jep_JepException_getPythonType(jexc)
                return PyExc if PyExc is not None else RuntimeError
            else:  # default
                return RuntimeError
        except jni.Throwable as exc:
            self.JException.printDescribe()
            return RuntimeError
