
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
        str_answer = "{\"commands\": []}"
        self.func_test_equals( str_answer, str_result )

    def test_func_pipeline_to_json_for_no_command( self ):
        """
        Test creating a pipeline with no command, capturing commandline parameters.
        """
        lstr_commands = []
        dict_arguments = {"left":"left.fasta", "right":"right.fasta", "count":1, "setting":2.3, "outputs":["file.txt", "file2.txt", "file3.txt"] }
        str_result = JSONManager.JSONManager.func_pipeline_to_json( lstr_commands, dict_arguments )
        str_answer = "{\"count\": 1, \"commands\": [], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
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
        str_answer = "{\"commands\": [{\"MAKES\": [\"/file/two.txt\", \"/file/three.txt\"], \"NEEDS\": [\"/file/one.txt\"], \"COMMAND\": \"This is the test command\"}]}"
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
        str_answer = "{\"count\": 1, \"commands\": [{\"MAKES\": [\"/file/two.txt\", \"/file/three.txt\"], \"NEEDS\": [\"/file/one.txt\"], \"COMMAND\": \"This is the test command\"}], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
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
        str_answer = "{\"count\": 1, \"commands\": [{\"MAKES\": [\"/file/two.txt\", \"/file/three.txt\"], \"NEEDS\": [\"/file/one.txt\"], \"COMMAND\": \"This is the test command 1\"}, {\"MAKES\": [\"/file/four.txt\", \"/file/five.txt\"], \"NEEDS\": [\"/file/three.txt\"], \"COMMAND\": \"This is the test command 2\"}], \"right\": \"right.fasta\", \"outputs\": [\"file.txt\", \"file2.txt\", \"file3.txt\"], \"setting\": 2.3, \"left\": \"left.fasta\"}"
        self.func_test_equals( str_answer, str_result )

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( JSONManagerTester )              
