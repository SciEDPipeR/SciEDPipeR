# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import Benchmarking
import os
import ParentPipelineTester
import unittest


"""
Tests the benchmarking module.
"""


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2016"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


class BenchmarkingTester(ParentPipelineTester.ParentPipelineTester):
    """
    Tests the Benchmarking object.
    """

    str_info = b'\n'.join([b'Name:\tbash',
                               b'Pid:\t1111',
                               b'VmSize:\t9136 kB',
                               b'VmRSS:\t0 kB',
                               b'VmStk:\t1 kB',
                               b'SigQ:\t0/3067',
                               b'SigPnd:\t0000000000000000'])

    ########################
    # func_human_readable
    ########################
    def test_human_readable_for_bytes_neg_1(self):
        """ Testing human readable for -1 bytes amount. """
        i_amount = -1
        str_answer = b'0.00 B'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_bytes_0(self):
        """ Testing human readable for 0 bytes amount. """
        i_amount = 0
        str_answer = b'0.00 B'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_bytes_1(self):
        """ Testing human readable for 1 bytes amount. """
        i_amount = 1
        str_unit = b'B'
        str_answer = b'1.00 B'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_bytes_1023(self):
        """ Testing human readable for 1023 bytes amount. """
        i_amount = 1023
        str_answer = b'1023.00 B'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_bytes_1024(self):
        """ Testing human readable for 1024 bytes amount. """
        i_amount = 1024
        str_answer = b'1.00 KB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_bytes_1025(self):
        """ Testing human readable for 1025 bytes amount. """
        i_amount = 1025
        str_answer = b'1.00 KB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_MB_bound_low(self):
        """ Testing human readable for the lower bound of MB. """
        i_amount = 1 * 1024 * 1024
        str_answer = b'1.00 MB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_MB_bound_high(self):
        """ Testing human readable for the higher bound of MB. """
        i_amount = 1023 * 1024 * 1024
        str_answer = b'1023.00 MB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_GB_bound_low(self):
        """ Testing human readable for the lower bound of GB. """
        i_amount = 1 * 1024 * 1024 *1024
        str_answer = b'1.00 GB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_GB_bound_high(self):
        """ Testing human readable for the higher bound of GB. """
        i_amount = 1023 * 1024 * 1024 * 1024
        str_answer = b'1023.00 GB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_PB_bound_low(self):
        """ Testing human readable for the lower bound of PB. """
        i_amount = 1 * 1024 * 1024 * 1024 * 1024 * 1024
        str_answer = b'1.00 PB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_PB_bound_high(self):
        """ Testing human readable for the higher bound of PB. """
        i_amount = 1023 * 1024 * 1024 * 1024 * 1024 * 1024
        str_answer = b'1023.00 PB'
        str_result = Benchmarking.func_human_readable(i_amount)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_KB(self):
        """ Testing human readable for a number given in KB. """
        i_amount = 1074
        str_unit = b'KB'
        str_answer = b'1.05 MB'
        str_result = Benchmarking.func_human_readable(i_amount, str_unit)
        self.func_test_equals(str_answer,str_result)

    def test_human_readable_for_GB(self):
        """ Testing human readable for a number given in GB. """
        i_amount = .5
        str_unit = b'GB'
        str_answer = b'512.00 MB'
        str_result = Benchmarking.func_human_readable(i_amount,str_unit)
        self.func_test_equals(str_answer,str_result)

    ########################
    # func_get_process_file
    ########################
    def test_func_get_process_file(self):
        """ Testing func_get_process file. """
        i_pid = 1
        str_answer = os.path.sep.join([b'proc', str(i_pid), b'status'])
        str_result = Benchmarking.func_get_process_file(i_pid)
        self.func_test_equals(str_answer,str_result)

    ########################
    # func_parse_measure
    ########################
    def test_func_parse_measure_mem(self):
        """ Testing func_parse_measure file. """
        str_key = Benchmarking.c_STR_MEM
        str_mem_info = self.str_info
        str_answer = b'9136.0'
        str_result = Benchmarking.func_parse_measure(str_key, str_mem_info)
        self.func_test_equals(str_answer,str_result)

    def test_func_parse_measure_stk(self):
        """ Testing func_parse_measure file. """
        str_key = Benchmarking.c_STR_RES
        str_mem_info = self.str_info
        str_answer = b'0.0'
        str_result = Benchmarking.func_parse_measure(str_key, str_mem_info)
        self.func_test_equals(str_answer,str_result)

    def test_func_parse_measure_rss(self):
        """ Testing func_parse_measure file. """
        str_key = Benchmarking.c_STR_STK
        str_mem_info = self.str_info
        str_answer = b'1.0'
        str_result = Benchmarking.func_parse_measure(str_key, str_mem_info)
        self.func_test_equals(str_answer,str_result)

#Creates a suite of tests
def suite():
    """ Suite aggregates tests and is used to run tests. """
    return unittest.TestLoader().loadTestsFromTestCase(BenchmarkingTester)
