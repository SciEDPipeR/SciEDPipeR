
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
import os
import sys

# Constants
C_STR_ARGUMENTS_SECTION = "ARGUMENTS_OVER_WRITE"
C_STR_COMMANDS_SECTION = "COMMANDS"
C_STR_PATH_SECTION = "PATH"
C_STR_ENV_PATH_SECTION = "ENV_PATH"
C_STR_SCRIPT_PATH_SECTION = "SCRIPT_PATH"
C_STR_PYTHON_PATH_SECTION = "PYTHON_PATH"
C_STR_PRECOMMANDS_SECTION = "PRECOMMANDS"
C_STR_POSTCOMMANDS_SECTION = "POSTCOMMANDS"
C_STR_RESOURCES_SECTION = "RESOURCES"

class ConfigManager( object ):
    """
    Manages SciEDPipeR configuration files. These configuration files allow one to over write parameters passed
    into scripts. This allows different environmental setting to be passed in while still using an otherwise
    standard command or changing calls to the pipeline only because the script is in a different environment.
    """

    def __init__( self, str_configuration_file_path ):

        # Read in configuration file
        self.config = ConfigParser.RawConfigParser()
        self.config.read( str_configuration_file_path )


    def _func_type_cast( self, str_type_string, str_value ):

        if str_value == "None":
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


    def func_update_arguments( self, args_parsed, dict_args_info, str_resource_config ):

        if not args_parsed:
            return {}

        # Make a dict of flags to key for the args
        # { flag : destination }
        dict_args_key = {}
        if dict_args_info:
            for str_key, dict_values in dict_args_info.items():
                if not str_key == Arguments.C_STR_POSITIONAL_ARGUMENTS:
                    for str_flag in dict_values[ Arguments.C_STR_OPTION_STRINGS ]:
                        dict_args_key[ str_flag ] = str_key
                        dict_args_key[ str_flag.lstrip( "-" ) ] = str_key

        # For each entry in the Arguments section, update the argparser
        # use the argument flag
        for str_config_key, str_config_value in self.config.items( C_STR_ARGUMENTS_SECTION ):
            if not str_config_key in dict_args_key:
                # If the argument not found from the config file in the pipeline arguments, except.
                raise NameError( " ".join([ "ConfigManager::func_update_arguments:Could not find the entry from the config file in this pipeline's arguments.",
                                            "Check to make sure the following argument is in the pipeline's arguments:",
                                            str_config_key ]) )
            str_variable = dict_args_info[ dict_args_key[ str_config_key ] ][ Arguments.C_STR_VARIABLE_NAME ]
            str_config_type = dict_args_info[ dict_args_key[ str_config_key ] ][ Arguments.C_STR_TYPE ]
            setattr( args_parsed, str_variable, self._func_type_cast( str( str_config_type ), str_config_value ) )

        # Update the resources arguments.
        # If this tries to update something updated within the arguments section of the config file, error
        # Should be unique from the arguments over write section
        dict_resource_info = {}
        ## Read in file and strip
        if str_resource_config:
            with open( str_resource_config, "r" ) as hndl_resource_config:
                lstr_resource_values = [ line.split(":") for line in hndl_resource_config ]
                for lstr_resource in lstr_resource_values:
                    dict_resource_info[ lstr_resource[ 0 ].strip() ] = lstr_resource[ 1 ].strip()
        ## Stop if arguments are in common
        if len( list( set( dict_resource_info.keys() ) & set( dict_args_key.keys() ) ) ) > 0:
            raise ValueError( "ConfigManager::func_update_arguments:Arguments over write and reosurces sections can not update the same arguments. Argument/s in common: " + str( intersect( dict_resource_info.keys(), dict_args_key.keys() ) ) )

        ## Read in Resource section
        ## Pull in the resource section keys that should refer to keys in the resource config
        ## if it is there update with it.
        for str_resource_key, str_resource_value in self.config.items( C_STR_RESOURCES_SECTION ):
            if str_resource_key in dict_resource_info:
                setattr( args_parsed, str_resource_value, dict_resource_info[ str_resource_key ] )

        # Check to make sure the config file substitutions did not violate any
        # Choices specified.
        for str_long_flag, dict_flag_info in dict_args_info.items():
            if dict_flag_info[ Arguments.C_STR_CHOICES ]:
                if not getattr( args_parsed, dict_flag_info[ Arguments.C_STR_VARIABLE_NAME ] ) in dict_flag_info[ Arguments.C_STR_CHOICES ]:
                    print " ".join( [ "When using the pipeline config file, please be aware of variables with restricted values (or choices).",
                                      "Please only use allowed choices for the variable. Look into the help for the flag :", str_long_flag ] )
                    exit( 103 )
        return args_parsed


    def func_update_env_path( self ):
        # Read in the path updates
        for str_config_key, str_config_value in self.config.items( C_STR_PATH_SECTION ):
            # Update ENV PATH with str_config_value
            if str_config_key.lower() == C_STR_ENV_PATH_SECTION.lower():
                os.environ[ "PATH" ] = os.environ[ "PATH" ] + ":" + str_config_value.rstrip("/")
                return str_config_value.rstrip("/")
        return None

    def func_update_python_path( self ):
        # Read in the python path updates
        for str_config_key, str_config_value in self.config.items( C_STR_PATH_SECTION ):
            # Update PATH with str_config_value
            if str_config_key.lower() == C_STR_PYTHON_PATH_SECTION.lower():
                sys.path.append( str_config_value.rstrip("/") )
                if "PYTHONPATH" in os.environ:
                    os.environ[ "PYTHONPATH" ] = os.environ[ "PYTHONPATH" ] + ":" + str_config_value.rstrip("/")
                else:
                    os.environ[ "PYTHONPATH" ] = str_config_value.rstrip("/")
                return str_config_value.rstrip("/")
        return None


    def func_update_script_path( self, str_script_path ):
        # Update the script path or return False indicating that it was not needed.
        for str_config_key, str_config_value in self.config.items( C_STR_PATH_SECTION ):
            if str_config_key.lower() == C_STR_SCRIPT_PATH_SECTION.lower():
                return os.path.join( str_config_value, str_script_path )
        return False


    def func_get_precommands( self ):
        for str_command_key, str_command_value in self.config.items( C_STR_COMMANDS_SECTION ):
            if str_command_key.lower() == C_STR_PRECOMMANDS_SECTION.lower():
                return str_command_value


    def func_get_postcommands( self ):
        for str_command_key, str_command_value in self.config.items( C_STR_COMMANDS_SECTION ):
            if str_command_key.lower() == C_STR_POSTCOMMANDS_SECTION.lower():
                return str_command_value
