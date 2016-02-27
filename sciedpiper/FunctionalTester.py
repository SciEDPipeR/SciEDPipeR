
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Commandline
import os
import ParentPipelineTester
import Pipeline
import unittest

class FunctionalTester( ParentPipelineTester.ParentPipelineTester ):
    """
    End-to_end tests for the App. Starting at command line.
    """

    str_script = os.path.join( "bin", "ExampleScript.py" )
 
    def func_clean_up_example_script( self, str_output_dir ):
        """
        Cleans up the directories and files made by the example script.
        """
        
        dict_structure = self.func_get_example_script_dirs_files( str_output_dir )
        self.func_remove_files( dict_structure["files"] )
        self.func_remove_dirs( dict_structure["directories"] )
        
    def func_get_example_script_dirs_files( self, str_output_dir ):
        """
        Gets the standard files and dirs make by the ExampleScript.py.
        They are returned in an order which can be used for file / dir deletion.
        """
        
        str_dir_1 = os.path.join( str_output_dir, "dir1" )
        str_dir_2 = os.path.join( str_output_dir, "dir2" )
        str_dir_3 = os.path.join( str_output_dir, "dir3" )
        str_dir_4 = os.path.join( str_dir_1, "dir4" )
        str_dir_5 = os.path.join( str_dir_1, "dir5" )
        str_dir_6 = os.path.join( str_dir_2, "dir6" )
        
        str_file_1 = os.path.join( str_dir_1, "file1.txt" )
        str_file_2 = os.path.join( str_dir_4, "file2.txt" )
        str_file_2_ok = os.path.join( str_dir_4, ".file2.txt.ok" )
        str_file_3 = os.path.join( str_dir_4, "file3.txt" )
        str_file_3_ok = os.path.join( str_dir_4, ".file3.txt.ok" )
        str_file_4 = os.path.join( str_dir_6, "file4.txt" )
        str_file_5 = os.path.join( str_dir_3, "file5.txt" )
        str_file_6 = os.path.join( str_dir_3, "file6.txt" )
        str_file_6_ok = os.path.join( str_dir_3, ".file6.txt.ok" )
        str_file_7 = os.path.join( str_dir_3, "file7.txt" )
        str_file_7_ok = os.path.join( str_dir_3, ".file7.txt.ok" )
        
        return( { "files" : [ str_file_1, str_file_2, str_file_3,
                            str_file_4, str_file_5, str_file_6, str_file_7,
                            str_file_2_ok, str_file_3_ok, str_file_6_ok, str_file_7_ok ],
                "directories": [ str_dir_4, str_dir_5, str_dir_6, str_dir_1, str_dir_2, str_dir_3 ] } )

    def test_app_for_vanilla_base_run( self ):
        """
        Test the scenario where the example script is ran on all defaults.
        """
        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_vanilla_base_run" )
        self.func_make_dummy_dir( str_env )
        
        # Call Example script
        str_command = "python " + self.str_script + " --example test_app_for_vanilla_base_run --out_dir "+ str_env
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_remove_dirs( [ str_env ] )
        # Evaluate
        self.func_test_true( f_success )

    

    def test_app_for_run_with_no_compression( self ):
        """
        Test the scenario where the example script is ran with no compression.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_no_compression" )
        self.func_make_dummy_dir( str_env )
        
        # Call Example script
        str_compression = "none"
        str_command = "python " + self.str_script + " --example test_app_for_run_with_no_compression --out_dir "+ str_env +" --compress " + str_compression
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )

        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_remove_dirs( [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_success )
 
    def test_app_for_run_with_compression_archive( self ):
        """
        Test the scenario where the example script is ran with compression, archive mode.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_compression_archive" )
        str_archive = str_env + ".tar.gz"
        self.func_make_dummy_dir( str_env )
        
        # Call Example script
        str_compression = Pipeline.STR_COMPRESSION_ARCHIVE
        str_command = "python " + self.str_script + " --example test_app_for_run_with_compression_archive --out_dir "+ str_env +" --compress " + str_compression
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ not os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
        f_success = f_success and os.path.exists( str_archive )

        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_remove_files( [ str_archive ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_success )


    def test_app_for_run_with_compression_first_level( self ):
        """
        Test the scenario where the example script is ran with compression, first level mode.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_compression_first_level" )
        str_archive_dir1 = os.path.join( str_env, "dir1" + ".tar.gz" )
        str_archive_dir2 = os.path.join( str_env, "dir2" + ".tar.gz" )
        str_archive_dir3 = os.path.join( str_env, "dir3" + ".tar.gz" )
        self.func_make_dummy_dir( str_env )
        
        # Call Example script
        str_compression = Pipeline.STR_COMPRESSION_FIRST_LEVEL_ONLY
        str_command = "python " + self.str_script + " --example test_app_for_run_with_compression_first_level --out_dir "+ str_env +" --compress " + str_compression
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ not os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
        f_success = f_success and os.path.exists( str_archive_dir1 )
        f_success = f_success and os.path.exists( str_archive_dir2 )
        f_success = f_success and os.path.exists( str_archive_dir3 )

        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_remove_files( str_archive_dir1 )
        self.func_remove_files( str_archive_dir2 )
        self.func_remove_files( str_archive_dir3 )
        self.func_remove_dirs( [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_success )

    def test_app_for_run_clean_with_intermediary( self ):
        """
        Test the scenario where the example script is ran with clean intermediary mode.
        """
        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_clean_with_intermediary" )
        str_dir_1 = os.path.join( str_env, "dir1" )
        str_dir_2 = os.path.join( str_env, "dir2" )
        str_dir_3 = os.path.join( str_env, "dir3" )
        str_dir_4 = os.path.join( str_dir_1, "dir4" )
        str_dir_5 = os.path.join( str_dir_1, "dir5" )
        str_dir_6 = os.path.join( str_dir_2, "dir6" )
        str_file_1 = os.path.join( str_dir_1, "file1.txt" )
        str_file_2 = os.path.join( str_dir_4, "file2.txt" )
        str_file_2_ok = os.path.join( str_dir_4, ".file2.txt.ok" )
        str_file_3 = os.path.join( str_dir_4, "file3.txt" )
        str_file_3_ok = os.path.join( str_dir_4, ".file3.txt.ok" )
        str_file_4 = os.path.join( str_dir_6, "file4.txt" )
        str_file_5 = os.path.join( str_dir_3, "file5.txt" )
        str_file_6 = os.path.join( str_dir_3, "file6.txt" )
        str_file_6_ok = os.path.join( str_dir_3, ".file6.txt.ok" )
        str_file_7 = os.path.join( str_dir_3, "file7.txt" )
        str_file_7_ok = os.path.join( str_dir_3, ".file7.txt.ok" )
        self.func_make_dummy_dir( str_env )

        # Call Example script
        str_command = "python " + self.str_script + " --example test_app_for_run_clean_with_intermediary --out_dir "+ str_env +" --clean"
        Commandline.Commandline().func_CMD( str_command )

        # Check test environment for results
        lstr_files_should_exist = [ str_file_1, str_file_2_ok,
                                    str_file_3_ok,  str_file_4, 
                                    str_file_5, str_file_6_ok,
                                    str_file_7, str_file_7_ok ]
        lstr_files_should_not_exist = [ str_file_2, str_file_3, str_file_6 ]
        f_success = sum( [ os.path.exists( str_path ) for str_path in lstr_files_should_exist ] ) == len( lstr_files_should_exist )
        f_success = f_success and sum( [ not os.path.exists( str_path ) for str_path in lstr_files_should_not_exist ] ) == len( lstr_files_should_not_exist )

        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_remove_dirs( [ str_env ] )

        # Evaluate
        self.func_test_true( f_success )
 
    def test_app_for_run_with_compression_intermediary( self ):
        """
        Test the scenario where the example script is ran with compression, intermediary mode.
        """
        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_compression_intermediary" )
        str_dir_1 = os.path.join( str_env, "dir1" )
        str_dir_2 = os.path.join( str_env, "dir2" )
        str_dir_3 = os.path.join( str_env, "dir3" )
        str_dir_4 = os.path.join( str_dir_1, "dir4" )
        str_dir_5 = os.path.join( str_dir_1, "dir5" )
        str_dir_6 = os.path.join( str_dir_2, "dir6" )
        str_file_1 = os.path.join( str_dir_1, "file1.txt" )
        str_file_2_gz = os.path.join( str_dir_4, "file2.txt.gz" )
        str_file_2 = os.path.join( str_dir_4, "file2.txt" )
        str_file_2_ok = os.path.join( str_dir_4, ".file2.txt.ok" )
        str_file_3 = os.path.join( str_dir_4, "file3.txt" )
        str_file_3_gz = os.path.join( str_dir_4, "file3.txt.gz" )
        str_file_3_ok = os.path.join( str_dir_4, ".file3.txt.ok" )
        str_file_4 = os.path.join( str_dir_6, "file4.txt" )
        str_file_5 = os.path.join( str_dir_3, "file5.txt" )
        str_file_6_gz = os.path.join( str_dir_3, "file6.txt.gz" )
        str_file_6 = os.path.join( str_dir_3, "file6.txt" )
        str_file_6_ok = os.path.join( str_dir_3, ".file6.txt.ok" )
        str_file_7_gz = os.path.join( str_dir_3, "file7.txt.gz" )
        str_file_7 = os.path.join( str_dir_3, "file7.txt" )
        str_file_7_ok = os.path.join( str_dir_3, ".file7.txt.ok" )
        self.func_make_dummy_dir( str_env )

        # Call Example script
        str_compression = Pipeline.STR_COMPRESSION_AS_YOU_GO
        str_command = "python " + self.str_script + " --example test_app_for_run_with_compression_intermediary --out_dir "+ str_env +" --compress " + str_compression
        Commandline.Commandline().func_CMD( str_command )

        # Check test environment for results
        lstr_files_should_exist = [ str_file_1, str_file_2_gz, str_file_2_ok,
                                    str_file_3_gz, str_file_3_ok,
                                    str_file_4, str_file_5, str_file_6_gz, str_file_6_ok,
                                    str_file_7_gz, str_file_7_ok ]
        lstr_files_should_not_exist = [ str_file_2, str_file_3, str_file_6, str_file_7 ]
        f_success = sum( [ os.path.exists( str_path ) for str_path in lstr_files_should_exist ] ) == len( lstr_files_should_exist )
        f_success = f_success and sum( [ not os.path.exists( str_path ) for str_path in lstr_files_should_not_exist ] ) == len( lstr_files_should_not_exist )

        # Destroy environment
        self.func_remove_files( [ str_file_2_gz, str_file_3_gz, str_file_6_gz, str_file_7_gz ] )
        self.func_clean_up_example_script( str_env )
        self.func_remove_dirs( [ str_env ] )

        # Evaluate
        self.func_test_true( f_success )

    def test_app_for_run_with_archiving_move( self ):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a move.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_move" )
        str_env_move = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_move_2" )
        self.func_make_dummy_dirs( [ str_env, str_env_move ] )
        
        # Call Example script
        str_command = "python " + self.str_script + " --example test_app_for_run_with_archiving_move --out_dir "+ str_env + " --move " + str_env_move
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ not os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
                        
        dict_env = self.func_get_example_script_dirs_files( os.path.join( str_env_move, "test_app_for_run_with_archiving_move" ) )
        f_success = f_success and sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )

        # Destroy environment
        self.func_clean_up_example_script( os.path.join( str_env_move, "test_app_for_run_with_archiving_move" ) )
        self.func_remove_dirs( [ str_env, str_env_move ] )
        
        # Evaluate
        self.func_test_true( f_success )

    def test_app_for_run_with_archiving_copy( self ):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a copy to two locations.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy" )
        str_env_copy_2 = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_2" )
        str_env_copy_3 = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_3" )
        self.func_make_dummy_dirs( [ str_env, str_env_copy_2, str_env_copy_3 ] )
        
        # Call Example script
        str_command = " ".join( [ "python", self.str_script, "--example test_app_for_run_with_archiving_move --out_dir",
                            str_env,"--copy", str_env_copy_2, "--copy", str_env_copy_3 ] )
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
                        
        dict_env = self.func_get_example_script_dirs_files( os.path.join( str_env_copy_2, "test_app_for_run_with_archiving_copy" ) )
        f_success = f_success and sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
                        
        dict_env = self.func_get_example_script_dirs_files( os.path.join( str_env_copy_3, "test_app_for_run_with_archiving_copy" ) )
        f_success = f_success and sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )

        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_clean_up_example_script( os.path.join( str_env_copy_2, "test_app_for_run_with_archiving_copy" ) )
        self.func_clean_up_example_script( os.path.join( str_env_copy_3, "test_app_for_run_with_archiving_copy" ) )
        self.func_remove_dirs( [ str_env_copy_2, str_env_copy_3, str_env ] )
        
        # Evaluate
        self.func_test_true( f_success )

    def test_app_for_run_with_archiving_copy_move( self ):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a copy to one location.
        The output directory is then moved to another.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move" )
        str_env_move = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_move" )
        str_env_copy = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_copy" )
        self.func_make_dummy_dirs( [ str_env, str_env_move, str_env_copy ] )
        
        # Call Example script
        str_command = " ".join( ["python", self.str_script, "--example test_app_for_run_with_archiving_copy_move",
                                 "--out_dir", str_env, "--move", str_env_move, "--copy", str_env_copy ] )
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        dict_env = self.func_get_example_script_dirs_files( str_env )
        f_success = sum( [ not os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
                        
        dict_env = self.func_get_example_script_dirs_files( os.path.join( str_env_move, "test_app_for_run_with_archiving_copy_move" ) )
        f_success = f_success and sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )
                        
        dict_env = self.func_get_example_script_dirs_files( os.path.join( str_env_copy, "test_app_for_run_with_archiving_copy_move" ) )
        f_success = f_success and sum( [ os.path.exists( str_path ) 
                          for str_path in dict_env["files"] + dict_env["directories"] ] 
                        ) == len( dict_env["files"] + dict_env["directories"] )

        # Destroy environment
        self.func_clean_up_example_script( str_env )
        self.func_clean_up_example_script( os.path.join( str_env_move, "test_app_for_run_with_archiving_copy_move" ) )
        self.func_clean_up_example_script( os.path.join( str_env_copy, "test_app_for_run_with_archiving_copy_move" ) )
        self.func_remove_dirs( [ str_env, str_env_move, str_env_copy ] )
        
        # Evaluate
        self.func_test_true( f_success )
        
    def test_app_for_run_with_archiving_copy_move_compress( self ):
        """
        Test the scenario where the example script is ran with archiving of the output directory using a copy to one location.
        The output directory is then moved to another. The output directory in this case is compressed into one archive
        before moving.
        """

        # Create test environment
        str_env = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress" )
        str_env_move = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_move" )
        str_env_copy = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_copy" )
        str_env_archive = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress.tar.gz" )
        str_env_move_archive = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_move", "test_app_for_run_with_archiving_copy_move_compress.tar.gz" )
        str_env_copy_archive = os.path.join( self.str_test_directory, "test_app_for_run_with_archiving_copy_move_compress_copy", "test_app_for_run_with_archiving_copy_move_compress.tar.gz" )
        self.func_make_dummy_dirs( [ str_env, str_env_move, str_env_copy ] )
        
        # Call Example script
        str_command = " ".join( ["python", self.str_script, "--example test_app_for_run_with_archiving_copy_move",
                                 "--out_dir", str_env, "--move", str_env_move, "--copy", str_env_copy,
                                 "--compress", Pipeline.STR_COMPRESSION_ARCHIVE ] )
        Commandline.Commandline().func_CMD( str_command )
        
        # Check test environment for results
        f_success = not os.path.exists( str_env_archive )
        f_success = f_success and os.path.exists( str_env_move_archive )
        f_success = f_success and os.path.exists( str_env_copy_archive )

        # Destroy environment
        self.func_remove_files( [ str_env_move_archive, str_env_copy_archive ] )
        self.func_remove_dirs( [ str_env, str_env_move, str_env_copy ] )
        
        # Evaluate
        self.func_test_true( f_success )

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( FunctionalTester )
