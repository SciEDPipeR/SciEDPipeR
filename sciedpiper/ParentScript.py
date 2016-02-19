#!/usr/bin/env python

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse
import Arguments
import ConfigManager
import Commandline
import csv
import JSONManager
import logging
import os
import Pipeline
import multiprocessing
import stat
import sys


# Constants
C_STR_CONFIG_EXTENSION = ".config"
C_STR_JOB_LOGGER_NAME = "JobRunner"
C_STR_OUTPUT_DIR = "str_file_base"
C_STR_NO_PIPELINE_CONFIG_ARG = "--no_pipeline_config"
C_STR_PIPELINE_CONFIG_FILE_ARG = "--pipeline_config_file"
C_STR_SAMPLE_FILE_ARG = "--sample_file"
C_STR_SAMPLE_FILE_DEST = "str_sample_file"

# Keys for alignment return ( dicts )
INDEX_CMD = "cmd"
INDEX_FILE = "out_file"
INDEX_FOLDER = "align_folder"

# Locked arguments (can not be updated by the pipeline config file.
# Make sure to include all flags and move argparse to the correct group.
C_LSTR_LOCKED_ARGS = [ "-o", "--out_dir", C_STR_SAMPLE_FILE_ARG, "--concurrent_jobs" ]


class ParentScript:


    def __init__( self ):
        self.ns_arguments = None
        self.dict_args_info = None
        self.str_orig_output_dir = None
        self.f_is_multi_job = False
        self.dispr_cur = None

        # Manage arguments
        self.func_manage_arguments( )
        self.func_manage_output_dir( )

        # Keeps tack of errors
        f_error_occured = False

        # Get logging
        self.logr_job = self.func_make_logger()

        # Set in func_parse_jobs()
        self.str_possible_config_file = None
        self.llstr_sample_data = self.func_parse_jobs( )

        # If a resource config file is given, the pipeline config file must be given
        if self.ns_arguments.str_resource_config and not self.str_possible_config_file:
            self.logr_job.error( "A pipeline config file must be used to map resources from the Resource Config file to the command. Please use a pipeline config file." )


    def func_tag_file( self, str_file, str_tag ):
        """ 
        Adds a tag to a file name (at the end of the basename before the extension.
        """
        if not str_file or not str_tag:
            return str_file
        str_base, str_ext = os.path.splitext( str_file )
        return str_base + "_" + str_tag + str_ext


    def func_base_file( self, str_file ):
        return os.path.splitext( os.path.basename( str_file ) )[ 0 ] 


    def func_update_file_location( self, str_file, str_new_dir ):
        return os.path.join( str_new_dir, os.path.basename( str_file ) ) 


    def func_switch_ext( self, str_file, str_ext ):
        return os.path.splitext( str_file )[ 0 ] + "." + str_ext


    def func_create_arguments( self ):
        """
        Create arguments.
        
        return : Standard set of arguments
               : Arguments
        """

        # Standard command line arguments
        prsr_arguments = argparse.ArgumentParser( prog = "custom.py", description = "Custom Script", conflict_handler="resolve", formatter_class = argparse.ArgumentDefaultsHelpFormatter )

        # Built-in functionality
        grp_builtin = prsr_arguments.add_argument_group( "Builtins", "Functionality builtin with the SciEDPipeR engine." )

        grp_builtin.add_argument( "-b", "--bsub_queue", metavar = "BSUB_Queue", dest = "str_bsub_queue", default = None, help = "If given, each command will sequentially be ran on this queue with bsub." )
        grp_builtin.add_argument( "-c", "--clean", dest = "f_clean", default = False, action="store_true", help = "Turns on (true) or off (false) cleaning of intermediary product files." ) 
        grp_builtin.add_argument( "--copy", metavar = "Copy_location", dest = "lstr_copy", default = None, action="append", help="Paths to copy the output directory after the pipeline is completed. Output directory must be specified; can be used more than once for multiple copy locations.")
        grp_builtin.add_argument( "-g", "--log", metavar = "Optional_logging_file", dest = "str_log_file", default = None, help = "Optional log file, if not given logging will be to the standard out." )
        grp_builtin.add_argument( "--json_out", metavar = "JSON_out", dest = "str_json_file_out", default = None, help = "Write script to a JSON file." )
        grp_builtin.add_argument( "--jobs_file", metavar = "JOBS_file", dest = "str_jobs_file", default = None, help = "File with different jobs to run." )
        grp_builtin.add_argument( "-m", "--max_bsub_memory", metavar = "Max_BSUB_Mem", dest = "str_max_memory", default = "8", help = "The max amount of memory in GB requested when running bsub commands." )
        grp_builtin.add_argument( "--move", metavar = "Move_location", dest = "str_move_dir", default = None, help = "The path where to move the output directory after the pipeline ends. Can be used with the copy argument if both copying to one location(s) and moving to another is needed. Must specify output directory." )
        grp_builtin.add_argument( "-n", "--threads", metavar = "Process_threads", dest = "i_number_threads", type = int, default = 1, help = "The number of threads to use for multi-threaded steps." )
        grp_builtin.add_argument( "-o", "--out_dir", metavar = "Output_directory", dest = C_STR_OUTPUT_DIR, default = "", help = "The output directory where results will be placed. If not given a directory will be created from sample names and placed with the samples." )
        grp_builtin.add_argument( "-t", "--test", dest = "f_Test", default = False, action = "store_true", help = "Will check the environment and display commands line but not run.")
        grp_builtin.add_argument( "--user_ordered_commands", dest = "f_self_organize", action = "store_false", default = True, help = "Commands are ordered for execution by dependency and product relationship by default. When including this flag, commands will be ran in the order provided in the script (in the list of commands)." )
        grp_builtin.add_argument( "--timestamp", dest = "i_time_stamp_diff", default = None, type=float, help = "Using this will turn on timestamp and will require the parent to be atleast this amount or more younger than a product in order to invalidate the product.")
        grp_builtin.add_argument( "-u", "--update_command", dest = "str_update_classpath", default = None, help = "Allows a class path to be added to the jars. eg. 'command.jar:/APPEND/THIS/PATH/To/JAR,java.jar:/Append/Path'")
        grp_builtin.add_argument( "--compress", dest = "str_compress", default = "none", choices = Pipeline.LSTR_COMPRESSION_HANDLING_CHOICES, help = "Turns on compression of products and intermediary files made by the pipeline. Valid choices include:" + str( Pipeline.LSTR_COMPRESSION_HANDLING_CHOICES ) )
        grp_builtin.add_argument( "--wait", dest = "lstr_wait", default = "5,15,40", help = "The number of seconds and times the pipeline will wait to check for products after each pipeline command ends. This compensates for IO lag. Should be just integers in seconds delimited by commas. 3,10,20 would indicate wait three seconds, then try again after 10 seconds, and lastly wait for 20 seconds." )

        # Job submission associated
        grp_jobs = prsr_arguments.add_argument_group( "Job Submission", "Pipeline parameters specifically for job submission." )
        grp_jobs.add_argument( C_STR_SAMPLE_FILE_ARG, dest = C_STR_SAMPLE_FILE_DEST, default = None, help = "Sample file for multiple job submission. Tied to the pipeline with the pipeline config file. Must be tab delimited." )
        grp_jobs.add_argument( "--concurrent_jobs", metavar = "Concurrent_Jobs", dest = "i_number_jobs", type = int, default = 1, help = "The maximum number of jobs to run concurrently." )
        grp_jobs.add_argument( "--job_system", metavar = "Queueing_System", dest = "str_job_system", default = C_STR_QSUB, help = "Which system to run the jobs on: " + ", ".join( C_LSTR_DISPATCH_CHOICES ) )

        # Config associated
        grp_config = prsr_arguments.add_argument_group( "Pipeline Config", "Pipeline config files change the running of pipelines. Useful when managing envrionments." )
        grp_config.add_argument( C_STR_NO_PIPELINE_CONFIG_ARG, dest = "f_use_pipeline_config", default = True, action = "store_false", help = "Use this flag to ignore the pipeline config file." )
        grp_config.add_argument( C_STR_PIPELINE_CONFIG_FILE_ARG, dest = "str_pipeline_config_file", default = None, help = "The pipeline config file to use, if not given and using the pipeline config files is turned on then the program will look in the directory where the script is located." )
        grp_config.add_argument( "--resources", dest = "str_resource_config", default = None, help = "Resource config file must be used in conjunction with a pipeline config file." )

        # Experimental functionality
        grp_experimental = prsr_arguments.add_argument_group( "Experimental", "Functionality in process, or not completely genericized." )
        grp_experimental.add_argument( "--wdl", dest = "str_wdl", default = None, help = "When used, the pipeline will not run but instead a wdl file will be generated for the workflow, then this argument is used, please pass the file path to which the wdl file should be written." )

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


    def func_make_logger( self ):

        # Make logger for all jobs
        logr_job = logging.getLogger( C_STR_JOB_LOGGER_NAME )
        hdlr_job = logging.FileHandler( filename = os.path.join( self.ns_arguments.str_file_base, C_STR_JOB_LOGGER_NAME + ".log" ), mode = "w" )
        hdlr_job.setFormatter( logging.Formatter( "%(asctime)s - %(name)s - %(levelname)s - %(message)s" ) )
        logr_job.addHandler( hdlr_job )
        logr_job.setLevel( logging.INFO )
        return( logr_job )


    def func_manage_arguments( self ):

        ## Manage the arguments
        # Start with the parent arguments
        # Allow children script arguments to be added
        # Update arguments with config file for environemntal options
        ##
        # Allow child object to update arguments
        prsr_arguments = self.func_create_arguments()

        # If a prsr is returned, write over the old one.
        # Otherwise do not because it was updated in the function
        prsr_return = self.func_update_arguments( prsr_arguments )
        if prsr_return:
            prsr_arguments = prsr_return

        # Store information about the arguments needed for later functionality
        self.dict_args_info = Arguments.Arguments.func_extract_argument_info( prsr_arguments )

        # Parse arguments from command line
        self.ns_arguments = prsr_arguments.parse_args()

        # Min value for threads is 1
        self.ns_arguments.i_number_jobs = max( self.ns_arguments.i_number_jobs, 1 )

        # Original output file
        self.str_orig_output_dir = self.ns_arguments.str_file_base
 

    def func_manage_output_dir( self ):

        # Make sure the output directory is set
        self.func_set_output_dir( )

        ParentScript.func_make_output_dir( self.ns_arguments )


    def func_parse_jobs( self ):

        llstr_sample_data = [ None ]
        if self.ns_arguments.str_sample_file:
            with open( self.ns_arguments.str_sample_file, "r" ) as hndl_samples:
                llstr_sample_data = [ lstr_row for lstr_row in csv.reader( hndl_samples, delimiter = "\t" ) ]

        if len( llstr_sample_data ) > 1 and self.ns_arguments.i_number_jobs > 1:
            self.f_is_multi_job = True

        # No more job threads than number of jobs requested
        self.ns_arguments.i_number_jobs = min( self.ns_arguments.i_number_jobs, len( llstr_sample_data ) )

        # To run multiple samples, a pipeline confif is required
        if self.ns_arguments.str_pipeline_config_file:
            self.str_possible_config_file = os.path.realpath( self.ns_arguments.str_pipeline_config_file )
        else:
            self.str_possible_config_file = os.path.splitext( os.path.realpath( sys.argv[0] ) )[ 0 ] + C_STR_CONFIG_EXTENSION 
        if not os.path.exists( self.str_possible_config_file ):
            self.logr_job.error( "All jobs with sample files need pipeline config files." )
            return( None )

        return( llstr_sample_data )


    def func_run_pipeline( self ):
        """
        Runs housekeeping code before the pipeline is ran.
        
        This is the function that is called by children objects to run.
        """

        if self.f_is_multi_job:
            self.func_run_many_jobs()
        else:
            script_running.func_run_jobs_locally()


    def func_get_jobs( self ):
        return( self.llstr_sample_data )


    def func_run_jobs_locally( self ):

        # Run for each sample line (passing None once if no sample was given)
        if not self.llstr_sample_data:
            self.logr_job.error( "ParentScript::func_run_pipeline No job found." )
            exit( 998 )

        for lstr_sample_data in self.llstr_sample_data:
            str_current_job = "= " + lstr_sample_data[ 0 ] if lstr_sample_data else ""
            self.logr_job.info( "ParentScript::func_run_pipeline. Start Running job " + str_current_job )

            # Run a sample
            try:
                f_return = self.func_run_sample( lstr_sample_data )

                if f_return:
                    self.logr_job.info( "ParentScript::func_run_pipeline. Ran WITHOUT error, job" + str_current_job )
                else:
                    self.logr_job.info( "ParentScript::func_run_pipeline. An ERROR occured while running job" + str_current_job )
                self.logr_job.info( "ParentScript::func_run_pipeline. End Running job" + str_current_job )


                f_error_occured = f_error_occured or ( not f_return )
            except Exception as e:
                f_error_occured = True
                self.logr_job.info( "ParentScript::func_run_pipeline. Serious error occured for job" + str_current_job )
                self.logr_job.info( "ParentScript::func_run_pipeline. Exception for job" + str_current_job + "\n" + str( e ) )

        if f_error_occured:
            exit( 999 )
        else:
            exit( 0 )


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


    def func_make_script( self, str_additional_env_path,
                                str_additional_python_path, str_updated_script_path,
                                str_precommands, str_postcommands ):

        str_full_script_name = os.path.join( self.ns_arguments.str_file_base, os.path.basename( str_updated_script_path ) )
        str_full_script_name = os.path.splitext( str_full_script_name )[0]+".sh"
        lstr_positionals = []

        # Make dict to translate dest to flag
        dict_dest_to_flag = {}
        for str_info_key in self.dict_args_info:
            if not str_info_key == Arguments.C_STR_POSITIONAL_ARGUMENTS:
                dict_dest_to_flag[ self.dict_args_info[ str_info_key ][ Arguments.C_STR_VARIABLE_NAME ] ] = str_info_key

        with open( str_full_script_name, "w" ) as hndl_write_script:
            lstr_script_call = [ str_full_script_name ]
            # Add flags and positional arguments
            for str_arg_dest, str_arg_value in vars( self.ns_arguments ).items():
                if not str_arg_dest in self.dict_args_info[ Arguments.C_STR_POSITIONAL_ARGUMENTS ][ Arguments.C_STR_VARIABLE_NAME ]:
                    # If the value is boolean
                    # Check the action if it is action_true or action_false
                    # If it is then use the correct flag presence depending on the value and the action.
                    cur_str_flag = dict_dest_to_flag[ str_arg_dest ]
                    if ( isinstance( str_arg_value, bool )):
                        # Handle special cases help
                        if cur_str_flag in [ "-h", "--help" ]:
                            if str_arg_value:
                                lstr_script_call.append( cut_str_flag )
                        elif not str_arg_value == self.dict_args_info[ cur_str_flag ][ Arguments.C_STR_DEFAULT ]:
                            lstr_script_call.append( cur_str_flag )
                    else:
                        lstr_script_call.extend([ cur_str_flag, str( str_arg_value ) ])

            # Add in no config pipeline otherwise the config file is read again and this
            # Both cases make code execute again making an inf loop.
            if not C_STR_NO_PIPELINE_CONFIG_ARG in lstr_script_call:
                lstr_script_call.append( C_STR_NO_PIPELINE_CONFIG_ARG )
            

            # Add positional arguments
            lstr_script_call.extend( lstr_positionals )

            # Make / write script body
            lstr_script = [ "#!/usr/bin/env bash",
                            "",
                            "set -e",
                            "PATH=$PATH:"+str_additional_env_path,
                            "PYTHONPATH=$PYTHONPATH:"+str_additional_python_path,
                            str_precommands,
                            " ".join( lstr_script_call ),
                            str_postcommands ]
            hndl_write_script.write( "\n".join( lstr_script ) )
        os.chmod( str_full_script_name, 0774 )
        return str_full_script_name


    def func_set_output_dir( self ):
        ## Output dir related
        if not hasattr( self.ns_arguments, "str_file_base") or not self.ns_arguments.str_file_base:
            self.ns_arguments.str_file_base = os.getcwd()
        self.ns_arguments.str_file_base = os.path.abspath( self.ns_arguments.str_file_base )


    @classmethod
    def func_make_output_dir( self, ns_arguments ):

        # If an output / project folder is indicated.
        if hasattr( ns_arguments, "str_file_base" ):
            # Make the output directory if it does not exist
            if ns_arguments.str_file_base and not os.path.isdir( ns_arguments.str_file_base ):
                os.mkdir( ns_arguments.str_file_base )
        return ns_arguments.str_file_base


    def func_update_command( self, lstr_sample_info ):

        self.ns_arguments.str_file_base = self.str_orig_output_dir
        cur_config_manager = ConfigManager.ConfigManager( self.str_possible_config_file )
        self.ns_arguments = cur_config_manager.func_update_arguments( args_parsed=self.ns_arguments,
                                                                     dict_args_info=self.dict_args_info,
                                                                     lstr_sample_arguments = lstr_sample_info,
                                                                     lstr_locked_arguments = C_LSTR_LOCKED_ARGS )
        str_additional_env_path = cur_config_manager.func_update_env_path()
        str_additional_python_path = cur_config_manager.func_update_python_path()
        str_updated_script_path = cur_config_manager.func_update_script_path( sys.argv[ 0 ] )
        str_precommands = cur_config_manager.func_get_precommands()
        str_postcommands = cur_config_manager.func_get_postcommands()
        # If needing to update the script path, or add pre/post commands write a script in the output and call it.
        if str_updated_script_path or str_precommands or str_postcommands:
            ## Make output directory
            ParentScript.func_make_output_dir( self.ns_arguments )
            ## Make the script in the output directory
            str_script_to_run = self.func_make_script( str_additional_env_path,
                                   str_additional_python_path, str_updated_script_path,
                                   str_precommands, str_postcommands )

        # Set dispatcher
        self.dspr_cur = Dispatcher.func_make_job_runner( self.ns_arguments.str_job_system )

        # Run script
        return( str_script_to_run )


    def func_get_job_commands( self ):
        lstr_cmds = []
        for lstr_sample_info in self.llstr_sample_data:
            str_cmd = self.func_update_command( lstr_sample_info )
            if str_cmd:
                lstr_cmds.append( self.dispr_cur( str_cmd ) )
        return lstr_cmds


    def func_run_sample( self, lstr_sample_info ):

        str_cmd = func_update_command( lstr_sample_info )
        if str_cmd:
            return( Commandline.Commandline().func_CMD( str_cmd, f_use_bash = True ) )
        elif str_cmd is None:
            # Handle time stamp
            if ( not self.ns_arguments.i_time_stamp_diff is None ):
                self.ns_arguments.i_time_stamp_diff = max( self.ns_arguments.i_time_stamp_diff, 0 )

            # Holds the commands to run
            lcmd_commands = []

            ## Output dir related
            # If the output dir is not specified then move and copy functions are disabled
            f_archive = True
            if not hasattr( self.ns_arguments, "str_file_base") or not self.ns_arguments.str_file_base:
                f_archive = False

            ## Make output directory
            ParentScript.func_make_output_dir( self.ns_arguments )

            # Make pipeline object and indicate Log file
            pline_cur = Pipeline.Pipeline( str_name = prsr_arguments.prog, 
                                       str_log_to_file = self.ns_arguments.str_log_file if hasattr( self.ns_arguments, "str_log_file" ) else os.path.join( self.ns_arguments.str_file_base, "custom_log.txt"), 
                                       str_update_source_path = self.ns_arguments.str_update_classpath if hasattr( self.ns_arguments, "str_update_classpath" ) else None )

            # Update the logger with the arguments
            pline_cur.logr_logger.info( "ParentScript.func_run_pipeline: The call to the pipeline was: " + " ".join( [ "\n" ] + sys.argv + [ "\n" ] ) )
            pline_cur.logr_logger.info( "ParentScript.func_run_pipeline: This run was started with the following arguments.\n" +
                                    "\n".join( [ str( str_namespace_key ) + " = " + str( str_namespace_value )
                                    for str_namespace_key, str_namespace_value in vars( self.ns_arguments ).items() ] + [ "\n" ] ) )

            # Put pipeline in test mode if needed.
            if hasattr( self.ns_arguments, "f_Test" ) and self.ns_arguments.f_Test:
                pline_cur.func_test_mode()

            # Turn off archiving if output directory was not given
            if hasattr( self.ns_arguments, "f_archive" ) and not f_archive:
                pline_cur.logr_logger.warning( "ParentScript.func_run_pipeline: Turning off archiving, please specify an output directory if you want this feature enabled.")
                pline_cur.f_archive = False
    
            # Make commands bsub if indicated
            if hasattr( self.ns_arguments, "str_bsub_gueue" ) and self.ns_arguments.str_bsub_queue:
                pline_cur.func_do_bsub( str_memory = self.ns_arguments.str_max_memory, str_queue = self.ns_arguments.str_bsub_queue )

            # Run the user based pipeline
            # If the commands are not existent ( parsed from JSON )
            # then build them from script
            # Where variables are being used.
            if self.ns_arguments.str_wdl:
                # If WDL is being output, switch the vlaue sof the arguments with the name to track
                import inspect
                import copy
                ns_wdl_arguments = copy.deepcopy( self.ns_arguments )
                lstr_members = [ member[0] for member in inspect.getmembers( ns_wdl_arguments )
                                 if not ( member[0].startswith( "_" ) or member[0].endswith( "_" ) or inspect.isroutine( member )) ]
                for str_member in lstr_members:
                    setattr( ns_wdl_arguments, str_member, "${"+str_member+"}" )
                lcmd_commands = self.func_make_commands( args_parsed = ns_wdl_arguments, cur_pipeline = pline_cur )
            else:
                lcmd_commands = self.func_make_commands( args_parsed = self.ns_arguments, cur_pipeline = pline_cur )

            # Write JSON file
            if hasattr( self.ns_arguments, "str_json_file_out" ) and self.ns_arguments.str_json_file_out:
                JSONManager.JSONManager.func_pipeline_to_json( lcmd_commands=lcmd_commands , dict_args=vars( self.ns_arguments ), str_file=self.ns_arguments.str_json_file_out, f_pretty=True )
                pline_cur.logr_logger.info( "Writing JSON file to: " + self.ns_arguments.str_json_file_out )
            # Run commands
            if not hasattr( self.ns_arguments, "lstr_copy" ):
                setattr( self.ns_arguments, "lstr_copy", None )
            if not hasattr( self.ns_arguments, "str_move_dir" ):
                setattr( self.ns_arguments, "str_move_dir", None )
            if not hasattr( self.ns_arguments, "str_compress" ):
                setattr( self.ns_arguments, "str_compress",  "none" )
            if not hasattr( self.ns_arguments, "f_clean" ):
                setattr( self.ns_arguments, "f_clean", False )
            if not hasattr( self.ns_arguments, "i_time_stamp_diff" ):
                setattr( self.ns_arguments, "i_time_stamp_diff", None )
            if not pline_cur.func_run_commands( lcmd_commands = lcmd_commands, 
                                                str_output_dir = self.ns_arguments.str_file_base,
                                                f_clean = self.ns_arguments.f_clean,
                                                f_self_organize_commands = self.ns_arguments.f_self_organize,
                                                li_wait = [ int( str_wait ) for str_wait in self.ns_arguments.lstr_wait.split(",") ],
                                                lstr_copy = self.ns_arguments.lstr_copy if self.ns_arguments.lstr_copy else None,
                                                str_move = self.ns_arguments.str_move_dir if self.ns_arguments.str_move_dir else None,
                                                str_compression_mode = self.ns_arguments.str_compress,
                                                i_time_stamp_wiggle = self.ns_arguments.i_time_stamp_diff,
                                                str_wdl = self.ns_arguments.str_wdl,
                                                args_original = ( self.ns_arguments if self.ns_arguments.str_wdl else None )):
                return( False )


    def func_run_many_jobs( self ):
        try:
            pool = multiprocessing.Pool() 
            lrslt_success = pool.map_async( func_run_sample, self.func_get_job_commands() )
            lf_success = [ f_success for f_success in lrslt_success.get() ]
        except Exception as e:
            f_error_occured = True
            self.logr_job.info( "ParentScript::func_run_pipeline. Serious error occured for job" )
            self.logr_job.info( "ParentScript::func_run_pipeline. \n" + str( e ) )


# Do no move from top level of module.
# Needs to be here do to pickling and multiprocessing and the pain of it all.
def func_run_sample( str_job ):
        return( Commandline.Commandline().func_CMD( str_job, f_use_bash = True ) )
