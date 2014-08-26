
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import Command
import Commandline
import DependencyTree
import logging
import os
import shutil
import sys
import time


# Constants
# This is a list of paths that should never be allowed to be deleted
LSTR_INVALID_OUTPUT_DIRECTORIES = [ os.path.sep ]
# File extensions
STR_GZIPPED_EXT = ".gz"


class Pipeline:
    """
    This object is an aggregation of functions needed to simply and easily create analysis pipelines.
    """
    
    c_lstr_special_commands = [ "cd", "rm", "mkdir" ]
    """
    These are special commands which should not be handled by subproc but should be
    handled in other ways including using os functions. This is not a complete list and should be
    added to as the need arises.
    """


    def __init__( self, str_name = "", str_log_to_file = None, str_log_level = logging.INFO, str_update_source_path = None ):
        """ 
        Initiator has an optional parameter to set logging for a specific file.
        
        * str_name : String
                     Name of the pipeline, currently used in logging

        * str_log_to_file : String ( file path )
                            If a file path is given, logging will occur to the file.
                            Otherwise, logging is directed to standard out.

        * str_log_level : String ( logging level )
                          Controls the level of logging. must be a valid logging level, see argparse.
        """

        self.cmdl_execute = Commandline.Commandline( str_name )
        """ Simple interface for running commandline """
        
        self.f_execute = True
        """ If made false, the pipeline documents itself but does not execute """

        self.f_use_bash = False
        """ 
        If made true, will tell the commandline to be ran in bash (for bash specific commands).
        If true will reduce the range of OS this can be ran on, not WIndows for instance.
        """

        self.str_name = str_name
        """ Pipeline name """
        
        self.str_prefix_command = ""
        """ A prefix to add to all commands, used to make commands bsub commands """
        
        #Lastly make logger
        self.str_log_file = str_log_to_file
        """ File to log to """
        
        self.logr_logger = self.func_make_logger( str_log_file = self.str_log_file, str_logging_level = str_log_level )
        """ Logger for the pipeline. """
        
        #Holds updates for class paths
        #Paths to prefix to the jar command
        self.dict_update_path = {}
        if str_update_source_path:
            for str_path in str_update_source_path.split( "," ):
                str_command, str_path = str_path.split( ":" )
                self.dict_update_path[ str_command ] = str_path


    # Tested
    def func_check_files_exist( self, lstr_files ):
        """
        Makes sure files exist before starting
        
        * lstr_files : List of strings ( file paths )
                       Each file path will be checked to see if it points
                       to a real file. If not an error will be logged and false returned.
        
        * Return : Boolean
                   True indicates all files exist.
        """

        self.logr_logger.debug( "Pipeline.func_check_files_exist: Checking that files exist." )
        
        if not lstr_files:
            return False
        
        # Check for the files existing
        # If they do return true else indicate in logging and return false.
        f_success = True
        for str_file in lstr_files:
            if not os.path.isfile( str_file ):
                f_success = False
                self.logr_logger.error( " ".join( ["Pipeline.func_check_files_exist:", str_file, "does not exist." ] ) )
        return f_success


    # Tested 2
    def func_do_bsub( self, str_memory = 8, str_queue = "" ):
        """
        Makes each command a bsub command.
        The commands will not run at once but will run one after the other using bsub.
        
        * str_memory : String
                       The max amount of memory a task will use, this ammount will be requested

        * str_queue : String
                      Which queue to run in.
        """
        self.logr_logger.debug( "Pipeline.func_do_bsub: BSUBing files")
        lstr_bsub_logging = [] if not self.str_log_file else [ "-o ", os.path.splitext( self.str_log_file )[0], ".out ",
                                                              " -e ", os.path.splitext( self.str_log_file )[0], ".err " ]
        self.str_prefix_command = "".join( [ "bsub -N " ] + 
                                           lstr_bsub_logging + 
                                           [ "-q ", str_queue, " -K -R \"rusage[mem=", str( str_memory ), "]\" " ] ) 


    # Tested
    def func_do_special_command( self, cmd_cur, f_test = False ):
        """
        Perform a special command as opposed to using sub proc.
        
        * cmd_cur : Command
                    Handles commands which can not use subproc.

        Return : Boolean
                 True indicates the command was handled. This does not mean executed.
                 For example, in test mode, the command will be logged but not executed.
        """

        str_cmd = cmd_cur.str_command.split(" ")[0].lower()
        
        # Handle cd
        if str_cmd == "cd":
            if f_test:
                return True
            str_path = cmd_cur.str_command.split(" ")[ 1 ]
            
            # Handle relative paths
            if not str_path[ 0 ] == os.path.sep:
                str_path = os.path.join( os.getcwd(), str_path )
            self.logr_logger.debug( " ".join( [ "Pipeline.func_do_special_command: chdir to", str_path ] ) )
            
            # If in execute mode actually perform command
            self.logr_logger.info( "".join( [ "Pipeline.func_do_special_command: Moving to ", str_path, 
                                                " which exists." if os.path.exists( str_path ) else " which does NOT exist." ] ) )
            
            try:
                os.chdir( str_path )
            except OSError:
                return False
            return True
        
        # Handle rm
        elif( str_cmd == "rm"):
            self.logr_logger.info( " ".join( [ "Pipeline.func_do_special_command: rm should not be used as a command.",
                                              "Path removal should instead be handled through the pipeline's",
                                              "built-in cleaning levels ( which have safety checks )." ] ) )
        
        # handle mkdir
        elif( str_cmd == "mkdir" ):
            self.logr_logger.info( " ".join( [ "Pipeline.func_do_special_command: mkdir should not be used as a command.",
                                              "The pipeline has specific functions to handle safe directory creation.",
                                              "Try using Pipeline's method func_mkdirs."] ))

        return False
    
    
    def func_make_logger( self, str_log_file = None, str_logging_level = logging.INFO ):
        """
        Sets up the logger for the pipeline.

        * str_log_to_file : String ( file path )
                            If a file path is given, logging will occur to the file.
                            Otherwise, logging is directed to standard out.

        * str_log_level : String ( logging level )
                          Controls the level of logging. must be a valid logging level, see argparse.

        * Return : Logger
               : Logger named the same as the pipeline
        """

        logr_logger = logging.getLogger( self.str_name )
        """ Logger for the pipeline"""

        # If a file is given, log to file, otherwise log to stdout
        # Create logger, set formatting, and add level
        hndl_logging = logging.StreamHandler( stream = sys.stdout )
        if str_log_file:
	    str_log_folder = os.path.dirname( str_log_file )
	    if str_log_folder:
	        if not os.path.exists( str_log_folder ):
		    os.makedirs( str_log_folder )
            hndl_logging = logging.FileHandler( filename = str_log_file, mode = "w" )
        hndl_logging.setFormatter( logging.Formatter( "%(asctime)s - %(name)s - %(levelname)s - %(message)s" ) )
        logr_logger.addHandler( hndl_logging )
        logr_logger.setLevel( str_logging_level )
        return logr_logger


    # Tested
    def func_get_ok_file_path( self, str_path ):
        """
        Make the file path for an "ok" file, currently used
        as an invisible file indicating a file is valid for use
        being produced from a command that completed without error.
        
        * str_path : String
                     Path of file to base the ok file on
                     
        * Return : String
                   A path for an ok file. This does not create the file.
        """

        if not str_path:
            return ".ok"
        str_path, str_file = os.path.split( str_path ) 
        return( os.path.join( str_path, "".join( [ ".", str_file, ".ok" ] ) if str_file else ".ok" ) )


    # Tested
    def func_handle_gzip( self, lstr_files ):
        """
        Changes the name of the file to a command to uncompress the file if it is compressed.
    
        lstr_files : List of strings
                   : Paths to files that may or may not be gzipped.
               
        Return : lstr_files
               : List of file paths updated to commands that will uncompress the files if needed           
        """

        if not lstr_files:
            return lstr_files
        
        # Handle in case a string is accidently given
        if isinstance( lstr_files, basestring ):
            lstr_files = [ lstr_files ] 

        # If gzipped files are used then let pipeline know so the bash shell is used
        lstr_return_string = []
        for str_uncompress_files in lstr_files:
            if os.path.splitext( str_uncompress_files )[1] == STR_GZIPPED_EXT:
                lstr_return_string.append( " ".join( [ "<( zcat", str_uncompress_files, ")" ] ) )
                self.f_use_bash = True
            else:
                lstr_return_string.append( str_uncompress_files )
        return lstr_return_string
    

#    def func_check_installed( self, lstr_programs ):
#        """ Checks that each of the programs are installed. """
#        
#        # Test mode does nothing
#        if not self.f_execute:
#            return True
#
#        f_success = True
#        for str_program in lstr_programs:
#            self.logr_logger.info( " ".join( [ "Checking if", str_program, "exists."] ) )
#            f_check_program = True
#            if True: # TODO fix
#                self.logr_logger.info( " ".join( [ "Found", str_program ] ) )
#        else:
#            self.logr_logger.error( " ".join( [ "Could not find", str_program, "stopping analysis, premature termination of pipeline." ] ) )
#            f_success = f_success and f_check_program
#        return f_success


    # Tested
    def func_is_special_command( self, cmd_cur ):
        """
        Check to see if the command is a special command which should not be handled as a subprocess.
        
        An example would be cd which uses os commands.
        
        cmd_cur : Command
                  Command to be checked to see if it needs special handling outside of subproc.

        Return : Boolean
                 True indicates the command needs special handling
        """
        
        return cmd_cur.str_command.split(" ")[0].lower() in Pipeline.c_lstr_special_commands


    # Tested
    def func_is_valid_path_for_removal( self, str_path, str_output_directory ):
        """
        Checks if a file or directory is valid for deletion.
        
        Here this is defined as being in the output directory and the output directory not being '/'
        
        Note: The output directory must be an absolute path
        
        * str_path : String
                   : Path to remove
                   
        * str_output_directory : String
                               : Directory that bounds the deletion area
                               
        * Return : Boolean
                 : True indicates the path is valid for deletion
        """
        
        # Ignore invalid states
        if ( not str_path ) or ( not str_output_directory ):
            return False
        
        # Check to make sure the output directory is an absolute path
        if not str_output_directory[ 0 ] == os.path.sep:
            return False
        
        # Check to make sure the file/directory is an absolute path
        if not str_path[ 0 ] == os.path.sep:
            return False
        
        # Resolve the paths as absolute paths ( in case of craziness like /path/path2/../path3/.. )
        str_output_directory = os.path.abspath( str_output_directory )
        str_path = os.path.abspath( str_path )
        
        # Make sure both paths are not in the invalid directories to delete
        if str_output_directory in LSTR_INVALID_OUTPUT_DIRECTORIES or str_path in LSTR_INVALID_OUTPUT_DIRECTORIES:
            return False
        
        # The path must be found in the output dir so the output dir can not be longer than the path
        # They can be equal if the output directory is deleted
        i_out_dir_length = len( str_output_directory )
        if( len( str_path ) < i_out_dir_length ):
            return False
        
        # Check to make sure the output directory is the beginning of the path
        if ( not str_path[0: i_out_dir_length ] == str_output_directory ):
            return False
        
        return True


    # Tested
    def func_mkdirs( self, lstr_directory_paths ):
        """ 
        Makes sure all directories exist and if not creates them.
        
        * lstr_directory_paths : List of strings ( paths )
                                 Each path to a directory will be made if it does not exist.
        
        * Return : Boolean
                   True indicates all directories either existed or were created. 
        """
        
        # Test mode checks to see if directories exist
        if not self.f_execute:
            self.logr_logger.debug( "Pipeline.func_mkdirs: Checking folders exists, making any that do not." )
            for str_dir in lstr_directory_paths:
                if os.path.exists( str_dir ):
                    self.logr_logger.info( " ".join( [ "Pipeline.func_mkdirs: Test mode:: This directory already exists are you sure you want to use it? ", str_dir] ) )
                else:
                    self.logr_logger.info( " ".join( [ "Pipeline.func_mkdirs: Test mode:: This directory would be made. ", str_dir ] ) )
            return True
        
        # Execute mode
        try:
            for str_dir in lstr_directory_paths:
                if not os.path.exists( str_dir ):
                    os.makedirs( str_dir )
                    self.logr_logger.info( " ".join( [ "Pipeline.func_mkdirs: Created directory", str_dir ] ) )
                else:
                    self.logr_logger.info( " ".join( [ "Pipeline.func_mkdirs: Did not create the following directory because it already exists", str_dir ] ) )
            return True
        except Exception as e:
            self.logr_logger.error( " ".join( [ "Pipeline.func_mkdirs: Received an error while creating the", str_dir, "directory. Stopping analysis, premature termination of pipeline. Error = ", str( e ) ] ) )
        return False
    

    # Tested, could test more (products)
    def func_paths_are_from_valid_run( self, cmd_command, f_dependencies ):
        """
        Check to make sure the file is from a command that completed, not one that prematurely ended.
        Can check either if the products or the dependencies of the command are valid.
        
        * cmd_command : Command
                    Command to check dependencies.
        * f_dependencies : Boolean
                         : True checks dependencies, false checks products
        * Return : Boolean
                   True indicates the dependency is safe to use from a completed command.
        """

        # Return false on invalid data
        if not cmd_command or not cmd_command.func_is_valid():
            self.logr_logger.error( "Pipeline.func_paths_are_from_valid_run: Received an invalid command to check validity. Comamnd=" + str( cmd_command ) )
            return False
        
        # Check that each dependency is valid
        for str_dependency in cmd_command.lstr_dependencies if f_dependencies else cmd_command.lstr_products:
            if not os.path.exists( self.func_get_ok_file_path( str_dependency ) ):
                return False
        return True


    # Tested
    def func_remove_paths( self, cmd_command, str_output_directory, dt_dependency_tree, f_remove_products, f_test = False ):
        """
        This handles the deletion of a path and should be the only place in the pipeline deletion can occur.
        Deleting files and directories are both very dangerous operations.
        
        For products, remove all products
        For dependencies, remove dependencies of the correct cleaning level
        ( Files of the clean level Command.ALWAYS are always cleaned, Command.NEVER are never cleaned )
        Paths can be files or directories, directories are removed in total, including *_all_* contents.
        
        Note the output directory path and the paths in the command to be deleted should be absolute.

        To be removed a path must:
        1. Exist
        2. Be valid for removal ( in the output directory )
        3. Be of the correct clean level or a less restrictive level ( dependencies )
        4. Be an intermediate file that is no longer needed ( dependencies unless the clean level is ALWAYS, or a product )
        5. NO dependency will be removed that has a file's clean level is NEVER
        Also removes the ok file if needed
        
        * cmd_command : Command
                        Command in which all products listed will be deleted.
                        
        * str_output_directory : String
                               : The output directory for the pipeline run.
                               : The pipeline can only delete in it's output directory
                        
        * dt_dependency_tree : DependencyTree
                             : The dependency tree for the pipeline run, indicates if a file is intermediary
        
        * f_remove_products : Boolean
                            : True removes products, False remove dependencies

        * Return : Boolean
                 : True indicates all paths were safely removed
        """

        if not cmd_command or not cmd_command.func_is_valid() or not str_output_directory or not dt_dependency_tree:
            return False

        # If the output directory path is not absolute, do not delete.
        if not str_output_directory[ 0 ] == os.path.sep:
            self.logr_logger.error( " ".join( [ "Pipeline.func_remove_paths: The output directory was not absolute, no removing will occur.",
                                               "Output directory =", str_output_directory ] ) )
            return False

        # Check first if each product is valid to be removed
        # We want to fail together so nothing is removed if one is a problem
        lstr_paths_to_remove = cmd_command.lstr_products if f_remove_products else cmd_command.func_get_dependencies_to_clean_level( Command.CLEAN_NEVER )
        # Remove any input file
        lstr_paths_to_remove = list( set( lstr_paths_to_remove ) - set( dt_dependency_tree.lstr_inputs ) )
        
        # If testing, indicate what files would be deleted and return
        if f_test:
            self.logr_logger.info( "".join( [ "In test mode, would have deleted the following paths: ",",".join( lstr_paths_to_remove ) ] ) )
            return True

        for str_path in lstr_paths_to_remove:
            # Make sure paths are valid first, no playing in directories we are not supposed to be in
            if not self.func_is_valid_path_for_removal(str_path = str_path, str_output_directory = str_output_directory):
                self.logr_logger.error( " ".join( [ "Pipeline.func_remove_paths: Could not remove this path, it is not valid to remove.",
                                                  "You should only be deleting from the output directory of the pipeline.",
                                                  "Output directory =", str_output_directory,". Path =", str_path ] ) )
                return False

        # Handle removing paths
        # For products, remove all products
        # For dependencies, remove dependencies of the correct cleaning level    
        # Paths are removed if they:
        # 1. Exist
        # 2. Are valid for removal ( in the output directory )
        # 3. Of the correct clean level or a less restrictive level ( dependencies )
        # 4. Is an intermediate file that is no longer needed ( dependencies unless the clean level is ALWAYS )
        # 5. NO dependency will be removed if it is of clean level NEVER ( this logic is in func_get_dependencies_to_clean_level )
        # Also removes the ok file, this is done first so if there is an error during the path removal, the
        # Ok file will already be removed and the path will be considered invalid by the rest of the pipeline
        for str_path in lstr_paths_to_remove:
            # TODO Add back
            # If the file does not exist, remove the ok file
            if not os.path.exists( str_path ):
#                self.logr_logger.error( " ".join( [ "Could not remove this path, it does not exist.",
#                                                   "Deleting ok file ( if it exists ) and moving on."
#                                                   "Path = ", str_path ] ) )
#                str_ok = self.func_get_ok_file_path( str_path = str_path )
#                if self.f_execute:
#                    if os.path.exists( str_ok ):
#                        os.remove( str_ok )
                continue

            # If it is a dependency, if needed check if it is a dependency that is intermediate and used.
            # If it is still needed, skip over it unless it is indicated
            # To always be deleted...should not set a file to ALWAYS unless you mean it
            if not f_remove_products:

                i_clean_level = cmd_command.func_get_clean_level( str_file_path = str_path )
#                 if i_clean_level is None:
#                     self.logr_logger.error( " ".join( [ "Pipeline.func_remove_paths: Could not find the clean level for this file so could not delete. File =", str_path ] ) )
#                     continue

                if i_clean_level == Command.CLEAN_AS_TEMP:
                    if not dt_dependency_tree.func_is_used_intermediate_file( str_path ):
                        self.logr_logger.info( " ".join( [ "Pipeline.func_remove_paths: Not removing the following path, it is still needed.", str_path ] ) )
                        continue
            
	    else:
                # Remove ok file first to invalidate
                str_ok = self.func_get_ok_file_path( str_path = str_path )

                if os.path.exists( str_ok ):
                    self.logr_logger.info( " ".join( [ "Pipeline.func_remove_paths: Removing the ok file:", str_ok ] ) )
                    if self.f_execute:
                        os.remove( str_ok )
            
            # Remove path
            if os.path.isfile( str_path ):
                self.logr_logger.info( " ".join( [ "Pipeline.func_remove_paths: Removing the file:", str_path ] ) )
                if self.f_execute:
                    os.remove( str_path )
            else:
                self.logr_logger.info( " ".join( [ "Pipeline.func_remove_paths: Removing the directory:", str_path ] ) )
                if self.f_execute:
                    shutil.rmtree( str_path )
        # No errors occurred so returning true                    
        return True


    def func_run_commands( self, lcmd_commands, str_output_dir, f_clean = False, str_run_name = "", li_wait = None ):
        """
        Runs all commands in serial and logs the time each took.
        Will stop on error.
        
        * lstr_commands : List of strings ( commands )
                          Each command will be ran in order until completion or failure.
                          Each command will also be logged and timed.

        * f_clean : Boolean
                    True indicates files should be deleted when no longer needed dependent on their clean level.

        * Return : Boolean
                   True indicates no error occurred
        """

        # Check incoming parameters
        if not lcmd_commands or not len( lcmd_commands ) or not str_output_dir:
            return False
        
        # Keeps track of success.
        f_success = True

        # Log the beginning of the pipeline
        self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Starting pipeline", self.str_name ] ) )
        
        # Make sure the output directory is an absolute path
        # Need to work with absolute files so that it can be
        # Identified that the input files are in the output directory
        str_current_path_for_abs_paths = os.getcwd()
        if not str_output_dir[ 0 ] == os.path.sep:
                str_output_dir = os.path.join( str_current_path_for_abs_paths, str_output_dir )

        # Update the paths of commands before the dependency tree is made, otherwise they will not match the current state of the commands
        for cmd_command in lcmd_commands:
            # Update the command with a path if needed.
            self.func_update_command_path( cmd_command, self.dict_update_path )

        # Load up the commands and build the dependency tree
        # This skips special commands
        dt_dependencies = DependencyTree.DependencyTree( [ cmd_cur for cmd_cur in lcmd_commands 
                                                          if not self.func_is_special_command( cmd_cur ) ],
                                                          self.logr_logger )
        # Manage the wait for checking for products
        # Set the wait for checking for products
        if not li_wait is None:
            dt_dependencies.li_waits_for_products = li_wait
        # If we are testing only, remove the wait
        if not self.f_execute:
            dt_dependencies.func_remove_wait()
        
        # Run each command until all are completed or a failure occurs.
        for cmd_command in lcmd_commands:
            # Log the start
            self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Starting", str( cmd_command ) ] ) )
            # Do not execute if the products are already made.
            # We do want to clean up if they ask for it.
            if ( self.func_paths_are_from_valid_run( cmd_command, f_dependencies = False ) ):
                self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Skipping command, resulting file already exist from previous valid command. Current command:", cmd_command.str_command ] ) )

                # Complete the command in case it was not
                dt_dependencies.func_complete_command( cmd_command, f_wait = False, f_test = not self.f_execute )
                
                # Add cleaning dependencies
                if f_clean:
                    self.func_remove_paths( cmd_command = cmd_command, str_output_directory = str_output_dir, 
                                        dt_dependency_tree = dt_dependencies, f_remove_products = False, f_test = not self.f_execute )
                continue
            
            # Attempt a command.
            # Start the timing
            d_start = time.time()
 
            # Handle changing directories and other special commands
            if self.func_is_special_command( cmd_command ):
                f_success = self.func_do_special_command( cmd_command, f_test = not self.f_execute )
            else:
                # Add bsub prefix if needed to the command.
                str_executed_command = "".join( [ self.str_prefix_command, cmd_command.str_command ] )
                self.logr_logger.info( "".join( [ "Pipeline.func_run_commands: executing ", str_executed_command ] ) )
                f_success = f_success and self.cmdl_execute.func_CMD( str_executed_command, f_use_bash = self.f_use_bash, f_test = not self.f_execute )
                self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Successfully executed." ] ) )
                # If the command is successful, indicate it is complete and potentially clean up stale dependencies
                if f_success:
                    f_success = f_success and dt_dependencies.func_complete_command( cmd_command, f_test = not self.f_execute )
                    self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Updated dependencies.", str( f_success ) ] ) )

                # Update the products so the pipeline knows they are from valid command calls
                # Make sure that the products area indicated to be complete
                if f_success and self.f_execute:
                    if not self.func_update_products_validity_status( cmd_command = cmd_command, dt_tree = dt_dependencies ):
                        self.logr_logger.error( "Pipeline.func_run_commands: Could not indicate to future commands that a product is valid" )
                        self.logr_logger.error( " ".join([ "Pipeline.func_run_commands: The following files are invalid and should be removed if they exist,",
                                                          "an attempt was made to remove them." ] + cmd_command.lstr_products ) )
                        f_success = False
                        
                # Add cleaning dependencies if executing and cleaning
                if f_success and f_clean:
                    f_success = f_success and self.func_remove_paths( cmd_command = cmd_command, str_output_directory = str_output_dir, 
                                        dt_dependency_tree = dt_dependencies, f_remove_products = False, f_test = not self.f_execute )
                        
                if not f_success:
                    # If the command was not successful, remove all products if cleaning.
                    self.logr_logger.error( " ".join( [ "Pipeline.func_run_commands: Was not successful, deleting products produced by error." ] ) )
                    
                    # Remove products
                    self.func_remove_paths( cmd_command = cmd_command, str_output_directory = str_output_dir,
                                            dt_dependency_tree = dt_dependencies, f_remove_products = True, f_test = not self.f_execute )
                
            if self.f_execute:
                self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Time::", str( round( time.time() - d_start ) ) ] ) )
            
            # Return on failure
            if ( not f_success ) and self.f_execute:
                self.logr_logger.error( "Pipeline.func_run_commands: The last command was not successful. Pipeline run failed." )
                return f_success
       
        # Log successful completion and return success.
        if f_success:
            self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Successfully ended pipeline", self.str_name ] ) )
            if f_clean:
                self.logr_logger.info( "\n".join( [ "Pipeline.func_run_commands: This pipeline had cleaning turned on.",
                                       "The following products were terminal and should exist:",
                                       ",".join( dt_dependencies.lstr_terminal_products ),
                                       "The following input dependencies should still exist:",
                                       ", ".join( dt_dependencies.lstr_inputs ),
                                       "If a file was requested to exist with clean settings, it should also exist." ] ) )
            else:
                self.logr_logger.info("Pipeline.func_run_commands: Cleaning was not turned on. All files should be available.")
        else:
            self.logr_logger.error( "Pipeline.func_run_commands: The pipeline completed but was unsuccessful. Pipeline run failed." )
        return f_success


    # 1 test
    def func_update_command_path( self, cmd_cur, dict_update_cur ):
        """
        Allows a way to update commands with a path but from the external call incase they can not be put in an env path.
        
        * cmd_cur : Command
                  : Command to update (update is permanent)
        * dict_update_cur : Dictionary { 'command', 'path' }
                          : Dictionary with paths to prefix to the commands
        """

        if cmd_cur and cmd_cur.func_is_valid():
            for str_cmd, str_path in dict_update_cur.iteritems():
                if str_cmd in cmd_cur.str_command:
                    cmd_cur.str_command = cmd_cur.str_command.replace( str_cmd, os.path.join( str_path, str_cmd ) )
                    

    # Tested
    def func_update_products_validity_status( self, cmd_command, dt_tree ):
        """
        Indicates to the dependency tree object that the products of the given command are valid.
        These products must exist if made valid (this is checked).
        
        * cmd_command : Command
                        Command which contains the products to update.
                       
        * Return : Boolean
                   Indicator of success, if false the status was not updated.
        """
        
        # Return false on invalid data
        if not cmd_command or not cmd_command.func_is_valid():
            self.logr_logger.error( "Pipeline.func_update_products_validity_status: Received an invalid command to update validity. Did not update." )
            return False
        
        if not dt_tree:
            self.logr_logger.error( "Pipeline.func_update_products_validity_status: Received an invalid dependency tree. Did not update." )
            return False
        
        # Handle making valid by making an ok file for the dir or file (each product)
        if not dt_tree.func_products_are_made( cmd_command ):
            self.logr_logger.error( "Pipeline.func_update_products_validity_status: Was to validate a command's products, some of which were missing. Did not update.")
            return False
        
        if self.f_execute:
            for str_product in cmd_command.lstr_products:
                open( self.func_get_ok_file_path( str_product ), "a" ).close()
                
        return True


    # Tested
    def func_test_mode( self ):
        """
        Switches pipeline into test mode.
        """
        self.f_execute = False