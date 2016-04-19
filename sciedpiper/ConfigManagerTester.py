
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2016"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Arguments
import ConfigManager
import os
import ParentPipelineTester
import unittest


class ConfigManagerTester(ParentPipelineTester.ParentPipelineTester):
    """
    Tests the ConfigManager object.
    """

    str_config_default = "file_1.config"
    str_config_content = "\n".join(["[ARGUMENTS_OVER_WRITE]",
                                    "--threads:0",
                                    "log: new_log",
                                    "--wdl:True",
                                    "json_out: True",
                                    "b:   new_bsub_queue",
                                    "--copy: None",
                                    "test:True",
                                    "compress : none",
                                    "--timestamp :  0.0",
                                    "m :11",
                                    "help :  False",
                                    "--clean :False",
                                    "move : None",
                                    "--resources : ExampleScript.resource.config",
                                    "\n",
                                    "[RESOURCES]",
                                    "-z : reference",
                                    "\n",
                                    "[SAMPLE_FILE]",
                                    "--sample_name : 1",
                                    "--file_one : 2",
                                    "--file_two : 3",
                                    "\n",
                                    "[PATH]",
                                    "ENV_PATH: /some/tool",
                                    "PYTHON_PATH: /python/path/",
                                    "\n",
                                    "[COMMANDS]",
                                    "PRECOMMANDS:",
                                    "POSTCOMMANDS:"])

    str_config_default_2 = "file_2.config"
    str_config_2_content = "\n".join(["[ARGUMENTS_OVER_WRITE]",
                                      "--threads:0",
                                      "log: new_log",
                                      "--wdl:True",
                                      "json_out: True",
                                      "b:   new_bsub_queue",
                                      "--copy: None",
                                      "test:True",
                                      "compress : none",
                                      "--timestamp :  0.0",
                                      "m :11",
                                      "help :  False",
                                      "--clean :False",
                                      "move : None",
                                      "--resources : ExampleScript.resource.config",
                                      "\n",
                                      "[RESOURCES]",
                                      "-z : reference",
                                      "\n",
                                      "[SAMPLE_FILE]",
                                      "--sample_name : 1",
                                      "--file_one : 2",
                                      "--file_two : 3",
                                      "\n",
                                      "[PATH]",
                                      "ENV_PATH: /some/tool",
                                      "PYTHON_PATH: /python/path/",
                                      "SCRIPT_PATH: /script/path",
                                      "\n",
                                      "[COMMANDS]",
                                      "PRECOMMANDS: 1. precommand",
                                      "POSTCOMMANDS: 1. postcommand"])

    str_config_default_3 = "file_3.config"
    str_config_3_content = "\n".join(["[ARGUMENTS_OVER_WRITE]",
                                      "--threads:0",
                                      "log: new_log",
                                      "--wdl:True",
                                      "json_out: True",
                                      "b:   new_bsub_queue",
                                      "--copy: None",
                                      "test:True",
                                      "compress : none",
                                      "--timestamp :  0.0",
                                      "m :11",
                                      "help :  False",
                                      "--clean :False",
                                      "move : None",
                                      "--resources : ExampleScript.resource.config",
                                      "\n",
                                      "[RESOURCES]",
                                      "-z : reference",
                                      "\n",
                                      "[SAMPLE_FILE]",
                                      "--sample_name : 1",
                                      "--file_one : 2",
                                      "--file_two : 3",
                                      "\n",
                                      "[PATH]",
                                      "ENV_PATH: /some/tool",
                                      "PYTHON_PATH: /python/path/",
                                      "SCRIPT_PATH: /script/path",
                                      "\n",
                                      "[COMMANDS]",
                                      "PRECOMMANDS: 1. precommand",
                                      "    2. precommand",
                                      "POSTCOMMANDS: 1. postcommand",
                                      "    2. postcommand"])

    def func_create_test_config(self, str_file_name, str_config_content):
        """ Create config file. """
        with open(str_file_name, "w") as hndl_output:
            hndl_output.write(str_config_content)

    def func_delete_test_config(self, str_file_name):
        """ Delete the file name """
        if os.path.exists(str_file_name):
            os.remove(str_file_name)

    def func_prep_environ_parameter(self, str_env_param):
        """ Stored an environmental parameter to be restored after the test. """
        if str_env_param in os.environ:
            return os.environ[str_env_param]
        else:
            os.environ[str_env_param]=""
        return None

    def func_restore_environ_parameter(self, str_env_param, str_env_value):
        """ Restore an envornmental parameter after a test. """
        if str_env_value:
            os.environ[str_env_param]=str_env_value
        elif str_env_value is None:
            del os.environ[str_env_param]

    def test_func_type_cast_for_none(self):
        """ Test func_type_case for none """
        str_answer = "None"
        x_value = None
        str_type = Arguments.C_STR_INT_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        str_result = cfmg_test._func_type_cast(str_type, x_value)
        self.func_test_equals( str_answer, str(str_result) )

    def test_func_type_cast_for_none_2( self ):
        """ Test func_type_case for none 2 """
        str_answer = "None"
        x_value = "None"
        str_type = Arguments.C_STR_INT_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        str_result = cfmg_test._func_type_cast(str_type, x_value)
        self.func_test_equals( str_answer, str(str_result) )

    def test_func_type_cast_for_int( self ):
        """ Test func_type_case for int """
        x_answer = 1
        str_value = "1"
        str_type = Arguments.C_STR_INT_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        x_result = cfmg_test._func_type_cast(str_type, str_value)
        self.func_test_equals( x_answer, str(x_result) )

    def test_func_type_cast_for_float( self ):
        """ Test func_type_case for float """
        x_answer = 0.0
        str_value = "0.0"
        str_type = Arguments.C_STR_FLOAT_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        x_result = cfmg_test._func_type_cast(str_type, str_value)
        self.func_test_equals( x_answer, str(x_result) )

    def test_func_type_cast_for_bool_true( self ):
        """ Test func_type_case for bool true """
        x_answer = True
        str_value = "True"
        str_type = Arguments.C_STR_BOOL_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        x_result = cfmg_test._func_type_cast(str_type, str_value)
        self.func_test_equals( x_answer, str(x_result) )

    def test_func_type_cast_for_bool_false( self ):
        """ Test func_type_case for bool false """
        x_answer = False
        str_value = "False"
        str_type = Arguments.C_STR_BOOL_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        x_result = cfmg_test._func_type_cast(str_type, str_value)
        self.func_test_equals( x_answer, str(x_result) )

    def test_func_type_cast_for_string( self ):
        """ Test func_type_case for bool string """
        x_answer = "string"
        str_value = "string"
        str_type = Arguments.C_STR_STRING_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        x_result = cfmg_test._func_type_cast(str_type, str_value)
        self.func_test_equals( x_answer, str(x_result) )

    def test_func_type_cast_for_list( self ):
        """ Test func_type_case for list """
        x_answer = sorted([1,1.22,"hello",[]])
        str_value = '[[],"hello",1,1.22]'
        str_type = Arguments.C_STR_LIST_TYPE
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        x_result = sorted(cfmg_test._func_type_cast(str_type, str_value))
        self.func_test_equals( x_answer, str(x_result) )

    def test_func_normalize_argument_for_empty_string( self ):
        """ Test func_normalize_argument for an empty string """
        str_env = os.path.join(self.str_test_directory,
                               "func_normalize_argument_for_empty_string")
        str_argument = ""
        dict_args = {}
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        try:
            cfmg_test.func_normalize_argument(str_argument,dict_args)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_func_normalize_argument_for_none_string( self ):
        """ Test func_normalize_argument for an none string """
        str_env = os.path.join(self.str_test_directory, "func_normalize_argument_for_none_string")
        str_answer = ""
        str_argument = None
        dict_args = {}
        try:
            cfmg_test.func_normalize_argument(str_argument,dict_args)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_func_normalize_argument_for_present_string( self ):
        """ Test func_normalize_argument for a string that is present """
        str_env = os.path.join(self.str_test_directory, "func_normalize_argument_for_present_string")
        str_answer = "copy"
        str_argument = "COPY"
        dict_args = {"COPY":"copy"}
        cfmg_test = ConfigManager.ConfigManager(self.str_config_default)
        str_result = cfmg_test.func_normalize_argument(str_argument, dict_args )
        self.func_test_equals( str_answer, str_result )

    def test_func_normalize_argument_for_not_present_string( self ):
        """ Test func_normalize_argument for a string that is not present """
        str_env = os.path.join(self.str_test_directory, "func_normalize_argument_for_not_present_string")
        self.func_make_dummy_dir( str_env )
        str_answer = ""
        str_argument = ""
        dict_args = {}
        try:
            cfmg_test.func_normalize_argument(str_argument,dict_args)
            self.func_remove_dirs([str_env])
            self.assertTrue(False)
        except:
            self.func_remove_dirs([str_env])
            self.assertTrue(True)

    def test_func_update_env_path( self ):
        """ Test func_update_env_path """
        str_env = os.path.join(self.str_test_directory, "func_update_env_path")
        str_config_file = os.path.join(str_env, self.str_config_default)
        self.func_make_dummy_dir(str_env)
        self.func_create_test_config(str_config_file, self.str_config_content)
        str_add_path = os.sep.join(["", "some", "tool"])
        str_restore = self.func_prep_environ_parameter("PATH")
        str_answer = os.environ[ "PATH" ] + ":" + str_add_path
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        cfmg_test.func_update_env_path()
        str_result = os.environ[ "PATH" ]
        self.func_restore_environ_parameter("PATH",str_restore)
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals( str_answer, str_result )

    def test_func_update_python_path(self):
        """ Test func_update_python_path """
        str_env = os.path.join(self.str_test_directory, "func_update_python_path")
        str_config_file = os.path.join(str_env, self.str_config_default)
        self.func_make_dummy_dir(str_env)
        self.func_create_test_config(str_config_file, self.str_config_content)
        str_add_path = os.sep.join(["", "python", "path"])
        str_restore = self.func_prep_environ_parameter("PYTHONPATH")
        str_answer = os.environ[ "PYTHONPATH" ] + ":" + str_add_path
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        cfmg_test.func_update_python_path()
        str_result = os.environ[ "PYTHONPATH" ]
        self.func_restore_environ_parameter("PYTHONPATH",str_restore)
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str_answer, str_result)

    def test_func_update_script_for_false(self):
        """ Test func_update_script_path for no update """
        str_env = os.path.join(self.str_test_directory, "func_update_script_for_false")
        str_config_file = os.path.join(str_env, self.str_config_default)
        self.func_make_dummy_dir(str_env)
        str_script = ""
        x_answer = False
        self.func_create_test_config(str_config_file, self.str_config_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_update_script_path(str_script)
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_update_script_for_an_update(self):
        """ Test func_update_script_path for an update """
        str_env = os.path.join(self.str_test_directory, "func_update_script_for_an_update")
        str_config_file = os.path.join(str_env, self.str_config_default_2)
        self.func_make_dummy_dir(str_env)
        str_script = ""
        x_answer = "/script/path/"
        self.func_create_test_config(str_config_file, self.str_config_2_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_update_script_path(str_script)
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_update_script_for_an_update_append(self):
        """ Test func_update_script_path for an update and an intial path. """
        str_env = os.path.join(self.str_test_directory, "func_update_script_for_an_update")
        str_config_file = os.path.join(str_env, self.str_config_default_2)
        self.func_make_dummy_dir(str_env)
        str_script = "root"
        x_answer = "/script/path/root"
        self.func_create_test_config(str_config_file, self.str_config_2_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_update_script_path(str_script)
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_get_precommands_for_no_command(self):
        """ Test func_get_precommands for no existing precommand """
        str_env = os.path.join(self.str_test_directory, "func_get_precommands_for_no_command")
        str_config_file = os.path.join(str_env, self.str_config_default)
        self.func_make_dummy_dir(str_env)
        x_answer = ""
        self.func_create_test_config(str_config_file, self.str_config_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_get_precommands()
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_get_precommands_for_one_command( self ):
        """ Test func_get_precommands for one existing precommand """
        str_env = os.path.join(self.str_test_directory, "func_get_precommands_for_one_command")
        str_config_file = os.path.join(str_env, self.str_config_default_2)
        self.func_make_dummy_dir( str_env )
        x_answer = "1. precommand"
        self.func_create_test_config(str_config_file, self.str_config_2_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_get_precommands()
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_get_precommands_for_many_command( self ):
        """ Test func_get_precommands for many precommands """
        str_env = os.path.join(self.str_test_directory, "func_get_precommands_for_many_command")
        str_config_file = os.path.join(str_env, self.str_config_default_3)
        self.func_make_dummy_dir(str_env)
        x_answer = "1. precommand\n2. precommand"
        self.func_create_test_config(str_config_file, self.str_config_3_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_get_precommands()
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_get_postcommands_for_no_command(self):
        """ Test func_get_postcommands for no existing precommand """
        str_env = os.path.join(self.str_test_directory, "func_get_postcommands_for_no_command")
        str_config_file = os.path.join(str_env, self.str_config_default)
        self.func_make_dummy_dir(str_env)
        x_answer = ""
        self.func_create_test_config(str_config_file, self.str_config_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_get_postcommands()
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_get_postcommands_for_one_command( self ):
        """ Test func_get_postcommands for one existing postcommand """
        str_env = os.path.join(self.str_test_directory, "func_get_postcommands_for_one_command")
        str_config_file = os.path.join(str_env, self.str_config_default_2)
        self.func_make_dummy_dir(str_env)
        x_answer = "1. postcommand"
        self.func_create_test_config(str_config_file, self.str_config_2_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_get_postcommands()
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

    def test_func_get_postcommands_for_many_command( self ):
        """ Test func_get_postcommands for many postcommands """
        str_env = os.path.join(self.str_test_directory, "func_get_postcommands_for_many_command")
        str_config_file = os.path.join(str_env, self.str_config_default_3)
        self.func_make_dummy_dir( str_env )
        x_answer = "1. postcommand\n2. postcommand"
        self.func_create_test_config(str_config_file, self.str_config_3_content)
        cfmg_test = ConfigManager.ConfigManager(str_config_file)
        x_result = cfmg_test.func_get_postcommands()
        self.func_delete_test_config(str_config_file)
        self.func_remove_dirs([str_env])
        self.func_test_equals(str(x_answer), str(x_result))

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( ConfigManagerTester )
