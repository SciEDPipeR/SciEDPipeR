#!/usr/bin/env python


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

#import inspect
import os
import Command
import PipelineRunner

class ExampleScript(PipelineRunner.PipelineRunner):
    """
    An example script to run as a test or use as an example.
    This script creates a small directory hierarchy and
    creates files in those directories. Output dir is given by arguments.
    This script incorporates a config file ExampleConfig.config .
    
    output_dir - dir1 - dir4 - file2.txt
                             - file3.txt
                      - dir5
                      - file1.txt
               - dir2 - dir6 - file4.txt
               - dir3 - file5.txt
                      - file6.txt
                      - file7.txt
                      
    Dependency tree for files:
    file1.txt, file5.txt, and file4.txt are treated as input files
    
    file1.txt               file5.txt  file4.txt
    |                        |
    file2.txt                file6.txt
    |                        |
    file3.txt                |
    |________________________|
    |
    file7.txt

    """
    
    def func_update_arguments(self,
                              arg_raw):
        """
        Updates to the arg parser, command line options
        
        * arg_raw : Arguments (not yet parsed)
                  : Arguments
        * return  : Updated Arguments
                  : Arguments
        """

        arg_raw.prog = "ExampleScript.py"
        arg_raw.description = "New Example Description."
        arg_raw.add_argument("-z",
                             "--example",
                             dest="str_new_variable_to_play_with",
                             default="Hello",
                             help="An example help text.")
        return(arg_raw)

    def func_make_commands(self,
                           args_parsed,
                           cur_pipeline):
        """
        Allows:
        - the creation of commands in the child object.
        - the creation of directories.
        - checking that files exist.
        
        To know the variables available from command line
        look in the ParentScript in func_create_arguments.
        """

        # Make directories and check files that need to exist before beginning
        str_dir_1 = os.path.join(args_parsed.str_out_dir, "dir1")
        str_dir_2 = os.path.join(args_parsed.str_out_dir, "dir2")
        str_dir_3 = os.path.join(args_parsed.str_out_dir, "dir3")
        str_dir_4 = os.path.join(str_dir_1, "dir4")
        str_dir_5 = os.path.join(str_dir_1, "dir5")
        str_dir_6 = os.path.join(str_dir_2, "dir6")
        cur_pipeline.func_mkdirs([args_parsed.str_out_dir,
                                  str_dir_1,
                                  str_dir_2,
                                  str_dir_3,
                                  str_dir_4,
                                  str_dir_5,
                                  str_dir_6])
        
        #Make file names and input files
        str_file_1 = os.path.join(str_dir_1, "file1.txt")
        str_file_2 = os.path.join(str_dir_4, "file2.txt")
        str_file_3 = os.path.join(str_dir_4, "file3.txt")
        str_file_4 = os.path.join(str_dir_6, "file4.txt")
        str_file_5 = os.path.join(str_dir_3, "file5.txt")
        str_file_6 = os.path.join(str_dir_3, "file6.txt")
        str_file_7 = os.path.join(str_dir_3, "file7.txt")
        with open(str_file_1, "w") as hndl_file1:
            hndl_file1.write(args_parsed.str_new_variable_to_play_with)
        with open(str_file_4, "w") as hndl_file4:
            hndl_file4.write(args_parsed.str_new_variable_to_play_with)
        with open(str_file_5, "w") as hndl_file5:
            hndl_file5.write(args_parsed.str_new_variable_to_play_with)
        
        # Make commands
        # Make other files given the dependency tree
        lcmd_commands = []
        lcmd_commands.extend([Command.Command(str_cur_command="cat " + str_file_1 + " > " + str_file_2,
                                               lstr_cur_dependencies=[str_file_1], 
                                               lstr_cur_products=[str_file_2]),
                             Command.Command(str_cur_command="cat " + str_file_2 + " > " + str_file_3,
                                               lstr_cur_dependencies=[str_file_2], 
                                               lstr_cur_products=[str_file_3]),
                             Command.Command(str_cur_command="cat " + str_file_5 + " > " + str_file_6,
                                               lstr_cur_dependencies=[str_file_5], 
                                               lstr_cur_products=[str_file_6]),
                             Command.Command(str_cur_command="cat " + str_file_3 + " > " + str_file_7,
                                               lstr_cur_dependencies=[str_file_3, str_file_6], 
                                               lstr_cur_products=[str_file_7])])
        return lcmd_commands
    
    
if __name__ == "__main__":

    # Needed to run, calls the script
    ExampleScript().func_run_pipeline()
