
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import Command
import DependencyTree
import os
import Pipeline
import ParentPipelineTester
import Resource
import time
import unittest


class PipelineTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the Pipeline object
    """

# func_check_files_exist
    def test_func_check_files_exist_no_file( self ):
        """ Check if files exist for one no file """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_check_files_exist_no_file" )
        f_exists = cur_pipe.func_check_files_exist( [ ] )
        self.func_test_true( not f_exists )


    def test_func_check_files_exist_one_false_file( self ):
        """ Check if files exist for one non-existent file """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_check_files_exist_one_false_file" )
        f_exists = cur_pipe.func_check_files_exist( [ "nope_thisiflfjhfljhflkshfsdlkj" ] )
        self.func_test_true( not f_exists )
        

    def test_func_check_files_exist_five_false_file( self ):
        """ Check if files exist for five non-existent files """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_check_files_exist_five_false_file" )
        f_exists = cur_pipe.func_check_files_exist( [ "nope_thisiflfjhfljhflkshfsdlkjhghg",
                                                     "nope_thisiflfjhfljhflkshfsdlkjrtert",
                                                     "nope_thisiflfjhfljhflkshfsdlkjggdfg",
                                                     "nope_thisiflfjhfljhflkshfsdlkjsdsds",
                                                     "nope_thisiflfjhfljhflkshfsdlkjdsdfsd" ] )
        self.func_test_true( not f_exists )
        

    def test_func_check_files_exist_one_file( self ):
        """ Check if files exist for one file """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_check_files_exist_one_file" )
        str_env = os.path.join( self.str_test_directory, "test_func_check_files_exist_one_file" )
        str_file_1 = os.path.join( str_env, "test_func_check_files_exist_one_file_file_1.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        f_exists = cur_pipe.func_check_files_exist( [ str_file_1 ] )
        self.func_remove_files([ str_file_1 ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_exists )


    def test_func_check_files_exist_three_file( self ):
        """ Check if files exist for three files """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_check_files_exist_three_file" )
        str_env = os.path.join( self.str_test_directory, "test_func_check_files_exist_three_file" )
        str_file_1 = os.path.join( str_env, "test_func_check_files_exist_three_file_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_check_files_exist_three_file_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_check_files_exist_three_file_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( str_file_3 )
        f_exists = cur_pipe.func_check_files_exist( [ str_file_1, str_file_2, str_file_3 ] )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3 ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_exists )
        

    def test_func_check_files_exist_three_file_on_missing( self ):
        """ Check if files exist for three files when one is missing """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_check_files_exist_three_file_on_missing" )
        str_env = os.path.join( self.str_test_directory, "test_func_check_files_exist_three_file_on_missing" )
        str_file_1 = os.path.join( str_env, "test_func_check_files_exist_three_file_on_missing_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_check_files_exist_three_file_on_missing_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_check_files_exist_three_file_on_missing_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_3 )
        f_exists = cur_pipe.func_check_files_exist( [ str_file_1, str_file_2, str_file_3 ] )
        self.func_remove_files([ str_file_1, str_file_3 ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_exists )

# func_copy_move
    def test_func_copy_move_for_bad_case_move_two_files( self ):
        """ Run copy move for bad case. Too many destinations for move (more than one, here two destinations). """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_move_two_files" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_move_two_files" )
        lstr_destination = [ os.path.join( str_env, "destination1" ), os.path.join( str_env, "destination2" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path1 = os.path.join( os.path.join( str_env, "destination1", "archive_file.txt" ) )
        str_new_path2 = os.path.join( os.path.join( str_env, "destination2", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        self.func_remove_files( [ str_new_path1, str_new_path1 ] )
        f_copy = False
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path1 ) and not os.path.exists( str_new_path2 )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path1, str_new_path2 ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and not f_success )
        
    def test_func_copy_move_for_bad_case_move_to_file( self ):
        """ Run copy move for bad case. Move to a file not a directory. """
        
        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_move_to_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_move_to_file" )
        lstr_destination = [ os.path.join( str_env, "destination.txt" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( lstr_destination[0], "archive_file.txt" )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_files( [ str_archive ] + lstr_destination )
        self.func_remove_files( [ str_new_path ] )
        f_copy = False
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive ) and os.path.exists( lstr_destination[0] )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] + lstr_destination )
        self.func_remove_dirs( [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and not f_success )
        
    def test_func_copy_move_for_move_case_move_to_nonexistant_dir( self ):
        """ Run copy move for bad case. Move to a directory that does not exist. """
        
        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_move_case_move_to_nonexistant_dir" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_move_case_move_to_nonexistant_dir" )
        str_dest_dir = os.path.join( str_env, "destination" )
        lstr_destination = [ str_dest_dir ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_dest_dir, "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_file( str_archive )
        self.func_remove_dirs( [ str_dest_dir ] )
        self.func_remove_files( [ str_new_path ] )
        f_copy = False
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and not f_success )
        
    def test_func_copy_move_for_bad_case_copy_to_empty_destination( self ):
        """ Run copy move for bad case. Copy to an empty destination list. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_copy_to_empty_destination" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_copy_to_empty_destination" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        self.func_remove_files( [ str_new_path ] )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = [], str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_files_does_not_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_files_does_not_exist and not f_success )

    def test_func_copy_move_for_bad_case_copy_to_nonexistant_dir( self ):
        """ Run copy move for bad case. Copy to a directory that does not exist, with others that do. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_copy_to_nonexistant_dir" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_copy_to_nonexistant_dir" )
        str_destination_1 = os.path.join( str_env, "destination1" )
        str_destination_2 = os.path.join( str_env, "destination2" )
        str_destination_3 = os.path.join( str_env, "destination3" )
        lstr_destination = [ str_destination_1, str_destination_2 ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path_1 = os.path.join( os.path.join( str_env, "destination1", "archive_file.txt" ) )
        str_new_path_2 = os.path.join( os.path.join( str_env, "destination2", "archive_file.txt" ) )
        str_new_path_3 = os.path.join( os.path.join( str_env, "destination3", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        lstr_destination.append( str_destination_3 )
        self.func_remove_dirs( [ str_destination_3 ] )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_1 )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_2 )
        f_correct_files_do_not_exist = not os.path.exists( str_new_path_1 )
        f_correct_files_do_not_exist = f_correct_files_do_not_exist and not os.path.exists( str_new_path_2 )
        f_correct_files_do_not_exist = f_correct_files_do_not_exist and not os.path.exists( str_new_path_3 )
        f_correct_files_do_not_exist = f_correct_files_do_not_exist and not os.path.exists( str_destination_3 )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path_1, str_new_path_2, str_new_path_3 ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_files_do_not_exist and not f_success )

    def test_func_copy_move_for_bad_case_copy_to_file( self ):
        """ Run copy move for bad case. Copy to a directory that is a file, with others are not. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_copy_to_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_copy_to_file" )
        str_destination_1 = os.path.join( str_env, "destination1" )
        str_destination_2 = os.path.join( str_env, "destination2" )
        str_destination_3 = os.path.join( str_env, "destination3.txt" )
        lstr_destination = [ str_destination_1, str_destination_2, str_destination_3 ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path_1 = os.path.join( os.path.join( str_env, "destination1", "archive_file.txt" ) )
        str_new_path_2 = os.path.join( os.path.join( str_env, "destination2", "archive_file.txt" ) )
        str_new_path_3 = os.path.join( os.path.join( str_env, "destination3.txt", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env, str_destination_1, str_destination_2 ] )
        self.func_make_dummy_files( [ str_archive, str_destination_3 ] )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_1 )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_2 )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_3 )
        f_correct_files_do_not_exist = not os.path.exists( str_new_path_1 )
        f_correct_files_do_not_exist = f_correct_files_do_not_exist and not os.path.exists( str_new_path_2 )
        f_correct_files_do_not_exist = f_correct_files_do_not_exist and not os.path.exists( str_new_path_3 )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path_1, str_new_path_2, str_new_path_3, str_destination_3 ] )
        self.func_remove_dirs( [ str_destination_1, str_destination_2, str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_files_do_not_exist and not f_success )
        
    def test_func_copy_move_for_bad_case_copy_to_bad_file_name( self ):
        """ Run copy move for bad case. Copy to a directory that is a bad file name, with others that are not. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_copy_to_bad_file_name" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_copy_to_bad_file_name" )
        str_destination_1 = os.path.join( str_env, "destination1" )
        str_destination_2 = os.path.join( str_env, "destination2" )
        lstr_destination = [ str_destination_1, str_destination_2 ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path_1 = os.path.join( os.path.join( str_env, "destination1", "archive_file.txt" ) )
        str_new_path_2 = os.path.join( os.path.join( str_env, "destination2", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_files( [ str_archive ] )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination + [ None ], str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )

        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_1 )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_destination_2 )
        f_correct_files_do_not_exist = not os.path.exists( str_new_path_1 )
        f_correct_files_do_not_exist = f_correct_files_do_not_exist and not os.path.exists( str_new_path_2 )

        # Tear down
        self.func_remove_files( [ str_archive, str_new_path_1, str_new_path_2 ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_files_do_not_exist and not f_success )


    def test_func_copy_move_for_test_case_copy_one_file( self ):
        """ Run copy move for test case in copy mode for one file. During tests, files should not be moved. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_test_case_copy_one_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_test_case_copy_one_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = True
        f_test = True
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and f_success )

    def test_func_copy_move_for_bad_case_copy_none_destination_file( self ):
        """ Run copy move for bad case in copy mode for a none destination file. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_copy_none_destination_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_copy_none_destination_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = None, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and not f_success )

    def test_func_copy_move_for_test_case_move_one_file( self ):
        """ Run copy move for test case in move mode for one file. During tests the files should not be moved. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_test_case_move_one_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_test_case_move_one_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_files( [ str_archive ] )
        f_copy = False
        f_test = True
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and f_success )

    def test_func_copy_move_for_bad_case_move_none_destination_file( self ):
        """ Run copy move for bad case in move mode for none file. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_move_none_destination_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_move_none_destination_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = False
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = None, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and not f_success )
        
    def test_func_copy_move_for_bad_case_move_none_archive_file( self ):
        """ Run copy move for bad case in move mode for none archive file. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_bad_case_move_none_archive_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_bad_case_move_none_archive_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = False
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = None,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_does_not_files_exist = not os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_does_not_files_exist and not f_success )

    def test_func_copy_move_for_good_case_copy_one_file( self ):
        """ Run copy move for good case in copy mode for one file. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_good_case_copy_one_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_good_case_copy_one_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_success )
        
    def test_func_copy_move_for_good_case_copy_one_file_twice( self ):
        """ Run copy move for good case in copy mode for one file copied twice. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_good_case_copy_one_file_twice" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_good_case_copy_one_file_twice" )
        lstr_destination = [ os.path.join( str_env, "destination1" ),
                            os.path.join( str_env, "destination2" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path_1 = os.path.join( os.path.join( str_env, "destination1", "archive_file.txt" ) )
        str_new_path_2 = os.path.join( os.path.join( str_env, "destination2", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = True
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_exist = os.path.exists( str_archive )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_new_path_1 )
        f_correct_files_exist = f_correct_files_exist and os.path.exists( str_new_path_2 )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path_1, str_new_path_2 ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_success )
        
    def test_func_copy_move_for_good_case_move_one_file( self ):
        """ Run copy move for good case in move mode for one file. """

        # Set up
        str_env = os.path.join( self.str_test_directory, "test_func_copy_move_for_good_case_move_one_file" )
        cur_pipeline = Pipeline.Pipeline( "test_func_copy_move_for_good_case_move_one_file" )
        lstr_destination = [ os.path.join( str_env, "destination" ) ]
        str_archive = os.path.join( str_env, "archive_file.txt" )
        str_new_path = os.path.join( os.path.join( str_env, "destination", "archive_file.txt" ) )
        self.func_make_dummy_dirs( [ str_env ] + lstr_destination )
        self.func_make_dummy_file( str_archive )
        f_copy = False
        f_test = False
        
        # Run test
        f_success = cur_pipeline.func_copy_move( lstr_destination = lstr_destination, str_archive = str_archive,
                                                 f_copy = f_copy, f_test = f_test )
        
        # Evaluate
        f_correct_files_does_not_exist = not os.path.exists( str_archive )
        f_correct_files_exist = os.path.exists( str_new_path )
        
        # Tear down
        self.func_remove_files( [ str_archive, str_new_path ] )
        self.func_remove_dirs( lstr_destination + [ str_env ] )
        
        # Evaluate
        self.func_test_true( f_correct_files_exist and f_correct_files_does_not_exist and f_success )

# func_paths_are_from_valid_run
    def test_func_paths_are_from_valid_run_invalid_command_1( self ):
        """ Test for an invalid command, None """
        
        cmd_cur = None
        self.func_test_true( not Pipeline.Pipeline("test_func_paths_are_from_valid_run_invalid_command_1").func_paths_are_from_valid_run( cmd_cur, f_dependencies = True ))
 
 
#    def test_func_paths_are_from_valid_run_invalid_command_2( self ):
#        """ Test for an invalid command, Invalid command object"""
#        
#        cmd_cur = Command.Command( None, None, None )
#        self.func_test_true( not Pipeline.Pipeline("test_func_paths_are_from_valid_run_invalid_command_2").func_paths_are_from_valid_run( cmd_cur, f_dependencies = True ))


    def test_func_paths_are_from_valid_run_good_case_one_dependency( self ):
        """ Test for an invalid command, Good case testing the handling of one dependency in the command."""

        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_good_case_one_dependency" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_good_case_one_dependency" )
        str_dependency = os.path.join( str_env, "dependency_1.txt")
        str_dependency_ok = cur_pipeline.func_get_ok_file_path( str_dependency )
        str_product = os.path.join( str_env, "product_1.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency )
        self.func_make_dummy_file( str_dependency_ok )
        self.func_make_dummy_file( str_product )
        cmd_cur = Command.Command("command", [ str_dependency ], [ str_product ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = True )
        self.func_remove_files( [ str_dependency, str_dependency_ok, str_product ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_result )

    
    def test_func_paths_are_from_valid_run_good_case_one_dependency_dir( self ):
        """ Test for an invalid command, Good case testing the handling of one dependency, which is a directory in the command."""

        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_good_case_one_dependency_dir" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_good_case_one_dependency_dir" )
        str_dependency = os.path.join( str_env, "dependency_1")
        str_dependency_ok = cur_pipeline.func_get_ok_file_path( str_dependency )
        str_product = os.path.join( str_env, "product_1.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency )
        self.func_make_dummy_file( str_dependency_ok )
        self.func_make_dummy_file( str_product )
        cmd_cur = Command.Command("command", [ str_dependency ], [ str_product ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = True )
        self.func_remove_files( [ str_product, str_dependency, str_dependency_ok ] )
        self.func_test_true( f_result )
    

    def test_func_paths_are_from_valid_run_good_case_3_dependencies( self ):
        """ Test for an invalid command, Good case testing the handling of three dependencies in the command."""

        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_good_case_3_dependencies" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_good_case_3_dependencies" )
        str_dependency = os.path.join( str_env, "dependency_1")
        str_dependency_ok = cur_pipeline.func_get_ok_file_path( str_dependency )
        str_dependency_2 = os.path.join( str_env, "dependency_2.txt" )
        str_dependency_2_ok = cur_pipeline.func_get_ok_file_path( str_dependency_2 )
        str_dependency_3 = os.path.join( str_env, "dependency_3.txt" )
        str_dependency_3_ok = cur_pipeline.func_get_ok_file_path( str_dependency_3 )
        str_product = os.path.join( str_env, "product_1.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency )
        self.func_make_dummy_file( str_dependency_ok )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_dependency_2_ok )
        self.func_make_dummy_file( str_dependency_3 )
        self.func_make_dummy_file( str_dependency_3_ok )
        self.func_make_dummy_file( str_product )
        cmd_cur = Command.Command("command", [ str_dependency, str_dependency_2, str_dependency_3 ], [ str_product ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = True )
        self.func_remove_files( [ str_dependency, str_dependency_ok, str_dependency_2, str_dependency_2_ok, 
                                 str_dependency_3, str_dependency_3_ok, str_product ] )
        self.func_test_true( f_result )

    def test_func_paths_are_from_valid_run_not_ran_dependency_for_products( self ):
        """ Test for an invalid command, catch that a parent dependency has not been made for a product."""
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_not_ran_dependency_for_product" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_not_ran_dependency_for_product" )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        cmd_cur = Command.Command("command", [ str_dependency_1 ], [ str_product_1 ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = False )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_result )

    def test_func_paths_are_from_valid_run_young_dependency_for_products( self ):
        """ Test for an invalid command, catch that a parent dependency is younger than the product."""
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_young_dependency_for_products" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_young_dependency_for_products" )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_dependency_1_ok = cur_pipeline.func_get_ok_file_path( str_dependency_1 )
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        # Wait for 1 seconds
        time.sleep(1)
        self.func_make_dummy_file( str_dependency_1_ok )
        cmd_cur = Command.Command("command", [ str_dependency_1 ], [ str_product_1 ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = False, i_fuzzy_time = 0 )
        self.func_remove_files( [ str_dependency_1, str_dependency_1_ok, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_result )

    def test_func_paths_are_from_valid_run_young_dependency_for_products_to_short_fuzzy( self ):
        """ 
            Test for an invalid command, catch that a parent dependency is younger than the product 
            and a fuzzy time not long enough to validate parent.
        """
        i_wait = 3
        i_fuzzy = 1
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_young_dependency_for_products_to_short_fuzzy" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_young_dependency_for_products_to_short_fuzzy" )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_dependency_1_ok = cur_pipeline.func_get_ok_file_path( str_dependency_1 )
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        time.sleep(i_wait)
        self.func_make_dummy_file( str_dependency_1_ok )
        cmd_cur = Command.Command("command", [ str_dependency_1 ], [ str_product_1 ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = False, i_fuzzy_time = i_fuzzy )
        self.func_remove_files( [ str_dependency_1, str_dependency_1_ok, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_result )

    def test_func_paths_are_from_valid_run_young_dependency_for_products_to_enough_fuzzy( self ):
        """ 
            Test for an invalid command, catch that a parent dependency is younger than the product 
            and a fuzzy time long enough to validate parent.
        """
        i_wait = 2
        i_fuzzy = 4
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_young_dependency_for_products_to_enough_fuzzy" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_young_dependency_for_products_to_enough_fuzzy" )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_dependency_1_ok = cur_pipeline.func_get_ok_file_path( str_dependency_1 )
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        time.sleep(i_wait)
        self.func_make_dummy_file( str_dependency_1_ok )
        cmd_cur = Command.Command("command", [ str_dependency_1 ], [ str_product_1 ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = False, i_fuzzy_time = i_fuzzy )
        self.func_remove_files( [ str_dependency_1, str_dependency_1_ok, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_result )

    def test_func_paths_are_from_valid_run_young_mult_dependency_for_products_to_short_fuzzy( self ):
        """ 
            Test for an invalid command, catch that a parent dependency is younger than the product 
            and a fuzzy time not long enough to validate parent, multiple parent scenario.
        """
        i_wait = 3
        i_fuzzy = 1
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_young_mult_dependency_for_products_to_short_fuzzy" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_young_mult_dependency_for_products_to_short_fuzzy" )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_dependency_2 = os.path.join( str_env, "dependency_2.txt")
        str_dependency_1_ok = cur_pipeline.func_get_ok_file_path( str_dependency_1 )
        str_dependency_2_ok = cur_pipeline.func_get_ok_file_path( str_dependency_2 )
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_dependency_2_ok )
        self.func_make_dummy_file( str_product_1 )
        time.sleep(i_wait)
        self.func_make_dummy_file( str_dependency_1_ok )
        cmd_cur = Command.Command("command", [ str_dependency_1, str_dependency_2 ], [ str_product_1 ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = False, i_fuzzy_time = i_fuzzy )
        self.func_remove_files( [ str_dependency_1, str_dependency_1_ok, 
                                  str_dependency_2, str_dependency_2_ok,
                                  str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_result )

    def test_func_paths_are_from_valid_run_young_mult_dependency_for_products_to_enough_fuzzy( self ):
        """ 
            Test for an invalid command, catch that a parent dependency is younger than the product 
            and a fuzzy time long enough to validate parent, multiple parent scenario.
        """
        i_wait = 1
        i_fuzzy = 3
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_young_mult_dependency_for_products_to_enough_fuzzy" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_young_mult_dependency_for_products_to_enough_fuzzy" )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_dependency_2 = os.path.join( str_env, "dependency_2.txt")
        str_dependency_1_ok = cur_pipeline.func_get_ok_file_path( str_dependency_1 )
        str_dependency_2_ok = cur_pipeline.func_get_ok_file_path( str_dependency_2 )
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_dependency_2_ok )
        self.func_make_dummy_file( str_product_1 )
        time.sleep(i_wait)
        self.func_make_dummy_file( str_dependency_1_ok )
        cmd_cur = Command.Command("command", [ str_dependency_1, str_dependency_2 ], [ str_product_1 ])
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_cur, f_dependencies = False, i_fuzzy_time = i_fuzzy )
        self.func_remove_files( [ str_dependency_1, str_dependency_1_ok, 
                                  str_dependency_2, str_dependency_2_ok,
                                  str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_result )

    def test_func_paths_are_from_valid_run_not_ran_dependency_for_dependencies( self ):
        """ Test for an invalid command, catch that a parent dependency has not been made for a command dependency."""
        str_env = os.path.join( self.str_test_directory, "test_func_paths_are_from_valid_run_not_ran_dependency_for_dependencies" )
        cur_pipeline = Pipeline.Pipeline( "test_func_paths_are_from_valid_run_not_ran_dependency_for_dependencies" )
        str_dep_dep_1 = os.path.join( str_env, "dep_dep_1.txt")
        str_dep_dep_2 = os.path.join( str_env, "dep_dep_2.txt")
        str_dep_dep_2_ok = cur_pipeline.func_get_ok_file_path( str_dep_dep_2 )
        str_dependency_1 = os.path.join( str_env, "dependency_1.txt")
        str_dependency_1_ok = cur_pipeline.func_get_ok_file_path( str_dependency_1 )
        str_product_1 = os.path.join( str_env, "product_1.txt" )
        str_product_1_ok = cur_pipeline.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dep_dep_1 )
        self.func_make_dummy_file( str_dep_dep_2 )
        self.func_make_dummy_file( str_dep_dep_2_ok )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_1_ok )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        cmd_cur = Command.Command("command1", [ str_dependency_1 ], [ str_product_1 ])
        cmd_cur2 = Command.Command("command2", [ str_dep_dep_1, str_dep_dep_2 ], [ str_dependency_1 ])
        dt_tree = DependencyTree.DependencyTree( [ cmd_cur2, cmd_cur ] )
        cmd_check = dt_tree.graph_commands.func_get_vertex( "command2" )
        f_result = cur_pipeline.func_paths_are_from_valid_run( cmd_check, f_dependencies = True )
        self.func_remove_files( [ str_dep_dep_1, str_dep_dep_2, str_dep_dep_2_ok,
                                  str_dependency_1, str_dependency_1_ok, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_result )

# func_do_bsub
    def test_func_do_bsub_true( self ):
        """ Test to turn on bsubing commands """
        
        i_memory = 10
        str_queue = "testing_queue"
        str_answer_prefix = "".join( [ "bsub -N -q ", str_queue, " -K -R \"rusage[mem=", str( i_memory ), "]\" " ] )
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_bsub_true" )
        cur_pipe.func_do_bsub( str( i_memory ), str_queue )
        self.func_test_equals( str_answer_prefix, cur_pipe.str_prefix_command )
        
    def test_func_do_bsub_false( self ):
        """ Test do not turn on bsubing commands """

        str_answer_prefix = ""
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_bsub_false" )
        self.func_test_equals( str_answer_prefix, cur_pipe.str_prefix_command )


# func_do_special_command
    def test_func_do_special_command_for_good_case_rm( self ):
        """ RM should be handled with a false """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_special_command_for_good_case_rm" )
        cmd_cur = Command.Command( "rm hello", [ "Hello" ], [ "goodbye" ] )
        self.func_test_true( cur_pipe.func_do_special_command( cmd_cur ) )


    def test_func_do_special_command_for_good_case_mkdir( self ):
        """ MKDIR should be handled with a false """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_special_command_for_good_case_mkdir" )
        cmd_cur = Command.Command( "mkdir hello", [ "Hello" ], [ "goodbye" ] )
        self.func_test_true( cur_pipe.func_do_special_command( cmd_cur ) )


    def test_func_do_special_command_for_good_case_cd( self ):
        """ CD should be handled with moving to the dir and true """
        
        str_env = os.path.join( self.str_test_directory, "test_func_do_special_command_for_good_case_cd" )
        str_current_location = os.getcwd()
        self.func_make_dummy_dir( str_env )
        os.chdir( str_env )
        self.func_make_dummy_dir( os.path.join( str_env, "hello" ) )
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_special_command_for_good_case_cd" )
        cmd_cur = Command.Command( "cd hello", [ "Hello" ], [ "goodbye" ] )
        f_return = cur_pipe.func_do_special_command( cmd_cur )
        f_moved = os.path.abspath( os.getcwd() ) == os.path.abspath( os.path.join( str_env, "hello" ) )
        self.func_remove_dirs([ os.path.join( str_env, "hello" ), str_env ])
        os.chdir( str_current_location )
        self.func_test_true( f_moved and f_return )
        
        
    def test_func_do_special_command_for_bad_case_cd( self ):
        """ If CDing to a dir that does not exist, return false """
        
        str_env = os.path.join( self.str_test_directory, "test_func_do_special_command_for_bad_case_cd" )
        str_current_location = os.getcwd()
        self.func_make_dummy_dir( str_env )
        os.chdir( str_env )
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_special_command_for_bad_case_cd" )
        cmd_cur = Command.Command( "cd hello", [ "Hello" ], [ "goodbye" ] )
        f_return = cur_pipe.func_do_special_command( cmd_cur )
        self.func_remove_dirs([ str_env ])
        os.chdir( str_current_location )
        self.func_test_true( not f_return )
        

    def test_func_do_special_command_for_bad_case_random( self ):
        """ A random command that is not identified as special should be handled with a false """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_do_special_command_for_bad_case_random" )
        cmd_cur = Command.Command( "random hello", [ "Hello" ], [ "goodbye" ] )
        self.func_test_true( not cur_pipe.func_do_special_command( cmd_cur ) )


# func_get_ok_file_path
    def test_get_ok_file_for_empty_string( self ):
        """ Test for empty string """
        
        str_answer = ".ok"
        str_file = ""
        str_result = Pipeline.Pipeline( str_name = "test_get_ok_file_for_empty_string" ).func_get_ok_file_path( str_file )
        self.func_test_equals(str_answer, str_result)
        
        
    def test_get_ok_file_for_null_string( self ):
        """ Test for null string """
        
        str_answer = ".ok"
        str_file = None
        str_result = Pipeline.Pipeline( str_name = "test_get_ok_file_for_empty_string" ).func_get_ok_file_path( str_file )
        self.func_test_equals(str_answer, str_result)
        
        
    def test_get_ok_file_for_a_directory( self ):
        """ Test for a directory"""

        str_env = os.path.join( self.str_test_directory, "test_get_ok_file_for_a_directory" )
        str_file = str_env + os.path.sep
        str_answer = os.path.join( self.str_test_directory, "test_get_ok_file_for_a_directory",".ok" )
        str_result = Pipeline.Pipeline( str_name = "test_get_ok_file_for_empty_string" ).func_get_ok_file_path( str_file )
        self.func_test_equals(str_answer, str_result)
        
    
    def test_get_ok_file_for_a_file( self ):
        """ Test for a file """

        str_env = os.path.join( self.str_test_directory, "test_get_ok_file_for_a_file" )
        str_file = os.path.join( str_env, "test_get_ok_file_for_a_file" )
        str_answer = os.path.join( str_env, ".test_get_ok_file_for_a_file.ok" )
        str_result = Pipeline.Pipeline( str_name = "test_get_ok_file_for_empty_string" ).func_get_ok_file_path( str_file )
        self.func_test_equals(str_answer, str_result)


# func_handle_gzip
    def test_func_handle_gzip_for_bad_case_empty_list( self ):
        """ Testing being given a bad case, empty list. """
        
        lstr_input = []
        lstr_answer = []
        lstr_result = Pipeline.Pipeline().func_handle_gzip( lstr_input )
        self.func_test_equals(lstr_answer, lstr_result)
        
        
    def test_func_handle_gzip_for_bad_case_string( self ):
        """ Testing being given a bad case, empty list. """
        
        lstr_input = "testing.gz"
        lstr_answer = "['<( zcat testing.gz )']"
        lstr_result = Pipeline.Pipeline().func_handle_gzip( lstr_input )
        self.func_test_equals(lstr_answer, lstr_result)
        
        
    def test_func_handle_gzip_for_bad_case_string2( self ):
        """ Testing being given a bad case, empty list. """
        
        lstr_input = "testing"
        lstr_answer = "['testing']"
        lstr_result = Pipeline.Pipeline().func_handle_gzip( lstr_input )
        self.func_test_equals(lstr_answer, lstr_result)


    def test_func_handle_gzip_for_good_case_mixed( self ):
        """ Testing being given a good case, a collection of gzed and not files. """
        
        lstr_input = ["file1.fa","file2.fa.gz","file3.fa","file4.fa.gz","file5.fa.gz","file6.fa"]
        lstr_answer = ["file1.fa","<( zcat file2.fa.gz )","file3.fa","<( zcat file4.fa.gz )","<( zcat file5.fa.gz )","file6.fa"]
        lstr_result = Pipeline.Pipeline().func_handle_gzip( lstr_input )
        self.func_test_equals( sorted( lstr_answer ), sorted( lstr_result ) )


# func_is_special_command
    def test_func_is_special_command_true_cd( self ):
        """ Test if a command is handled in a special way for true ( cd )"""
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_is_special_command_true_cd" )
        cur_cmd = Command.Command( "cd", [], [] )
        self.func_test_true( cur_pipe.func_is_special_command( cur_cmd ) )
        
        
    def test_func_is_special_command_true_cd_2( self ):
        """ Test if a command is handled in a special way for true ( CD ).
        This is just verifying capitalization is not affecting the functions."""
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_is_special_command_true_cd_2" )
        cur_cmd = Command.Command( "CD", [], [] )
        self.func_test_true( cur_pipe.func_is_special_command( cur_cmd ) )
        
        
    def test_func_is_special_command_true_rm( self ):
        """ Test if a command is handled in a special way for true ( rm )"""
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_is_special_command_true_rm" )
        cur_cmd = Command.Command( "rm", [], [] )
        self.func_test_true( cur_pipe.func_is_special_command( cur_cmd ) )


    def test_func_is_special_command_true_mkdir( self ):
        """ Test if a command is handled in a special way for true ( mkdir )"""
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_is_special_command_true_mkdir" )
        cur_cmd = Command.Command( "mkdir", [], [] )
        self.func_test_true( cur_pipe.func_is_special_command( cur_cmd ) )
        

    def test_func_is_special_command_false( self ):
        """ Test if a command is handled in a special way for false """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_is_special_command_false" )
        cur_cmd = Command.Command( cur_pipe.c_lstr_special_commands[ 0 ] + "nope", [], [] )
        self.func_test_true( not cur_pipe.func_is_special_command( cur_cmd ) )


# func_is_valid_path_for_removal
    def test_func_is_valid_path_for_removal_good_case( self ):
        """ Test is a path is found to be valid. Relative paths """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_good_case" )
        str_file_path = os.path.join( str_env, "test" )
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_good_case" )
        self.func_test_true( cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        

    def test_func_is_valid_path_for_removal_good_case_2( self ):
        """ Test is a path is found to be valid. Both file and dir are the same."""

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_good_case_2" )
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_good_case_2" )
        self.func_test_true( cur_pipe.func_is_valid_path_for_removal( str_path = str_env,
                                                                      str_output_directory = str_env ) )
        
        
    def test_func_is_valid_path_for_removal_good_case_3( self ):
        """ Test is a path is found to be valid. Absolute paths """

        str_env = os.path.sep+os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_good_case_3" )
        str_file_path = os.path.join( str_env, "test" )
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_good_case_3" )
        self.func_test_true( cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_file_not_in_dir( self ):
        """ Test is a path is found to be invalid. Switched the file and dir of two cases that were working. """

        str_env = os.path.sep+os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_file_not_in_dir" )
        str_output_path = os.path.join( str_env, "test" )
        str_file_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_file_not_in_dir" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )


    def test_func_is_valid_path_for_removal_bad_case_file_path_ends_with_dir( self ):
        """ Test is a path is found to be invalid. Put the output directory in the end of the file path not the beginning """

        str_env = os.path.join( self.str_test_directory, "hello", "func_is_valid_path_for_removal_bad_case_file_path_ends_with_dir" )
        str_output_path = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_file_path_ends_with_dir" )
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_file_path_ends_with_dir" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_env,
                                                                      str_output_directory = str_output_path ) )


    def test_func_is_valid_path_for_removal_bad_case_none_1( self ):
        """ Test is a path is found to be invalid. Case: File= None, Dir= None """

        str_file_path = None
        str_output_path = None
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_none_1" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_none_2( self ):
        """ Test is a path is found to be invalid. Case: File= '', Dir= None """

        str_file_path = ""
        str_output_path = None
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_none_2" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )


    def test_func_is_valid_path_for_removal_bad_case_none_3( self ):
        """ Test is a path is found to be invalid. Case: File= None, Dir= '' """

        str_file_path = None
        str_output_path = ""
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_none_3" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )


    def test_func_is_valid_path_for_removal_bad_case_none_4( self ):
        """ Test is a path is found to be invalid. Case: File= '', Dir= '' """

        str_file_path = ""
        str_output_path = ""
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_none_4" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )

    def test_func_is_valid_path_for_removal_bad_case_not_in_dir_1( self ):
        """ Test is a path is found to be invalid. Case: File not in dir """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_not_in_dir_1" )
        str_file_path = ""
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_not_in_dir_1" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_not_in_dir_2( self ):
        """ Test is a path is found to be invalid. Case: File not in dir """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_not_in_dir_2" )
        str_file_path = "test"
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_not_in_dir_2" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )    


    def test_func_is_valid_path_for_removal_bad_case_not_in_dir_3( self ):
        """ Test is a path is found to be invalid. Case: File not in dir """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_not_in_dir_3" )
        str_file_path = os.path.sep+"test"
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_not_in_dir_3" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )    


    def test_func_is_valid_path_for_removal_bad_case_not_in_dir_4( self ):
        """ Test is a path is found to be invalid. Case: File not in dir """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_not_in_dir_4" )
        str_file_path = os.path.join( str_env, "test", "..", ".." )
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_not_in_dir_4" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_one_relative_1( self ):
        """ Test is a path is found to be invalid. Case: One file relative """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_one_relative_1" )
        str_file_path = os.path.sep+os.path.join( str_env, "test", "..", ".." )
        str_output_path = str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_one_relative_1" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_one_relative_2( self ):
        """ Test is a path is found to be invalid. Case: One dir relative """

        str_env = os.path.join( self.str_test_directory, "func_is_valid_path_for_removal_bad_case_one_relative_2" )
        str_file_path = os.path.join( str_env, "test", "..", ".." )
        str_output_path = os.path.sep+str_env
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_one_relative_2" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_not_allowed_dir_1( self ):
        """ Test is a path is found to be invalid. Case: The directory in use is not allowed. File matches dir."""

        str_file_path = os.path.sep
        str_output_path = os.path.sep
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_not_allowed_dir_1" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) )
        
        
    def test_func_is_valid_path_for_removal_bad_case_not_allowed_dir_2( self ):
        """ Test is a path is found to be invalid. Case: The directory in use is not allowed. File in dir."""

        str_file_path = os.path.sep
        str_output_path = os.path.sep+"test.txt"
        cur_pipe = Pipeline.Pipeline( str_name = "func_is_valid_path_for_removal_bad_case_not_allowed_dir_2" )
        self.func_test_true( not cur_pipe.func_is_valid_path_for_removal( str_path = str_file_path,
                                                                      str_output_directory = str_output_path ) ) 


# func_make_all_needed_dirs
    def test_func_make_all_needed_dirs_for_none( self ):
        """
        Test for the case of a none list.
        """
        str_test_dir = "test_func_make_all_needed_dirs_for_none"
        lstr_paths = None
        pipe_cur = Pipeline.Pipeline( str_name = str_test_dir )
        pipe_cur.func_make_all_needed_dirs( lstr_paths )
        self.func_test_true( True )

    def test_func_make_all_needed_dirs_for_list_none( self ):
        """
        Test for the case of a list of none.
        """
        str_test_dir = "test_func_make_all_needed_dirs_for_list_none"
        lstr_paths = [ None, None ]
        pipe_cur = Pipeline.Pipeline( str_name = str_test_dir )
        pipe_cur.func_make_all_needed_dirs( lstr_paths )
        self.func_test_true( True )

    def test_func_make_all_needed_dirs_for_good_case( self ):
        """
        Test for the case of a good list.
        """
        str_test_dir = "test_func_make_all_needed_dirs_for_good_case"
        str_file_1 = os.path.join( str_test_dir, "file.1" )
        str_file_2 = os.path.join( str_test_dir, str_test_dir, "file.2" )
        lstr_paths = [ str_file_1, str_file_2 ]
        pipe_cur = Pipeline.Pipeline( str_name = str_test_dir )
        pipe_cur.func_make_all_needed_dirs( lstr_paths )
        f_success = os.path.exists( str_test_dir ) and os.path.isdir( str_test_dir )
        f_success = os.path.exists( os.path.dirname( str_file_2) ) and os.path.isdir( os.path.dirname( str_file_2 )) and f_success
        self.func_remove_files( [ str_file_1, str_file_2 ] )
        self.func_remove_dirs( [ os.path.dirname( str_file_2 ) ] )
        self.func_remove_dirs( [ os.path.dirname( str_file_1 ) ] )
        self.func_test_true( f_success )

# func_mkdirs
    def test_func_mkdirs_for_terminal_dir( self ):
        """
        Test the case of a simple terminal directory creation.
        """
        
        # Set up environment
        str_test_dir = "test_func_mkdirs_for_terminal_dir"
        self.func_remove_dirs( [ str_test_dir ])
        
        # Send command and get result
        pipe_cur = Pipeline.Pipeline( str_name = "test_func_mkdirs_for_terminal_dir" )
        pipe_cur.func_mkdirs( [ str_test_dir ] )
        
        # Get confirmation that file was written correctly
        f_success = os.path.exists( str_test_dir )
        # Destroy environment
        self.func_remove_dirs( [ str_test_dir ] )
        
        self.func_test_true( f_success )
        
        
    def test_func_mkdirs_for_mult_dir( self ):
        """
        Test the case of a multiple terminal directory creation.
        """
        
        # Set up environment
        str_test_dir_1 = "test_func_mkdirs_for_terminal_dir_1"
        str_test_dir_2 = "test_func_mkdirs_for_terminal_dir_2"
        self.func_remove_dirs( [ str_test_dir_1, str_test_dir_2 ])
        
        # Send command and get result
        pipe_cur = Pipeline.Pipeline( str_name = "test_func_mkdirs_for_mult_dir" )
        pipe_cur.func_mkdirs( [ str_test_dir_1, str_test_dir_2 ] )
        
        # Get confirmation that file was written correctly
        f_success = os.path.exists( str_test_dir_1 ) and os.path.exists( str_test_dir_2 )
        # Destroy environment
        self.func_remove_dirs( [ str_test_dir_1, str_test_dir_2 ] )
        
        self.func_test_true( f_success )
        
        
    def test_func_mkdirs_for_dir_with_parent( self ):
        """
        Test the case of a directory creation of a directory with parents.
        """
        
        # Set up environment
        str_test_dir = os.path.join( "testtesttest","tested","test_func_mkdirs_for_dir_with_parent" )
        self.func_remove_dirs( [ str_test_dir ])
        
        # Send command and get result
        pipe_cur = Pipeline.Pipeline( str_name = "test_func_mkdirs_for_dir_with_parent" )
        pipe_cur.func_mkdirs( [ str_test_dir ] )
        
        # Get confirmation that file was written correctly
        f_success = os.path.exists( str_test_dir )
        # Destroy environment
        self.func_remove_dirs( [ str_test_dir ] )
        
        self.func_test_true( f_success )


# func_remove_paths
#    def test_func_remove_paths_for_bad_case_invalid_command( self ):
#        """ Bad case trying to remove one product, invalid command. """
#        
#        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_invalid_command" )
#        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_invalid_command" )
#        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
#        str_product_1 = os.path.join( str_env, "Product_1.txt" )
#        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
#        self.func_make_dummy_dir( str_env )
#        self.func_make_dummy_file( str_dependency_1 )
#        self.func_make_dummy_file( str_product_1 )
#        self.func_make_dummy_file( str_product_1_ok )
#        cur_cmd = Command.Command( None, None, None )
#        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
#                                                dt_dependency_tree = DependencyTree.DependencyTree(),
#                                                f_remove_products = True )
#        f_not_removed_files = os.path.exists( str_product_1 )
#        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_1_ok )
#        f_other_files_remain = os.path.exists( str_dependency_1 )
#        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
#        self.func_remove_dirs( [ str_env ] )
#        self.func_test_true( not f_success and f_not_removed_files and f_other_files_remain )
        
        
    def test_func_remove_paths_for_bad_case_none_command( self ):
        """ Bad case trying to remove one product, none command. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_none_command" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_none_command" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        cur_cmd = None
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_not_removed_files = os.path.exists( str_product_1 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_1_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_success and f_not_removed_files and f_other_files_remain )


    def test_func_remove_paths_for_bad_case_one_product_bad_output_directory( self ):
        """
        Bad case trying to remove one product, bad output directory (root).
        !!!! Always run this test in test mode.
        """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_one_product_bad_output_directory" )
        cur_pipe.func_test_mode() # Do not remove
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_one_product_bad_output_directory" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = os.path.sep,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_not_removed_files = os.path.exists( str_product_1 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_1_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_success and f_not_removed_files and f_other_files_remain )
        
        
    def test_func_remove_paths_for_bad_case_one_product_bad_dt( self ):
        """ Bad case trying to remove one product, bad dependency tree. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_one_product_bad_dt" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_one_product_bad_dt" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = None,
                                                f_remove_products = True )
        f_not_removed_files = os.path.exists( str_product_1 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_1_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_success and f_not_removed_files and f_other_files_remain )

    
    def test_func_remove_paths_for_good_case_one_product( self ):
        """ Good case trying to remove one product. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_one_product" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_one_product" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_removed_files = not os.path.exists( str_product_1 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_1_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )
        
    
    def test_func_remove_paths_for_good_case_one_dependency_NEVER( self ):
        """ Good case trying to remove one dependency at clean level NEVER, should not be cleaned. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_one_dependency_NEVER" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_one_dependency_NEVER" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_files( [ str_dependency_1, str_product_1, str_product_1_ok, 
                                     str_product_2, str_product_2_ok ] )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] ).func_set_resource_clean_level([ str_dependency_1, str_product_1 ] , Resource.CLEAN_NEVER)
        cur_cmd2 = Command.Command( "Command 2", [ str_product_1 ], [ str_product_2 ] ).func_set_resource_clean_level([ str_product_1, str_product_2 ] , Resource.CLEAN_NEVER)
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd2 ] )
        dt_cur.func_complete_command( cur_cmd )
        dt_cur.func_complete_command( cur_cmd2 )

        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd2, str_output_directory = str_env,
                                                dt_dependency_tree = dt_cur,
                                                f_remove_products = False )
        f_removed_files = os.path.exists( str_product_1 )
        f_removed_files = f_removed_files and os.path.exists( str_product_1_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_product_2 )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_product_2_ok )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok, str_product_2, str_product_2_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )
        

    def test_func_remove_paths_for_good_case_one_dependency_ASTEMP( self ):
        """ Good case trying to remove one dependency at clean level ASTEMP, only used intermediary files should be deleted. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_one_dependency_ASTEMP" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_one_dependency_ASTEMP" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_files( [ str_dependency_1, str_product_1, str_product_1_ok, 
                                     str_product_2, str_product_2_ok ] )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] ).func_set_resource_clean_level([ str_dependency_1, str_product_1 ] , Resource.CLEAN_AS_TEMP)
        cur_cmd2 = Command.Command( "Command 2", [ str_product_1 ], [ str_product_2 ] ).func_set_resource_clean_level([ str_product_1, str_product_2 ] , Resource.CLEAN_AS_TEMP)
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd2 ] )
        dt_cur.func_complete_command( cur_cmd )
        dt_cur.func_complete_command( cur_cmd2 )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd2, str_output_directory = str_env,
                                                dt_dependency_tree = dt_cur,
                                                f_remove_products = False )
        f_removed_files = not os.path.exists( str_product_1 )
        f_other_files_remain = f_removed_files and os.path.exists( str_product_1_ok )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_dependency_1 )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_product_2 )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_product_2_ok )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok, str_product_2, str_product_2_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )


    def test_func_remove_paths_for_good_case_ALWAYS_never_delete_input_file( self ):
        """ 
        Good case trying to remove one dependency at clean level ALWAYS, any always file is always deleted. 
        Here the input file and intermediate file is requested to be deleted but only the intermediate file is deleted. 
        """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_ALWAYS" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_ALWAYS" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_files( [ str_dependency_1, str_product_1, str_product_1_ok, 
                                     str_product_2, str_product_2_ok ] )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] ).func_set_resource_clean_level([ str_dependency_1, str_product_1 ] , Resource.CLEAN_ALWAYS)
        cur_cmd2 = Command.Command( "Command 2", [ str_product_1 ], [ str_product_2 ] ).func_set_resource_clean_level([ str_product_1 ] , Resource.CLEAN_ALWAYS)
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd2 ] )
        dt_cur.func_complete_command( cur_cmd )
        dt_cur.func_complete_command( cur_cmd2 )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd2, str_output_directory = str_env,
                                                dt_dependency_tree = dt_cur,
                                                f_remove_products = False )
        f_removed_files = not os.path.exists( str_product_1 )
        f_other_files_remain = f_removed_files and os.path.exists( str_product_1_ok )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_dependency_1 )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_product_2 )
        f_other_files_remain = f_other_files_remain and os.path.exists( str_product_2_ok )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok, str_product_2, str_product_2_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )
        
        
    def test_func_remove_paths_for_good_case_ALWAYS_clean_all_files( self ):
        """ 
        Good case trying to remove one dependency at clean level ALWAYS, any always file is always deleted. 
        Here all files are deleted (expect for the products of cmd 2).
        Note, input files can not be deleted by the remove paths function.
        """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_ALWAYS_clean_all_files" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_ALWAYS_clean_all_files" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_files( [ str_dependency_1, str_product_1, str_product_1_ok, 
                                     str_product_2, str_product_2_ok ] )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] ).func_set_resource_clean_level([ str_dependency_1, str_product_1 ] , Resource.CLEAN_ALWAYS)
        cur_cmd2 = Command.Command( "Command 2", [ str_product_1 ], [ str_product_2 ] ).func_set_resource_clean_level([ str_product_1, str_product_2 ] , Resource.CLEAN_ALWAYS)
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd2 ] )
        dt_cur.func_complete_command( cur_cmd )
        dt_cur.func_complete_command( cur_cmd2 )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = dt_cur,
                                                f_remove_products = False )
        f_success = f_success and cur_pipe.func_remove_paths( cmd_command = cur_cmd2, str_output_directory = str_env,
                                                dt_dependency_tree = dt_cur,
                                                f_remove_products = False )
        f_removed_files = not os.path.exists( str_product_1 )
        f_other_files = f_removed_files and os.path.exists( str_product_1_ok )
        f_other_files =  f_other_files and os.path.exists( str_product_2 )
        f_other_files = f_other_files and os.path.exists( str_product_2_ok )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok, str_product_2, str_product_2_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files)


    def test_func_remove_paths_for_bad_case_one_product_not_exist( self ):
        """
        Bad case trying to remove one product which does not exist.
        Should be true because the file does not exist.
        """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_one_product_not_exist" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_one_product_not_exist" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_other_files_remain )
        

    def test_func_remove_paths_for_good_case_three_product( self ):
        """ Good case trying to remove three products. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_three_product" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_three_product" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_3 = os.path.join( str_env, "Product_3.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        str_product_3_ok = cur_pipe.func_get_ok_file_path( str_product_3 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_2_ok )
        self.func_make_dummy_file( str_product_3 )
        self.func_make_dummy_file( str_product_3_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1, str_product_2, str_product_3 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_removed_files = not os.path.exists( str_product_1 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_1_ok )
        f_removed_files = f_removed_files and not os.path.exists( str_product_2 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_2_ok )
        f_removed_files = f_removed_files and not os.path.exists( str_product_3 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_3_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok,
                                 str_product_2, str_product_2_ok, str_product_3, str_product_3_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )
        
        
    def test_func_remove_paths_for_good_case_three_product_two_dir( self ):
        """ Good case trying to remove three products two of which are directories. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_good_case_three_product_two_dir" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_good_case_three_product_two_dir" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1" )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_3 = os.path.join( str_env, "Product_3" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        str_product_3_ok = cur_pipe.func_get_ok_file_path( str_product_3 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_dir( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_2_ok )
        self.func_make_dummy_dir( str_product_3 )
        self.func_make_dummy_file( str_product_3_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1, str_product_2, str_product_3 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_removed_files = not os.path.exists( str_product_1 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_1_ok )
        f_removed_files = f_removed_files and not os.path.exists( str_product_2 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_2_ok )
        f_removed_files = f_removed_files and not os.path.exists( str_product_3 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_3_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1_ok,
                                 str_product_2, str_product_2_ok, str_product_3_ok ] )
        self.func_remove_dirs( [ str_product_1, str_product_3,  str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )
        
        
    def test_func_remove_paths_for_bad_case_three_product_one_does_not_exist( self ):
        """ Bad case trying to remove three products, one does not exist. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_three_product_one_does_not_exist" )
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_three_product_one_does_not_exist" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_3 = os.path.join( str_env, "Product_3.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        str_product_3_ok = cur_pipe.func_get_ok_file_path( str_product_3 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_product_3 )
        self.func_make_dummy_file( str_product_3_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1, str_product_2, str_product_3 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_removed_files = not os.path.exists( str_product_1 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_1_ok )
        f_removed_files = f_removed_files and not os.path.exists( str_product_2 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_2_ok )
        f_removed_files = f_removed_files and not os.path.exists( str_product_3 )
        f_removed_files = f_removed_files and not os.path.exists( str_product_3_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok,
                                 str_product_2, str_product_2_ok, str_product_3, str_product_3_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success and f_removed_files and f_other_files_remain )
        
        
    def test_func_remove_paths_for_bad_case_three_products_one_not_in_output( self ):
        """ Bad case trying to remove three products, one which is not in the output directory. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_three_products_one_not_in_output" )
        str_env_1 = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_three_products_one_not_in_output_1" )
        str_env_2 = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_three_products_one_not_in_output_2" )
        str_dependency_1 = os.path.join( str_env_1, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env_1, "Product_1.txt" )
        str_product_2 = os.path.join( str_env_2, "Product_2.txt" )
        str_product_3 = os.path.join( str_env_1, "Product_3.txt" )
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        str_product_3_ok = cur_pipe.func_get_ok_file_path( str_product_3 )
        self.func_make_dummy_dir( str_env_1 )
        self.func_make_dummy_dir( str_env_2 )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_2_ok )
        self.func_make_dummy_file( str_product_3 )
        self.func_make_dummy_file( str_product_3_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1, str_product_2, str_product_3 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env_1,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_not_removed_files = os.path.exists( str_product_1 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_1_ok )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_2 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_2_ok )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_3 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_3_ok )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok,
                                 str_product_2, str_product_2_ok, str_product_3, str_product_3_ok ] )
        self.func_remove_dirs( [ str_env_1, str_env_2 ] )
        self.func_test_true( not f_success and f_not_removed_files and f_other_files_remain )


    def test_func_remove_paths_for_bad_case_three_products_one_is_root( self ):
        """
        Bad case trying to remove three products, one which is root.
        !!!! Note this test must be ran with the pipeline in test mode.
        !!!! Too dangerous to be ran in another mode.
        """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_remove_paths_for_bad_case_three_products_one_not_in_output" )
        cur_pipe.func_test_mode() # Do not delete.
        str_env = os.path.join( self.str_test_directory, "test_func_remove_paths_for_bad_case_three_products_one_not_in_output" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1.txt" )
        str_product_1 = os.path.join( str_env, "Product_1.txt" )
        str_product_2 = os.path.join( str_env, "Product_2.txt" )
        str_product_3 = os.path.sep
        str_product_1_ok = cur_pipe.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = cur_pipe.func_get_ok_file_path( str_product_2 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_1_ok )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_2_ok )
        cur_cmd = Command.Command( "Command 1", [ str_dependency_1 ], [ str_product_1, str_product_2, str_product_3 ] )
        f_success = cur_pipe.func_remove_paths( cmd_command = cur_cmd, str_output_directory = str_env,
                                                dt_dependency_tree = DependencyTree.DependencyTree(),
                                                f_remove_products = True )
        f_not_removed_files = os.path.exists( str_product_1 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_1_ok )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_2 )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_2_ok )
        f_not_removed_files = f_not_removed_files and os.path.exists( str_product_3 )
        f_other_files_remain = os.path.exists( str_dependency_1 )
        self.func_remove_files( [ str_dependency_1, str_product_1, str_product_1_ok,
                                 str_product_2, str_product_2_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_success and f_not_removed_files and f_other_files_remain )


# func_run_commands
    def test_func_run_commands_for_no_commands( self ):
        """ Test running commands for no commands. """
        
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_no_commands" )
        f_success = cur_pipe.func_run_commands( [], self.str_test_directory, li_wait = [0,0,0] )
        self.func_test_true( not f_success )


    def test_func_run_commands_for_one_command( self ):
        """ Tests running commands with one command. """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_one_command" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_one_command" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_pipe.func_run_commands( [ cur_cmd_1 ], str_env, f_clean = False, li_wait = [0,0,0])
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_2 )
        self.func_remove_files([ str_file_1, cur_pipe.func_get_ok_file_path( str_file_1 ),
                                str_file_2, cur_pipe.func_get_ok_file_path( str_file_2 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal )
    

    def test_func_run_commands_for_one_command_stale( self ):
        """
        Tests running commands with one command. This command is stale and has a
        dependency so it need not be run.
        """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_one_command_stale" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_one_command_stale" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        self.func_make_dummy_file( str_file_2 )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_pipe.func_run_commands( [ cur_cmd_1 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = not self.func_are_files_equivalent( str_file_1, str_file_2 )
        self.func_remove_files([ str_file_1, cur_pipe.func_get_ok_file_path( str_file_1 ),
                                str_file_2, cur_pipe.func_get_ok_file_path( str_file_2 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal )
   

    def test_func_run_commands_for_two_commands( self ):
        """ Tests running commands with two commands. """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_two_commands")
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_two_commands" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_2 )
        f_files_equal = f_files_equal and self.func_are_files_equivalent( str_file_2, str_file_3 )

        self.func_remove_files([ str_file_1, cur_pipe.func_get_ok_file_path( str_file_1),
                                str_file_2, cur_pipe.func_get_ok_file_path( str_file_2 ),
                                str_file_3, cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal )
        
    def test_func_run_commands_for_one_command_clean_after_error( self ):
        """
        When using clean, the run command should clean up any product.
        This creates one of two products and then runs a bad command
        and then expects products to be cleaned.
        """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_one_command_clean_after_error")
        str_env = os.path.join( self.str_test_directory, "not_test_func_run_commands_for_one_command_clean_after_error" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_2 )
        cur_cmd_1 = Command.Command( " ".join( [ "catddssdsds", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2, str_file_3 ])
        cur_pipe.func_run_commands( [ cur_cmd_1 ], str_env, f_clean = True, li_wait = [0,0,0] )
        f_success = os.path.exists( str_file_1 )
        f_success = f_success and ( not os.path.exists( str_file_2 ) )
        f_success = f_success and ( not os.path.exists( str_file_3 ) )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3 ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_success )
       
       
    def test_func_run_commands_for_two_commands_clean( self ):
        """
        Tests running commands with two commands.
        Intermediary products should be cleaned but not inputs or outputs.
        """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_two_commands_clean")
        str_env = os.path.join( self.str_test_directory, "not_test_func_run_commands_for_two_commands_clean" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ]).func_set_resource_clean_level( [ str_file_2 ], Resource.CLEAN_AS_TEMP )
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2 ], str_env, f_clean = True, li_wait = [0,0,0] )
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_3 )
        f_clean = not os.path.exists( str_file_2 )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3,
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal and f_clean )
        

    def test_func_run_commands_for_two_commands_no_clean( self ):
        """
        Tests running commands with two commands.
        Intermediary products should be NOT be cleaned, nor inputs nor outputs.
        """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_two_commands_clean")
        str_env = os.path.join( self.str_test_directory, "not_test_func_run_commands_for_two_commands_clean" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ]).func_set_resource_clean_level( [ str_file_2 ], Resource.CLEAN_AS_TEMP )
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_3 )
        f_clean = os.path.exists( str_file_1 ) and os.path.exists( str_file_2 ) and os.path.exists( str_file_3 )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3,
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal and f_clean )

       
    def test_func_run_commands_for_two_commands_one_stale( self ):
        """
        Tests running commands with two commands.
        One is command is stale and need not be run.
        """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_two_commands_one_stale" )
        str_env = os.path.join( self.str_test_directory, "not_test_func_run_commands_for_two_commands_one_stale" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = not self.func_are_files_equivalent( str_file_1, str_file_3 )
        f_files_equal = f_files_equal and self.func_are_files_equivalent( str_file_2, str_file_3 )
        f_clean = os.path.exists( str_file_1 )
        f_clean = f_clean and os.path.exists( str_file_2 )
        f_clean = f_clean and os.path.exists( str_file_3 )
        self.func_remove_files( [ str_file_1, str_file_2, str_file_3,
                                cur_pipe.func_get_ok_file_path( str_file_1 ),
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ] )
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal and f_clean )
   
       
    def test_func_run_commands_for_two_commands_stale( self ):
        """
        Tests running commands with two commands.
        Two commands are stale and need not be run.
        """

        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_two_commands_stale")
        str_env = os.path.join( self.str_test_directory, "not_test_func_run_commands_for_two_commands_stale" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        self.func_make_dummy_file( str_file_3 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])

        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = not self.func_are_files_equivalent( str_file_1, str_file_2 )
        f_files_equal = f_files_equal and ( not self.func_are_files_equivalent( str_file_2, str_file_3 ) )
        f_files_equal = f_files_equal and ( not self.func_are_files_equivalent( str_file_1, str_file_3 ) )

        self.func_remove_files([ str_file_1, str_file_2, str_file_3,
                                cur_pipe.func_get_ok_file_path( str_file_1 ),
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal )
   
       
    def test_func_run_commands_for_two_commands_stale_clean( self ):
        """
        Tests running commands with two commands.
        Two commands are stale and need not be run.
        So they also should not be cleaned.
        """
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_two_commands_stale_clean" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_two_commands_stale_clean" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        self.func_make_dummy_file( str_file_3 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ]).func_set_resource_clean_level( [ str_file_2 ], Resource.CLEAN_AS_TEMP )
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2 ], str_env, f_clean = True, li_wait = [0,0,0] )
        f_files_equal = not self.func_are_files_equivalent( str_file_1, str_file_3 )
        f_clean = os.path.exists( str_file_1 )
        f_clean = f_clean and ( not os.path.exists( str_file_2 ) )
        f_clean = f_clean and os.path.exists( str_file_3 )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3,
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [  str_env ] )
        self.func_test_true( f_files_equal and f_clean )


    def test_func_run_commands_for_three_commands_not_ran_parent( self ):
        """
        Tests running commands with three commands.
        Three commands the parent not ran, so must be reran.
        So they also should not be cleaned.
        """
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_three_commands_not_ran_parent" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_three_commands_not_ran_parent" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        str_file_4 = os.path.join( str_env, "test_func_run_commands_file_4.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        self.func_make_dummy_file( str_file_3 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        self.func_make_dummy_file( str_file_4 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_cmd_3 = Command.Command( " ".join( [ "cat", str_file_3, ">", str_file_4 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2, cur_cmd_3 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_2 )
        f_files_equal = f_files_equal and not self.func_are_files_equivalent( str_file_1, str_file_3 )
        f_clean = os.path.exists( str_file_1 )
        f_clean = f_clean and os.path.exists( str_file_2 )
        f_clean = f_clean and os.path.exists( str_file_3 )
        f_clean = f_clean and os.path.exists( str_file_4 )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3, str_file_4,
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_4 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_files_equal and f_clean )

    def test_func_run_commands_for_three_commands_young_parent( self ):
        """
        Tests running commands with three commands.
        Three commands with the parent the youngest, so must be reran.
        So they also should not be cleaned.
        """
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_three_commands_young_ran_parent" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_three_commands_young_ran_parent" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        str_file_4 = os.path.join( str_env, "test_func_run_commands_file_4.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        self.func_make_dummy_file( str_file_3 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        self.func_make_dummy_file( str_file_4 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        time.sleep(2)
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_cmd_3 = Command.Command( " ".join( [ "cat", str_file_3, ">", str_file_4 ] ),
                                     [ str_file_3 ],
                                     [ str_file_4 ])
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2, cur_cmd_3 ], str_env, f_clean = False, li_wait = [0,0,0], i_time_stamp_wiggle = 0 )
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_4 )
        f_clean = os.path.exists( str_file_1 )
        f_clean = f_clean and os.path.exists( str_file_2 )
        f_clean = f_clean and os.path.exists( str_file_3 )
        f_clean = f_clean and os.path.exists( str_file_4 )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3, str_file_4,
                                cur_pipe.func_get_ok_file_path( str_file_1 ),
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_4 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_files_equal and f_clean )

    def test_func_run_commands_for_three_commands_young_parent_2( self ):
        """
        Tests running commands with three commands.
        Three commands with the parent the youngest, so must be reran.
        So they also should not be cleaned.
        """
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_three_commands_young_ran_parent_2" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_three_commands_young_ran_parent_2" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        str_file_4 = os.path.join( str_env, "test_func_run_commands_file_4.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( str_file_3 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        self.func_make_dummy_file( str_file_4 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        time.sleep(2)
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_cmd_3 = Command.Command( " ".join( [ "cat", str_file_3, ">", str_file_4 ] ),
                                     [ str_file_3 ],
                                     [ str_file_4 ])
        cur_pipe.func_run_commands( [ cur_cmd_1, cur_cmd_2, cur_cmd_3 ], str_env, f_clean = False, li_wait = [0,0,0], i_time_stamp_wiggle = 0 )
        f_files_equal = not self.func_are_files_equivalent( str_file_1, str_file_2)
        f_files_equal = f_files_equal and self.func_are_files_equivalent( str_file_2, str_file_4 )
        f_clean = os.path.exists( str_file_1 )
        f_clean = f_clean and os.path.exists( str_file_2 )
        f_clean = f_clean and os.path.exists( str_file_3 )
        f_clean = f_clean and os.path.exists( str_file_4 )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3, str_file_4,
                                cur_pipe.func_get_ok_file_path( str_file_1 ),
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_4 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_files_equal and f_clean )

    def nottest_func_run_commands_for_linear_workflow_shuffled( self ):
        """

        In the process of adding this feature.

        Tests running commands with three commands.
        Three commands shuffled.
        So they also should not be cleaned.
        """
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_linear_workflow_shuffled" )
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_linear_workflow_shuffled" )
        str_file_1 = os.path.join( str_env, "test_func_run_commands_file_1.txt" )
        str_file_2 = os.path.join( str_env, "test_func_run_commands_file_2.txt" )
        str_file_3 = os.path.join( str_env, "test_func_run_commands_file_3.txt" )
        str_file_4 = os.path.join( str_env, "test_func_run_commands_file_4.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file_1 )
        self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        self.func_make_dummy_file( str_file_2 )
        self.func_make_dummy_file( str_file_3 )
        self.func_make_dummy_file( str_file_4 )
        cur_cmd_1 = Command.Command( " ".join( [ "cat", str_file_1, ">", str_file_2 ] ),
                                     [ str_file_1 ],
                                     [ str_file_2 ])
        cur_cmd_2 = Command.Command( " ".join( [ "cat", str_file_2, ">", str_file_3 ] ),
                                     [ str_file_2 ],
                                     [ str_file_3 ])
        cur_cmd_3 = Command.Command( " ".join( [ "cat", str_file_3, ">", str_file_4 ] ),
                                     [ str_file_3 ],
                                     [ str_file_4 ])
        cur_pipe.func_run_commands( [ cur_cmd_3, cur_cmd_2, cur_cmd_1 ], str_env, f_clean = False, li_wait = [0,0,0] )
        f_files_equal = self.func_are_files_equivalent( str_file_1, str_file_4)
        f_clean = os.path.exists( str_file_1 )
        f_clean = f_clean and os.path.exists( str_file_2 )
        f_clean = f_clean and os.path.exists( str_file_3 )
        f_clean = f_clean and os.path.exists( str_file_4 )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_1 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_2 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_3 ) )
        f_clean = f_clean and os.path.exists( cur_pipe.func_get_ok_file_path( str_file_4 ) )
        self.func_remove_files([ str_file_1, str_file_2, str_file_3, str_file_4,
                                cur_pipe.func_get_ok_file_path( str_file_1 ),
                                cur_pipe.func_get_ok_file_path( str_file_2 ),
                                cur_pipe.func_get_ok_file_path( str_file_4 ),
                                cur_pipe.func_get_ok_file_path( str_file_3 ) ])
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_files_equal and f_clean )


    def test_func_run_commands_for_complex_stale_clean( self ):
        """
        Tests running commands in a complex tree.
        Some commands are stale and need not be run.
        So they also should not be cleaned. Other intermediaries
        should be cleaned.
        Dependency Tree:
        D1 D2  D3  D4  D5  D6  D7  D8 P7
        |__|   |   |   |___|   |
         |     |   |     |     |
         C1   C2   |    C5    C6
         |     |   |     |     |
         P1   P2   |     |     |
         |_____|   |    P8    P9
            |      |
            C3     |
           ____    |
         |  |  |   |
        P3  P4 P5  |
               |___|
                 |
                C4
                 |
                P6
         D1,D2,D3,D4,D5,D6,D7,P3,P4,P6,P8,P9 should not be deleted
         P1,P2,P5 should be deleted
         D8 and P7 should not be deleted given it is not in the pipeline...just making sure ;-)
         In this case C1, C2, C3, and C6 will be stale and already made before running.
        """
        str_env = os.path.join( self.str_test_directory, "test_func_run_commands_for_complex_stale_clean" )
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_dependency_3 = os.path.join( str_env, "Dependencies_3.txt" )
        str_dependency_4 = os.path.join( str_env, "Dependencies_4.txt" )
        str_dependency_5 = os.path.join( str_env, "Dependencies_5.txt" )
        str_dependency_6 = os.path.join( str_env, "Dependencies_6.txt" )
        str_dependency_7 = os.path.join( str_env, "Dependencies_7.txt" )
        str_dependency_8 = os.path.join( str_env, "Dependencies_8.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        str_product_3 = os.path.join( str_env, "Products_3.txt" )
        str_product_4 = os.path.join( str_env, "Products_4.txt" )
        str_product_5 = os.path.join( str_env, "Products_5.txt" )
        str_product_6 = os.path.join( str_env, "Products_6.txt" )
        str_product_8 = os.path.join( str_env, "Products_8.txt" )
        str_product_9 = os.path.join( str_env, "Products_9.txt" )
        cmd_test_1 = Command.Command( " ".join( [ "cat",str_dependency_1,">",str_product_1 ] ), 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1 ] )
        cmd_test_2 = Command.Command( " ".join( [ "cat",str_dependency_3,">",str_product_2 ] ), 
                                      [ str_dependency_3 ],
                                      [ str_product_2 ] )
        cmd_test_3 = Command.Command( " ".join( [ "cat",str_product_1,">",str_product_3,
                                                  ";cat ",str_product_1," > ",str_product_4,
                                                  ";cat ",str_product_1," > ",str_product_5,";" ] ), 
                                      [ str_product_1, str_product_2 ],
                                      [ str_product_3, str_product_4, str_product_5 ] )
        cmd_test_4 = Command.Command( " ".join( [ "cat",str_product_5,">",str_product_6 ] ), 
                                      [ str_product_5, str_dependency_4 ],
                                      [ str_product_6 ] )
        cmd_test_5 = Command.Command( " ".join( [ "cat",str_dependency_6,">",str_product_8 ] ), 
                                      [ str_dependency_5, str_dependency_6 ],
                                      [ str_product_8 ] )
        cmd_test_6 = Command.Command( " ".join( [ "cat",str_dependency_7,">",str_product_9 ] ), 
                                      [ str_dependency_7 ],
                                      [ str_product_9 ] )
        self.func_make_dummy_dir( str_env )
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_complex_stale_clean" )
        for str_file in [ str_dependency_1, str_dependency_2, str_dependency_3, str_dependency_4,
                         str_dependency_5, str_dependency_6, str_dependency_7, str_dependency_8,
                         str_product_3, str_product_5 ]:
            self.func_make_dummy_file( str_file )
            self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file ))
        cur_pipe.func_run_commands( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ],
                                    str_env, f_clean = True, li_wait = [0,0,0]  )
        # Check for file which should have been cleaned
        f_cleaned = True
        for str_clean_file in [ str_product_1, str_product_2, str_product_5 ]:
            f_cleaned = f_cleaned and not os.path.exists( str_clean_file )
        # Check for files which should not have been cleaned
        f_not_cleaned = True
        for str_not_cleaned in [ str_dependency_1,str_dependency_2,str_dependency_3,
                                str_dependency_4,str_dependency_5,str_dependency_6,
                                str_dependency_7,str_dependency_8,
                                str_product_3, str_product_4, str_product_6,
                                str_product_8,str_product_9 ]:
            f_not_cleaned = f_not_cleaned and os.path.exists( str_not_cleaned )
        self.func_remove_files( [ str_dependency_1, cur_pipe.func_get_ok_file_path( str_dependency_1 ),
                                 str_dependency_2, cur_pipe.func_get_ok_file_path( str_dependency_2 ),
                                 str_dependency_3, cur_pipe.func_get_ok_file_path( str_dependency_3 ),
                                 str_dependency_4, cur_pipe.func_get_ok_file_path( str_dependency_4 ),
                                 str_dependency_5, cur_pipe.func_get_ok_file_path( str_dependency_5 ),
                                 str_dependency_6, cur_pipe.func_get_ok_file_path( str_dependency_6 ),
                                 str_dependency_7, cur_pipe.func_get_ok_file_path( str_dependency_7 ),
                                 str_dependency_8, cur_pipe.func_get_ok_file_path( str_dependency_8 ),
                                 str_dependency_6, cur_pipe.func_get_ok_file_path( str_dependency_6 ),
                                 str_dependency_7, cur_pipe.func_get_ok_file_path( str_dependency_7 ),
                                 str_dependency_8, cur_pipe.func_get_ok_file_path( str_dependency_8 ),
                                 str_product_1, cur_pipe.func_get_ok_file_path( str_product_1 ),
                                 str_product_2, cur_pipe.func_get_ok_file_path( str_product_2 ),
                                 str_product_3, cur_pipe.func_get_ok_file_path( str_product_3 ),
                                 str_product_4, cur_pipe.func_get_ok_file_path( str_product_4 ),
                                 str_product_5, cur_pipe.func_get_ok_file_path( str_product_5 ),
                                 str_product_6, cur_pipe.func_get_ok_file_path( str_product_6 ),
                                 str_product_8, cur_pipe.func_get_ok_file_path( str_product_8 ),
                                 str_product_9, cur_pipe.func_get_ok_file_path( str_product_9 ) ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( f_cleaned and f_not_cleaned )


    def test_func_run_commands_for_complex_stale_no_clean( self ):
        """
        Tests running commands in a complex tree.
        Some commands are stale and need not be run.
        
        Dependency Tree:
        
        D1 D2  D3  D4  D5  D6  D7  D8 P7
        |__|   |   |   |___|   |
         |     |   |     |     |
         C1   C2   |    C5    C6
         |     |   |     |     |
         P1   P2   |     |     |
         |_____|   |    P8    P9
            |      |
            C3     |
           ____    |
         |  |  |   |
        P3  P4 P5  |
               |___|
                 |
                C4
                 |
                P6
               
         D1,D2,D3,D4,D5,D6,D7,P3,P4,P6,P8,P9 should not be deleted
         P1,P2,P5 should be deleted
         D8 and P7 should not be deleted given it is not in the pipeline...just making sure ;-)
         In this case C3 and C6 will be stale and already made before running.
        """

        str_env = os.path.join( self.str_test_directory, "not_test_func_run_commands_for_complex_stale_no_clean" )
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_dependency_3 = os.path.join( str_env, "Dependencies_3.txt" )
        str_dependency_4 = os.path.join( str_env, "Dependencies_4.txt" )
        str_dependency_5 = os.path.join( str_env, "Dependencies_5.txt" )
        str_dependency_6 = os.path.join( str_env, "Dependencies_6.txt" )
        str_dependency_7 = os.path.join( str_env, "Dependencies_7.txt" )
        str_dependency_8 = os.path.join( str_env, "Dependencies_8.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        str_product_3 = os.path.join( str_env, "Products_3.txt" )
        str_product_4 = os.path.join( str_env, "Products_4.txt" )
        str_product_5 = os.path.join( str_env, "Products_5.txt" )
        str_product_6 = os.path.join( str_env, "Products_6.txt" )
        str_product_7 = os.path.join( str_env, "Products_7.txt" )
        str_product_8 = os.path.join( str_env, "Products_8.txt" )
        str_product_9 = os.path.join( str_env, "Products_9.txt" )

        cmd_test_1 = Command.Command( " ".join( [ "cat",str_dependency_1,">",str_product_1 ] ), 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1 ] )
        cmd_test_2 = Command.Command( " ".join( [ "cat",str_dependency_3,">",str_product_2 ] ), 
                                      [ str_dependency_3 ],
                                      [ str_product_2 ] )
        cmd_test_3 = Command.Command( " ".join( [ "cat",str_product_1,">",str_product_4 ] ), 
                                      [ str_product_1, str_product_2 ],
                                      [ str_product_3, str_product_4, str_product_5 ] )
        cmd_test_4 = Command.Command( " ".join( [ "cat",str_product_5,">",str_product_6 ] ), 
                                      [ str_product_5 ],
                                      [ str_product_6 ] )
        cmd_test_5 = Command.Command( " ".join( [ "cat",str_dependency_6,">",str_product_8 ] ), 
                                      [ str_dependency_5, str_dependency_6 ],
                                      [ str_product_8 ] )
        cmd_test_6 = Command.Command( " ".join( [ "cat",str_dependency_7,">",str_product_9 ] ), 
                                      [ str_dependency_7 ],
                                      [ str_product_9 ] )

        self.func_make_dummy_dir( str_env )
        cur_pipe = Pipeline.Pipeline( str_name = "test_func_run_commands_for_complex_stale_no_clean" )
        
        for str_file in [ str_product_1, str_product_2, str_product_3, str_product_4, str_product_5,
                         str_dependency_1, str_dependency_2, str_dependency_3, str_dependency_4,
                         str_dependency_5, str_dependency_6, str_dependency_7, str_dependency_8,
                         str_product_9, str_product_7 ]:
            self.func_make_dummy_file( str_file )
            self.func_make_dummy_file( cur_pipe.func_get_ok_file_path( str_file ) )

        cur_pipe.func_run_commands( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ],
                                    str_env, f_clean = False, li_wait = [0,0,0] )

        #Check for success
        f_success = not self.func_are_files_equivalent( str_dependency_1, str_product_1 )
        f_success = f_success and ( not self.func_are_files_equivalent( str_dependency_3, str_product_2 ) )
        f_success = f_success and ( not self.func_are_files_equivalent( str_product_1, str_product_4 ) )
        f_success = f_success and ( self.func_are_files_equivalent( str_product_5, str_product_6 ) )
        f_success = f_success and ( self.func_are_files_equivalent( str_dependency_6, str_product_8 ) )
        f_success = f_success and ( not self.func_are_files_equivalent( str_dependency_7, str_product_9) )

        self.func_remove_files( [ str_dependency_1, cur_pipe.func_get_ok_file_path( str_dependency_1 ),
                                 str_dependency_2, cur_pipe.func_get_ok_file_path( str_dependency_2 ),
                                 str_dependency_3, cur_pipe.func_get_ok_file_path( str_dependency_3 ),
                                 str_dependency_4, cur_pipe.func_get_ok_file_path( str_dependency_4 ),
                                 str_dependency_5, cur_pipe.func_get_ok_file_path( str_dependency_5 ),
                                 str_dependency_6, cur_pipe.func_get_ok_file_path( str_dependency_6 ),
                                 str_dependency_7, cur_pipe.func_get_ok_file_path( str_dependency_7 ),
                                 str_dependency_8, cur_pipe.func_get_ok_file_path( str_dependency_8 ),
                                 str_product_1, cur_pipe.func_get_ok_file_path( str_product_1 ),
                                 str_product_2, cur_pipe.func_get_ok_file_path( str_product_2 ),
                                 str_product_3, cur_pipe.func_get_ok_file_path( str_product_3 ),
                                 str_product_4, cur_pipe.func_get_ok_file_path( str_product_4 ),
                                 str_product_5, cur_pipe.func_get_ok_file_path( str_product_5 ),
                                 str_product_6, cur_pipe.func_get_ok_file_path( str_product_6 ),
                                 str_product_7, cur_pipe.func_get_ok_file_path( str_product_7 ),
                                 str_product_8, cur_pipe.func_get_ok_file_path( str_product_8 ),
                                 str_product_9, cur_pipe.func_get_ok_file_path( str_product_9 ) ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( f_success )    


# func_update_command_path
    def test_func_update_command_path_for_no_update_case( self ):
        """ Tst updating a command when there is no need for an update."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java update.jar -xmf 30 -f -g craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        dict_update_cur = { "no_update.jar": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_good_case_update_true( self ):
        """ Update a command with a prefix good case (update args TRUE)."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java prefix/path/to/update.jar -xmf 30 -f -g craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = True
        dict_update_cur = { "update.jar": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_good_case_update_false( self ):
        """ Update a command with a prefix good case (update args FALSE)."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java prefix/path/to/update.jar -xmf 30 -f -g craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = False
        dict_update_cur = { "update.jar": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_good_case_no_args_update_true( self ):
        """ Update a command with a prefix good case no args (True)."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java prefix/path/to/update.jar craziness.txt"
        cmd_cur = Command.Command( "java update.jar craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = True
        dict_update_cur = { "update.jar": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_good_case_no_args_update_false( self ):
        """ Update a command with a prefix good case no args (false)."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java prefix/path/to/update.jar craziness.txt"
        cmd_cur = Command.Command( "java update.jar craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = False
        dict_update_cur = { "update.jar": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_good_case_no_updating_argument_update_true( self ):
        """ Test updating a command when the arguments match ( but should not update ) (true)."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java update.jar -xmf 30 -f -g craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = True
        dict_update_cur = { "craziness.txt": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_good_case_no_updating_argument_update_false( self ):
        """ Test updating a command when the arguments match ( but should not update )."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java update.jar -xmf 30 -f -g prefix/path/to/craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = False
        dict_update_cur = { "craziness.txt": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_updating_command_and_no_updating_argument_update_true( self ):
        """ Test updating a command when the arguments match ( but should not update ) but the command should be updated."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java prefix/path/to/update.jar -xmf 30 -f -g craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = True
        dict_update_cur = { "update.jar": os.path.join( "prefix", "path","to" ), "craziness.txt": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

    def test_func_update_command_path_for_updating_command_and_no_updating_argument_update_false( self ):
        """ Test updating a command when the arguments match ( but should not update ) but the command should be updated."""
        pipe_cur = Pipeline.Pipeline( "test_func_update_command_path_for_good_case" )
        str_answer = "java prefix/path/to/update.jar -xmf 30 -f -g prefix/path/to/craziness.txt"
        cmd_cur = Command.Command( "java update.jar -xmf 30 -f -g craziness.txt", [ "str_depend" ], [ "str_product" ]  )
        cmd_cur.f_stop_update_at_flags = False
        dict_update_cur = { "update.jar": os.path.join( "prefix", "path","to" ), "craziness.txt": os.path.join( "prefix", "path","to" ) }
        pipe_cur.func_update_command_path( cmd_cur, dict_update_cur )
        self.func_test_equals( str_answer, cmd_cur.str_id )

# func_update_products_validity_status
#    def test_func_update_products_validity_status_for_bad_case_bad_command( self ):
#        """ A false should be returned on an invalid command. """
#
#        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_bad_case_bad_command" )
#        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_bad_case_bad_command" )
#        str_product = os.path.join( str_env, "product_1.txt")
#        str_product_ok = pipe_cur.func_get_ok_file_path( str_product )
#        self.func_make_dummy_dir( str_env )
#        self.func_make_dummy_file( str_product )
#        cur_command = Command.Command( None, None, None )
#        cur_dt = DependencyTree.DependencyTree()
#        cur_dt.func_remove_wait()
#        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
#        f_ok_file_made = os.path.exists( str_product_ok )
#        self.func_remove_files( [ str_product , str_product_ok ] )
#        self.func_remove_dirs( [ str_env ] )
#        self.func_test_true( not f_update and not f_ok_file_made )
        
        
    def test_func_update_products_validity_status_for_bad_case_none_command( self ):
        """ A false should be returned on a None command. """

        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_bad_case_none_command" )
        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_bad_case_none_command" )
        str_product = os.path.join( str_env, "product_1.txt")
        str_product_ok = pipe_cur.func_get_ok_file_path( str_product )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product )
        cur_command = None
        cur_dt = DependencyTree.DependencyTree()
        cur_dt.func_remove_wait()
        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
        f_ok_file_made = os.path.exists( str_product_ok )
        self.func_remove_files( [ str_product , str_product_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_update and not f_ok_file_made )


    def test_func_update_products_validity_status_for_bad_case_no_product( self ):
        """ A false should be returned if products do not exist. """

        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_bad_case_no_product" )
        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_bad_case_no_product" )
        str_product = os.path.join( str_env, "product_1.txt")
        str_product_ok = pipe_cur.func_get_ok_file_path( str_product )
        cur_command = Command.Command( "Command", "dependency", str_product )
        cur_dt = DependencyTree.DependencyTree()
        cur_dt.func_remove_wait()
        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
        f_ok_file_made = os.path.exists( str_product_ok )
        self.func_test_true( not f_update and not f_ok_file_made )


    def test_func_update_products_validity_status_for_bad_case_bad_dt( self ):
        """ A false should be returned on a bad dt. """

        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_bad_case_bad_dt" )
        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_bad_case_bad_dt" )
        str_product = os.path.join( str_env, "product_1.txt")
        str_product_ok = pipe_cur.func_get_ok_file_path( str_product )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product )
        cur_command = Command.Command( "Command", "dependency", str_product )
        cur_dt = None
        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
        f_ok_file_made = os.path.exists( str_product_ok )
        self.func_remove_files( [ str_product , str_product_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_update and not f_ok_file_made )
        
    def test_func_update_products_validity_status_for_bad_case_mult_products_one_missing( self ):
        """ A false should be returned if one of the products of the command is false. """

        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_bad_case_mult_products_one_missing" )
        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_bad_case_mult_products_one_missing" )
        str_product_1 = os.path.join( str_env, "product_1.txt")
        str_product_2 = os.path.join( str_env, "product_2.txt")
        str_product_3 = os.path.join( str_env, "product_3.txt")
        str_product_1_ok = pipe_cur.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = pipe_cur.func_get_ok_file_path( str_product_2 )
        str_product_3_ok = pipe_cur.func_get_ok_file_path( str_product_3 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_3 )
        cur_command = Command.Command( "Command", "dependency", [ str_product_1, str_product_2, str_product_3 ] )
        cur_dt = DependencyTree.DependencyTree()
        cur_dt.func_remove_wait()
        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
        f_ok_file_made = os.path.exists( str_product_1_ok )
        f_ok_file_made = f_ok_file_made and os.path.exists( str_product_2_ok )
        f_ok_file_made = f_ok_file_made and os.path.exists( str_product_3_ok )
        self.func_remove_files( [ str_product_1 , str_product_1_ok, str_product_2 , str_product_2_ok, str_product_3 , str_product_3_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( not f_update and not f_ok_file_made )
        
        
    def test_func_update_products_validity_status_for_good_case( self ):
        """ A true should be returned on a good case and the ok file should be made. """

        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_good_case" )
        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_good_case" )
        str_product_1 = os.path.join( str_env, "product_1.txt")
        str_product_ok = pipe_cur.func_get_ok_file_path( str_product_1 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1 )
        cur_command = Command.Command( "Command", [ "dependency" ], [ str_product_1 ] )
        cur_dt = DependencyTree.DependencyTree()
        cur_dt.func_remove_wait()
        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
        f_ok_file_made = os.path.exists( str_product_ok )
        self.func_remove_files( [ str_product_1 , str_product_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_update and f_ok_file_made )
        
        
    def test_func_update_products_validity_status_for_good_case_mult_products( self ):
        """ A true should be returned on a good case and the ok file should be made for each product. """

        str_env = os.path.join( self.str_test_directory, "test_func_update_products_validity_status_for_good_case_mult_products" )
        pipe_cur = Pipeline.Pipeline( "test_func_update_products_validity_status_for_good_case_mult_products" )
        str_product_1 = os.path.join( str_env, "product_1.txt")
        str_product_2 = os.path.join( str_env, "product_2.txt")
        str_product_3 = os.path.join( str_env, "product_3.txt")
        str_product_1_ok = pipe_cur.func_get_ok_file_path( str_product_1 )
        str_product_2_ok = pipe_cur.func_get_ok_file_path( str_product_2 )
        str_product_3_ok = pipe_cur.func_get_ok_file_path( str_product_3 )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_3 )
        cur_command = Command.Command( "Command", [ "dependency" ], [ str_product_1, str_product_2, str_product_3 ] )
        cur_dt = DependencyTree.DependencyTree()
        cur_dt.func_remove_wait()
        f_update = pipe_cur.func_update_products_validity_status( cmd_command = cur_command, dt_tree = cur_dt )
        f_ok_file_made = os.path.exists( str_product_1_ok )
        f_ok_file_made = f_ok_file_made and os.path.exists( str_product_2_ok )
        f_ok_file_made = f_ok_file_made and os.path.exists( str_product_3_ok )
        self.func_remove_files( [ str_product_1 , str_product_1_ok, str_product_2 , str_product_2_ok, str_product_3 , str_product_3_ok ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_update and f_ok_file_made )


# func_test_mode
    def test_func_test_mode( self ):
        """ Check to see if test mode turn on test mode. """
        pip_cur = Pipeline.Pipeline( str_name = "test_func_test_mode" )
        pip_cur.func_test_mode()
        self.func_test_true( not pip_cur.f_execute )


# func_get_ok_time_stamp
    def test_func_get_ok_time_stamp_for_good_case( self ):
        """ Make sure we are reading in the time stamp correctly """
        str_env = os.path.join( self.str_test_directory, "test_func_get_ok_time_stamp_for_good_case" )
        self.func_make_dummy_dir( str_env )
        pipe_cur = Pipeline.Pipeline( "test_func_get_ok_time_stamp_for_good_case" )
        str_product_1 = os.path.join( str_env, "product_1.txt")
        with open( str_product_1, "w" ) as hndl_setup:
            hndl_setup.write( "1441214830.0\nWed Sep  2 13:27:10 2015" )
        d_stamp = pipe_cur.func_get_ok_time_stamp( str_product_1 )
        self.func_remove_files( [ str_product_1 ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_equals( 1441214830.0, d_stamp )
 
#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( PipelineTester )
