# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os

"""
Utility functions used for benchmarking resources.
"""

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2016"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


# Sizes
c_STR_B = b'B'
c_STR_KB = b'KB'
c_STR_MB = b'MB'
c_STR_GB = b'GB'
c_STR_TB = b'TB'
c_STR_PB = b'PB'
c_LSTR_SIZES = [c_STR_B.lower(), c_STR_KB.lower(),
                c_STR_MB.lower(), c_STR_GB.lower(),
                c_STR_TB.lower(), c_STR_PB.lower()]
c_STR_MEM = b'VmSize'
c_STR_RES = b'VmRSS'
c_STR_STK = b'VmStk'


# Tested 6/19/2016
def func_get_process_file(str_pid):
    """
    Given a process id, get the file with the process information.
    ** Only linux compatible. **

    * str_pid : Process id to monitor.
                String id
    * return: String
              File to read process information from.
    """

    return(os.sep + os.sep.join([b'proc', str(str_pid), b'status']))


# Tested 6/19/2016
def func_human_readable(i_amount, str_measurement=c_STR_B):
    """
    Changes a measure of bytes to a human readable string.
    * i_amount : Measure in bytes.
                 Integer
    * str_measurement : If the i_amount is not in bytes but another
                       amount, give here so that conversion of bytes
                       will start at that measurement. For instance,
                       if the measurement is in KB instead of B.
                       Measurements can B, KB, MB, GB, TB, PB.
                       This module provides constants to use.
                       String (use the Benchmarking contants).
    * return : Human readable measurement.
             : String
    """

    if i_amount <= 0:
        return(b'0.00 B')

    # Set to bytes.
    i_units = c_LSTR_SIZES.index(str_measurement.lower())
    if i_units < 0:
        return(str(i_amount))
    else:
        i_amount = i_amount * (1024 ** i_units)

    # Change units to largest units
    i_magnitude = 0
    while((i_amount>1) and ((i_magnitude+1)<len(c_LSTR_SIZES))):
        i_amount = i_amount/1024.0
        i_magnitude = i_magnitude + 1
    if i_amount<1 and i_magnitude>0:
        i_amount = i_amount * 1024
        i_magnitude = i_magnitude - 1
    return(b' '.join([ str("{:.2f}".format(i_amount)),
                       c_LSTR_SIZES[i_magnitude].upper()]))


def func_memory(str_pid):
    """
    Return memory usage in bytes of current process.
    * str_pid: Process id about which to get memory.
             : String id
    * return: String representation of memory use.
    """

    str_memory = b'0.0'
    str_resident = b'0.0'
    str_stack = b'0.0'

    try:
        with open(func_get_process_file(str_pid),'r') as hndl_open:
            str_mem_info = hndl_open.read()
            i_memory = func_parse_measure(c_STR_MEM, str_mem_info)
            i_resident = func_parse_measure(c_STR_RES, str_mem_info)
            i_stack = func_parse_measure(c_STR_STK, str_mem_info)
            return([i_memory, i_resident, i_stack])
    except:
        return([0, 0, 0])


# Tested 6/19/2016
def func_parse_measure(str_key, str_mem_info):
    """
    Pull from a string a memory measurement (given a process id file).
    * str_key: Measure to pull from info
             : String (c_STR_MEM, c_STR_RES, c_STR_STK)
    * str_mem_info: Contents of the process status file
                  : String
    * return: String representation of the memory measurement.
    """

    i_location = str_mem_info.find(str_key)
    return(float(str_mem_info[i_location:].split(None,3)[1]))
