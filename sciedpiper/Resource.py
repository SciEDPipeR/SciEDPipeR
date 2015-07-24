
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Graph
import os

# The possible cleaning levels for dependencies
CLEAN_NEVER = 1
CLEAN_AS_TEMP = 2
CLEAN_ALWAYS = 3
CLEAN_DEFAULT = CLEAN_AS_TEMP
LSTR_CLEAN_LEVELS = [ CLEAN_NEVER, CLEAN_AS_TEMP, CLEAN_ALWAYS ]

# List of folders which are temporary and can not be dependencies
LSTR_TEMP_DIRECTORIES = [ os.sep+"dev" ]

STR_TYPE = "RESOURCE"
STR_NOT_MADE = "NOT"
STR_MADE = "MADE"
STR_ERROR = "ERROR"

class Resource( Graph.Vertex ):
    """
    Represents a file input or output to a command.
    Is treated as a node in the graph.
    """

    # Tested
    def __init__( self, str_path, f_is_product, i_clean=CLEAN_DEFAULT ):
        Graph.Vertex.__init__( self, str_path )
        if not self.str_id:
          raise ValueError("Please give a valid string value for the id, received:"+str(self.str_id)+".")
        self.str_id = Resource.func_make_paths_absolute( [ self.str_id ] )[0]
        self.f_is_product = f_is_product
        self.f_is_generated = False
        self.i_clean = i_clean
        self.str_type = STR_TYPE
        self.str_status = STR_NOT_MADE

    # Tested
    def __str__( self ):
        return " ".join( [ "PATH:", str( self.str_id ) + ",",
                          "CLEAN:", str( self.i_clean ) + ",",
                          "Product" if self.f_is_product else "Dependency",
                          "PARENTS:", str( [ str( vtx_parent.str_id ) for vtx_parent in self.func_get_parents() ] ),
                          "CHILDREN:", str( [ str( vtx_child.str_id ) for vtx_child in self.func_get_children() ] ) ] )

    # Tested
    @classmethod
    def func_make_paths_absolute( self, lstr_paths ):
        """
        Makes the file paths in the command absolute from the current working directory
        If they are not currently absolute. This happens automatically on
        initialization of the command instance. If the file is already absolute path then
        it is returned as is.

        * lstr_path : List of strings
                    : List of paths to convert if relative.

        * Return : List of strings
                 : List of paths all relative
                 : On bad data like empty list, the input is just returned.
        """

        lstr_return_list = []

        # Handle in case a string is accidently given
        if isinstance( lstr_paths, basestring ):
            lstr_paths = [ lstr_paths ]

        if lstr_paths:
            for str_path in lstr_paths:
                if str_path:
                  lstr_return_list.append( os.path.abspath( str_path ) )
        return lstr_return_list

    # Tested
    def func_is_dependency_clean_level( self, i_clean_level ):
        """
        Indicates that a dependency is of a certain clean level.

        * str_dependency : String
                         : The dependency to check if it is the given clean level

        * i_clean_level : Int
                        : The clean level in question

        * Return : Boolean
                 : Indicator of the dependency having that clean level
                 : True indicates it does, false is it does not or bad input.
        """

        if not i_clean_level:
            return False

        return self.i_clean == i_clean_level

    # Tested
    @classmethod
    def func_remove_temp_files( self, lstr_files ):
        """
        Remove temporary files from a list of files.

        * lstr_files : List of file paths
                     : Paths to files
        """

        # Check input param
        if not lstr_files:
            return []

        lstr_return = lstr_files[:]

        # Check each temp directory
        for str_temp_dir in LSTR_TEMP_DIRECTORIES:
            lstr_temp = []
            # If the path does not start with the temp directory add it to the return array
            # Keep reducing down the return array until nothing in it
            # Starts with any of the temp directories
            for str_path in lstr_return:
                # Ignore bad strings
                if not str_path:
                    continue
                f_temp_dir_is_longer = len( str_temp_dir ) > len( str_path )
                if f_temp_dir_is_longer:
                    lstr_temp.append( str_path )
                else:
                    # Make sure the path is at the start of the path
                    # And that the next char is not a char or a os.sep
                    f_temp_is_the_start = str_path[ : len( str_temp_dir ) ] == str_temp_dir
                    if f_temp_is_the_start:
                        if( ( len( str_temp_dir ) == len( str_path ) ) or
                            ( str_path[ : len( str_temp_dir ) + 1 ] == str_temp_dir + os.path.sep ) ):
                            continue
                    lstr_temp.append( str_path )
            lstr_return = lstr_temp
        return lstr_return
