
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import os

# The possible cleaning levels for dependencies
CLEAN_NEVER = 1
CLEAN_AS_TEMP = 2
CLEAN_ALWAYS = 3
CLEAN_DEFAULT = CLEAN_AS_TEMP
LSTR_CLEAN_LEVELS = [ CLEAN_NEVER, CLEAN_AS_TEMP, CLEAN_ALWAYS ]

# List of folders which are temporary and can not be dependencies
LSTR_TEMP_DIRECTORIES = [ os.sep+"dev" ]

class Command( object ):
    """
    Represents a command line call. Keeps together command, dependency, and products information.
    """
    
    # Tested
    def __init__( self, str_cur_command, lstr_cur_dependencies = [], lstr_cur_products = [] ):
        """
        Initializer. 
        All paths should be absolute paths.
        If given relative paths, the current working directory will be added on to the path to
        make the file path absolute.
        
        * str_cur_command : String
                            Command to execute
                            
        * lstr_cur_dependencies : List of strings
                                  List of absolute paths paths for dependencies
                                  
        * lstr_cur_products : List of strings
                              List of absolute paths for products to be made
        """
        
        self.str_command = str_cur_command if str_cur_command else ""
        self.lstr_dependencies = lstr_cur_dependencies
        self.lstr_products = lstr_cur_products
        
        self.dict_clean_level = {}


    @property
    def lstr_dependencies( self ):
        """
        Gets the list of dependencies
        
        * return : List of paths
                 : List of paths for dependencies
        """

        return self.__lstr_dependencies

    @lstr_dependencies.setter
    def lstr_dependencies( self, lstr_paths ):
        """
        Sets the dependencies.
        Will update to absolute paths
        Will not allow dependencies to be temporary files

        * lstr_paths : List of paths
                     : Paths to set as the dependencies
        """

        if isinstance( lstr_paths, basestring ):
            lstr_paths = [ lstr_paths ]

        self.__lstr_dependencies = lstr_paths if lstr_paths else []
        self.__lstr_dependencies = [ self.func_make_paths_absolute( str_path )[ 0 ] for str_path in self.__lstr_dependencies if str_path ]
        self.__lstr_dependencies = self.func_remove_temp_files( self.__lstr_dependencies )

    @classmethod
    def func_remove_temp_files( self, lstr_files ):
        """
        Remove temporary files from a list of files.

        * lstr_files : List of file paths
                     : Paths to files
        """

        lstr_return = lstr_files[:]
        for str_temp_dir in LSTR_TEMP_DIRECTORIES:
            lstr_temp = []
            for str_path in lstr_return:
                f_temp_dir_is_longer = len( str_temp_dir ) > len( str_path )
                if f_temp_dir_is_longer:
                    lstr_temp.append( str_path )
                else:
                    f_temp_is_the_start = str_path[ : len( str_temp_dir ) ] == str_temp_dir
                    if not f_temp_is_the_start:
                        lstr_temp.append( str_path )
            lstr_return = lstr_temp
        return lstr_return

    @property
    def lstr_products( self ):
        """
        Gets the list of products
        
        * return : List of paths
                 : List of paths for products
        """

        return self.__lstr_products


    @lstr_products.setter
    def lstr_products( self, lstr_paths ):
        """
        Sets the products.
        Will update to absolute paths
        
        * lstr_paths : List of paths
                     : Paths to set as the products
        """

        
        if isinstance( lstr_paths, basestring ):
            lstr_paths = [ lstr_paths ]

        self.__lstr_products = lstr_paths if lstr_paths else []
        self.__lstr_products = [ self.func_make_paths_absolute( str_path )[ 0 ] for str_path in self.__lstr_products if str_path ]


    # Tested
    def func_set_dependency_clean_level( self, lstr_file, i_level ):
        """
        Add a cleaning level for a list of files that are dependencies.
        
        * lstr_file : List of strings
                    : Paths to set to the given clean level
                    : Must be existing dependencies in the command
                    : If not absolute paths, will be given the current working dir as their prefix.

        * i_level : Int
                  : Clean level to set files to
                  
        * return : Self
                 : This command.
        """
        
        if ( not lstr_file ) or ( i_level not in LSTR_CLEAN_LEVELS ) or ( not self.lstr_dependencies ):
            return self

        # Handle in case a string is accidently given
        if isinstance( lstr_file, basestring ):
            lstr_file = [ lstr_file ]

        # Make sure are absolute paths
        lstr_file = self.func_make_paths_absolute( lstr_file )

        # Allow all files to be added as long as they are known dependencies
        for str_file in lstr_file:
            if str_file in self.lstr_dependencies:
                self.dict_clean_level.setdefault( i_level, [] ).append( str_file )
        return self


    def func_get_clean_level( self, str_file_path ):
        """
        Returns the clean level of the given product or dependency.
        
        * str_path : string
                   : String path of dependency or product to check clean level
                   
        * return : int
                 : Clean level ( Command constant )
        """

        for i_clean_level, lstr_files in self.dict_clean_level.iteritems():
            if str_file_path in lstr_files:
                return i_clean_level
        return CLEAN_DEFAULT

    
    # Tested
    def func_get_dependencies_to_clean_level( self, i_level ):
        """
        Gives the dependencies that should be cleaned at that level and any level less strict.
        
        Will never return files with a clean level NEVER
        
        If a path was not assigned a clean level, it is treated as the default cleaning level
        
        
        * i_level : Int, must be a value from Command's LSTR_CLEAN_LEVELS
                  : The cleaning level to remove
                  
        * return : List
                 : List of dependencies, empty list on invalid clean level
        """

        # Do not clean on bad level
        if i_level not in LSTR_CLEAN_LEVELS:
            return []
        
        # Holds all products to clean
        lstr_dependencies_to_clean = []
        
        # Never return NEVER
        if i_level == CLEAN_NEVER:
            i_level += 1

        # Get all products that are that level or greater
        # This does not include the defaults level
        for i_clean_level in xrange( i_level, CLEAN_ALWAYS+1 ):
            lstr_dependencies_to_clean.extend( self.dict_clean_level.get( i_clean_level, [] ) )

        # This is for paths that have not been given a cleaning level
        # They are treated like the default cleaning mode in the object
        # Defined above.
        # If the cleaning level is less than the default level
        # Include default as well
        if i_level <= CLEAN_DEFAULT:
            lstr_dependencies_with_level = []
            for lstr_dependencies_with_this_level in self.dict_clean_level:
                lstr_dependencies_with_level.extend( self.dict_clean_level[ lstr_dependencies_with_this_level ] )
            lstr_dependencies_to_clean.extend( set( self.lstr_dependencies ) - set( lstr_dependencies_with_level ) )

        return set( lstr_dependencies_to_clean )


    # Tested
    def func_is_dependency_clean_level( self, str_dependency, i_clean_level ):
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

        if not str_dependency or not i_clean_level:
            return False
        
        # Make sure are absolute paths
        str_dependency = self.func_make_paths_absolute( str_dependency )[0]
        return str_dependency in self.dict_clean_level.get( i_clean_level, [] )

    
    # Tested
    def func_is_valid( self ):
        """
        Returns true if there is a command with both dependencies and products.
        
        * Return : Boolean
                   True indicates the Command has entries for command, dependencies, and products
        """
        
        return self.str_command and self.lstr_dependencies and self.lstr_products


    # Tested
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
                lstr_return_list.append( os.path.abspath( str_path ) )
        return lstr_return_list


    def __str__( self ):
        """
        String representation of the command.
        """
        
        return self.str_command
    
    
    def __rep__( self ):
        """
        Represent command.
        """
        
        return self.str_command
    

    def __id__( self ):
        """
        Id for hashing
        """
        
        return hash( self.str_command )
