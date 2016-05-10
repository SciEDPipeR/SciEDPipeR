# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

"""
Utility functions working with arguments.
"""

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


# Constants
C_STR_CHOICES = "choices"
C_STR_DEFAULT = "default"
C_STR_OPTION_STRINGS = "option_strings"
C_STR_TYPE = "type"
C_STR_VARIABLE_NAME = "var_name"
C_STR_POSITIONAL_ARGUMENTS = "__positional_arguments__"

# Constants Types
C_STR_INT_TYPE = "<type 'int'>"
C_STR_LIST_TYPE = "<type 'list'>"
C_STR_FLOAT_TYPE = "<type 'float'>"
C_STR_STRING_TYPE = "<type 'str'>"
C_STR_BOOL_TYPE = "<type 'bool'>"

class Arguments(object):
    """
    Consolidates code involving arguments.
    """

    # Tested 3-21-2016 6 tests
    @classmethod
    def func_extract_argument_info(cls, args):
        """
        Extract information from parsed arguments and return
            a dict of argument information.

        * args : Namespace
                 Parsed arguments.

        * returns : Dict
                    Dictionary of argument information (both positional and optional.
        """

        if not args:
            return {}

        dict_argument_info = {}

        # Extract
        for _, str_arg_value in args._optionals._option_string_actions.items():

            str_long_flag = str_arg_value.option_strings[0]
            for str_flag in str_arg_value.option_strings:
                if (str_flag[0:2] == "--") and (not str_long_flag[0:2] == "--"):
                    str_long_flag = str_flag
                    break

            dict_argument_info[str_long_flag] = {}
            dict_argument_info[str_long_flag][C_STR_OPTION_STRINGS] = str_arg_value.option_strings

            # Find the name of the destination variable
            dict_argument_info[str_long_flag][C_STR_VARIABLE_NAME] = str_arg_value.dest

            # Find the argument type.
            dict_argument_info[str_long_flag][C_STR_TYPE] = str_arg_value.type
            if not dict_argument_info[str_long_flag][C_STR_TYPE]:
                if str_arg_value.nargs == 0:
                    dict_argument_info[str_long_flag][C_STR_TYPE] = C_STR_BOOL_TYPE
                elif str_arg_value.nargs > 1:
                    dict_argument_info[str_long_flag][C_STR_TYPE] = C_STR_LIST_TYPE
                else:
                    dict_argument_info[str_long_flag][C_STR_TYPE] = C_STR_STRING_TYPE

            # Set default for flags
            dict_argument_info[str_long_flag][C_STR_DEFAULT] = str_arg_value.default

            # Set choices for flags
            dict_argument_info[str_long_flag][C_STR_CHOICES] = str_arg_value.choices

        # Add in positionals
        dict_argument_info[C_STR_POSITIONAL_ARGUMENTS] = {C_STR_TYPE:C_STR_LIST_TYPE,
                                                          C_STR_VARIABLE_NAME:[stract_pos.dest for stract_pos in args._get_positional_actions()],
                                                          C_STR_OPTION_STRINGS:[],
                                                          C_STR_CHOICES : []}

        return dict_argument_info

