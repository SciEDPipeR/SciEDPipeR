#!/usr/bin/env python


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse
import JSONManager
import os
import Pipeline

# Constants
# Keys for alignment return ( dicts )
INDEX_CMD = "cmd"
INDEX_FILE = "out_file"
INDEX_FOLDER = "align_folder"

class ParentScript:
    
    def func_create_arguments( self ):
        """
        Create arguments.
        
        return : Standard set of arguments
               : Arguments
        """

        # Standard command line arguments
        prsr_arguments = argparse.ArgumentParser( prog = "custom.py", description = "Custom Script", conflict_handler="resolve", formatter_class = argparse.ArgumentDefaultsHelpFormatter )
        prsr_arguments.add_argument( "-b", "--bsub_queue", metavar = "BSUB_Queue", dest = "str_bsub_queue", default = None, help = "If given, each command will sequentially be ran on this queue with bsub." )
        prsr_arguments.add_argument( "-c", "--clean", dest = "f_clean", default = False, action="store_true", help = "Turns on (true) or off (false) cleaning of intermediary product files." ) 
        prsr_arguments.add_argument( "--copy", metavar = "Copy_location", dest = "lstr_copy", default = None, action="append", help="Paths to copy the output directory after the pipeline is completed. Output directory must be specified; can be used more than once for multiple copy locations.")
        prsr_arguments.add_argument( "-g", "--log", metavar = "Optional_logging_file", dest = "str_log_file", default = None, help = "Optional log file, if not given logging will be to the standard out." )
        prsr_arguments.add_argument( "--json_out", metavar = "JSON_out", dest = "str_json_file_out", default = None, help = "Write script to a JSON file." )
        prsr_arguments.add_argument( "-m", "--max_bsub_memory", metavar = "Max_BSUB_Mem", dest = "str_max_memory", default = "8", help = "The max amount of memory in GB requested when running bsub commands." )
        prsr_arguments.add_argument( "--move", metavar = "Move_location", dest = "str_move_dir", default = None, help = "The path where to move the output directory after the pipeline ends. Can be used with the copy argument if both copying to one location(s) and moving to another is needed. Must specify output directory." )
        prsr_arguments.add_argument( "-n", "--threads", metavar = "Process_threads", dest = "i_number_threads", type = int, default = 1, help = "The number of threads to use for multi-threaded steps." )
        prsr_arguments.add_argument( "-o", "--out_dir", metavar = "Output_directory", dest = "str_file_base", default = "", help = "The output directory where results will be placed. If not given a directory will be created from sample names and placed with the samples." )
        prsr_arguments.add_argument( "-t", "--test", dest = "f_Test", default = False, action = "store_true", help = "Will check the environment and display commands line but not run.")
        prsr_arguments.add_argument( "-u", "--update_command", dest = "str_update_classpath", default = None, help = "Allows a class path to be added to the jars. eg. 'command.jar:/APPEND/THIS/PATH/To/JAR,java.jar:/Append/Path'")
        prsr_arguments.add_argument( "--compress", dest = "str_compress", default = "none", choices = Pipeline.LSTR_COMPRESSION_HANDLING_CHOICES, help = "Turns on compression of products and intermediary files made by the pipeline. Valid choices include:" + str( Pipeline.LSTR_COMPRESSION_HANDLING_CHOICES ) )
        return prsr_arguments

    def func_update_arguments( self, args_raw ):
        """
        This will be overridden by the child of the parent script if there
        is a need to add to the arguments or to change the name of the parser.
        
        * args_call : Standardized arguments to add to / modify
                    : Arguments object
        * return : Updated arguments
                 : Arguments object
        """
        pass
    
    
    def func_run_pipeline( self ):
        """
        Runs housekeeping code before the pipeline is ran.
        
        This is the function that is called by children objects to run.
        """

        # Allow child object to update arguments
        prsr_arguments = self.func_create_arguments()
        self.func_update_arguments( prsr_arguments )

        # Parse arguments from command line
        args_call = prsr_arguments.parse_args()

        # Holds the commands to run
        lcmd_commands = []

        ## Output dir related
        # If the output dir is not specified then move and copy functions are disabled
        f_archive = True
        # Make a default output folder based on the time if not given
        # Make default log
        if not args_call.str_file_base:
            f_archive = False
            args_call.str_file_base = os.getcwd()

        # If an output / project folder is indicated.
        if args_call.str_file_base:
            # Make the output directory if it does not exist
            if not os.path.isdir( args_call.str_file_base ):
                os.mkdir( args_call.str_file_base )

        # Make pipeline object and indicate Log file
        pline_cur = Pipeline.Pipeline( str_name = "Custom_script", 
                                       str_log_to_file = args_call.str_log_file, 
                                       str_update_source_path = args_call.str_update_classpath if hasattr( args_call, "str_update_classpath" ) else None )

        # Put pipeline in test mode if needed.
        if args_call.f_Test:
            pline_cur.func_test_mode()
            
        # Turn off archiving if output directory was not given
        if not f_archive:
            pline_cur.logr_logger.warning( "ParentScript.func_run_pipeline: Turning off archiving, please specify an output directory if you want this feature enabled.")
            pline_cur.f_archive = False
    
        # Make commands bsub if indicated
        if args_call.str_bsub_queue:
            pline_cur.func_do_bsub( str_memory = args_call.str_max_memory, str_queue = args_call.str_bsub_queue )

        # Run the user based pipeline
        # If the commands are not existent ( parsed from JSON )
        # then build them from script
        if not lcmd_commands:
            lcmd_commands = self.func_make_commands( args_parsed = args_call, cur_pipeline = pline_cur )

        # Write JSON file
        if args_call.str_json_file_out:
            JSONManager.func_pipeline_to_json( lcmd_commands=lcmd_commands , dict_args=args_call , str_file=args_call.str_json_file_out )

        # Run commands
        if not pline_cur.func_run_commands( lcmd_commands = lcmd_commands, 
                                            str_output_dir = args_call.str_file_base,
                                            lstr_copy = args_call.lstr_copy if args_call.lstr_copy else None,
                                            str_move = args_call.str_move_dir if args_call.str_move_dir else None,
                                            str_compression_mode = args_call.str_compress,
                                            f_clean = args_call.f_clean ):
            exit( 99 )
    
    
    def func_make_commands( self,  args_parsed, cur_pipeline ):
        """
        Allows:
        - the creation of commands in the child object.
        - the creation of directories.
        - checking that files exist.
        
        The commands will then be ran after this method.
        The pipeline object is given here so that one can update
        the pipeline if needed. Please do not run the pipeline here.
        Please do not add the commands to the pipeline.
        
        * args_parsed : Current arguments from command line already parsed
                      : Parsed Arguments
        * cur_pipeline : Pipeline to run the commands incase configuring is needed.
                       : Pipeline
        * return : List of command objects
        """
        return []
