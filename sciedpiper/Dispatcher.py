__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2016"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Arguments
import os
import ParentScript

# Methods for dispatching jobs
C_STR_LOCAL = "local"
C_STR_BSUB = "bsub"
C_STR_QSUB = "qsub"
C_STR_LSF = "lsf"
C_STR_SGE = "sge"
C_LSTR_BSUB_CHOICES = [ C_STR_BSUB, C_STR_LSF ]
C_LSTR_QSUB_CHOICES = [ C_STR_QSUB, C_STR_SGE ]
C_LSTR_LOCAL_CHOICES = [ C_STR_LOCAL ]
C_LSTR_DISPATCH_CHOICES = C_LSTR_LOCAL_CHOICES + C_LSTR_QSUB_CHOICES


class Runner:
    """
    Parent Class for Job Dispatch Runners.
    To make a new Job Dispatch Runner over write the below functions
    that just pass.
    """

    def __init__( self ):

        self.str_error = ""
        self.str_error_file = None
        self.str_log_file = None


    # TODO Test
    def func_build_arguments( self, args_name_space, dict_args_info ):

        lstr_script = []

        # Make dict to translate dest to flag
        dict_dest_to_flag = {}
        for str_info_key in dict_args_info:
            if not str_info_key == Arguments.C_STR_POSITIONAL_ARGUMENTS:
                dict_dest_to_flag[ dict_args_info[ str_info_key ][ Arguments.C_STR_VARIABLE_NAME ] ] = str_info_key

        for str_arg_dest, str_arg_value in vars( args_name_space ).items():
            if not str_arg_dest in dict_args_info[ Arguments.C_STR_POSITIONAL_ARGUMENTS ][ Arguments.C_STR_VARIABLE_NAME ] + [ ParentScript.C_STR_JOB_SYSTEM_DEST  ]:
                # If the value is boolean
                # Check the action if it is action_true or action_false
                # If it is then use the correct flag presence depending on the value and the action.
                cur_str_flag = dict_dest_to_flag[ str_arg_dest ]
                if ( isinstance( str_arg_value, bool )): 
                    # Handle special cases help
                    if cur_str_flag in [ "-h", "--help" ]:
                        if str_arg_value:
                            lstr_script.append( cut_str_flag )
                    elif not str_arg_value == dict_args_info[ cur_str_flag ][ Arguments.C_STR_DEFAULT ]:
                        lstr_script.append( cur_str_flag )
                else:
                    lstr_script.extend([ cur_str_flag, str( str_arg_value ) ])

        # Add flags and positional arguments
        # Add in no config pipeline otherwise the config file is read again and this
        # Both cases make code execute again making an inf loop.
        if not ParentScript.C_STR_NO_PIPELINE_CONFIG_ARG in lstr_script:
            lstr_script.append( ParentScript.C_STR_NO_PIPELINE_CONFIG_ARG )

        # Add positional arguments
        lstr_script.extend( dict_args_info[ Arguments.C_STR_POSITIONAL_ARGUMENTS ][ Arguments.C_STR_VARIABLE_NAME ] )

        return( lstr_script )


    def func_update_command( self, str_command, args_name_space ):
        """
        Update commands from the script name and supplied arguments to the
        command to directly call on the command line.

        Overwrite in child implementation.
        """

        pass


    def func_make_run_script( self, str_full_script_name,
                                    args_name_space,
                                    dict_args_info,
                                    str_additional_env_path,
                                    str_additional_python_path,
                                    str_precommands,
                                    str_postcommands,
                                    str_sample_name ):
        """
        Make a (bash) script that is called to run the pipeline.
        This can be used to set environmental variable, paths, etc

        Overwrite in child implementation.
        """

        pass


    def func_check_run( self ):
        """
        Checks the job log / err for an indicator of error.
        If an error, the contents of the error file are saved to the runner and a False is returned.
        If if no error, the contents of the error file is an empty string and a True is returned.

        Overwrite in child implementation.
        """

        pass


class QSUBRunner( Runner ):
    """
    Job dispatcher for qsub systems (here implemented for SGE).
    """

    # TODO Test
    def func_update_command( self, str_command, args_name_space ):
        """
        Update commands from the script name and supplied arguments to the
        command to directly call on the command line.

        * str_command :
                      :
        * args_name_space :
                          :
        * returns : Command or None on invalid string command
                  : String or None
        """

        if not str_command:
            return( None )
        return( " ".join( [ "qsub", str_command ] ) )


    # TODO Test
    def func_make_run_script( self, str_full_script_name,
                                    args_name_space,
                                    dict_args_info,
                                    str_additional_env_path,
                                    str_additional_python_path,
                                    str_precommands,
                                    str_postcommands,
                                    str_sample_name ):
        """
        Make a (bash) script that is called to run the pipeline.
        This can be used to set environmental variable, paths, etc

        * str_full_script_name :
                               :
        * args_name_space :
                          :
        * returns :
                  :
        """

        # Start script name with arguments
        lstr_script_call = [ str_full_script_name ]
        lstr_script_call.extend( self.func_build_arguments( args_name_space, dict_args_info ) )

        # Make output and error files
        self.str_log_file = os.path.join( args_name_space.str_file_base, 
                                          str_sample_name + "_job.log" )
        self.str_error_file = os.path.join( args_name_space.str_file_base,
                                            str_sample_name + "_job.err" )

        # Make / write script body
        lstr_script = [ "#!/usr/bin/env bash",
                        "",
                        "#$ -o " + self.str_log_file,
                        "#$ -e " + self.str_error_file,
                        args_name_space.str_job_misc,
                        "",
                        "PATH=$PATH:"+str_additional_env_path,
                        "PYTHONPATH=$PYTHONPATH:"+str_additional_python_path,
                        "",
                        str_precommands,
                        "",
                        " ".join( lstr_script_call ),
                        "",
                        str_postcommands ]

        # Write to file that is later called on command line
        with open( str_full_script_name, "w" ) as hndl_write_script:
            hndl_write_script.write( "\n".join( lstr_script ) ) 

        # Make file executable
        os.chmod( str_full_script_name, 0774 )

        # Return the script file name to call. 
        return str_full_script_name


    # TODO Complete and Test
    def func_check_run( self ):
        """
        Checks the job log / err for an indicator of error.
        If an error, the contents of the error file are saved to the runner and a False is returned.
        If if no error, the contents of the error file is an empty string and a True is returned.

        * returns : False on error, True on NO error.
                  : Boolean
        """
todo add to parentscript
        if self.str_log_file and self.str_error_file:
            with open( self.str_log_file, "r" ) as hndl_log:
                str_log = hndl_log.read()
                if "" in str_log:
                    return( True )
            with open( self.str_error_file, "r" ) as hndl_err:
                self.str_error = hndl_err.read()
        return( False )


# TODO Test
def func_make_job_runner( str_key ):
    """
    Given a keyword, return the correct job runner.

    * str_key : Keyword for the Runner of interest
              : String

    * returns : A child implementation of a Runner or None when the keyword is not recongized.
              : Runner or None
    """

    if not str_key or str_key.lower() not in [ str_choice.lower() for str_choice in C_LSTR_DISPATCH_CHOICES ]:
        return None
    if str_key in [ str_choice.lower() for str_choice in C_LSTR_QSUB_CHOICES ]:
        return QSUBRunner()
    return None
