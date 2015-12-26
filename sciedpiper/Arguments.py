
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse

# Constants
C_STR_OPTION_STRINGS = "option_strings"
C_STR_TYPE = "type"
C_STR_VARIABLE_NAME = "var_name"

# Constants Types
C_STR_INT_TYPE = "<type 'int'>"
C_STR_LIST_TYPE = "<type 'list'>"
C_STR_FLOAT_TYPE = "<type 'float'>"
C_STR_STRING_TYPE = "<type 'str'>"
C_STR_BOOL_TYPE = "<type 'bool'>"

class Arguments( object ):
    """
    Consolidates code involving arguments.
    """

    @classmethod
    def func_extract_argument_info( self, args ):

        if not args:
            return {}

        dict_argument_info = {}

        # Extract 
        for str_arg_key, str_arg_value in args._optionals._option_string_actions.items():

            str_long_flag = str_arg_value.option_strings[ 0 ]
            for str_flag in str_arg_value.option_strings:
                if ( str_flag[ 0:2 ] == "--" ) and ( not str_long_flag[ 0:2 ] == "--" ):
                    str_long_flag = str_flag
                    break

            dict_argument_info[ str_long_flag ] = {}
            dict_argument_info[ str_long_flag ][ C_STR_OPTION_STRINGS ] = str_arg_value.option_strings

            # Find the name of the destination variable
            dict_argument_info[ str_long_flag ][ C_STR_VARIABLE_NAME ] = str_arg_value.dest

            # Find the argument type.
            dict_argument_info[ str_long_flag ][ C_STR_TYPE ] = str_arg_value.type
            if not dict_argument_info[ str_long_flag ][ C_STR_TYPE ]:
                if str_arg_value.nargs == 0:
                    dict_argument_info[ str_long_flag ][ C_STR_TYPE ] = C_STR_BOOL_TYPE
                elif str_arg_value.nargs > 1:
                    dict_argument_info[ str_long_flag ][ C_STR_TYPE ] = C_STR_LIST_TYPE
                else:
                    dict_argument_info[ str_long_flag ][ C_STR_TYPE ] = C_STR_STRING_TYPE

        return dict_argument_info

