
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse
import Arguments
import collections
import ConfigParser
import ParentScript
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
C_STR_SAMPLE_FILE_SECTION = "SAMPLE_FILE"

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

    # TODO Test
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


    # TODO Test
    def func_normalize_argument( self, str_argument, dict_args_normalized ):
        """ Takes an argument (short or long form) and normalizes the argument to one of the possible arguments.
            If the argument is not found, an exception (NameError) is raised.
            If the argument is found, a normalized value for it is returned.
        """

        if ( not str_argument ) or ( not str_argument in dict_args_normalized ):
            raise NameError( " ".join([ "ConfigManager::func_update_arguments:Could not find the entry from the config file in this pipeline's arguments.",
                                        "Check to make sure the following argument is in the pipeline's arguments:",
                                        str_argument ]) )
        return dict_args_normalized[ str_argument ]


    # TODO Test
    def func_update_arguments( self, args_parsed, dict_args_info, lstr_sample_arguments = None, lstr_locked_arguments = []):

        if not args_parsed:
            return {}

        # List of updated arguments
        lstr_updated_arguments = []

        # Make a dict of flags to key for the args
        # { flag( could be short or long with and without dashes ) : normalized flag }
        dict_args_key = {}
        if dict_args_info:
            for str_key, dict_values in dict_args_info.items():
                if not str_key == Arguments.C_STR_POSITIONAL_ARGUMENTS:
                    for str_flag in dict_values[ Arguments.C_STR_OPTION_STRINGS ]:
                        dict_args_key[ str_flag ] = str_key
                        dict_args_key[ str_flag.lstrip( "-" ) ] = str_key

        # Arguments section
        # For each entry in the Arguments section, update the argparser
        # Type cast as need and normalize argument.
        # Store updated argument
        for str_config_key, str_config_value in self.config.items( C_STR_ARGUMENTS_SECTION ):
            if not str_config_key in dict_args_key:
                # If the argument not found from the config file in the pipeline arguments, except.
                raise NameError( " ".join([ "ConfigManager::func_update_arguments:Could not find the entry from the config file in this pipeline's arguments.",
                                            "Check to make sure the following argument is in the pipeline's arguments:",
                                            str_config_key ]) )
            str_config_key_norm = self.func_normalize_argument( str_config_key, dict_args_key )
            if str_config_key_norm in lstr_locked_arguments:
                # Check to make sure the key is not locked.
                raise NameError( "\n".join([ "ConfigManager::func_update_arguments:Certain arguments can not be updated with a pipeline config file.",
                                            "These keys include: " ] + lstr_locked_arguments + [ "Please do not update " + str_config_key_norm + " in the pipeline config file. " ] ) )
            lstr_updated_arguments.append( str_config_key_norm )
            str_variable = dict_args_info[ str_config_key_norm ][ Arguments.C_STR_VARIABLE_NAME ]
            str_config_type = dict_args_info[ str_config_key_norm ][ Arguments.C_STR_TYPE ]
            setattr( args_parsed, str_variable, self._func_type_cast( str( str_config_type ), str_config_value ) )

        # Read in the resource file
        dict_resource_info = {}
        ## Read in file and strip
        if args_parsed.str_resource_config:
            with open( args_parsed.str_resource_config, "r" ) as hndl_resource_config:
                lstr_resource_values = [ line.split(":") for line in hndl_resource_config ]
                for lstr_resource in lstr_resource_values:
                    dict_resource_info[ lstr_resource[ 0 ].strip() ] = lstr_resource[ 1 ].strip()

        # Resource section
        ## Read in Resource section
        ## Pull in the resource section values that should refer to keys in the resource config
        ## if it is there update with it.
        for str_resource_key, str_resource_value in self.config.items( C_STR_RESOURCES_SECTION ):
            str_resource_key_norm = self.func_normalize_argument( str_resource_key, dict_args_key )
            if str_resource_key_norm in lstr_locked_arguments:
                # Check to make sure the key is not locked.
                raise NameError( "\n".join([ "ConfigManager::func_update_arguments:Certain arguments can not be updated with a pipeline config file.",
                                            "These keys include: " ] + lstr_locked_arguments + [ "Please do not update " + str_resource_key_norm + " in the pipeline config file. " ] ) )
            str_resource_variable = dict_args_info[ str_resource_key_norm ][ Arguments.C_STR_VARIABLE_NAME ]
            lstr_updated_arguments.append( str_resource_key_norm )
            if str_resource_value in dict_resource_info:
                setattr( args_parsed, str_resource_variable, dict_resource_info[ str_resource_value ] )

        # Sample Section
        # If given sample information over those arguments.
        # Should be unique from both the arguments and resource section.
        if lstr_sample_arguments:
            i_number_sample_items = len( lstr_sample_arguments )
            for str_sample_key, str_sample_value in self.config.items( C_STR_SAMPLE_FILE_SECTION ):
                str_sample_key_norm = self.func_normalize_argument( str_sample_key, dict_args_key )
                if str_sample_key_norm in lstr_locked_arguments:
                    # Check to make sure the key is not locked.
                    raise NameError( "\n".join([ "ConfigManager::func_update_arguments:Certain arguments can not be updated with a pipeline config file.",
                                                 "These keys include: " ] + lstr_locked_arguments + [ "Please do not update " + str_sample_key_norm + " in the pipeline config file. " ]) )
                str_sample_variable = dict_args_info[ str_sample_key_norm ][ Arguments.C_STR_VARIABLE_NAME ]
                lstr_updated_arguments.append( str_sample_key_norm )
                i_sample_item_index = int( str_sample_value ) - 1
                if ( i_sample_item_index >= i_number_sample_items ) or ( i_sample_item_index < 0 ):
                    raise ValueError( "ConfigManager::func_update_arguments:Please note that the sample file given with this pipeline does not have enough items in it given the pipeline config file. Please make sure the sample file is tab delimited. Also make sure that the sample file section does not refer to more elements than exist in the sample file. Remember the pipeline config section is base 1 NOT 0.\nNumber of items in samples file = " + str( i_number_sample_items ) + "\nItems number requested = " + str_sample_value + "\n" )
                setattr( args_parsed, str_sample_variable, lstr_sample_arguments[ i_sample_item_index ] )

            # Update the output directory with the sample name.
            ParentScript.ParentScript.func_make_output_dir( args_parsed )
            setattr( args_parsed, ParentScript.C_STR_OUTPUT_DIR, os.path.join( args_parsed.str_file_base, lstr_sample_arguments[ 0 ] ) )

            # Remove the sample file from the args incase a script is made
            # This will otherwise make an inf loop
            setattr( args_parsed, ParentScript.C_STR_SAMPLE_FILE_DEST, None )

        # Stop if arguments were updated multiple times.
        cntr_args = collections.Counter( lstr_updated_arguments )
        if max( cntr_args.values() ) > 1:
            raise ValueError( "\n".join( [ "ConfigManager::func_update_arguments:Arguments can not be updated multiple times. " ] + [ "Flag: " + str_cntr_key + " , Updated Times: " + str( i_cntr_values ) for str_cntr_key, i_cntr_values in cntr_args.items() ] ) )

        # Check to make sure the config file substitutions did not violate any
        # Choices specified.
        for str_long_flag, dict_flag_info in dict_args_info.items():
            if dict_flag_info[ Arguments.C_STR_CHOICES ]:
                if not getattr( args_parsed, dict_flag_info[ Arguments.C_STR_VARIABLE_NAME ] ) in dict_flag_info[ Arguments.C_STR_CHOICES ]:
                    print " ".join( [ "When using the pipeline config file, please be aware of variables with restricted values (or choices).",
                                      "Please only use allowed choices for the variable. Look into the help for the flag :", str_long_flag ] )
                    exit( 103 )
        return args_parsed


    # TODO Test
    def func_update_env_path( self ):
        # Read in the path updates
        for str_config_key, str_config_value in self.config.items( C_STR_PATH_SECTION ):
            # Update ENV PATH with str_config_value
            if str_config_key.lower() == C_STR_ENV_PATH_SECTION.lower():
                os.environ[ "PATH" ] = os.environ[ "PATH" ] + ":" + str_config_value.rstrip("/")
                return str_config_value.rstrip("/")
        return None


    # TODO Test
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


    # TODO Test
    def func_update_script_path( self, str_script_path ):
        # Update the script path or return False indicating that it was not needed.
        for str_config_key, str_config_value in self.config.items( C_STR_PATH_SECTION ):
            if str_config_key.lower() == C_STR_SCRIPT_PATH_SECTION.lower():
                return os.path.join( str_config_value, str_script_path )
        return False


    # TODO Test
    def func_get_precommands( self ):
        for str_command_key, str_command_value in self.config.items( C_STR_COMMANDS_SECTION ):
            if str_command_key.lower() == C_STR_PRECOMMANDS_SECTION.lower():
                return str_command_value


    # TODO Test
    def func_get_postcommands( self ):
        for str_command_key, str_command_value in self.config.items( C_STR_COMMANDS_SECTION ):
            if str_command_key.lower() == C_STR_POSTCOMMANDS_SECTION.lower():
                return str_command_value
