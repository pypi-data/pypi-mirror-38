# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the zlib/libpng License
# http://opensource.org/licenses/zlib

"""_jep"""

__all__ = ('JBOOLEAN_ID', 'JCHAR_ID', 'JBYTE_ID', 'JSHORT_ID', 'JINT_ID',
           'JLONG_ID', 'JFLOAT_ID', 'JDOUBLE_ID', 'JSTRING_ID',
           'findClass', 'forName', 'jarray', 'jproxy')
__all__ += ('JEP_NUMPY_ENABLED',)#'USE_NUMPY')

from ._constants import EJavaType
from ._util import to_jep_jtype

JBOOLEAN_ID = to_jep_jtype[EJavaType.BOOLEAN]
JCHAR_ID    = to_jep_jtype[EJavaType.CHAR]
JBYTE_ID    = to_jep_jtype[EJavaType.BYTE]
JSHORT_ID   = to_jep_jtype[EJavaType.SHORT]
JINT_ID     = to_jep_jtype[EJavaType.INT]
JLONG_ID    = to_jep_jtype[EJavaType.LONG]
JFLOAT_ID   = to_jep_jtype[EJavaType.FLOAT]
JDOUBLE_ID  = to_jep_jtype[EJavaType.DOUBLE]
JSTRING_ID  = to_jep_jtype[EJavaType.STRING]

del EJavaType, to_jep_jtype

from ._main import findClass, forName, jarray, jproxy
from ..__config__ import config
JEP_NUMPY_ENABLED = config.getboolean("NUMPY_ENABLED", True)
#USE_NUMPY        = JEP_NUMPY_ENABLED  # for compatibility with old Jep-s
del config
#from .pyembed    import mainInterpreterModules

# static PyObject* initjep(jboolean hasSharedModules):
#
#    if hasSharedModules:
#        from ??? import main_thread_modules      as mainInterpreterModules
#        from ??? import main_thread_modules_lock as mainInterpreterModulesLock
#
#    return modjep
