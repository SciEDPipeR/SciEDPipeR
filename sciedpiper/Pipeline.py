
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import Command
import Commandline
import Compression
import DependencyTree
import logging
import os
import shutil
import Resource
import sys
import time

# Constants
# This is a list of paths that should never be allowed to be deleted
LSTR_INVALID_OUTPUT_DIRECTORIES = [ os.path.sep ]
# File extensions
## This extension is auto-detected as compressed and uncompressed if FIFO is on
STR_GZIPPED_EXT = ".gz"
## Valid choices for ways of handling compression
STR_COMPRESSION_NONE = "none"
STR_COMPRESSION_ARCHIVE = "archive"
STR_COMPRESSION_FIRST_LEVEL_ONLY = "level1"
STR_COMPRESSION_AS_YOU_GO = "realtime"
LSTR_COMPRESSION_HANDLING_CHOICES = [ STR_COMPRESSION_NONE, STR_COMPRESSION_ARCHIVE, 
                                     STR_COMPRESSION_FIRST_LEVEL_ONLY, 
                                     STR_COMPRESSION_AS_YOU_GO ]


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
        
        self.f_archive = True
        """
        If made True, archiving (copying and moving the output directory is allowed if requested.
        If made False, archiving is turned off no matter the request.
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

    # Tested 15 tests 2-19-2015
    def func_copy_move( self, lstr_destination, str_archive, f_copy, f_test = False ):
        """
        Either moves a path to a location or copies a path to several locations.
        
        * lstr_destination : Absolute path(s) to copy / move location. When moving a list of 1 path should be provided.
                           : List of strings
        * str_archive : The absolute path that will be moved.
                      : String
        * f_copy : True indicates copy mode ( where the original archive will not be deleted and where multiple 
                   destinations can be copied to ). False indicates move mode ( where the original archive will 
                   be deleted and only one destination will be copied to ).
                 : Boolean
        * f_test : True indicates a test run occurs, no real copy / move action is made but the destination location
                   will be checked to make sure it exists.
                 : Boolean
        * return : Indicator of success ( True, success; False, failure )
        """
        
        # Check inputs
        if not lstr_destination or not str_archive:
            return False
        
        # Check to make sure the path to archive is valid.
        if not f_test and ( not str_archive or not os.path.exists( str_archive ) ):
            self.logr_logger.error( "Pipeline.func_copy_move: Could not move the following path, does not exist:" + str_archive )
            return False

        # Copy mode
        if f_copy:

            # Tracks success
            f_successfully_completed = True

            # Make sure there are locations to copy to
            if len( lstr_destination ) < 1:
                self.logr_logger.error( "Pipeline.func_copy_move: No location was provided to copy to" )
                return False
            
            # Check each destination directory, if any are invalid, not existing, or not a directory, do not copy
            f_file_check = True
            for str_copy_path in lstr_destination:
                # Check that destination exists
                if not str_copy_path or not os.path.exists( str_copy_path ) or not os.path.isdir( str_copy_path ):
                    self.logr_logger.error( "Pipeline.func_copy_move: Did not copy files. The following copy destination " +
                                              "either did not exist or was not a directory: " + str( str_copy_path ) )
                    f_file_check = False
            if not f_file_check:
                return False
            
            # Copy to each directory
            for str_copy_path in lstr_destination:                
                str_copy_file = os.path.join( str_copy_path, os.path.basename( str_archive ) )
                if f_test:
                    self.logr_logger.info( "Pipeline.func_copy_move: Will attempt to copy " + 
                                           str_archive + " to " + str_copy_file )
                else:
                    # Copy
                    if os.path.isdir( str_archive ):
                        # Copy File shutil.copy( src, dst )
                        shutil.copytree( src=str_archive , dst=str_copy_file )
                    else:
                        # Copy Folder shutil.copytree( src = str_output_dir, dst = os.path.join( str_move, str_output_dir ))
                        shutil.copy( src=str_archive, dst=str_copy_file )
                    # Log results
                    if os.path.exists( str_copy_file ):
                        self.logr_logger.info( "Pipeline.func_copy_move: Successfully copied file to " + str_copy_file )
                    else:
                        self.logr_logger.error( "Pipeline.func_copy_move: Failed to copy file to " + str_copy_file )
                        f_successfully_completed = False
            return f_successfully_completed
        else:
            if not len( lstr_destination ) == 1:
                self.logr_logger.error( "Pipeline.func_copy_move: Expected only one move location. " + 
                                       "If you need to move the output directory to multiple locations " +
                                       "please use the copy argument multiple times for multiple destinations "+
                                       " or the copy and move argument for a copy and a move." )
                return False
            # Make sure the target location exists
            str_move_destination = lstr_destination[ 0 ]
            if not str_move_destination or not os.path.exists( str_move_destination ) or not os.path.isdir( str_move_destination ):
                # Log problem with destination path
                self.logr_logger.error( "Pipeline.func_copy_move: Skipped the following move destination. " +
                                              "Either did not exist or was not a directory: " + 
                                              str_move_destination )
                return False
            # Move and check
            str_move_file = os.path.join( str_move_destination, os.path.basename( str_archive ) )
            
            if f_test:
                self.logr_logger.info( "Pipeline.func_copy_move: Will attempt to move " +
                                       str_archive + " to " + str_move_file )
                return True
            else:
                shutil.move( src=str_archive, dst=str_move_file )
                if os.path.exists( str_move_file ):
                    self.logr_logger.info( "Pipeline.func_copy_move: Moved output to: " + str_move_file )
                    return True
                else:
                    self.logr_logger.error( "Pipeline.func_copy_move: Did not move output.")
                    return False

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

        str_cmd = cmd_cur.str_id.split(" ")[0].lower()
        
        # Handle cd
        if str_cmd == "cd":
            if f_test:
                return True
            str_path = cmd_cur.str_id.split(" ")[ 1 ]
            
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
        
        return cmd_cur.str_id.split(" ")[0].lower() in Pipeline.c_lstr_special_commands


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

    # 3 tests
    def func_make_all_needed_dirs( self, lstr_paths ):
        """
        Makes all dirs needed for products.

        * lstr_paths : Paths for which all dirs will be made.
                     : List of paths
        """

        if not lstr_paths:
            return

        for str_file in lstr_paths:
            if not str_file:
                continue
            try:
                os.makedirs( os.path.dirname( str_file ) )
            except OSError:
                pass

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
    
    def func_get_ok_time_stamp( self, str_ok_file_path ):
        """
        Gets the time stamp from an ok file as a float.

        * str_ok_file_path : String
                           : File path to ok file.
        * return : float
        """
        with open( str_ok_file_path, "r" ) as hndl_ok:
            str_time_stamp = hndl_ok.readline()
            str_time_stamp = str_time_stamp.strip("\n" )
            return float( str_time_stamp )

    # Tested, could test more (products)
    def func_paths_are_from_valid_run( self, cmd_command, f_dependencies, i_fuzzy_time = 0 ):
        """
        Check to make sure the file is from a command that completed, not one that prematurely ended.
        This translates to checking for a small invisible file (the "ok file" ) stored with the file
        which has timestamp information. If i_fuzzy_time is not None and is an actualy number, this will 
        also make sure that, when checking a product, the time stamp is checked
        against the parent to make sure the parent has an earlier time stamp. If not the ok file of the product is removed.
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
            self.logr_logger.error( "".join(["Pipeline.func_paths_are_from_valid_run: Received an invalid command to check validity. Command=", str( cmd_command ) if cmd_command is None else cmd_command.str_id ]))
            return False

        # Check that each product is valid
        f_return_valid = True
        # Check that each product is valid
        for rsc_file in cmd_command.lstr_dependencies if f_dependencies else cmd_command.lstr_products:
            str_cur_ok_file = self.func_get_ok_file_path( rsc_file.str_id )
            if not os.path.exists( str_cur_ok_file ):
                self.logr_logger.error( "Pipeline.func_paths_are_from_valid_run: Not yet created without error. PATH=" + cmd_command.str_id )
                f_return_valid = False
            elif ( not i_fuzzy_time is None ):
                i_target_product_time_stamp = self.func_get_ok_time_stamp( str_cur_ok_file )
                for rsc_parent_dep in rsc_file.func_get_dependencies():
                    str_cur_parent_ok_file = self.func_get_ok_file_path( rsc_parent_dep.str_id )
                    if not os.path.exists( str_cur_parent_ok_file ):
                        self.logr_logger.error( " ".join( [ "Pipeline.func_paths_are_from_valid_run: Parent dependency was not been created yet.",
                                                            "Target product PATH=" + rsc_file.str_id,
                                                            "Parent dependency PATH=" + rsc_parent_dep.str_id ] ) )
                        f_return_valid = False
                        continue
                    i_parent_time_stamp = self.func_get_ok_time_stamp( str_cur_parent_ok_file )
                    if ( i_parent_time_stamp + i_fuzzy_time ) < i_target_product_time_stamp:
                        self.logr_logger.error( " ".join( [ "Pipeline.func_paths_are_from_valid_run: Parent dependency was younger than the target product.",
                                                            "Remaking products.",
                                                            "Target product PATH=" + rsc_file.str_id ] ) )
                      
                        #delete ok file
                        f_return_valid = False
                       
        return f_return_valid


    # Tested
    def func_remove_paths( self, cmd_command, str_output_directory, dt_dependency_tree, f_remove_products, f_test = False ):
        """
        This handles the deletion of a path and should be the only place in the pipeline deletion can occur.
        Deleting files and directories are both very dangerous operations.
        
        For products, remove all products including ok files. This is used to delete generated files which are errors.
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
        Also WILL NOT remove the ok file if one is generated unless this is in product mode

        * cmd_command : Command
                        Command in which all products listed will be deleted.
                        
        * str_output_directory : String
                               : The output directory for the pipeline run.
                               : The pipeline can only delete in it's output directory
                        
        * dt_dependency_tree : DependencyTree
                             : The dependency tree for the pipeline run, indicates if a file is intermediary
        
        * f_remove_products : Boolean
                            : True removes products, False remove dependencies, True will remove ok files, used to delete error products.

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
        lstr_paths_to_remove = cmd_command.lstr_products if f_remove_products else cmd_command.func_get_dependencies_to_clean_level( Resource.CLEAN_NEVER )
        lstr_paths_to_remove = [ rsc_remove.str_id for rsc_remove in lstr_paths_to_remove ]
        # Remove any input file
        lstr_paths_to_remove = list( set( lstr_paths_to_remove ) - set( dt_dependency_tree.lstr_inputs ) )
        
        # If testing, indicate what files would be deleted and return
        if f_test:
            self.logr_logger.info( "".join( [ "In test mode, would have deleted the following paths: ",",".join( lstr_paths_to_remove ) ] ) )
            return True

        for str_rsc in lstr_paths_to_remove:
            # Make sure paths are valid first, no playing in directories we are not supposed to be in
            if not self.func_is_valid_path_for_removal(str_path = str_rsc, str_output_directory = str_output_directory):
                self.logr_logger.error( " ".join( [ "Pipeline.func_remove_paths: Could not remove this path, it is not valid to remove.",
                                                  "You should only be deleting from the output directory of the pipeline.",
                                                  "Output directory =", str_output_directory,". Path =", str_rsc ] ) )
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
        # Ok file will not be removed unless in product mode
        for str_path in lstr_paths_to_remove:
            # Checks to make sure the file exists.
            # This is necessary because this function is used to clear out products from a
            # command that error. Given an error is is unknown if the files actually exist
            if not os.path.exists( str_path ):
                continue

            # If it is a dependency, if needed check if it is a dependency that is intermediate and used.
            # If it is still needed, skip over it unless it is indicated
            # To always be deleted...should not set a file to ALWAYS unless you mean it
            if not f_remove_products:
                cur_vertex = dt_dependency_tree.graph_commands.func_get_vertex( str_path )
                i_clean_level = cur_vertex.i_clean
#                 if i_clean_level is None:
#                     self.logr_logger.error( " ".join( [ "Pipeline.func_remove_paths: Could not find the clean level for this file so could not delete. File =", str_path ] ) )
#                     continue

                if i_clean_level == Resource.CLEAN_AS_TEMP:
                    if not dt_dependency_tree.func_is_used_intermediate_file( cur_vertex ):
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
                # If the path is a dir
                self.logr_logger.info( " ".join( [ "Pipeline.func_remove_paths: Removing the directory:", str_path ] ) )
                if self.f_execute:
                    shutil.rmtree( str_path )
        # No errors occurred so returning true                    
        return True


    def func_run_commands( self, lcmd_commands, str_output_dir, f_clean = False, str_run_name = "",
                           li_wait = None, lstr_copy = None, str_move = None, str_compression_mode = None,
                           str_compression_type = "gz", i_time_stamp_wiggle = 0 ):
        """
        Runs all commands in serial and logs the time each took.
        Will NOT stop on error but will attempt all commands.
        
        * lstr_commands : List of strings ( commands )
                          Each command will be ran in order until completion or failure.
                          Each command will also be logged and timed.

        * f_clean : Boolean
                    True indicates files should be deleted when no longer needed dependent on their clean level.

        * i_time_stamp_wiggle : int
                                Time stamps must bemore than this difference in order to be evaluated, otherwise they pass.

        * Return : Boolean
                   True indicates no error occurred
        """

        # Check incoming parameters
        if not lcmd_commands or not len( lcmd_commands ) or not str_output_dir:
            return False
        
        # Keeps track of success.
        f_success = True
        
        # Manages compression in this run
        cur_compression = Compression.Compression() if str_compression_mode else None

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

            # Make all the directories needed for the commands
            self.func_make_all_needed_dirs( [ rsc_product.str_id for rsc_product in cmd_command.lstr_products ] )

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
        # lstr_made_dependencies_to_compress tracks products that are mode which have yet to be compressed.
        # Should be a set
        sstr_made_dependencies_to_compress = set()
        for cmd_command in lcmd_commands:

            # Log the start
            self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Starting", str( cmd_command.str_id ) ] ) )
            # Do not execute if the products are already made.
            # We do want to clean up if they ask for it.
            # We do want to compress if they ask for it.
            if ( self.func_paths_are_from_valid_run( cmd_command, f_dependencies = False, i_fuzzy_time = i_time_stamp_wiggle ) ):
                self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Skipping command, resulting file already exist from previous valid command. Current command:", cmd_command.str_id ] ) )

                # Complete the command in case it was not
                dt_dependencies.func_complete_command( cmd_command, f_wait = False, f_test = not self.f_execute )
                
                # Add cleaning dependencies
                if f_clean:
                    self.func_remove_paths( cmd_command = cmd_command, str_output_directory = str_output_dir, 
                                        dt_dependency_tree = dt_dependencies, f_remove_products = False, f_test = not self.f_execute )
                    
                # Compress if requested, cleaning is going to remove some files so it is easiest to let that happen,
                # Then if the file still exists go ahead and compress if needed.
                # I am at this point trusting all products were made ( because func_complete_command does this )
                # and that things missing were cleaned.
                if str_compression_mode and str_compression_mode.lower() == STR_COMPRESSION_AS_YOU_GO.lower():
                    # Record products made, they may have been cleaned so check that they exist
                    for str_product in cmd_command.lstr_products:
                        if os.path.exists( str_product ):
                            sstr_made_dependencies_to_compress.add( str_product )
                    # Optionally compress paths if the system is done with the path
                    sstr_removed = set()
                    for str_product_compress in sstr_made_dependencies_to_compress:
                        if not dt_dependencies.func_dependency_is_needed( str_product_compress ):
                            self.logr_logger.info( "Pipeline.func_run_commands: Compressing " + str_product_compress )
                            str_compression_success = cur_compression.func_compress( str_file_path=str_product_compress,
                                                           str_output_directory = str_output_dir,
                                                           str_compression_type=str_compression_type,
                                                           str_compression_mode=STR_COMPRESSION_ARCHIVE.lower(),
                                                           f_test = not self.f_execute )
                            sstr_removed.add( str_product_compress )
                            f_success = not str_compression_success is None
                    sstr_made_dependencies_to_compress = sstr_made_dependencies_to_compress - sstr_removed
                continue
            
            # Attempt a command.
            # Start the timing
            d_start = time.time()
 
            # Handle changing directories and other special commands
            if self.func_is_special_command( cmd_command ):
                f_success = self.func_do_special_command( cmd_command, f_test = not self.f_execute )
            else:
                # Add bsub prefix if needed to the command.
                str_executed_command = "".join( [ self.str_prefix_command, cmd_command.str_id ] )
                self.logr_logger.info( "".join( [ "Pipeline.func_run_commands: start command line: ", str_executed_command ] ) )
                f_success = f_success and self.cmdl_execute.func_CMD( str_executed_command, f_use_bash = self.f_use_bash, f_test = not self.f_execute )
                self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: end commandline." ] ) )
                # If the command is successful, indicate it is complete and potentially clean up stale dependencies
                if f_success:
                    f_success = f_success and dt_dependencies.func_complete_command( cmd_command, f_test = not self.f_execute )
                    self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Updated dependencies.", str( f_success ) ] ) )
                # Update the products so the pipeline knows they are from valid command calls
                # Make sure that the products are indicated to be complete
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

                if f_success and str_compression_mode and str_compression_mode.lower() == STR_COMPRESSION_AS_YOU_GO.lower():
                    # Compress if requested, cleaning is going to remove some files so it is easiest to let that happen,
                    # Then if the file still exists go ahead and compress if needed.
                    # I am at this point trusting all products were made ( because func_complete_command does this )
                    # and that things missing were cleaned.
                    # Record products made, they may have been cleaned so check that they exist
                    for str_product in cmd_command.lstr_products:
                        if os.path.exists( str_product.str_id ):
                            sstr_made_dependencies_to_compress.add( str_product )
                    sstr_removed = set()
                    for str_product_compress in sstr_made_dependencies_to_compress:
                        if not dt_dependencies.func_dependency_is_needed( str_product_compress ):
                            str_compression_success = cur_compression.func_compress( str_file_path = str_product_compress.str_id,
                                                                                     str_output_directory = str_output_dir,
                                                                                     str_compression_type = str_compression_type,
                                                                                     str_compression_mode = STR_COMPRESSION_ARCHIVE.lower(),
                                                                                     f_test = not self.f_execute )
                            sstr_removed.add( str_product_compress )
                            f_success = f_success and ( not str_compression_success is None )
                    sstr_made_dependencies_to_compress = sstr_made_dependencies_to_compress - sstr_removed
            if self.f_execute:
                self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Time::", str( round( time.time() - d_start ) ) ] ) )
            
            # Indicate failure
            if ( not f_success ) and self.f_execute:
                self.logr_logger.error( "Pipeline.func_run_commands: The last command was not successful. Pipeline run failed." )
       
        # Log successful completion
        if f_success:
            self.logr_logger.info( " ".join( [ "Pipeline.func_run_commands: Successfully ended pipeline", self.str_name ] ) )
            if f_clean:
                self.logr_logger.info( "\n".join( [ "Pipeline.func_run_commands: This pipeline had cleaning turned on.",
                                       "The following products were terminal and should exist:",
                                       ",".join( [ rsc_prod.str_id for rsc_prod in dt_dependencies.lstr_terminal_products ] ),
                                       "The following input dependencies should still exist:",
                                       ", ".join( [ rsc_input.str_id for rsc_input in dt_dependencies.lstr_inputs ] ),
                                       "If a file was requested to exist with clean settings, it should also exist." ] ) )
            else:
                self.logr_logger.info("Pipeline.func_run_commands: Cleaning was not turned on. All files should be available.")
        else:
            self.logr_logger.error( "Pipeline.func_run_commands: The pipeline but was unsuccessful. Pipeline run failed." )
            if self.f_execute:
                return f_success
                

        # Compress output directory
        # Archive
        if f_success:
            str_target_output_directory = str_output_dir
            if str_compression_mode and ( str_compression_mode.lower() in [ STR_COMPRESSION_ARCHIVE.lower(), STR_COMPRESSION_FIRST_LEVEL_ONLY.lower() ] ):
                str_target_output_directory = cur_compression.func_compress( str_file_path=str_output_dir,
                                                                             str_output_directory = str_output_dir,
                                                                             str_compression_type = str_compression_type, 
                                                                             str_compression_mode = str_compression_mode.lower(),
                                                                             f_test = not self.f_execute )
            # Move or copy output directory if indicated
            if str_target_output_directory:
                if lstr_copy:
                    if not self.f_archive:
                        self.logr_logger.error("Pipeline.func_run_commands: Could not copy the output, archiving turned off.")
                        f_success = False
                    else:
                        f_success = f_success and self.func_copy_move( lstr_destination=lstr_copy,
                                                           str_archive=str_target_output_directory,
                                                           f_copy=True, f_test = not self.f_execute )
                if str_move:
                    if not self.f_archive:
                        self.logr_logger.error("Pipeline.func_run_commands: Could not move the output, archiving turned off.")
                        f_success = False
                    else:
                        f_success = f_success and self.func_copy_move( lstr_destination=[ str_move ],
                                                           str_archive=str_target_output_directory,
                                                           f_copy=False, f_test = not self.f_execute )

        # Return success
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
                if str_cmd in cmd_cur.str_id:
                    cmd_cur.str_id = cmd_cur.str_id.replace( str_cmd, os.path.join( str_path, str_cmd ) )
                    

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

        # Make the ok file and place a time stamp in the ok file of when the file is made 
        if self.f_execute:
            for rsc_product in cmd_command.lstr_products:
                str_product = rsc_product.str_id
                with open( self.func_get_ok_file_path( str_product ), "a" ) as file_product:
                    file_product.write( str( os.path.getmtime( str_product ) ) + "\n" )
                    file_product.write( time.ctime( os.path.getmtime( str_product ) ) + "\n" )
        return True


    # Tested
    def func_test_mode( self ):
        """
        Switches pipeline into test mode.
        """
        self.f_execute = False
