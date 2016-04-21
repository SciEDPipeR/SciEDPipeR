
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Commandline
import os
import ParentPipelineTester
import ParentScript
import Pipeline
import time
import unittest

class FunctionalTester(ParentPipelineTester.ParentPipelineTester):
    """
    End-to_end tests for the App. Starting at command line.
    """

    str_script = os.path.join("sciedpiper","ExampleScript.py")
    str_script_config = os.path.join("sciedpiper","ExampleConfig.py")
    str_script_shuffled = os.path.join("sciedpiper","ExampleShuffledScript.py")
    str_script_timestamp = os.path.join("sciedpiper","ExampleTimeStamp.py")
    str_script_one_sample = os.path.join("sciedpiper","ExampleOneSample.py")
    str_sample_one_file = os.path.join("sciedpiper","ExampleOneSample.sample.txt")
    str_script_three_sample = os.path.join("sciedpiper","ExampleThreeSample.py")
    str_sample_three_file = os.path.join("sciedpiper","ExampleThreeSample.sample.txt")
    str_python = "/usr/bin/python2.7"
    str_log_file_name = "test.log"
 
    def func_clean_up_example_script(self, str_output_dir):
        """
        Cleans up the directories and files made by the example script.
        """
        
        dict_structure = self.func_get_example_script_dirs_files(str_output_dir)
        self.func_remove_files(dict_structure["files"])
        self.func_remove_dirs(dict_structure["directories"])
        
    def func_get_example_script_dirs_files(self, str_output_dir):
        """
        Gets the standard files and dirs make by the ExampleScript.py.
        They are returned in an order which can be used for file / dir deletion.
        """
        
        str_dir_1 = os.path.join(str_output_dir, "dir1")
        str_dir_2 = os.path.join(str_output_dir, "dir2")
        str_dir_3 = os.path.join(str_output_dir, "dir3")
        str_dir_4 = os.path.join(str_dir_1, "dir4")
        str_dir_5 = os.path.join(str_dir_1, "dir5")
        str_dir_6 = os.path.join(str_dir_2, "dir6")
        str_file_1 = os.path.join(str_dir_1, "file1.txt")
        str_file_2 = os.path.join(str_dir_4, "file2.txt")
        str_file_2_ok = os.path.join(str_dir_4, ".file2.txt.ok")
        str_file_3 = os.path.join(str_dir_4, "file3.txt")
        str_file_3_ok = os.path.join(str_dir_4, ".file3.txt.ok")
        str_file_4 = os.path.join(str_dir_6, "file4.txt")
        str_file_5 = os.path.join(str_dir_3, "file5.txt")
        str_file_6 = os.path.join(str_dir_3, "file6.txt")
        str_file_6_ok = os.path.join(str_dir_3, ".file6.txt.ok")
        str_file_7 = os.path.join(str_dir_3, "file7.txt")
        str_file_7_ok = os.path.join(str_dir_3, ".file7.txt.ok")

        str_job_log = os.path.join(str_output_dir,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        str_log = os.path.join(str_output_dir, self.str_log_file_name)
        
        return({"files": [str_file_1, str_file_2, str_file_3,
                          str_file_4, str_file_5, str_file_6, str_file_7,
                          str_file_2_ok, str_file_3_ok, str_file_6_ok,
                          str_file_7_ok, str_job_log, str_log],
                "directories": [str_dir_4, str_dir_5, str_dir_6,
                                str_dir_1, str_dir_2, str_dir_3]})

    ####
    ## Baseline test
    ###
    def nottest_app_for_vanilla_base_run(self):
        """
        Test the scenario where the example script is ran on all defaults.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_vanilla_base_run")
        self.func_make_dummy_dir(str_env)
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--example",
                                "test_app_for_vanilla_base_run",
                                "--log",
                                os.path.join(str_env, self.str_log_file_name),
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                         for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test self-organizing
    ####
    def nottest_app_for_shuffled_commands_run_success(self):
        """
        Test the scenario where the example script is written with commands
        out of order and allowed to reorder.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_shuffled_run_success")
        self.func_make_dummy_dir(str_env)
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_shuffled,
                                "--example",
                                "test_app_for_shuffled_cmds",
                                "--log",
                                os.path.join(str_env, self.str_log_file_name),
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path)
                        for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_shuffled_commands_run_fail(self):
        """
        Test the scenario where the example script is written with commands
        out of order and not allowed to reorder.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_shuffled_run_fail")
        self.func_make_dummy_dir(str_env)
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_shuffled,
                                "--example",
                                "test_app_for_shuffled_cmds",
                                "--user_ordered_commands",
                                "--log",
                                os.path.join(str_env, self.str_log_file_name),
                                "--out_dir",
                                str_env])
        x_result = not Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path)
                        for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = (not f_success) and x_result
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test cleaning
    ####
    def nottest_app_for_run_clean_with_intermediary(self):
        """
        Test the scenario where the example script is ran with clean
        intermediary mode.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_run_clean_with_intermediary")
        str_dir_1 = os.path.join(str_env, "dir1")
        str_dir_2 = os.path.join(str_env, "dir2")
        str_dir_3 = os.path.join(str_env, "dir3")
        str_dir_4 = os.path.join(str_dir_1, "dir4")
        str_dir_5 = os.path.join(str_dir_1, "dir5")
        str_dir_6 = os.path.join(str_dir_2, "dir6")
        str_file_1 = os.path.join(str_dir_1, "file1.txt")
        str_file_2 = os.path.join(str_dir_4, "file2.txt")
        str_file_2_ok = os.path.join(str_dir_4, ".file2.txt.ok")
        str_file_3 = os.path.join(str_dir_4, "file3.txt")
        str_file_3_ok = os.path.join(str_dir_4, ".file3.txt.ok")
        str_file_4 = os.path.join(str_dir_6, "file4.txt")
        str_file_5 = os.path.join(str_dir_3, "file5.txt")
        str_file_6 = os.path.join(str_dir_3, "file6.txt")
        str_file_6_ok = os.path.join(str_dir_3, ".file6.txt.ok")
        str_file_7 = os.path.join(str_dir_3, "file7.txt")
        str_file_7_ok = os.path.join(str_dir_3, ".file7.txt.ok")
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        self.func_make_dummy_dir(str_env)

        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--example",
                                "test_app_for_run_clean_with_intermediary",
                                "--log",
                                str_log_file,
                                "--out_dir",
                                str_env,
                                "--clean",
                                "--user_ordered_commands"])
        x_result = Commandline.Commandline().func_CMD(str_command)

        # Check test environment for results
        lstr_files_should_exist = [str_file_1, str_file_2_ok,
                                   str_file_3_ok,  str_file_4, 
                                   str_file_5, str_file_6_ok,
                                   str_file_7, str_file_7_ok,
                                   str_log_file]
        lstr_files_should_not_exist = [str_file_2, str_file_3, str_file_6]
        f_success = sum([os.path.exists(str_path) for str_path in lstr_files_should_exist]) == len(lstr_files_should_exist)
        f_success = f_success and sum([not os.path.exists(str_path) for str_path in lstr_files_should_not_exist]) == len(lstr_files_should_not_exist)
        f_success = f_success and x_result
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_run_self_organize_clean_with_intermediary(self):
        """
        Test the scenario where the example script is ran with clean intermediary mode.
        This is also using self-organizing.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_run_self_organize_clean_with_intermediary")
        str_dir_1 = os.path.join(str_env, "dir1")
        str_dir_2 = os.path.join(str_env, "dir2")
        str_dir_3 = os.path.join(str_env, "dir3")
        str_dir_4 = os.path.join(str_dir_1, "dir4")
        str_dir_5 = os.path.join(str_dir_1, "dir5")
        str_dir_6 = os.path.join(str_dir_2, "dir6")
        str_file_1 = os.path.join(str_dir_1, "file1.txt")
        str_file_2 = os.path.join(str_dir_4, "file2.txt")
        str_file_2_ok = os.path.join(str_dir_4, ".file2.txt.ok")
        str_file_3 = os.path.join(str_dir_4, "file3.txt")
        str_file_3_ok = os.path.join(str_dir_4, ".file3.txt.ok")
        str_file_4 = os.path.join(str_dir_6, "file4.txt")
        str_file_5 = os.path.join(str_dir_3, "file5.txt")
        str_file_6 = os.path.join(str_dir_3, "file6.txt")
        str_file_6_ok = os.path.join(str_dir_3, ".file6.txt.ok")
        str_file_7 = os.path.join(str_dir_3, "file7.txt")
        str_file_7_ok = os.path.join(str_dir_3, ".file7.txt.ok")
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        self.func_make_dummy_dir(str_env)

        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_shuffled,
                                "--example",
                                "test_app_for_run_self_organize_clean_with_intermediary",
                                "--log",
                                str_log_file,
                                "--out_dir",
                                str_env,
                                "--clean"])
        x_result = Commandline.Commandline().func_CMD(str_command)

        # Check test environment for results
        lstr_files_should_exist = [str_file_1, str_file_2_ok,
                                   str_file_3_ok,  str_file_4, 
                                   str_file_5, str_file_6_ok,
                                   str_file_7, str_file_7_ok]
        lstr_files_should_not_exist = [str_file_2, str_file_3, str_file_6]
        f_success = sum([os.path.exists(str_path) for str_path in lstr_files_should_exist]) == len(lstr_files_should_exist)
        f_success = f_success and sum([not os.path.exists(str_path) for str_path in lstr_files_should_not_exist]) == len(lstr_files_should_not_exist)
        f_success = f_success and x_result

        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test outputing JSON
    ####
    def nottest_app_for_output_json(self):
        """
        Test the scenario where the example script is not ran but instead a
        json file is created.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_output_json")
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_json = os.path.join(str_env, "test.json")
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        self.func_make_dummy_dir(str_env)
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--json_out",
                                str_json,
                                "--example",
                                "test_app_for_output_json",
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        str_dir_4 = os.path.join(str_env, "dir1", "dir4")
        str_dir_3 = os.path.join(str_env, "dir3")
        dict_env = self.func_get_example_script_dirs_files(str_env)
        lstr_files_exist = [str_json,
                            str_log_file,
                            str_job_log]
        lstr_files_not_exist = [os.path.join(str_dir_4, "file2.txt"),
                                os.path.join(str_dir_4, "file3.txt"),
                                os.path.join(str_dir_3, "file6.txt"),
                                os.path.join(str_dir_3, "file7.txt")]
        f_success = sum([os.path.exists(str_path) 
                          for str_path in lstr_files_exist] 
                       ) == len(lstr_files_exist)
        f_success = f_success and (sum([os.path.exists(str_path)
                                        for str_path in lstr_files_not_exist]
                                      )==0)
        f_success = f_success and os.path.exists(str_json)
        f_success = f_success and x_result
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_files([str_json])
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(x_result)

    ####
    ## Test inputing JSON
    ####

    ####
    ## Test outputing WDL
    ####

    ####
    ## Testing graph output
    ####

    ####
    ## Test config file
    ####
    def nottest_app_for_config_file(self):
        """
        Test the scenario where the example script is with a configfile.
        The --example will be overwritten and so should be different than
        what is set up here. If it is not changed this test will catch it,
        this is how it checks for the config file being used.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_config_file")
        self.func_make_dummy_dir(str_env)
        str_log = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        str_message = "should_not_show_up"
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_config,
                                "--example",
                                str_message,
                                "--log",
                                str_log,
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                         for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        for str_path in dict_env["files"]:
            str_ext = os.path.splitext(str_path)[1]
            if(str_path not in [str_log, str_job_log] and (str_ext!=".ok")):
                with open(str_path, "r") as hndl_read:
                    str_message = hndl_read.read()
                    f_success = f_success and (str_message==str_message)
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_files([os.path.join(str_env,"ExampleConfig.sh"),
                                os.path.join(str_env,"ExampleScript_job.err"),
                                os.path.join(str_env,"ExampleScript_job.log")])
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test job running 1 sample local
    ####
    def fixtest_app_for_config_and_one_sample(self):
        """
        Test the scenario where the example script is with a config file
        and a sample file with one sample.
        The --example will be overwritten and so should be different than
        what is set up here. If it is not changed this test will catch it,
        this is how it checks for the config file being used. The sample file
        is checked because it will lend it's name to the sample directory.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_config_sample_file")
        self.func_make_dummy_dir(str_env)
        str_log = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        str_message = "should_not_show_up"
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_one_sample,
                                "--example",
                                str_message,
                                "--sample_file",
                                self.str_sample_one_file,
                                "--log",
                                str_log,
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                         for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        for str_path in dict_env["files"]:
            str_ext = os.path.splitext(str_path)[1]
            if(str_path not in [str_log, str_job_log] and (str_ext!=".ok")):
                with open(str_path, "r") as hndl_read:
                    str_message = hndl_read.read()
                    f_success = f_success and (str_message==str_message)
        # Destroy environment
        #self.func_clean_up_example_script(str_env)
        #self.func_remove_files([os.path.join(str_env,"ExampleConfig.sh"),
        #                        os.path.join(str_env,"ExampleScript_job.err"),
        #                        os.path.join(str_env,"ExampleScript_job.log")])
        #self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test job running for 3 samples local
    ####
    def test_app_for_config_and_three_sample(self):
        """
        Test the scenario where the example script is with a config file
        and a sample file with three sample.
        The --example will be overwritten and so should be different than
        what is set up here. If it is not changed this test will catch it,
        this is how it checks for the config file being used. The sample file
        is checked because it will lend it's name to the sample directory.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_config_and_three_sample")
        self.func_make_dummy_dir(str_env)
        str_log = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        str_message = "should_not_show_up"
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_three_sample,
                                "--example",
                                str_message,
                                "--sample_file",
                                self.str_sample_three_file,
                                "--log",
                                str_log,
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                         for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        for str_path in dict_env["files"]:
            str_ext = os.path.splitext(str_path)[1]
            if(str_path not in [str_log, str_job_log] and (str_ext!=".ok")):
                with open(str_path, "r") as hndl_read:
                    str_message = hndl_read.read()
                    f_success = f_success and (str_message==str_message)
        # Destroy environment
        #self.func_clean_up_example_script(str_env)
        #self.func_remove_files([os.path.join(str_env,"ExampleConfig.sh"),
        #                        os.path.join(str_env,"ExampleScript_job.err"),
        #                        os.path.join(str_env,"ExampleScript_job.log")])
        #self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test timestamp for no stale
    ####
    def nottest_app_for_timestamp_no_stale(self):
        """
        Test the scenario where the example script does not replace
        any files for timestamping.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_time_stamp")
        str_log = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        self.func_make_dummy_dir(str_env)
        lstr_dirs = [os.path.join(str_env, "dir1"),
                     os.path.join(str_env, "dir2"),
                     os.path.join(str_env, "dir3"),
                     os.path.join(str_env, "dir1", "dir4"),
                     os.path.join(str_env, "dir1", "dir5"),
                     os.path.join(str_env, "dir2", "dir6")]
        lstr_files = [os.path.join(str_env, "dir1", "file1.txt"),
                      os.path.join(str_env, "dir1", "dir4", "file2.txt"),
                      os.path.join(str_env, "dir1", "dir4", ".file2.txt.ok"),
                      os.path.join(str_env, "dir1", "dir4", "file3.txt"),
                      os.path.join(str_env, "dir1", "dir4", ".file3.txt.ok"),
                      os.path.join(str_env, "dir2", "dir6", "file4.txt"),
                      os.path.join(str_env, "dir3", "file5.txt"),
                      os.path.join(str_env, "dir3", "file6.txt"),
                      os.path.join(str_env, "dir3", ".file6.txt.ok"),
                      os.path.join(str_env, "dir3", "file7.txt"),
                      os.path.join(str_env, "dir3", ".file7.txt.ok")]
        dict_file_dirs = self.func_get_example_script_dirs_files(str_env)
        for str_dir in sorted(lstr_dirs):
            self.func_make_dummy_dir(str_dir)
        for str_file in sorted(lstr_files):
            self.func_make_dummy_file(str_file,"Notdeleted")
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_timestamp,
                                "--timestamp",
                                "5",
                                "--example",
                                "test_app_for_time_stamp",
                                "--log",
                                str_log,
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                         for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        for str_file_made in lstr_files:
            with open(str_file_made,"r") as hndl_check_file:
                str_file_key = hndl_check_file.read().split("\n")[-1]
                f_success = f_success and str_file_key == "Notdeleted"

        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test timestamp for some files replaced
    ####
    def nottest_app_for_timestamp_replace_files(self):
        """
        Test the scenario where the example script replaces some
        files due to time stamp eventhough they exist.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_timestamp_replace_files")
        str_log = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        str_file_3 = os.path.join(str_env, "dir1", "dir4", "file3.txt")
        str_file_3_ok = os.path.join(str_env, "dir1", "dir4", ".file3.txt.ok")
        str_file_7 = os.path.join(str_env, "dir3", "file7.txt")
        str_file_7_ok = os.path.join(str_env, "dir3", ".file7.txt.ok")
        self.func_make_dummy_dir(str_env)
        lstr_dirs = [os.path.join(str_env, "dir1"),
                     os.path.join(str_env, "dir2"),
                     os.path.join(str_env, "dir3"),
                     os.path.join(str_env, "dir1", "dir4"),
                     os.path.join(str_env, "dir1", "dir5"),
                     os.path.join(str_env, "dir2", "dir6")]
        lstr_files = [os.path.join(str_env, "dir1", "file1.txt"),
                      os.path.join(str_env, "dir1", "dir4", "file2.txt"),
                      os.path.join(str_env, "dir1", "dir4", ".file2.txt.ok"),
                      str_file_3,
                      str_file_3_ok,
                      os.path.join(str_env, "dir2", "dir6", "file4.txt"),
                      os.path.join(str_env, "dir3", "file5.txt"),
                      os.path.join(str_env, "dir3", "file6.txt"),
                      os.path.join(str_env, "dir3", ".file6.txt.ok"),
                      str_file_7,
                      str_file_7_ok]
        dict_file_dirs = self.func_get_example_script_dirs_files(str_env)
        for str_dir in sorted(lstr_dirs):
            self.func_make_dummy_dir(str_dir)
        for str_file in sorted(lstr_files):
            self.func_make_dummy_file(str_file,"Notdeleted")
        # Throw off timing
        self.func_remove_files([str_file_3, str_file_3_ok])
        time.sleep(5)
        self.func_make_dummy_file(str_file_3,
                                  "NEW") 
        self.func_make_dummy_file(str_file_3_ok,
                                  "NEW") 
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script_timestamp,
                                "--timestamp",
                                "3",
                                "--example",
                                "test_app_for_time_stamp",
                                "--log",
                                str_log,
                                "--out_dir",
                                str_env])
        x_result = Commandline.Commandline().func_CMD(str_command)
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                         for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result
        for str_file_made in lstr_files:
            with open(str_file_made,"r") as hndl_check_file:
                str_file_key = hndl_check_file.read().split("\n")[-1]
                if str_file_made in [str_file_3,
                                     str_file_3_ok,
                                     str_file_7]:
                    f_success = f_success and str_file_key == "NEW"
                elif str_file_made in [str_file_7_ok]:
                    f_success = f_success and str_file_key == ""
                else:
                    f_success = f_success and str_file_key == "Notdeleted"
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        # Evaluate
        self.func_test_true(f_success)

    ####
    ## Test compression and archiving
    ####
    def nottest_app_for_run_with_no_compression(self):
        """
        Test the scenario where the example script is ran with no compression.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_no_compression")
        self.func_make_dummy_dir(str_env)
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_compression = "none"
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_no_compression",
                                "--out_dir",
                                str_env,
                                "--compress",
                                str_compression])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result

        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])
        
        # Evaluate
        self.func_test_true(f_success)
 
    def nottest_app_for_run_with_compression_archive(self):
        """
        Test the scenario where the example script is ran with compression, archive mode.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory,
                               "test_app_for_run_with_compression_archive")
        str_archive = str_env + ".tar.gz"
        self.func_make_dummy_dir(str_env)
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_compression = Pipeline.STR_COMPRESSION_ARCHIVE
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_compression_archive",
                                "--out_dir",
                                str_env,
                                "--compress",
                                str_compression])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([not os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and os.path.exists(str_archive)
        f_success = f_success and x_result

        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_files([str_archive])
        self.func_remove_dirs([str_env])
        
        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_run_with_compression_first_level(self):
        """
        Test the scenario where the example script is ran with compression, first level mode.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_compression_first_level")
        str_archive_dir1 = os.path.join(str_env, "dir1" + ".tar.gz")
        str_archive_dir2 = os.path.join(str_env, "dir2" + ".tar.gz")
        str_archive_dir3 = os.path.join(str_env, "dir3" + ".tar.gz")
        self.func_make_dummy_dir(str_env)
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_compression = Pipeline.STR_COMPRESSION_FIRST_LEVEL_ONLY
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_compression_first_level",
                                "--out_dir",
                                str_env,
                                "--compress",
                                str_compression])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        lstr_should_not_exist = [os.path.join(str_env, "dir1"),
                                 os.path.join(str_env, "dir2"),
                                 os.path.join(str_env, "dir3")]
        lstr_should_exist = [str_log_file + ".tar.gz",
                             str_job_log + ".tar.gz"]
        f_success = sum([not os.path.exists(str_path) 
                          for str_path in lstr_should_not_exist] 
                       ) == len(lstr_should_not_exist)
        f_success = (sum([os.path.exists(str_path) 
                          for str_path in lstr_should_exist] 
                       ) == len(lstr_should_exist))
        f_success = os.path.exists(str_archive_dir1)
        f_success = os.path.exists(str_archive_dir2)
        f_success = os.path.exists(str_archive_dir3)
        f_success = x_result
        
        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_remove_files(str_archive_dir1)
        self.func_remove_files(str_archive_dir2)
        self.func_remove_files(str_archive_dir3)
        self.func_remove_files(str_log_file + ".tar.gz")
        self.func_remove_files(str_job_log + ".tar.gz")
        self.func_remove_dirs([str_env])
        
        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_run_with_compression_intermediary(self):
        """
        Test the scenario where the example script is ran with compression, intermediary mode.
        """
        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_compression_intermediary")
        str_dir_1 = os.path.join(str_env, "dir1")
        str_dir_2 = os.path.join(str_env, "dir2")
        str_dir_3 = os.path.join(str_env, "dir3")
        str_dir_4 = os.path.join(str_dir_1, "dir4")
        str_dir_5 = os.path.join(str_dir_1, "dir5")
        str_dir_6 = os.path.join(str_dir_2, "dir6")
        str_file_1 = os.path.join(str_dir_1, "file1.txt")
        str_file_2_gz = os.path.join(str_dir_4, "file2.txt.gz")
        str_file_2 = os.path.join(str_dir_4, "file2.txt")
        str_file_2_ok = os.path.join(str_dir_4, ".file2.txt.ok")
        str_file_3 = os.path.join(str_dir_4, "file3.txt")
        str_file_3_gz = os.path.join(str_dir_4, "file3.txt.gz")
        str_file_3_ok = os.path.join(str_dir_4, ".file3.txt.ok")
        str_file_4 = os.path.join(str_dir_6, "file4.txt")
        str_file_5 = os.path.join(str_dir_3, "file5.txt")
        str_file_6_gz = os.path.join(str_dir_3, "file6.txt.gz")
        str_file_6 = os.path.join(str_dir_3, "file6.txt")
        str_file_6_ok = os.path.join(str_dir_3, ".file6.txt.ok")
        str_file_7_gz = os.path.join(str_dir_3, "file7.txt.gz")
        str_file_7 = os.path.join(str_dir_3, "file7.txt")
        str_file_7_ok = os.path.join(str_dir_3, ".file7.txt.ok")
        self.func_make_dummy_dir(str_env)
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)

        # Call Example script
        str_compression = Pipeline.STR_COMPRESSION_AS_YOU_GO
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_compression_intermediary",
                                "--out_dir",
                                str_env,
                                "--compress",
                                str_compression])
        x_result = Commandline.Commandline().func_CMD(str_command)

        # Check test environment for results
        lstr_files_should_exist = [str_file_1, str_file_2_gz, str_file_2_ok,
                                    str_file_3_gz, str_file_3_ok,
                                    str_file_4, str_file_5, str_file_6_gz, str_file_6_ok,
                                    str_file_7_gz, str_file_7_ok]
        lstr_files_should_not_exist = [str_file_2, str_file_3, str_file_6, str_file_7]
        f_success = sum([os.path.exists(str_path) for str_path in lstr_files_should_exist]) == len(lstr_files_should_exist)
        f_success = f_success and sum([not os.path.exists(str_path) for str_path in lstr_files_should_not_exist]) == len(lstr_files_should_not_exist)
        f_success = f_success and x_result

        # Destroy environment
        self.func_remove_files([str_file_2_gz, str_file_3_gz, str_file_6_gz, str_file_7_gz])
        self.func_clean_up_example_script(str_env)
        self.func_remove_dirs([str_env])

        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_run_with_archiving_move(self):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a move.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_move")
        str_env_move = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_move_2")
        self.func_make_dummy_dirs([str_env, str_env_move])
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_archiving_move",
                                "--out_dir",
                                str_env,
                                "--move",
                                str_env_move])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([not os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
                        
        dict_env = self.func_get_example_script_dirs_files(os.path.join(str_env_move, "test_app_for_run_with_archiving_move"))
        f_success = f_success and sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result

        # Destroy environment
        self.func_clean_up_example_script(os.path.join(str_env_move, "test_app_for_run_with_archiving_move"))
        self.func_remove_dirs([str_env, str_env_move])
        
        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_run_with_archiving_copy(self):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a copy to two locations.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy")
        str_env_copy_2 = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_2")
        str_env_copy_3 = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_3")
        self.func_make_dummy_dirs([str_env, str_env_copy_2, str_env_copy_3])
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_archiving_move",
                                "--out_dir",
                                str_env,
                                "--copy",
                                str_env_copy_2,
                                "--copy",
                                str_env_copy_3])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
                        
        dict_env = self.func_get_example_script_dirs_files(os.path.join(str_env_copy_2, "test_app_for_run_with_archiving_copy"))
        f_success = f_success and sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
                        
        dict_env = self.func_get_example_script_dirs_files(os.path.join(str_env_copy_3, "test_app_for_run_with_archiving_copy"))
        f_success = f_success and sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result

        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_clean_up_example_script(os.path.join(str_env_copy_2, "test_app_for_run_with_archiving_copy"))
        self.func_clean_up_example_script(os.path.join(str_env_copy_3, "test_app_for_run_with_archiving_copy"))
        self.func_remove_dirs([str_env_copy_2, str_env_copy_3, str_env])
        
        # Evaluate
        self.func_test_true(f_success)

    def nottest_app_for_run_with_archiving_copy_move(self):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a copy to one location.
        The output directory is then moved to another.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move")
        str_env_move = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_move")
        str_env_copy = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_copy")
        self.func_make_dummy_dirs([str_env, str_env_move, str_env_copy])
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_archiving_copy_move",
                                "--out_dir",
                                str_env,
                                "--move",
                                str_env_move,
                                "--copy",
                                str_env_copy])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files(str_env)
        f_success = sum([not os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
                        
        dict_env = self.func_get_example_script_dirs_files(os.path.join(str_env_move, "test_app_for_run_with_archiving_copy_move"))
        f_success = f_success and sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
                        
        dict_env = self.func_get_example_script_dirs_files(os.path.join(str_env_copy, "test_app_for_run_with_archiving_copy_move"))
        f_success = f_success and sum([os.path.exists(str_path) 
                          for str_path in dict_env["files"] + dict_env["directories"]] 
                       ) == len(dict_env["files"] + dict_env["directories"])
        f_success = f_success and x_result

        # Destroy environment
        self.func_clean_up_example_script(str_env)
        self.func_clean_up_example_script(os.path.join(str_env_move, "test_app_for_run_with_archiving_copy_move"))
        self.func_clean_up_example_script(os.path.join(str_env_copy, "test_app_for_run_with_archiving_copy_move"))
        self.func_remove_dirs([str_env, str_env_move, str_env_copy])
        
        # Evaluate
        self.func_test_true(f_success)
        
    def nottest_app_for_run_with_archiving_copy_move_compress(self):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a copy to one location.
        The output directory is then moved to another. The output directory in this case is compressed into one archive
        before moving.
        """

        # Create test environment
        str_env = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress")
        str_env_move = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_move")
        str_env_copy = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_copy")
        str_env_archive = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress.tar.gz")
        str_env_move_archive = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_move", "test_app_for_run_with_archiving_copy_move_compress.tar.gz")
        str_env_copy_archive = os.path.join(self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_copy", "test_app_for_run_with_archiving_copy_move_compress.tar.gz")
        self.func_make_dummy_dirs([str_env, str_env_move, str_env_copy])
        str_log_file = os.path.join(str_env, self.str_log_file_name)
        str_job_log = os.path.join(str_env,
                                   ParentScript.C_STR_JOB_LOGGER_NAME)
        
        # Call Example script
        str_command = " ".join([self.str_python,
                                self.str_script,
                                "--log",
                                str_log_file,
                                "--example",
                                "test_app_for_run_with_archiving_copy_move",
                                "--out_dir",
                                str_env,
                                "--move",
                                str_env_move,
                                "--copy",
                                str_env_copy,
                                "--compress",
                                Pipeline.STR_COMPRESSION_ARCHIVE])
        x_result = Commandline.Commandline().func_CMD(str_command)
        
        # Check test environment for results
        f_success = not os.path.exists(str_env_archive)
        f_success = f_success and os.path.exists(str_env_move_archive)
        f_success = f_success and os.path.exists(str_env_copy_archive)
        f_success = f_success and x_result

        # Destroy environment
        self.func_remove_files([str_env_move_archive, str_env_copy_archive])
        self.func_remove_dirs([str_env, str_env_move, str_env_copy])
        
        # Evaluate
        self.func_test_true(f_success)

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(FunctionalTester)
