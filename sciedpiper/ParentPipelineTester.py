
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import calendar
import os
import unittest
import time

class ParentPipelineTester(unittest.TestCase):
    """
    Holds the utility testing functions useful when testing pipelines.
    """

    str_current_dir = os.getcwd()
    """ Current location to test in."""
    
    str_test_directory = os.path.join( str_current_dir, "test")
    """ Test directory """

    def func_dict_to_string( self, dict_cur ):
        """
        Takes a dict and returns a string with the internal items alphanumerically sorted by key.

        * dict_cur : Dict to get a standardized representation of the internal state.
                     Dict

        * return : String representation of the dict, sorted alphanumerically by keys
                 : String
        """

        # On a null and bad value return empty dict
        if not dict_cur:
            return str({})

        # Sort keys and make string
        return( "{" + ", ".join([ ": ".join([ str( str_key ), str( dict_cur[ str_key ])]) for str_key in sorted(dict_cur.keys()) ]) + "}" )

    def func_are_files_equivalent( self, str_file_path_1, str_file_path_2 ):
        """
        Returns if the contents of to files are the same.
        
        Errors if the files are missing.
        
        * str_file_path_1 : String
                            Path of the first of the two files to compare to each other
                            
        * str_file_path_2 : String
                            Path of the second of two files to compare to each other
                            
        * Return : Boolean
                   True indicates the contents of the files are exact.
        """
        
        if not os.path.exists( str_file_path_1 ):
            raise IOError( "Missing file: " + str_file_path_1 )
        if not os.path.exists( str_file_path_2 ):
            raise IOError( "Missing file: " + str_file_path_2 )

        # Compare line by line and short circuit on a mismatched line.        
        with open( str_file_path_1 ) as hndle_1:
            with open( str_file_path_2 ) as hndle_2:
                for str_line in hndle_1:
                    if not str_line == hndle_2.next():
                        return False
        return True
    

    def func_make_dummy_file( self, str_path, str_message = None ):
        """
        Creates a quick file.
        
        * str_path : String
                     The path to the file to create.
                     
        * str_message : String
                        A message to put in the file as contents.
                        if not provided, the path is used.
                        
        * Return : Boolean
                   True indicates the file was created.
        """
        
        if str_path:
            if not os.path.exists( str_path ):
                with open( str_path, "w" ) as hndle_open:
                    if str_message != "":
                        cur_time = calendar.timegm( time.gmtime() )
                        hndle_open.write( str( cur_time  ) + "\n" )
                        hndle_open.write( str( time.ctime( cur_time ) ) + "\n" )
                        hndle_open.write( str_message if str_message else str_path )
                return True
        return False
    
    
    def func_make_dummy_files( self, lstr_paths, str_message = None ):
        """
        Quickly creates a series of files with the optional message.
        
        * lstr_paths : A list of strings
                     : Paths of files to create / write over.
                     
        * str_message : String
                      : Optional message to write in files.

        * Return : Boolean
                   True indicates all files are created.
        """
        
        if lstr_paths:
            f_success = True
            for str_path in lstr_paths:
                f_success = f_success and self.func_make_dummy_file( str_path, str_message )
            return f_success
        return False


    def func_make_dummy_dir( self, str_path ):
        """
        Creates a directory.
        
        * str_path : String
                     Path to the directory to make.
                     
        * Return : Boolean
                   True indicates that the directory was made.
        """
        
        if str_path:
            if not os.path.exists( str_path ):
                os.makedirs( str_path )
                return True
        return False
    
    
    def func_make_dummy_dirs( self, lstr_paths ):
        """
        Creates a list of directories if they do not already exist.
        
        * lstr_paths : List of strings
                     : List of paths of directories ot make if they are not already existent.
                     
        * Return : Boolean
                   TRue indicates that the directories were made.
        """

        if lstr_paths:
            f_success = True
            for str_dir in lstr_paths:
                f_success = f_success and self.func_make_dummy_dir( str_dir )
            return f_success
        return False


    def func_remove_dirs( self, lstr_dirs ):
        """
        Removes a list of directories if they exist.
        
        * lstr_dirs : List of strings
                      List of directory paths to delete if they exist.
        """

        # Handle in case a string is accidently given
        if isinstance( lstr_dirs, basestring ):
            lstr_dirs = [ lstr_dirs ]
            
        # Make sure root is not deleted
        # Delete each path
        for str_dir in lstr_dirs:
            if str_dir == os.path.sep:
                continue
            if os.path.exists( str_dir ):
                os.removedirs( str_dir )

                
    def func_remove_files( self, lstr_files ):
        """
        Removes a list of files if they exist.
        
        * lstr_files : List of strings
                       List of file paths to remove if they exist
        """

        # Handle in case a string is accidently given
        if isinstance( lstr_files, basestring ):
            lstr_files = [ lstr_files ] 

        for str_file in lstr_files:
            if os.path.exists( str_file ):
                os.remove( str_file )

    def func_test_error( self, *params ):
        """
        Handles testing for a situation where an error is expected.
        """

        with self.assertRaises( params[0], params[1], *params[2:] ):
            self.assertTrue(true)
        self.assertTrue(false)

    def func_test_equals( self, str_answer, str_result ):
        """
        A standardized way to report the asserting of two strings or str( object ) being equal.
        """
        
        self.assertEqual( str( str_answer ), str( str_result ), 
                          "".join( [ str( self ), "::\nExpected=\n", str( str_answer ), ". \nReceived=\n",str( str_result ),"." ] ) )


    def func_test_true(self, f_result ):
        """
        A standardized way to report the asserting of a result to be True.
        """
        
        self.assertTrue( f_result, 
                          "".join( [ str( self ), "::\nExpected=\n True. \nReceived=\n",str( f_result ),"." ] ) )
