#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import argparse
import Arguments
import ConfigManager
import Commandline
import csv
import Dispatcher
import JSONManager
import logging
import os
import Pipeline
import multiprocessing
import stat
import sys


# Constants
C_STR_CONFIG_EXTENSION = ".config"
C_STR_JOB_DIR = "jobs"
C_STR_JOB_LOGGER_NAME = "JobRunner.log"
C_STR_JOB_SYSTEM_DEST = "str_job_system"
C_STR_LOG_DIR = "logs"
C_STR_SCRIPT_LOG = "str_log_file"

# Keys for alignment return (dicts)
INDEX_CMD = "cmd"
INDEX_FILE = "out_file"
INDEX_FOLDER = "align_folder"

class PipelineRunner:

    def __init__(self):

        self.ns_arguments = None
        self.dict_args_info = None
        self.str_orig_output_dir = None
        self.f_is_multi_job = False
        self.prog = "custom"

        # Retrieve and manage arguments
        self.func_manage_arguments()
        self.func_manage_output_dir()

        # Keeps tack of errors
        f_error_occured = False

        # Job dispatcher.
        self.dspr_cur = Dispatcher.func_make_job_runner(self.ns_arguments.str_job_system)

        # Get logging
        self.logr_job = self.func_make_job_logger()

        # Set in func_parse_jobs()
        self.str_possible_config_file = None
        self.llstr_sample_data = self.func_parse_jobs()

        # Check version
        self.version = None

        # If a resource config file is given,
        # the pipeline config file must be given
        if (self.ns_arguments.str_resource_config and
            not self.str_possible_config_file):
            self.logr_job.error("".join(["A pipeline config file must be used ",
                                         "to map resources from the Resource ",
                                         "Config file to the command. Please ",
                                         "use a pipeline config file."]))
            exit(996)

    # TODO Test
    def func_tag_file(self, str_file, str_tag):
        """
        Adds a tag to a file name (at the end of the basename
        before the extension).
        Convenience function for pipeline building.

        * str_file: File path to modify.
                  : String
        * str_tag: Tag tring to add to the file name.
                 : String
        * return: Updated path with tag added before extension.
                : String (file path)
        """

        if not str_file or not str_tag:
            return str_file
        str_base, str_ext = os.path.splitext(str_file)
        return str_base + "_" + str_tag + str_ext

    # TODO Test
    def func_base_file(self, str_file):
        """
        Get the file base of the file path.
        (No directory information, no extension.)
        Convenience function for pipeline building.

        * str_file: File path to modify.
                  : String
        * return: File name without extension.
                : String (file path)
        """

        return os.path.splitext(os.path.basename(str_file))[0]

    # TODO Test
    def func_update_file_location(self, str_file, str_new_dir):
        """
        Adds a tag to a file name
        (at the end of the basename before the extension).
        Convenience function for pipeline building.

        * str_file: File path to modify.
                  : String
        * str_new_dir: New directory path to update file path
                       (placing the file in the given directory).
                     : String
        * return: File path of file in new directory.
                : String (file path)
        """

        return os.path.join(str_new_dir, os.path.basename(str_file))

    # TODO Test
    def func_switch_ext(self, str_file, str_ext):
        """
        Changes the extension of a file to another extension.
        Convenience function for pipeline building.

        * str_file : File path to modify.
                   : String
        * str_ext : Extension to use in place of the current extension.
                  : String
        * return : Updated path for the file using a new extension.
                 : String (file path)
        """
        if(not str_file) or (not str_ext):
            return str_file
        if not (str_ext[0] in ["_", "."]):
            str_ext = "." + str_ext
        return os.path.splitext(str_file)[0] + str_ext

    # TODO Test
    def func_create_arguments(self, prsr_arguments, f_suppress=True):
        """
        Creates arguements for pipeline and adds to current argparser.
        * prsr_arguments : Parser to update.
        * return : Standard set of arguments
               : Argument Parser
        """
        # Built-in functionality
        str_builtin_name = "Builtins " + Arguments.C_STR_SCIEDPIPER_ARG_GROUP
        str_builtin_desc = "".join(["Functionality builtin with the job ",
                                    "runner engine",
                                    Arguments.C_STR_SCIEDPIPER_ARG_GROUP])
        grp_builtin = prsr_arguments.add_argument_group(str_builtin_name,
                                                        str_builtin_desc)

        grp_builtin.add_argument("--mem_benchmark",
                                 default=None,
                                 dest="i_mem_benchmark",
                                 type=int,
                                 help="".join(["The amount of seconds wait",
                                               " between polling commands ",
                                               "when benchmarking memory. ",
                                               "By default turned off. "]))

        grp_builtin.add_argument("--clean",
                                 dest="f_clean",
                                 default=False,
                                 action="store_true",
                                 help="".join(["Turns on (true) or off (false)",
                                               " cleaning of intermediary ",
                                               "product files."]))
        grp_builtin.add_argument("--copy",
                                 metavar="Copy_location",
                                 dest="lstr_copy",
                                 default=None,
                                 action="append",
                                 help="".join(["Paths to copy the output ",
                                               "directory after the pipeline ",
                                               "is completed. Output directory",
                                               " must be specified; can be ",
                                               "used more than once for ",
                                               "multiple copy locations."]))
        grp_builtin.add_argument("--dot_file",
                                 metavar="Dot_file",
                                 dest="str_dot_path",
                                 default=None,
                                 help="".join(["When provided a dot file ",
                                               "of the underlying graph ",
                                               "will be written to this ",
                                               "file."]))
        grp_builtin.add_argument("--log",
                                 metavar="Optional_logging_file",
                                 dest=C_STR_SCRIPT_LOG,
                                 default=None,
                                 help="".join(["Optional log file, if not ",
                                               "given logging will be to the ",
                                               "standard out."]))
        grp_builtin.add_argument("--json_out",
                                 metavar="JSON_out",
                                 dest="str_json_file_out",
                                 default=None,
                                 help="".join(["Write script to a JSON file. ",
                                               "(Does not execute pipeline.)"]))
        grp_builtin.add_argument("--move",
                                 metavar="Move_location",
                                 dest="str_move_dir",
                                 default=None,
                                 help="".join(["The path where to move the ",
                                               "output directory after the ",
                                               "pipeline ends. Can be used ",
                                               "with the copy argument if ",
                                               "both copying to one ",
                                               "location(s) and moving to ",
                                               "another is needed. Must ",
                                               "specify output directory."]))
        grp_builtin.add_argument("--out_dir",
                                 metavar="Output_directory",
                                 dest=Arguments.C_STR_OUTPUT_DIR,
                                 default="",
                                 help="".join(["The output directory where ",
                                               "results will be placed. If ",
                                               "not given a directory will ",
                                               "be created from sample names ",
                                               "and placed with the samples."]))
        grp_builtin.add_argument("--test",
                                 dest="f_Test",
                                 default=False,
                                 action="store_true",
                                 help="".join(["Will check the environment ",
                                               "and display commands line but",
                                               " not run."]))
        grp_builtin.add_argument("--graph_ordered_commands",
                                 dest="f_graph_organize",
                                 action="store_true",
                                 default=False,
                                 help="".join(["Commands are ordered for ",
                                               "execution by dependency and ",
                                               "product relationship by ",
                                               "default. When including this ",
                                               "flag, commands will be ran in",
                                               " the order provided in the ",
                                               "script (in the list of ",
                                               "commands)."]))
        grp_builtin.add_argument("--timestamp",
                                 dest="i_time_stamp_diff",
                                 default=-1,
                                 type=float,
                                 help="".join(["Using this will turn on ",
                                               "timestamp and will require the",
                                               " parent to be atleast this ",
                                               "amount or more younger than a",
                                               " product in order to ",
                                               "invalidate the product. A ",
                                               "negative value will be ",
                                               "ignored."]))
        grp_builtin.add_argument("--update_command",
                                 dest="str_update_classpath",
                                 default=None,
                                 help="".join(["Allows a class path to be ",
                                               "added to the jars. eg. ",
                                               "'command.jar:",os.sep,
                                               "APPEND",os.sep,
                                               "THIS",os.sep,
                                               "PATH",os.sep,"To",os.sep,
                                               "JAR,java.jar:",os.sep,
                                               "Append",os.sep,"Path'"]))
        grp_builtin.add_argument("--compress",
                                 dest="str_compress",
                                 default="none",
                                 choices=Pipeline.LSTR_COMPRESSION_HANDLING_CHOICES,
                                 help="".join(["Turns on compression of ",
                                               "products and intermediary ",
                                               "files made by the pipeline. ",
                                               "Valid choices include: ",
                                               str(Pipeline.LSTR_COMPRESSION_HANDLING_CHOICES)]))
        grp_builtin.add_argument("--wait",
                                 dest="lstr_wait",
                                 default="5,15,40",
                                 help="".join(["The number of seconds and ",
                                               "times the pipeline will wait ",
                                               "to check for products after ",
                                               "each pipeline command ends. ",
                                               "This compensates for IO lag. ",
                                               "Should be just integers in ",
                                               "seconds delimited by commas. ",
                                               "3,10,20 would indicate wait ",
                                               "three seconds, then try again",
                                               " after 10 seconds, and lastly",
                                               " wait for 20 seconds."]))

        # Job submission associated
        str_jobs_name = "".join(["Job Submission ",
                                 Arguments.C_STR_SCIEDPIPER_ARG_GROUP])
        str_jobs_desc = "".join(["Pipeline parameters specifically for ",
                                 "job submission ",
                                 Arguments.C_STR_SCIEDPIPER_ARG_GROUP])
        grp_jobs = prsr_arguments.add_argument_group(str_jobs_name,
                                                     str_jobs_desc)
        grp_jobs.add_argument(Arguments.C_STR_SAMPLE_FILE_ARG,
                              dest=Arguments.C_STR_SAMPLE_FILE_DEST,
                              default=None,
                              help="".join(["Sample file for multiple job ",
                                            "submission. Tied to the pipeline ",
                                            "with the pipeline config file. ",
                                            "Must be tab delimited."]))
        grp_jobs.add_argument("--concurrent_jobs",
                              metavar="Concurrent_Jobs",
                              dest="i_number_jobs",
                              type=int,
                              default=1,
                              help="".join(["The maximum number of jobs to ",
                                            "run concurrently."]))
        grp_jobs.add_argument("--job_system",
                              metavar="Queueing_System",
                              dest=C_STR_JOB_SYSTEM_DEST,
                              default=Dispatcher.C_STR_LOCAL,
                              help="".join(["Which system to run the jobs on: ",
                                            ", ".join(Dispatcher.C_LSTR_DISPATCH_CHOICES)]))
        grp_jobs.add_argument("--job_memory",
                              metavar="Memory_for_job",
                              dest="i_job_memory",
                              default=8,
                              type=int,
                              help="Maximum memory requested.")
        grp_jobs.add_argument("--job_queue",
                              metavar="Queue_for_job",
                              dest="str_job_queue",
                              default=None,
                              help="Job queue.")
        grp_jobs.add_argument("--job_misc",
                              metavar="Misc_job_arguments",
                              dest="str_job_misc",
                              default="",
                              help="".join(["Misc arguments not covered ",
                                            "to be added to the command."]))

        # Config associated
        str_config_name = "".join(["Pipeline Config ",
                                   Arguments.C_STR_SCIEDPIPER_ARG_GROUP])
        str_config_desc = "".join(["Pipeline config files change the running ",
                                   "of pipelines. Useful when managing ",
                                   "environments.",
                                   Arguments.C_STR_SCIEDPIPER_ARG_GROUP])
        grp_config = prsr_arguments.add_argument_group(str_config_name,
                                                       str_config_desc)
        grp_config.add_argument(Arguments.C_STR_NO_PIPELINE_CONFIG_ARG,
                                dest="f_use_pipeline_config",
                                default=True,
                                action="store_false",
                                help="".join(["Use this flag to ignore the ",
                                              "pipeline config file."]))
        grp_config.add_argument(Arguments.C_STR_PIPELINE_CONFIG_FILE_ARG,
                                dest="str_pipeline_config_file",
                                default=None,
                                help="".join(["The pipeline config file to ",
                                              "use, if not given and using ",
                                              "the pipeline config files is ",
                                              "turned on then the program will",
                                              " look in the directory where ",
                                              "the script is located."]))
        grp_config.add_argument("--resources",
                                dest="str_resource_config",
                                default=None,
                                help="".join(["Resource config file must be ",
                                              "used in conjunction with a ",
                                              "pipeline config file."]))

        # Experimental functionality
        #str_exp_name = "Builtins " + .ArgumentsC_STR_SCIEDPIPER_ARG_GROUP
        #str_exp_desc = "".join(["Functionality in process, or not completely ",
        #                        "genericized. ",
        #                        Arguments.C_STR_SCIEDPIPER_ARG_GROUP])
        #grp_experimental = prsr_arguments.add_argument_group(str_exp_name,
        #                                                     str_exp_desc)
        # To add back, reomve default in manage arguments section.
        #grp_experimental.add_argument("--wdl",
        #                              dest="str_wdl",
        #                              default=None,
        #                              help="".join(["When used, the pipeline ",
        #                                            "will not run but instead ",
        #                                            "a wdl file will be ",
        #                                            "generated for the ",
        #                                            "workflow, then this ",
        #                                            "argument is used, please ",
        #                                            "pass the file path to ",
        #                                            "which the wdl file should",
        #                                            " be written."]))

        return prsr_arguments

    def func_update_arguments(self, args_raw):
        """
        This will be overridden by the child of the parent script if there
        is a need to add to the arguments or to change the name of the parser.

        * args_raw : Standardized arguments to add to / modify.
                   : Arguments object
        * return : Updated arguments.
                 : Arguments object
        """

        pass

    # TODO Test
    def func_make_job_logger(self):
        """
        Make logger for job runner.

        * return: Logger for the job runner
                : Logger
        """

        # Make logger for all jobs
        logr_job = logging.getLogger(C_STR_JOB_LOGGER_NAME)
        hdlr_job = logging.FileHandler(filename=os.path.join(self.ns_arguments.str_out_dir,
                                                             C_STR_JOB_LOGGER_NAME),
                                                             mode="w")
        hdlr_job.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logr_job.addHandler(hdlr_job)
        logr_job.setLevel(logging.INFO)
        return(logr_job)

    # TODO Test
    def func_manage_arguments(self):
        """
        Parses arguments, stores some information in the instance,
        checks specific arguments for values.
        """

        ## Manage the arguments
        # Start with the parent arguments
        # Allow children script arguments to be added
        # Update arguments with config file for environemntal options
        ##
        # Allow child object to update arguments
        prsr_arguments = argparse.ArgumentParser(
            prog="custom.py",
            description="Custom Script",
            conflict_handler="resolve",
            formatter_class=Arguments.PipelineDefaultHelpFormatter)
        #prsr_arguments.add_argument("--sciedpiper",
        #                            dest="f_see_sciedpiper",
        #                            action="store_true",
        #                            default=False,
        #                            help="".join(["Use to view all SciEDPipeR options"]))
        prsr_return = self.func_update_arguments(prsr_arguments)
        prsr_arguments = self.func_create_arguments(prsr_return)

        # Store information about the arguments needed for later functionality
        self.dict_args_info = Arguments.Arguments.func_extract_argument_info(prsr_arguments)

        # Set program name
        self.prog = prsr_arguments.prog

        # Parse arguments from command line
        self.ns_arguments = prsr_arguments.parse_args()

        # Need to make sure if a string value is written as None
        # that it is not recorded as 'None'
        # Need to check lists too because of nargs.
        for str_item, x_value in vars(self.ns_arguments).items():
            if x_value == "None":
                setattr(self.ns_arguments, str_item, None)
            if isinstance(x_value, type([])):
                x_value = [None if x_item == "None" else x_item for x_item in x_value]
                x_value = [x_item for x_item in x_value if x_item]
                setattr(self.ns_arguments, str_item, x_value)

        # Min value for threads is 1
        self.ns_arguments.i_number_jobs = max(self.ns_arguments.i_number_jobs, 1)

        # Original output file
        self.str_orig_output_dir = self.ns_arguments.str_out_dir

    # TODO Test
    def func_manage_output_dir(self):
        """
        Store the output directory location to the instance and then
        make the directory. if it has not been made.
        """

        # Make sure the output directory is set
        self.func_set_output_dir()

        PipelineRunner.func_make_output_dir(self.ns_arguments)

    # TODO Test
    def func_parse_jobs(self):
        """
        Parse sample info from the sample file (Sample.txt).
        Manages associated parameters like tuning on multiprocessing,
        selecting the number of threads, making a pipeline.config file
        required for job running, and other associated business logic.
        """

        # Parse job info, if no sample file is given then return [None].
        # Does not do this immediately beause there are other variables
        # to manage depending in the number of samples or existence of a sample
        # sheet.
        llstr_sample_data = [None]
        if self.ns_arguments.str_sample_file:
            with open(self.ns_arguments.str_sample_file, "r") as hndl_samples:
                llstr_sample_data = [lstr_row for lstr_row in csv.reader(hndl_samples, delimiter = b"\t")]

        # Turn on Job running
        if len(llstr_sample_data) > 1 and self.ns_arguments.i_number_jobs > 1:
            self.f_is_multi_job = True
        else:
            self.f_is_multi_job = False

        # No more job threads than number of jobs requested
        self.ns_arguments.i_number_jobs = min(self.ns_arguments.i_number_jobs,
                                              len(llstr_sample_data))

        # To run multiple samples, a pipeline config is required
        if self.ns_arguments.str_pipeline_config_file:
            self.str_possible_config_file = os.path.realpath(self.ns_arguments.str_pipeline_config_file)
        else:
            self.str_possible_config_file = os.path.splitext(os.path.realpath(sys.argv[0]))[0] + C_STR_CONFIG_EXTENSION
        if self.ns_arguments.str_sample_file and (not os.path.exists(self.str_possible_config_file)):
            self.logr_job.error("All jobs with sample files need pipeline config files.")
            exit(997)

        return(llstr_sample_data)

    # TODO Test
    def func_run_pipeline(self):
        """
        Runs housekeeping code before the pipeline is ran.
        This is the function that is called by children objects to run.
        """
        if self.f_is_multi_job:
            self.func_run_many_jobs()
        else:
            self.func_run_jobs_locally()

    # TODO Test
    def func_run_jobs_locally(self):
        # Run for each sample line (passing None once if no sample was given)
        if not self.llstr_sample_data:
            self.logr_job.error("".join(["PipelineRunner.func_run_jobs_locally::",
                                         " No job found."]))
            exit(998)

        f_error_occured = False
        for lstr_sample_data in self.llstr_sample_data:
            str_current_job = "= " + lstr_sample_data[0] if lstr_sample_data else ""
            self.logr_job.info("".join(["PipelineRunner.func_run_jobs_locally::",
                                        " Start Running job ",
                                        str_current_job]))
            # Run a sample
#            try:
            f_return = self.func_run_sample(lstr_sample_data)
            if f_return:
                self.logr_job.info("".join(["PipelineRunner.func_run_jobs",
                                            "_locally:: Ran WITHOUT error,",
                                            " job",
                                            str_current_job]))
            else:
                self.logr_job.info("".join(["PipelineRunner.func_run_jobs_",
                                            "locally:: An ERROR occured ",
                                            "while running job",
                                            str_current_job]))
            self.logr_job.info("".join(["PipelineRunner.func_run_jobs_",
                                        "locally:: End Running job",
                                        str_current_job]))

            f_error_occured = f_error_occured or (not f_return)
#            except Exception as e:
#                f_error_occured = True
#                self.logr_job.info("".join(["PipelineRunner.func_run_jobs_",
#                                            "locally:: Serious error occured ",
#                                            "for job", str_current_job]))
#                self.logr_job.info("".join(["PipelineRunner.func_run_jobs_",
#                                            "locally:: Exception for job",
#                                            str_current_job,
#                                            "\n" + str(e)]))

        if f_error_occured:
            exit(999)
        else:
            exit(0)

    def func_make_commands(self,  args_parsed, cur_pipeline):
        """
        Allows:
        - the creation of commands in the child object.
        - the creation of directories.
        - checking that files exist.

        The commands will then be ran after this method.
        The pipeline object is given here so that one can update
        the pipeline if needed. Please do not run the pipeline here.
        Please do not add the commands to the pipeline.
        * args_parsed: Current arguments from command line already parsed
                     : Parsed Arguments
        * cur_pipeline: Pipeline to run the commands in case
                        configuring is needed.
                      : Pipeline
        * return: List of command objects
        """

        return []

    # TODO Test
    def func_make_script(self,
                         str_additional_env_path,
                         str_additional_python_path,
                         str_updated_script_path,
                         str_precommands,
                         str_postcommands,
                         str_sample_name):

        str_full_script_name = os.path.join(self.ns_arguments.str_out_dir,
                                            os.path.basename(str_updated_script_path))
        str_full_script_name = os.path.splitext(str_full_script_name)[0]+".sh"
        return(self.dspr_cur.func_make_run_script(str_full_script_name,
                                                  os.path.abspath(str_updated_script_path),
                                                  self.ns_arguments,
                                                  self.dict_args_info,
                                                  str_additional_env_path,
                                                  str_additional_python_path,
                                                  str_precommands,
                                                  str_postcommands,
                                                  str_sample_name))

    # TODO Test
    def func_set_output_dir(self):
        """
        If the output directory is given, set the output directory as the
        absolute path of the given output directory path. Otherwise set to
        the current working directory.
        """

        ## Output dir related
        if(not hasattr(self.ns_arguments, Arguments.C_STR_OUTPUT_DIR) or
           not self.ns_arguments.str_out_dir):
            self.ns_arguments.str_out_dir = os.getcwd()
        self.ns_arguments.str_out_dir = os.path.abspath(self.ns_arguments.str_out_dir)

    # TODO Test
    @classmethod
    def func_make_output_dir(self, ns_arguments):
        """
        If the output directory is in the arguments and if it does not exits,
        create output directory.

        * ns_arguments: Arguments to search for output directory argument
                      : Name Space
        * returns: The output directory or None if no directory was made.
                 : File path (String)
        """
        # If an output / project folder is indicated.
        if hasattr(ns_arguments, Arguments.C_STR_OUTPUT_DIR):
            # Make the output directory if it does not exist
            if(ns_arguments.str_out_dir and
               not os.path.isdir(ns_arguments.str_out_dir)):
                os.mkdir(ns_arguments.str_out_dir)
            return ns_arguments.str_out_dir
        return None

    # TODO Test
    def func_update_command(self, lstr_sample_info):
        """
        Takes the sample info (which may have sample names as well as sample
        metadata) and check the potential config file. Certain updates will
        require a bash script to be made, for most updates we try to do this
        way so a record of the command is kept.
        """
        str_script_to_run = None
        # Read in the config file and check to see if there are updates
        self.ns_arguments.str_out_dir = self.str_orig_output_dir
        str_additional_env_path = None
        str_additional_python_path = None
        str_updated_script_path = None
        str_precommands = None
        str_postcommands = None
        if os.path.exists(self.str_possible_config_file) and self.ns_arguments.f_use_pipeline_config:
            cur_config_manager = ConfigManager.ConfigManager(self.str_possible_config_file)
            self.ns_arguments = cur_config_manager.func_update_arguments(args_parsed=self.ns_arguments,
                                                                         dict_args_info=self.dict_args_info,
                                                                         lstr_sample_arguments = lstr_sample_info,
                                                                         lstr_locked_arguments = Arguments.C_LSTR_LOCKED_ARGS)
            str_additional_env_path = cur_config_manager.func_update_env_path()
            str_additional_python_path = cur_config_manager.func_update_python_path()
            str_updated_script_path = cur_config_manager.func_update_script_path(sys.argv[0])
            str_precommands = cur_config_manager.func_get_precommands()
            str_postcommands = cur_config_manager.func_get_postcommands()
        # Make a bash script
        ## Make output directory
        PipelineRunner.func_make_output_dir(self.ns_arguments)
        ## Make the script in the output directory
        str_script_to_run = None
        if(str_additional_env_path or
           str_additional_python_path or
           str_updated_script_path or
           str_precommands or
           str_postcommands):
            str_script_to_run = self.func_make_script(str_additional_env_path = str_additional_env_path,
                                                      str_additional_python_path = str_additional_python_path,
                                                      str_updated_script_path = str_updated_script_path,
                                                      str_precommands = str_precommands,
                                                      str_postcommands = str_postcommands,
                                                      str_sample_name = lstr_sample_info[0] if lstr_sample_info else self.func_base_file(self.prog))
        # Return script to run.
        return(str_script_to_run)

    # TODO Test
    def func_get_job_commands(self):
        """
        Update the command per sample and return a list of commands to run.
        This triggers the creation of bash scripts to run the commands given
        the provided sample information.
        """

        lstr_cmds = []
        for lstr_sample_info in self.llstr_sample_data:
            str_cmd = self.func_update_command(lstr_sample_info)
            if str_cmd:
                lstr_cmds.append(self.dispr_cur(str_cmd))
        return lstr_cmds

    # TODO Test
    def func_run_sample(self, lstr_sample_info):
        # str_script is None indicates a bash script was not made and the raw
        # command can be run. This is a case of running a pipeline locally
        # without sample.txt files or config files that update aspects of the
        # pipeline that would require a script to encapsulate those changes,
        # for example a Path change.
        # Also a dispatch command outside of local dispatching will also
        # require a script to be ran,

        # Check to see if a script needs to be made and ran.
        # Happens on certain proccessing requirements
        # like updating environmental variables with pipeline
        # config files.
        str_script = self.func_update_command(lstr_sample_info)
        if str_script:
            return(Commandline.Commandline().func_CMD(str_script,
                                                      f_use_bash=True))
        elif str_script is None:
            # Holds the commands to run
            lcmd_commands = []

            ## Output dir related
            # If the output dir is not specified then move and copy functions are disabled
            f_archive = True
            if(not hasattr(self.ns_arguments, Arguments.C_STR_OUTPUT_DIR)
               or not self.ns_arguments.str_out_dir):
                f_archive = False

            ## Make output directory
            PipelineRunner.func_make_output_dir(self.ns_arguments)

            # Make pipeline object and indicate Log file
            pline_cur = Pipeline.Pipeline(str_name=self.prog,
                                          str_log_to_file=self.ns_arguments.str_log_file if hasattr(self.ns_arguments, "str_log_file") else os.path.join(self.ns_arguments.str_out_dir, "custom_log.txt"),
                                          str_update_source_path=self.ns_arguments.str_update_classpath if hasattr(self.ns_arguments, "str_update_classpath") else None)
            # Update the logger with the arguments
            if self.version:
                str_version_log = "".join(["PipelineRunner.func_run_sample:: ",
                                           "Pipeline version:",
                                           str(self.version), "\n",
                                           "PipelineRunner.func_run_sample:: ",
                                           "The call to the pipeline was: ",
                                           " ".join(["\n"] + sys.argv + ["\n"]),
                                           "PipelineRunner.func_run_sample:: ",
                                           "This run was started with the ",
                                           "following arg.\n"])
                str_args_log = "\n".join([str(str_namespace_key) + " = " + str(str_namespace_value)
                                          for str_namespace_key, str_namespace_value in vars(self.ns_arguments).items()] + ["\n"])
                pline_cur.logr_logger.info(str_version_log)
                pline_cur.logr_logger.info(str_args_log)
            # Put pipeline in test mode if needed.
            if hasattr(self.ns_arguments, "f_Test") and self.ns_arguments.f_Test:
                pline_cur.func_test_mode()
            # Turn off archiving if output directory was not given
            if hasattr(self.ns_arguments, "f_archive") and not f_archive:
                pline_cur.logr_logger.warning("PipelineRunner.func_run_sample:: Turning off archiving, please specify an output directory if you want this feature enabled.")
                pline_cur.f_archive = False
            # Run the user based pipeline
            # If the commands are not existent (parsed from JSON)
            # then build them from script
            # Where variables are being used.
            #if self.ns_arguments.str_wdl:
            #    # If WDL is being output, switch the values of the arguments
            #    # with the name of the argument allowing us to track them,
            #    import inspect
            #    import copy
            #    ns_wdl_arguments = copy.deepcopy(self.ns_arguments)
            #    lstr_members = [member[0] for member in inspect.getmembers(ns_wdl_arguments)
            #                     if not (member[0].startswith("_") or member[0].endswith("_") or inspect.isroutine(member))]
            #    for str_member in lstr_members:
            #        setattr(ns_wdl_arguments, str_member, "${"+str_member+"}".encode('utf-8'))
            #    lcmd_commands = self.func_make_commands(args_parsed = ns_wdl_arguments, cur_pipeline = pline_cur)
            #else:
            lcmd_commands = self.func_make_commands(args_parsed=self.ns_arguments,
                                                    cur_pipeline=pline_cur)

            # Write JSON file
            if hasattr(self.ns_arguments, "str_json_file_out") and self.ns_arguments.str_json_file_out:
                JSONManager.JSONManager.func_pipeline_to_json(lcmd_commands=lcmd_commands,
                                                              dict_args=vars(self.ns_arguments),
                                                              str_file=self.ns_arguments.str_json_file_out,
                                                              f_pretty=True)
                pline_cur.logr_logger.info("Writing JSON file to: " + self.ns_arguments.str_json_file_out)
                return(True)

            # Run commands
            if not hasattr(self.ns_arguments, "lstr_copy"):
                setattr(self.ns_arguments, "lstr_copy", None)
            if not hasattr(self.ns_arguments, "str_move_dir"):
                setattr(self.ns_arguments, "str_move_dir", None)
            if not hasattr(self.ns_arguments, "str_compress"):
                setattr(self.ns_arguments, "str_compress",  "none")
            if not hasattr(self.ns_arguments, "f_clean"):
                setattr(self.ns_arguments, "f_clean", False)
            if not hasattr(self.ns_arguments, "i_time_stamp_diff"):
                setattr(self.ns_arguments, "i_time_stamp_diff", None)
            return(pline_cur.func_run_commands(lcmd_commands=lcmd_commands,
                                               str_output_dir=self.ns_arguments.str_out_dir,
                                               f_clean=self.ns_arguments.f_clean,
                                               f_self_organize_commands=self.ns_arguments.f_graph_organize,
                                               li_wait=[int(str_wait) for str_wait in self.ns_arguments.lstr_wait.split(",")],
                                               lstr_copy=self.ns_arguments.lstr_copy if self.ns_arguments.lstr_copy else None,
                                               str_move=self.ns_arguments.str_move_dir if self.ns_arguments.str_move_dir else None,
                                               str_compression_mode=self.ns_arguments.str_compress,
                                               i_time_stamp_wiggle=self.ns_arguments.i_time_stamp_diff,
                                               #str_wdl=self.ns_arguments.str_wdl,
                                               str_dot_file=self.ns_arguments.str_dot_path,
                                               i_benchmark_secs=self.ns_arguments.i_mem_benchmark,
                                               args_original=None ))
                                               #args_original = (self.ns_arguments if self.ns_arguments.str_wdl else None)))

    # TODO Test
    def func_run_many_jobs(self):
        """
        Run jobs in a multiprocessing pool. Each process is one job.
        """

        try:
            pool = multiprocessing.Pool()
            lrslt_success = pool.map_async(func_run_job,
                                           self.func_get_job_commands())
            lf_success = [f_success for f_success in lrslt_success.get()]
        except Exception as e:
            f_error_occured = True
            self.logr_job.info("".join(["PipelineRunner.func_run_many_jobs:: ",
                                        "Serious error occured for job"]))
            self.logr_job.info("PipelineRunner.func_run_many_jobs:: \n" + str(e))


# TODO Test
# Do no move from top level of module.
# Needs to be here do to pickling and multiprocessing and the pain of it all.
def func_run_job(str_job):
    """
    Run the command for the job on the commandline.
    """

    return(Commandline.Commandline().func_CMD(str_job,
                                              f_use_bash=True))
