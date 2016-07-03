# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

"""
Functions involving sending commands to the commandline.
"""
import Benchmarking
import logging
import os
import subprocess as sp
import time

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


class Commandline:
    """
    This class wraps calls to the command line in a simple interface.
    """

    def __init__(self, str_name=None, logr_cur=None):
        """
        Initializer that allows one to set the logger.

        * logr_cur : Logger
                     Optional parameter for logging.
                     If supplied this logger will be used,
                     otherwise the root logger will be used.
        """

        self.logr_cur = logr_cur if logr_cur else logging.getLogger(str_name)


    # Tested
    def func_CMD(self,
                 str_command,
                 f_use_bash=False,
                 f_test=False,
                 f_stdout=False,
                 i_secs=None):
        """
  	    Runs the given command.
        * str_command : Command to run on the commandline
                      : String
        * f_use_bash : Boolean
                     : If true, sends the command through using
                       BASH not SH (Bourne) or default shell (windows)
                     : Although the False is _I believe_ is not specific
                       to an OS, True is.
	      * f_test : Boolean
	                 If true, the commands will not run but will be logged.
        * f_stdout : Boolean
                   : If true, stdout will be given instead of True.
                     On a fail False (boolean) will still be given.
        * i_secs : Number of seconds to measure memory within.
                 : integer
	      * Return : Boolean
	                 True indicates success
	      """

        i_return_code = None

        # Update command for bash shell
        if f_use_bash:
            str_command = "".join([os.sep, "bin", os.sep,
                                   "bash -c \'", str_command, "\'"])

        # Do not do anything when testing
        if f_test:
            return True

        try:
            # Perform command and wait for completion
            if f_stdout:
                subp_cur = sp.Popen(str_command,
                                    shell=True,
                                    cwd=os.getcwd(),
                                    stdout=sp.PIPE)
            else:
                subp_cur = sp.Popen(str_command, shell=True, cwd=os.getcwd())
            str_pid = str(subp_cur.pid)

            # If seconds are given, record memory usage within those
            # seconds.
            str_out = " "
            if i_secs:
                ld_max_mem = [-1,-1,-1]
                while(i_return_code is None):
                    ld_mem_info = Benchmarking.func_memory(str_pid)
                    ld_max_mem = [max(info) for info
                                  in zip(ld_mem_info,ld_max_mem)]
                    time.sleep(i_secs)
                    i_return_code = subp_cur.poll()
                if(-1 in ld_max_mem):
                    str_mem = b''.join([b'Memory benchmarking is only ',
                                        b'compatible with Linux ',
                                        b'operating systems.'])
                else:
                    str_mem = b''.join([b'Memory: '+Benchmarking.func_human_readable(ld_max_mem[0]),
                                        b' Resident Memory: '+Benchmarking.func_human_readable(ld_max_mem[1]),
                                        b' Stack Size: '+Benchmarking.func_human_readable(ld_max_mem[2])])
                self.logr_cur.info(b'Memory benchmark::'+str_mem)
            else:
                str_out, str_err = subp_cur.communicate()
                i_return_code = subp_cur.returncode

            # 0 indicates success
            # On Stdout == true return a true string (stdout or 1 blank space)
            if i_return_code == 0:
                if f_stdout:
                    return str_out
                return True
            else:
                self.logr_cur.error("".join([self.__class__.__name__,
                                             "::Error::Received return code = ",
                                             str(i_return_code)]))
                self.logr_cur.error("".join([self.__class__.__name__,
                                             "::Error::Command = ",
                                             str_command]))
                self.logr_cur.error("".join([self.__class__.__name__,
                                             "::Error::Error out= ",
                                             str(str_out)]))
                self.logr_cur.error("".join([self.__class__.__name__,
                                             "::Error::Error= ",
                                             str(str_err)]))
                return False

        # Inform on errors:w
        except(OSError, TypeError) as e:
            self.logr_cur.error("".join([self.__class__.__name__,
                                         "::Error::Fatal error."]))
            self.logr_cur.error("".join([self.__class__.__name__,
                                         "::Error::Command = ", str_command]))
            self.logr_cur.error("".join([self.__class__.__name__,
                                         "::Error:: Error = ", str(e)]))
            return False
        return False

    # Tested
    def func_CMDs(self, lstr_command,
                  f_use_bash=False, f_test=False,
                  i_secs=None):
        """
        Convenience function to run multiple commands at one time in serial.
	      Will stop and return error if any command fails.
	      * lstr_command : List of strings
	                       Each string will be execute on command line in serial
	      * f_test : Boolean
	                 If true, no command line will execute but will be logged.

        * f_use_bash : Boolean
                     : If true, sends the command through using 
                       BASH not SH (Bourne) or default shell (windows)
                     : Although the False is _I believe_ is not
                       specific to an OS, True is.
	      * Return : Boolean
	                 True indicates success
	      """

        # Handle in case a string is accidently given
        if isinstance(lstr_command, basestring):
            lstr_command = [lstr_command]

        for str_command in lstr_command:
            if not self.func_CMD(str_command=str_command,
                                 f_use_bash=f_use_bash,
                                 f_test=f_test,
                                 i_secs=i_secs):
                return False
        return True
