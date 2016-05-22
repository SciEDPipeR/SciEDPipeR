# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Commandline
import os
import ParentPipelineTester
import unittest

class CommandlineTester(ParentPipelineTester.ParentPipelineTester):
    """
    Tests the Commandline object
    """

    def test_func_cmd_for_simple_command(self):
        """
        Test the case of send a simple command
        """
        # Set up environment
        str_test_file = "test_func_cmd_for_simple_command.txt"
        str_answer = "hello"
        self.func_remove_files([str_test_file])
        str_command = "echo \"" + str_answer + "\" > " + str_test_file
        # Send command and get result
        cmdl_cur = Commandline.Commandline()
        cmdl_cur.func_CMD(str_command = str_command)
        # Get confirmation that file was written correctly
        with open(str_test_file) as hndl_test:
            str_result = hndl_test.read()[:-1]
            self.func_test_equals(str_answer, str_result)
        # Destroy environment
        self.func_remove_files([str_test_file])

    def test_func_cmd_for_simple_command_return_zero(self):
        """
        Test the case of sending a simple command and getting the return
        value of 0 (success)
        """
        # Set up environment
        str_answer = str(True)
        str_command = "".join(["python sciedpiper", os.path.sep,
                               "make_return_code.py -r 0"])
        cmdl_cur = Commandline.Commandline()
        str_return = str(cmdl_cur.func_CMD(str_command = str_command))
        self.func_test_equals(str_answer, str_return)

    def test_func_cmd_for_simple_command_return_negative(self):
        """
        Test the case of sending a simple command and getting the return
        value of -11 (failure)
        """
        # Set up environment
        str_answer = str(False)
        str_command = "python sciedpiper/make_return_code.py -r -11"
        cmdl_cur = Commandline.Commandline()
        str_return = str(cmdl_cur.func_CMD(str_command = str_command))
        self.func_test_equals(str_answer, str_return)

    def test_func_cmd_for_simple_command_return_positive(self):
        """
        Test the case of sending a simple command and getting the return
        value of 99 (failure)
        """
        # Set up environment
        str_answer = str(False)
        str_command = "python sciedpiper/make_return_code.py -r 99"
        cmdl_cur = Commandline.Commandline()
        str_return = str(cmdl_cur.func_CMD(str_command = str_command))
        self.func_test_equals(str_answer, str_return)

    def test_func_cmd_for_simple_command_return_exception(self):
        """
        Test the case of sending a simple command and having an exception
        throw in the call (failure)
        """
        # Set up environment
        str_answer = str(False)
        str_command = "python sciedpiper/make_return_code.py -e"
        cmdl_cur = Commandline.Commandline()
        str_return = str(cmdl_cur.func_CMD(str_command = str_command))
        self.func_test_equals(str_answer, str_return)

    def test_func_cmd_for_test_mode(self):
        """
        Test the case of send a simple command
        """
        # Set up environment
        str_test_file = "test_func_cmd_for_simple_command.txt"
        str_answer = "hello"
        self.func_remove_files([str_test_file])
        str_command = "echo \"" + str_answer + "\" > " + str_test_file
        # Send command and get result
        cmdl_cur = Commandline.Commandline()
        f_success = cmdl_cur.func_CMD(str_command = str_command, f_test = True)
        # Get confirmation that file was written correctly
        f_success = f_success and not os.path.exists(str_test_file)
        # Destroy environment
        self.func_remove_files([str_test_file])


    def test_func_cmd_for_piped_command(self):
        """
        Test the case of send a piped command
        """
        # Set up environment
        str_test_file_1 = "test_func_cmd_for_piped_command_1.txt"
        str_test_file_2 = "test_func_cmd_for_piped_command_2.txt"
        str_answer = "hello"
        str_expected_answer = "he"
        self.func_remove_files([str_test_file_1, str_test_file_2])
        str_setup_command = "echo \"" + str_answer + "\" > " + str_test_file_1
        str_command = "".join(["cat ", str_test_file_1, " | cut -f 1 -d ",
                               str_answer[2], " > ", str_test_file_2])
        # Send command and get result
        cmdl_cur = Commandline.Commandline()
        cmdl_cur.func_CMD(str_command = str_setup_command)
        cmdl_cur.func_CMD(str_command = str_command)
        # Get confirmation that file was written correctly
        with open(str_test_file_2) as hndl_test:
            str_result = hndl_test.read()[:-1]
            self.func_test_equals(str_expected_answer, str_result)
        # Destroy environment
        self.func_remove_files([str_test_file_1, str_test_file_2])


    def test_func_cmds_for_two_commands(self):
        """
        Test the case of send a piped command
        """
        # Set up environment
        str_test_file_1 = "test_func_cmd_for_piped_command_1.txt"
        str_test_file_2 = "test_func_cmd_for_piped_command_2.txt"
        str_answer = "hello"
        str_expected_answer = "he"
        self.func_remove_files([str_test_file_1, str_test_file_2])
        str_setup_command = "echo \"" + str_answer + "\" > " + str_test_file_1
        str_command = "".join(["cat ", str_test_file_1, " | cut -f 1 -d ",
                               str_answer[2], " > ", str_test_file_2])
        # Send command and get result
        cmdl_cur = Commandline.Commandline()
        cmdl_cur.func_CMDs([str_setup_command, str_command])
        # Get confirmation that file was written correctly
        with open(str_test_file_2) as hndl_test:
            str_result = hndl_test.read()[:-1]
            self.func_test_equals(str_expected_answer, str_result)
        # Destroy environment
        self.func_remove_files([str_test_file_1, str_test_file_2])

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(CommandlineTester)
