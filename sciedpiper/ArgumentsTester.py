# -*- coding: utf-8 -*-


"""
Tests the arguments module.
"""

import argparse
import Arguments
import ParentPipelineTester
import unittest

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2016"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


class ArgumentsTester(ParentPipelineTester.ParentPipelineTester):
    """
    Tests the Argument object.
    """

    str_help = "".join(["--help: {'default': '==SUPPRESS==', ",
                        "'var_name': 'help', ",
                        "'type': \"<type 'bool'>\", ",
                        "'option_strings': ['-h', '--help'], ",
                        "'choices': None}"])
    str_empty_positionals = "".join(["__positional_arguments__: ",
                                     "{'var_name': [], ",
                                     "'type': \"<type 'list'>\", ",
                                     "'option_strings': [], ",
                                     "'choices': []"])

    ########################
    # func_extract_arguments
    ########################
    def test_func_extract_arguments_for_one_string_flag(self):
        """ Testing extract_arguments for one string flag. """
        prsr_arguments = argparse.ArgumentParser(prog="test_func_extract_arguments_for_one_string_flag",
                                                 description="Custom Script",
                                                 conflict_handler="resolve",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        prsr_arguments.add_argument("-b",
                                    dest="str_one",
                                    default=None)
        str_answer = Arguments.Arguments.func_extract_argument_info(prsr_arguments)
        str_result = "".join(["{",
                              self.str_help,
                              ", ",
                              "-b: {'default': None, ",
                              "'var_name': 'str_one', ",
                              "'type': \"<type 'str'>\", ",
                              "'option_strings': ['-b'], ",
                              "'choices': None}",
                              ", ",
                              self.str_empty_positionals,
                              "}}"])
        self.func_test_equals(str_result, self.func_dict_to_string(str_answer))

    def test_func_extract_arguments_for_one_string_flag_default(self):
        """ Testing extract_arguments for one string flag checking the default. """
        prsr_arguments = argparse.ArgumentParser(prog="test_func_extract_arguments_for_one_string_flag",
                                                 description="Custom Script",
                                                 conflict_handler="resolve",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        prsr_arguments.add_argument("-b",
                                    dest="str_one",
                                    default="DEFAULT")
        str_answer = Arguments.Arguments.func_extract_argument_info(prsr_arguments)
        str_result = "".join(["{",
                              self.str_help,
                              ", ",
                              "-b: {'default': 'DEFAULT', ",
                              "'var_name': 'str_one', ",
                              "'type': \"<type 'str'>\", ",
                              "'option_strings': ['-b'], ",
                              "'choices': None}",
                              ", ",
                              self.str_empty_positionals,
                              "}}"])
        self.func_test_equals(str_result, self.func_dict_to_string(str_answer))

    def test_func_extract_arguments_for_one_positional(self):
        """ Testing extract_arguments for one positional argument. """
        prsr_arguments = argparse.ArgumentParser(prog="test_func_extract_arguments_for_one_positional",
                                                 description="Custom Script",
                                                 conflict_handler="resolve",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        prsr_arguments.add_argument(dest="str_one")
        str_answer = Arguments.Arguments.func_extract_argument_info(prsr_arguments)
        str_result = "".join(["{",
                              self.str_help,
                              ", ",
                              "__positional_arguments__: ",
                              "{'var_name': ['str_one'], ",
                              "'type': \"<type 'list'>\", ",
                              "'option_strings': [], ",
                              "'choices': []",
                              "}}"])
        self.func_test_equals(str_result, self.func_dict_to_string(str_answer))

    def test_func_extract_arguments_for_three_positional(self):
        """ Testing extract_arguments for three positional argument. """
        prsr_arguments = argparse.ArgumentParser(prog="test_func_extract_arguments_for_three_positional",
                                                 description="Custom Script",
                                                 conflict_handler="resolve",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        prsr_arguments.add_argument(dest="str_a")
        prsr_arguments.add_argument(dest="str_b")
        prsr_arguments.add_argument(dest="str_c")
        str_answer = Arguments.Arguments.func_extract_argument_info(prsr_arguments)
        str_result = "".join(["{",
                              self.str_help,
                              ", ",
                              "__positional_arguments__: ",
                              "{'var_name': ['str_a', 'str_b', 'str_c'], ",
                              "'type': \"<type 'list'>\", ",
                              "'option_strings': [], ",
                              "'choices': []",
                              "}}"])
        self.func_test_equals(str_result, self.func_dict_to_string(str_answer))

    def test_func_extract_arguments_for_one_positional_one_flag(self):
        """ Testing extract_arguments for one positional and one flag argument. """
        prsr_arguments = argparse.ArgumentParser(prog="test_func_extract_arguments_for_one_positional_one_flag",
                                                 description="Custom Script",
                                                 conflict_handler="resolve",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        prsr_arguments.add_argument(dest="str_one")
        prsr_arguments.add_argument("-b",
                                    dest="str_one",
                                    default="DEFAULT")
        str_answer = Arguments.Arguments.func_extract_argument_info(prsr_arguments)
        str_result = "".join(["{",
                              self.str_help,
                              ", ",
                              "-b: {'default': 'DEFAULT', ",
                              "'var_name': 'str_one', ",
                              "'type': \"<type 'str'>\", ",
                              "'option_strings': ['-b'], ",
                              "'choices': None}",
                              ", ",
                              "__positional_arguments__: ",
                              "{'var_name': ['str_one'], ",
                              "'type': \"<type 'list'>\", ",
                              "'option_strings': [], ",
                              "'choices': []",
                              "}}"])
        self.func_test_equals(str_result, self.func_dict_to_string(str_answer))

    def test_func_extract_arguments_for_many_types(self):
        """ Testing extract_arguments for flags of many types and features. """
        prsr_arguments = argparse.ArgumentParser(prog="test_func_extract_arguments_for_many_types",
                                                 description="Custom Script",
                                                 conflict_handler="resolve",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # str
        prsr_arguments.add_argument("-b",
                                    dest="str_one",
                                    default=None)
        # str default
        prsr_arguments.add_argument("-c",
                                    dest="str_two",
                                    default="test")
        # int
        prsr_arguments.add_argument("-i",
                                    dest="int_one",
                                    type=int,
                                    default=8)
        # boolean true
        prsr_arguments.add_argument("-a",
                                    dest="f_one",
                                    default=True,
                                    action="store_false")
        # boolean false
        prsr_arguments.add_argument("-f",
                                    dest="f_two",
                                    default=False,
                                    action="store_true")
        # list
        prsr_arguments.add_argument("-d",
                                    dest="list_one",
                                    default=[],
                                    nargs="*")
        # str choices
        prsr_arguments.add_argument("-e",
                                    dest="str_choices",
                                    default=None,
                                    choices=["one", "two", "three"])
        str_answer = Arguments.Arguments.func_extract_argument_info(prsr_arguments)
        str_result = "".join(["{",
                              self.str_help,
                              ", ",
                              "-a: {'default': True, ",
                              "'var_name': 'f_one', ",
                              "'type': \"<type 'bool'>\", ",
                              "'option_strings': ['-a'], ",
                              "'choices': None}, ",
                              "-b: {'default': None, ",
                              "'var_name': 'str_one', ",
                              "'type': \"<type 'str'>\", ",
                              "'option_strings': ['-b'], ",
                              "'choices': None}, ",
                              "-c: {'default': 'test', ",
                              "'var_name': 'str_two', ",
                              "'type': \"<type 'str'>\", ",
                              "'option_strings': ['-c'], ",
                              "'choices': None}, ",
                              "-d: {'default': [], ",
                              "'var_name': 'list_one', ",
                              "'type': \"<type 'list'>\", ",
                              "'option_strings': ['-d'], ",
                              "'choices': None}, ",
                              "-e: {'default': None, ",
                              "'var_name': 'str_choices', ",
                              "'type': \"<type 'str'>\", ",
                              "'option_strings': ['-e'], ",
                              "'choices': ['one', 'two', 'three']}, ",
                              "-f: {'default': False, ",
                              "'var_name': 'f_two', ",
                              "'type': \"<type 'bool'>\", ",
                              "'option_strings': ['-f'], ",
                              "'choices': None}, ",
                              "-i: {'default': 8, ",
                              "'var_name': 'int_one', ",
                              "'type': <type 'int'>, ",
                              "'option_strings': ['-i'], ",
                              "'choices': None}",
                              ", ",
                              self.str_empty_positionals,
                              "}}"])
        self.func_test_equals(str_result, self.func_dict_to_string(str_answer))


#Creates a suite of tests
def suite():
    """ Suite aggregates tests and is used to run tests. """
    return unittest.TestLoader().loadTestsFromTestCase(ArgumentsTester)
