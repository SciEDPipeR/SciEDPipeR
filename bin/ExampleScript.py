#!/usr/bin/env python


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import os
import sciedpiper.Command as Command
import sciedpiper.ParentScript as ParentScript

class ExampleScript( ParentScript.ParentScript ):
    
    def func_update_arguments(self, arg_raw ):
        """
        Updates to the arg parser, command line options
        
        * arg_raw : Arguments ( not yet parsed )
                  : Arguments
        * return  : Updated Arguments
                  : Arguments
        """

        arg_raw.prog = "ExampleScript.py"
        arg_raw.description = "New Example Description."
        arg_raw.add_argument("-z","--example", dest = "str_new_variable_to_play_with", default = "Defaultvalue", help = "An example help text." )        


    def func_make_commands( self, args_parsed, cur_pipeline ):
        """
        Allows:
        - the creation of commands in the child object.
        - the creation of directories.
        - checking that files exist.
        
        To know the variables available from command line look in the ParentScript in func_create_arguments.
        """

        # Have file names, using the os library to have dynamic paths
        str_test_file_dependency = "ExampleScript.py"
        str_test_file_product = os.path.join( args_parsed.str_file_base, "ExampleScriptCopy.txt")
        
        # Make directories and check files that need to exist before beginning
        cur_pipeline.func_mkdirs( [ args_parsed.str_file_base ] )
        cur_pipeline.func_check_files_exist( [ str_test_file_dependency ] )
        
        # Make commands
        lcmd_commands = []
        lcmd_commands.append( Command.Command( str_cur_command = "cat "+str_test_file_dependency+" > "+str_test_file_product,
                                               lstr_cur_dependencies = [ str_test_file_dependency ], 
                                               lstr_cur_products = [ str_test_file_product ] ) )
        
        return lcmd_commands
    
    
if __name__ == "__main__":

    # Needed to run, calls the script
    ExampleScript().fun_run_pipeline()
