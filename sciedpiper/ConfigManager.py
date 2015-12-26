
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse
import Arguments
import ConfigParser

# Constants
C_STR_ARGUMENTS_SECTION = "arguments_over_write"
    
class ConfigManager( object ):
    """
    Manages SciEDPipeR configuration files. These configuration files allow one to over write parameters passed
    into scripts. This allows different environmental setting to be passed in while still using an otherwise
    standard command or changing calls to the pipeline only because the script is in a different environment.
    """

    @classmethod
    def _func_type_cast( self, str_type_string, str_value ):

        if str_value.lower() == "none":
            return None
        if str_type_string == Arguments.C_STR_INT_TYPE:
            return int( str_value )
        elif str_type_string == Arguments.C_STR_LIST_TYPE:
            return eval( str_value )
        elif str_type_string == Arguments.C_STR_FLOAT_TYPE:
            return float( str_value )
        elif str_type_string == Arguments.C_STR_BOOL_TYPE:
            return eval( str_value )
        elif str_type_string == Arguments.C_STR_STRING_TYPE:
            return str_value
        else:
            raise TypeError( "ConfigManager::_func_type_cast:Unknown type string. Type =" + str( str_type_string ) )


    @classmethod
    def func_update_arguments( self, args_parsed, dict_args_info, str_configuration_file_path ):

        if not args_parsed or not str_configuration_file_path:
            return {}

        # Read in configuration file
        config = ConfigParser.RawConfigParser()
        config.read( str_configuration_file_path )

        # Make a dict of flags to key for the args
        dict_args_key = {}
        for str_key, dict_values in dict_args_info.items():
            for str_flag in dict_values[ Arguments.C_STR_OPTION_STRINGS ]:
                dict_args_key[ str_flag ] = str_key
                dict_args_key[ str_flag.lstrip( "-" ) ] = str_key

        # For each entry in the Arguments section, update the argparser
        # use the argument flag
        for str_config_key, str_config_value in config.items( C_STR_ARGUMENTS_SECTION ):
            if not str_config_key in dict_args_key:
                # If the argument not found from the config file in the pipeline arguments, except.
                raise NameError( " ".join([ "ConfigManager::func_update_arguments:Could not find the entry from the config file in this pipeline's arguments.",
                                            "Check to make sure the following argument is in the pipeline's arguments:",
                                            str_config_key ]) )
            str_variable = dict_args_info[ dict_args_key[ str_config_key ] ][ Arguments.C_STR_VARIABLE_NAME ]
            str_config_type = dict_args_info[ dict_args_key[ str_config_key ] ][ Arguments.C_STR_TYPE ]
            # Need to set type.
            setattr( args_parsed, str_variable, ConfigManager._func_type_cast( str( str_config_type ), str_config_value ) )
        return args_parsed
