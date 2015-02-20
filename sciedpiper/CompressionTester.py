
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import Compression
import os
import ParentPipelineTester
import tarfile
import unittest

class CompressionTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the Compression object
    """
    
    def test_func_compress_for_none( self ):
        """
        Test the case of compressing a none path
        Should return false
        """
        
        # Set up environment
        str_answer = None
        str_to_compress = None
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_compress( str_file_path = str_to_compress, str_output_directory = str_to_compress )
        
        # Check answer
        self.func_test_equals( str_answer, return_result )

    def test_func_compress_for_not_existing_file( self ):
        """
        Test the case of compressing a file path that does not exist
        Should return false
        """
        
        # Set up environment
        str_answer = None
        str_env = os.path.join( self.str_test_directory, "test_func_compress_for_not_existing_file" )
        str_to_compress = os.path.join( str_env, "test_func_compress_for_not_existing_file.txt" )
        self.func_remove_files( [ str_to_compress ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_compress( str_file_path = str_to_compress, str_output_directory = str_env )
        
        # Check answer
        self.func_test_equals( str_answer, return_result )
        
    def test_func_compress_for_valid_file( self ):
        """
        Test the case of compressing a valid file path
        Should return true
        """
        
        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_func_compress_for_valid_file" )
        self.func_make_dummy_dir( str_env )
        str_to_compress = os.path.join( str_env, "test_func_compress_for_valid_file_good_file.txt" )
        self.func_make_dummy_file( str_to_compress )
        str_answer = str_to_compress + ".gz"
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_compress( str_file_path = str_to_compress, str_output_directory = str_env )
        
        # Check env
        f_files_should_exist = not os.path.exists( str_to_compress )
        f_files_should_exist = f_files_should_exist and os.path.exists( str_answer )
        
        # Destroy environment
        self.func_remove_files( [ str_to_compress, str_answer ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_true( f_files_should_exist and str_answer == return_result )
        
    def test_func_compress_for_valid_dir_empty( self ):
        """
        Test the case of compressing a valid empty directory path
        Should return true
        """
        
        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_func_compress_for_valid_dir_empty" )
        str_answer = str_env + ".tar.gz"
        self.func_make_dummy_dir( str_env )
        self.func_remove_files( [ str_answer ] )
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_compress( str_file_path = str_env, str_output_directory = str_env  )
        
        # Check answer
        f_dir_file_count_correct = False
        f_files_should_exist = os.path.exists( str_answer )
        if f_files_should_exist:
            with tarfile.open( str_answer ) as hndl_answer:
                f_dir_file_count_correct = len( hndl_answer.getnames() ) == 1

        # Destroy environment
        self.func_remove_files( [ str_answer ] )
        self.func_remove_dirs( [ str_env ] )
                
        self.func_test_true( f_files_should_exist and f_dir_file_count_correct and str_answer == return_result )
        
    def test_func_compress_for_compressed_file( self ):
        """
        Test the case of attempting to compress a compressed file path
        Should return true
        """
        
        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_func_compress_for_valid_file" )
        self.func_make_dummy_dir( str_env )
        str_to_compress = os.path.join( str_env, "test_func_compress_for_valid_file_good_file.txt" )
        self.func_make_dummy_file( str_to_compress )
        str_answer = str_to_compress + ".gz"
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_compress( str_file_path = str_to_compress, str_output_directory = str_env )
        
        # Check answer
        f_files_should_exist = not os.path.exists( str_to_compress )
        f_files_should_exist = f_files_should_exist and os.path.exists( str_answer )
        
        # Destroy environment
        self.func_remove_files( [ str_to_compress, str_answer ] )
        self.func_remove_dirs( [ str_env ] )
        
        self.func_test_true( f_files_should_exist and str_answer == return_result )

    def test_func_compress_for_valid_dir_with_two_files( self ):
        """
        Test the case of compressing a valid directory path containing 2 files
        Should return true
        """
        
        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_func_compress_for_valid_dir_with_two_files" )
        str_answer = str_env + ".tar.gz"
        str_file_1 = os.path.join( str_env, "file1.txt" )
        str_file_2 = os.path.join( str_env, "file2.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_files( [ str_file_1, str_file_2 ] )
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_compress( str_file_path = str_env, str_output_directory = str_env )
        
        # Check answer
        f_dir_file_count_correct = False
        f_files_should_exist = os.path.exists( str_answer )
        if f_files_should_exist:
            with tarfile.open( str_answer ) as hndl_answer:
                f_dir_file_count_correct = len( hndl_answer.getnames() ) == 3
        
        # Destroy environment
        self.func_remove_files( [ str_answer, str_file_1, str_file_2 ] )
        self.func_remove_dirs( [ str_env ] )
        
        self.func_test_true( f_files_should_exist and f_dir_file_count_correct and str_answer == return_result )
        
## func_is_compressed
    def test_func_is_compressed_for_none( self ):
        """
        Test the case of checking a none file path is compressed
        """
        
        # Set up environment
        f_answer = None
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_is_compressed( str_file_path = None )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_not_existing_path( self ):
        """
        Test the case of checking a file path which does not exist is compressed
        """
        
        # Set up environment
        f_answer = None
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_not_existing_path" )
        str_file = os.path.join( str_env, "this_file_should_not_exist_delete_me.txt" )
        self.func_remove_files( [ str_file ] )
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_is_compressed( str_file_path = str_file )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_uncompressed_file( self ):
        """
        Test the case of checking a file path which is not compressed
        """
        
        # Set up environment
        f_answer = False
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_uncompressed_file" )
        str_file = os.path.join( str_env, "this_file_should_not_exist_delete_me.txt" )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file )
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_is_compressed( str_file_path = str_file )
        
        # Destroy environment
        self.func_remove_files( [ str_file ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_uncompressed_dir( self ):
        """
        Test the case of checking a file path which is not compressed
        """
        
        # Set up environment
        f_answer = False
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_uncompressed_dir" )
        str_dir = os.path.join( str_env, "test_func_is_compressed_for_existing_uncompressed_dir" )
        self.func_make_dummy_dirs( [ str_env, str_dir ] )
        
        # Send command and get result
        cprs_cur = Compression.Compression()
        return_result = cprs_cur.func_is_compressed( str_file_path = str_dir )
        
        # Destroy environment
        self.func_remove_dirs( [ str_dir, str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_file_gz( self ):
        """
        Test the case of checking a file path which is gz compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_file_gz" )
        str_file = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_file_gz.txt" )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_files( [ str_file ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_file, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_GZ )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_file, str_compressed_file ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_dir_gz( self ):
        """
        Test the case of checking a dir path which is gz compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_dir_gz" )
        str_dir = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_dir_gz" )
        self.func_make_dummy_dirs( [ str_env, str_dir ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_dir, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_GZ )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_compressed_file ] )
        self.func_remove_dirs( [ str_dir, str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_file_bz2( self ):
        """
        Test the case of checking a file path which is bz2 compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_file_bz2" )
        str_file = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_file_bz2.txt" )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_files( [ str_file ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_file, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_BZ2 )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_file, str_compressed_file ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_dir_bz2( self ):
        """
        Test the case of checking a dir path which is bz2 compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_dir_bz2" )
        str_dir = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_dir_bz2" )
        self.func_make_dummy_dirs( [ str_env, str_dir ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_dir, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_BZ2 )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        # Destroy environment
        self.func_remove_files( [ str_compressed_file ] )
        self.func_remove_dirs( [ str_dir, str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_file_zip( self ):
        """
        Test the case of checking a file path which is zip compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_file_zip" )
        str_file = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_file_zip.txt" )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_files( [ str_file ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_file, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_ZIP )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_file, str_compressed_file ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )

    def test_func_is_compressed_for_existing_compressed_dir_zip( self ):
        """
        Test the case of checking a dir path which is zip compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_dir_zip" )
        str_file = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_empty_dir_zip.txt" )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_file( str_file )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_env, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_ZIP )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )

        # Destroy environment
        self.func_remove_files( [ str_compressed_file, str_file ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_empty_dir_gz( self ):
        """
        Test the case of checking an empty dir path which is gz compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_empty_dir_gz" )
        str_file = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_empty_dir_gz.txt" )
        self.func_make_dummy_dirs( [ str_env ] )
        self.func_make_dummy_file( str_file )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_env, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_GZ )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_compressed_file, str_file ] )
        self.func_remove_dirs( [ str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )
        
    def test_func_is_compressed_for_existing_compressed_empty_dir_bz2( self ):
        """
        Test the case of checking an empty dir path which is bz2 compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_empty_dir_bz2" )
        str_dir = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_empty_dir_bz2" )
        self.func_make_dummy_dirs( [ str_env, str_dir ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_dir, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_BZ2 )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_compressed_file ] )
        self.func_remove_dirs( [ str_dir, str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )

    def test_func_is_compressed_for_existing_compressed_empty_dir_zip( self ):
        """
        Test the case of checking an empty dir path which is zip compressed
        """
        
        # Set up environment
        f_answer = True
        str_env = os.path.join( self.str_test_directory, "test_func_is_compressed_for_existing_compressed_empty_dir_zip" )
        str_dir = os.path.join( str_env, "test_func_is_compressed_for_existing_compressed_empty_dir_zip" )
        self.func_make_dummy_dirs( [ str_env, str_dir ] )

        # Send command and get result
        cprs_cur = Compression.Compression()
        str_compressed_file = cprs_cur.func_compress( str_file_path = str_dir, str_output_directory = str_env, str_compression_type = Compression.STR_COMPRESSION_ZIP )
        return_result = cprs_cur.func_is_compressed( str_file_path = str_compressed_file )
        
        # Destroy environment
        self.func_remove_files( [ str_compressed_file ] )
        self.func_remove_dirs( [ str_dir, str_env ] )
        
        # Check answer
        self.func_test_equals( f_answer, return_result )

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( CompressionTester )