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
C_LSTR_LOCKED_ARGS = [ "-o", "--out_dir", C_STR_SAMPLE_FILE_ARG ]

class ParentScript:


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
    
    
    def func_run_pipeline( self ):
        """
        Runs housekeeping code before the pipeline is ran.
        
        This is the function that is called by children objects to run.
        """

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
        dict_args_info = Arguments.Arguments.func_extract_argument_info( prsr_arguments )
        # Parse arguments from command line
        ns_arguments = prsr_arguments.parse_args()

        # Make sure the output directory is set
        self.func_set_output_dir( ns_arguments )

        # Make logger for all jobs
        logr_job = logging.getLogger( C_STR_JOB_LOGGER_NAME )
        hdlr_job = logging.FileHandler( filename = os.path.join( ns_arguments.str_file_base, C_STR_JOB_LOGGER_NAME + ".log" ), mode = "w" )
        hdlr_job.setFormatter( logging.Formatter( "%(asctime)s - %(name)s - %(levelname)s - %(message)s" ) )
        logr_job.addHandler( hdlr_job )
        logr_job.setLevel( logging.INFO )

        # Sample file is outside of the config file, it can not be updated.
        llstr_sample_data = [ None ]
        if ns_arguments.str_sample_file:
            with open( ns_arguments.str_sample_file, "r" ) as hndl_samples:
                llstr_sample_data = [ lstr_row for lstr_row in csv.reader( hndl_samples, delimiter = "\t" ) ]

        # Original output file
        str_orig_out_dir = ns_arguments.str_file_base
 
        # Keeps tack of errors
        f_error_occured = False

        # Run for each sample line (passing None once if no sample was given)
        for lstr_sample_data in llstr_sample_data:

            ns_arguments.str_file_base = str_orig_out_dir

            logr_job.info( "ParentScript::func_run_pipeline. Start Running job = " + lstr_sample_data[ 0 ] )

            # Run a sample
            try:
                f_return = self.func_run_sample( ns_arguments = ns_arguments,
                                                 dict_args_info = dict_args_info,
                                                 lstr_sample_info = lstr_sample_data )

                if f_return:
                    logr_job.info( "ParentScript::func_run_pipeline. Ran WITHOUT error, job = " + lstr_sample_data[ 0 ] )
                else:
                    logr_job.info( "ParentScript::func_run_pipeline. An ERROR occured while running job = " + lstr_sample_data[ 0 ] )
                logr_job.info( "ParentScript::func_run_pipeline. End Running job = " + lstr_sample_data[ 0 ] )


                f_error_occured = f_error_occured or ( not f_return )
            except Exception as e:
                f_error_occured = True
                logr_job.info( "ParentScript::func_run_pipeline. Serious error occured for " + lstr_sample_data[ 0 ] + "." )
                logr_job.info( "ParentScript::func_run_pipeline. Exception for " + lstr_sample_data[ 0 ] + "\n" + str( e ) )
                print( "Could not run sample " + lstr_sample_data[ 0 ] )
                print( e )

        if f_error_occured:
            exit( 999 )
        else:
            exit( 0 )

    def func_run_sample( self, ns_arguments, dict_args_info, lstr_sample_info ):

        # Update the arguments with the config file.
        if ns_arguments.str_pipeline_config_file:
            str_possible_config_file = os.path.realpath( ns_arguments.str_pipeline_config_file )
        else:
            str_possible_config_file = os.path.splitext( os.path.realpath( sys.argv[0] ) )[ 0 ] + C_STR_CONFIG_EXTENSION 
        if os.path.exists( str_possible_config_file ) and ns_arguments.f_use_pipeline_config:
            cur_config_manager = ConfigManager.ConfigManager( str_possible_config_file )
            ns_arguments = cur_config_manager.func_update_arguments( args_parsed=ns_arguments,
                                                                     dict_args_info=dict_args_info,
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
                ParentScript.func_make_output_dir( ns_arguments )
                ## Make the script in the output directory
                str_script_to_run = self.func_make_script( ns_arguments, dict_args_info, str_additional_env_path,
                                       str_additional_python_path, str_updated_script_path,
                                       str_precommands, str_postcommands )
                # Run script
                return( Commandline.Commandline().func_CMD( str_script_to_run, f_use_bash = True ) )
                
        # If a resource config file is given, the pipeline config file must be given
        elif ns_arguments.str_resource_config:
            print "A pipeline config file must be used to map resources from the Resource Config file to the command. Please use a pipeline config file."
            prsr_arguments.print_help()
            return( False )

        # Handle time stamp
        if ( not ns_arguments.i_time_stamp_diff is None ):
            ns_arguments.i_time_stamp_diff = max( ns_arguments.i_time_stamp_diff, 0 )

        # Holds the commands to run
        lcmd_commands = []

        ## Output dir related
        # If the output dir is not specified then move and copy functions are disabled
        f_archive = True
        if not hasattr( ns_arguments, "str_file_base") or not ns_arguments.str_file_base:
            f_archive = False

        ## Make output directory
        ParentScript.func_make_output_dir( ns_arguments )

        # Make pipeline object and indicate Log file
        pline_cur = Pipeline.Pipeline( str_name = prsr_arguments.prog, 
                                       str_log_to_file = ns_arguments.str_log_file if hasattr( ns_arguments, "str_log_file" ) else os.path.join( ns_arguments.str_file_base, "custom_log.txt"), 
                                       str_update_source_path = ns_arguments.str_update_classpath if hasattr( ns_arguments, "str_update_classpath" ) else None )

        # Update the logger with the arguments
        pline_cur.logr_logger.info( "ParentScript.func_run_pipeline: The call to the pipeline was: " + " ".join( [ "\n" ] + sys.argv + [ "\n" ] ) )
        pline_cur.logr_logger.info( "ParentScript.func_run_pipeline: This run was started with the following arguments.\n" +
                                    "\n".join( [ str( str_namespace_key ) + " = " + str( str_namespace_value )
                                    for str_namespace_key, str_namespace_value in vars( ns_arguments ).items() ] + [ "\n" ] ) )

        # Put pipeline in test mode if needed.
        if hasattr( ns_arguments, "f_Test" ) and ns_arguments.f_Test:
            pline_cur.func_test_mode()

        # Turn off archiving if output directory was not given
        if hasattr( ns_arguments, "f_archive" ) and not f_archive:
            pline_cur.logr_logger.warning( "ParentScript.func_run_pipeline: Turning off archiving, please specify an output directory if you want this feature enabled.")
            pline_cur.f_archive = False
    
        # Make commands bsub if indicated
        if hasattr( ns_arguments, "str_bsub_gueue" ) and ns_arguments.str_bsub_queue:
            pline_cur.func_do_bsub( str_memory = ns_arguments.str_max_memory, str_queue = ns_arguments.str_bsub_queue )

        # Run the user based pipeline
        # If the commands are not existent ( parsed from JSON )
        # then build them from script
        # Where variables are being used.
        if ns_arguments.str_wdl:
            # If WDL is being output, switch the vlaue sof the arguments with the name to track
            import inspect
            import copy
            ns_wdl_arguments = copy.deepcopy( ns_arguments )
            lstr_members = [ member[0] for member in inspect.getmembers( ns_wdl_arguments )
                             if not ( member[0].startswith( "_" ) or member[0].endswith( "_" ) or inspect.isroutine( member )) ]
            for str_member in lstr_members:
                setattr( ns_wdl_arguments, str_member, "${"+str_member+"}" )
            lcmd_commands = self.func_make_commands( args_parsed = ns_wdl_arguments, cur_pipeline = pline_cur )
        else:
            lcmd_commands = self.func_make_commands( args_parsed = ns_arguments, cur_pipeline = pline_cur )

        # Write JSON file
        if hasattr( ns_arguments, "str_json_file_out" ) and ns_arguments.str_json_file_out:
            JSONManager.JSONManager.func_pipeline_to_json( lcmd_commands=lcmd_commands , dict_args=vars( ns_arguments ), str_file=ns_arguments.str_json_file_out, f_pretty=True )
            pline_cur.logr_logger.info( "Writing JSON file to: " + ns_arguments.str_json_file_out )
        # Run commands
        if not hasattr( ns_arguments, "lstr_copy" ):
            setattr( ns_arguments, "lstr_copy", None )
        if not hasattr( ns_arguments, "str_move_dir" ):
            setattr( ns_arguments, "str_move_dir", None )
        if not hasattr( ns_arguments, "str_compress" ):
            setattr( ns_arguments, "str_compress",  "none" )
        if not hasattr( ns_arguments, "f_clean" ):
            setattr( ns_arguments, "f_clean", False )
        if not hasattr( ns_arguments, "i_time_stamp_diff" ):
            setattr( ns_arguments, "i_time_stamp_diff", None )
        if not pline_cur.func_run_commands( lcmd_commands = lcmd_commands, 
                                            str_output_dir = ns_arguments.str_file_base,
                                            f_clean = ns_arguments.f_clean,
                                            f_self_organize_commands = ns_arguments.f_self_organize,
                                            li_wait = [ int( str_wait ) for str_wait in ns_arguments.lstr_wait.split(",") ],
                                            lstr_copy = ns_arguments.lstr_copy if ns_arguments.lstr_copy else None,
                                            str_move = ns_arguments.str_move_dir if ns_arguments.str_move_dir else None,
                                            str_compression_mode = ns_arguments.str_compress,
                                            i_time_stamp_wiggle = ns_arguments.i_time_stamp_diff,
                                            str_wdl = ns_arguments.str_wdl,
                                            args_original = ( ns_arguments if ns_arguments.str_wdl else None )):
            return( False )
    
 
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


    def func_make_script( self, ns_arguments, dict_args_info, str_additional_env_path,
                                str_additional_python_path, str_updated_script_path,
                                str_precommands, str_postcommands ):

        str_full_script_name = os.path.join( ns_arguments.str_file_base, os.path.basename( str_updated_script_path ) )
        str_full_script_name = os.path.splitext( str_full_script_name )[0]+".sh"
        lstr_positionals = []

        # Make dict to translate dest to flag
        dict_dest_to_flag = {}
        for str_info_key in dict_args_info:
            if not str_info_key == Arguments.C_STR_POSITIONAL_ARGUMENTS:
                dict_dest_to_flag[ dict_args_info[ str_info_key ][ Arguments.C_STR_VARIABLE_NAME ] ] = str_info_key

        with open( str_full_script_name, "w" ) as hndl_write_script:
            lstr_script_call = [ str_full_script_name ]
            # Add flags and positional arguments
            for str_arg_dest, str_arg_value in vars( ns_arguments ).items():
                if not str_arg_dest in dict_args_info[ Arguments.C_STR_POSITIONAL_ARGUMENTS ][ Arguments.C_STR_VARIABLE_NAME ]:
                    # If the value is boolean
                    # Check the action if it is action_true or action_false
                    # If it is then use the correct flag presence depending on the value and the action.
                    cur_str_flag = dict_dest_to_flag[ str_arg_dest ]
                    if ( isinstance( str_arg_value, bool )):
                        # Handle special cases help
                        if cur_str_flag in [ "-h", "--help" ]:
                            if str_arg_value:
                                lstr_script_call.append( cut_str_flag )
                        elif not str_arg_value == dict_args_info[ cur_str_flag ][ Arguments.C_STR_DEFAULT ]:
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

    def func_set_output_dir( self, ns_arguments ):

        ## Output dir related
        if not hasattr( ns_arguments, "str_file_base") or not ns_arguments.str_file_base:
            ns_arguments.str_file_base = os.getcwd()
        ns_arguments.str_file_base = os.path.abspath( ns_arguments.str_file_base )


    @classmethod
    def func_make_output_dir( self, ns_arguments ):

        # If an output / project folder is indicated.
        if hasattr( ns_arguments, "str_file_base" ):
            # Make the output directory if it does not exist
            if ns_arguments.str_file_base and not os.path.isdir( ns_arguments.str_file_base ):
                os.mkdir( ns_arguments.str_file_base )
        return ns_arguments.str_file_base
