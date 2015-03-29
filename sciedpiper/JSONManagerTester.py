
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import Command
import JSONManager
import os
import ParentPipelineTester
import unittest

class JSONManagerTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the JSON Manager object.
    """
    
    def test_func_pipeline_to_json_for_no_command_or_argmuents( self ):
        """
        Test creating a pipeline with no command, capturing commandline parameters.
        """
        lstr_commands = []
        dict_arguments = {}
        str_result = JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments )
        str_answer = "{\"" + JSONManager.COMMANDS + "\": []}"
        self.func_test_equals( str_answer, str_result )


    def test_func_pipeline_to_json_for_no_command( self ):
        """
        Test creating a pipeline with no command, capturing commandline parameters.
        """
        lstr_commands = []
        dict_arguments = {"left":"left.fasta", "right":"right.fasta", "count":1, "setting":2.3, "outputs":["file.txt", "file2.txt", "file3.txt"] }
        str_result = JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments )
        str_answer = "{\"count\": 1, \"" + JSONManager.COMMANDS + "\": [], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
        self.func_test_equals( str_answer, str_result )


    def test_func_pipeline_to_json_for_one_command_no_arguments( self ):
        """
        Test creating a pipeline with one command, no commandline parameters.
        """
        lstr_commands = [ Command.Command( str_cur_command = "This is the test command",
                                           lstr_cur_dependencies = ["/file/one.txt"],
                                           lstr_cur_products = ["/file/two.txt","/file/three.txt"] ) ]
        dict_arguments = {}
        str_result = JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments )
        str_answer = "{\"" + JSONManager.COMMANDS + "\": [{\""+Command.STR_PRODUCTS_JSON+"\": [\"/file/two.txt\", \"/file/three.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\"/file/one.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"This is the test command\"}]}"
        self.func_test_equals( str_answer, str_result )

        
    def test_func_pipeline_to_json_for_one_command_and_arguments( self ):
        """
        Test creating a pipeline with one command, and commandline parameters.
        """
        lstr_commands = [ Command.Command( str_cur_command = "This is the test command",
                                           lstr_cur_dependencies = ["/file/one.txt"],
                                           lstr_cur_products = ["/file/two.txt","/file/three.txt"] ) ]
        dict_arguments = {"left":"left.fasta", "right":"right.fasta", "count":1, "setting":2.3, "outputs":["file.txt", "file2.txt", "file3.txt"] }
        str_result = JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments )
        str_answer = "{\"count\": 1, \"" + JSONManager.COMMANDS + "\": [{\""+Command.STR_PRODUCTS_JSON+"\": [\"/file/two.txt\", \"/file/three.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\"/file/one.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"This is the test command\"}], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
        self.func_test_equals( str_answer, str_result )


    def test_func_pipeline_to_json_for_two_commands_and_arguments( self ):
        """
        Test creating a pipeline with two commands, and commandline parameters.
        """
        lstr_commands = [ Command.Command( str_cur_command = "This is the test command 1",
                                           lstr_cur_dependencies = ["/file/one.txt"],
                                           lstr_cur_products = ["/file/two.txt","/file/three.txt"] ),
                          Command.Command( str_cur_command = "This is the test command 2",
                                           lstr_cur_dependencies = ["/file/three.txt"],
                                           lstr_cur_products = ["/file/four.txt","/file/five.txt"] ) ]
        dict_arguments = {"left":"left.fasta", "right":"right.fasta", "count":1, "setting":2.3, "outputs":["file.txt", "file2.txt", "file3.txt"] }
        str_result = JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments )
        str_answer = "{\"count\": 1, \"" + JSONManager.COMMANDS + "\": [{\""+Command.STR_PRODUCTS_JSON+"\": [\"/file/two.txt\", \"/file/three.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\"/file/one.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"This is the test command 1\"}, {\""+Command.STR_PRODUCTS_JSON+"\": [\"/file/four.txt\", \"/file/five.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\"/file/three.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"This is the test command 2\"}], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
        self.func_test_equals( str_answer, str_result )


    def test_func_pipeline_to_json_for_two_commands_and_arguments_write_to_file( self ):
        """
        Test creating a pipeline with two commands, and commandline parameters.
        This tests that a write to file occurs and the correct json string is written.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_func_pipeline_to_json_for_two_commands_and_arguments_write_to_file" )
        str_result_file = os.path.join( str_env, "test_func_pipeline_to_json_for_two_commands_and_arguments_write_to_file.txt" )
        self.func_make_dummy_dir( str_env )

        lstr_commands = [ Command.Command( str_cur_command = "This is the test command 1",
                                           lstr_cur_dependencies = ["/file/one.txt"],
                                           lstr_cur_products = ["/file/two.txt","/file/three.txt"] ),
                          Command.Command( str_cur_command = "This is the test command 2",
                                           lstr_cur_dependencies = ["/file/three.txt"],
                                           lstr_cur_products = ["/file/four.txt","/file/five.txt"] ) ]
        dict_arguments = {"left":"left.fasta", "right":"right.fasta", "count":1, "setting":2.3, "outputs":["file.txt", "file2.txt", "file3.txt"] }
        JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments, str_file=str_result_file )
        str_answer = "{\"count\": 1, \"" + JSONManager.COMMANDS + "\": [{\""+Command.STR_PRODUCTS_JSON+"\": [\"/file/two.txt\", \"/file/three.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\"/file/one.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"This is the test command 1\"}, {\""+Command.STR_PRODUCTS_JSON+"\": [\"/file/four.txt\", \"/file/five.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\"/file/three.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"This is the test command 2\"}], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
        
        # Evaluate
        str_result = ""
        with open( str_result_file, "r" ) as hndl_result:
          str_result = hndl_result.read()
        self.func_test_equals( str_answer, str_result )

        # Destroy environment
        self.func_remove_files( [ str_result_file ] )
        self.func_remove_dirs( [ str_env ] )


    def test_func_json_to_commands_None_string( self ):
        """
        Test making command and argument objects from a None json string.
        """
        # Create test environment
        str_json = None
        str_answer = "{}"

        # Get Results
        dict_pipeline_info = JSONManager.JSONManager.func_json_to_commands( str_json )

        # Evaluate Results
        self.func_test_equals( str( dict_pipeline_info ), str_answer )


    def test_func_json_to_commands_blank_string( self ):
        """
        Test making command and argument objects from a None json string.
        """

        # Create test environment
        str_json = ""
        str_answer = "{}"

        # Get Results
        dict_pipeline_info = JSONManager.JSONManager.func_json_to_commands( str_json )

        # Evaluate Results
        self.func_test_equals( str( dict_pipeline_info ), str_answer )


    def test_func_json_to_commands_arguments_only_string( self ):
        """
        Test making command and argument objects from a json string. Only arguments given here.
        """
        # Create test environment
        str_answer = "{\'" + JSONManager.COMMANDS + "\': [], \'" + JSONManager.ARGUMENTS + "\': {argument1: 1, argument2: str2, argument3: False, argument4: /a/b/c/d/argument4.txt, argument5: [u'hello', 1, 1.2]}}"
        str_json = "{ \"argument1\" : 1, \"argument2\" : \"str2\", \"argument3\" : false, \"argument4\" : \"/a/b/c/d/argument4.txt\", \"argument5\" : [\"hello\",1,1.2] }"
        # Get Results
        dict_pipeline_info = JSONManager.JSONManager.func_json_to_commands( str_json )
        list_commands_pipe = dict_pipeline_info[ JSONManager.COMMANDS ]
        dict_commands_pipe = dict_pipeline_info[ JSONManager.ARGUMENTS ]
        str_result = u"{\'"+JSONManager.COMMANDS+"\': " + str( list_commands_pipe ) + ", \'" + JSONManager.ARGUMENTS+"\': " + str( dict_commands_pipe ) + "}"
        # Evaluate Results
        self.func_test_equals( str_answer, str_result )


    def test_func_json_to_commands_commands_only_string( self ):
        """
        Test making command and argument objects from a json string. Only commands given here.
        """
        # Create test environment
        str_answer = "{\'" + JSONManager.COMMANDS + "\': [u'Command: command.sh; Dependencies: /file2.txt,/file3.txt; Products: /file1.txt; Cleaning: '], \'" + JSONManager.ARGUMENTS + "\': {}}"
        str_json = "{\"" + JSONManager.COMMANDS + "\": [{\""+Command.STR_PRODUCTS_JSON+"\": [\""+os.path.sep+"file1.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\""+os.path.sep+"file2.txt\",\""+os.path.sep+"file3.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"command.sh\"}]}"
        # Get Results
        dict_pipeline_info = JSONManager.JSONManager.func_json_to_commands( str_json )
        list_commands_pipe = dict_pipeline_info[ JSONManager.COMMANDS ]
        dict_commands_pipe = dict_pipeline_info[ JSONManager.ARGUMENTS ]
        str_result = "{\'"+JSONManager.COMMANDS+"\': " + str( [ cur_cmd.func_detail() for cur_cmd in list_commands_pipe ] ) + ", \'" + JSONManager.ARGUMENTS+"\': " + str( dict_commands_pipe ) + "}"
        # Evaluate Results
        self.func_test_equals( str_answer, str_result )


    def test_func_json_to_commands_arguments_and_arguments_string( self ):
        """
        Test making command and argument objects from a json string. Commands and arguments given here.
        """
        # Create test environment
        str_answer = "{\'" + JSONManager.COMMANDS + "\': [u'Command: command.sh; Dependencies: /file2.txt,/file3.txt; Products: /file1.txt; Cleaning: '], \'" + JSONManager.ARGUMENTS + "\': {argument1: 1, argument2: str2, argument3: False, argument4: /a/b/c/d/argument4.txt, argument5: [u'hello', 1, 1.2]}}"
        str_json = "{ \"" + JSONManager.COMMANDS + "\": [{\""+Command.STR_PRODUCTS_JSON+"\": [\""+os.path.sep+"file1.txt\"], \"" + Command.STR_DEPENDENCIES_JSON + "\": [\""+os.path.sep+"file2.txt\",\""+os.path.sep+"file3.txt\"], \"" + Command.STR_COMMAND_JSON + "\": \"command.sh\"}], \"argument1\" : 1, \"argument2\" : \"str2\", \"argument3\" : false, \"argument4\" : \"/a/b/c/d/argument4.txt\", \"argument5\" : [\"hello\",1,1.2] }"
        # Get Results
        dict_pipeline_info = JSONManager.JSONManager.func_json_to_commands( str_json )
        list_commands_pipe = dict_pipeline_info[ JSONManager.COMMANDS ]
        dict_commands_pipe = dict_pipeline_info[ JSONManager.ARGUMENTS ]
        str_result = "{\'"+JSONManager.COMMANDS+"\': " + str( [ cur_cmd.func_detail() for cur_cmd in list_commands_pipe ] ) + ", \'" + JSONManager.ARGUMENTS+"\': " + str( dict_commands_pipe ) + "}"
        # Evaluate Results
        self.func_test_equals( str_answer, str_result )

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( JSONManagerTester )              
