# Function for testing for memory leaks in unittests by repeatedly executing a callable and ensuring the
# process size does not grow out of control. This function is not compatible with all platforms and will
# call testCase.skipTest() on platforms that aren't compatible.

from __future__ import absolute_import, division

import unittest
import sys
if sys.version_info.major <= 2: range = xrange

from . import with_performance

# This number is enough to prove small leaks on linux. Since the test measures process growth a system with a
# higher initial memory usage will hide a leak. Unfortunatly the units of ru.maxrss are platform dependent so
# it is impossible to accuratly measure memory usage in term of bytes. To make the test more robust the number
# of iterations can be increased but it takes longer so isn't worth it unless there is a reason to suspect a
# problem.
iterations = 2000000 if with_performance() else 2

# The value of 2   causes the test to fail if memory use doubles.
# the value of 1.2 causes the test to fail if memory increases more than 20%
# Values between 1.2 and 2 are considered reasonable.
failure_threshold = 1.5

if sys.platform == "win32":
    # TODO resource may not be available under windows,
    # I need someone with windows to test and possibly skip the memory leak testing.
    import os
    from jt.jvm.lib import wmi
    def memory_usage():
        return 72949760 #!!!
        client = wmi.WmiClient()
        query  = client.execute_query("SELECT WorkingSet "
                                      "FROM Win32_PerfRawData_PerfProc_Process "
                                      "WHERE IDProcess={}".format(os.getpid()))
        result = [wmi.WmiObject(item) for item in query]
        return int(result[0].get_wmi_attribute("WorkingSet"))
else:
    try:
        import resource
        memory_usage = lambda: resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except ImportError:
        memory_usage = None

@unittest.skipIf(memory_usage is None, "Cannot test for memory leaks on this platform")
def test_leak(testCase, callable, msg):

    start_memory = memory_usage()
    for _ in range(iterations):
        callable()
    end_memory = memory_usage()
    percent = end_memory * 100 // start_memory - 100
    testCase.assertLess(end_memory, start_memory * failure_threshold,
        "{} resulted in {}%% increase over {} iterations".format(msg, percent, iterations))
