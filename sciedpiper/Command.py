
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Graph
import os
import Resource

DICT_CLEAN_TO_KEY = { Resource.CLEAN_NEVER : "NEVER", Resource.CLEAN_AS_TEMP : "TEMP", Resource.CLEAN_ALWAYS : "ALWAYS" }
DICT_JSON_CLEAN_INT = { u'never' : Resource.CLEAN_NEVER, u'temp' : Resource.CLEAN_AS_TEMP, 'always' : Resource.CLEAN_ALWAYS }

# JSON related
STR_CLEAN_JSON = "CLEAN"
USTR_CLEAN_JSON = u'Clean'
STR_CLEAN_NEVER = "NEVER_CLEAN"
STR_CLEAN_ALWAYS = "ALWAYS_CLEAN"
STR_COMMAND_JSON = "COMMAND"
USTR_COMMAND_JSON = u'COMMAND'
STR_DEPENDENCIES_JSON = "NEEDS"
USTR_DEPENDENCIES_JSON = u'NEEDS'
STR_PATH_JSON = "PATH"
USTR_PATH_JSON = u'PATH'
STR_PRODUCTS_JSON = "MAKES"
USTR_PRODUCTS_JSON = u'MAKES'
LSTR_JSON_KEYS = [ STR_COMMAND_JSON, STR_DEPENDENCIES_JSON, STR_PRODUCTS_JSON ]

STR_TYPE = "COMMAND"

STR_NOT_RUN = "NOT"
STR_RUNNING = "RUN"
STR_COMPLETE = "DONE"
STR_ERROR = "ERROR"

# Clean levels, here for backwards compatability
CLEAN_NEVER = Resource.CLEAN_NEVER
CLEAN_AS_TEMP = Resource.CLEAN_AS_TEMP
CLEAN_ALWAYS = Resource.CLEAN_ALWAYS
CLEAN_DEFAULT = Resource.CLEAN_DEFAULT
LSTR_CLEAN_LEVELS = Resource.LSTR_CLEAN_LEVELS

class Command( Graph.Vertex ):
    """
    Represents a command line call. Keeps together command, dependency, and products information.
    """
    
    # Tested
    def __init__( self, str_cur_command, lstr_cur_dependencies, lstr_cur_products ):
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

        # Set there id for the parent vertex
        Graph.Vertex.__init__( self,str_cur_command )
        self.str_type = STR_TYPE
        self.str_status = STR_NOT_RUN
        for str_dependency in lstr_cur_dependencies:
            rsc_dep = Resource.Resource( str_dependency, f_is_product=False )
            self.func_add_parent( rsc_dep )
            rsc_dep.func_add_child( self )
        for str_product in lstr_cur_products:
            rsc_prod = Resource.Resource( str_product, f_is_product=True )
            self.func_add_child( rsc_prod )
            rsc_prod.func_add_parent( self )

    # Used in testing
    @property
    def lstr_dependencies( self ):
        """
        Gets the list of dependencies
        
        * return : List of paths
                 : List of paths for dependencies
        """

        return self.func_get_parents()

    # Used in testing
    @property
    def lstr_products( self ):
        """
        Gets the list of products
        
        * return : List of paths
                 : List of paths for products
        """

        return self.func_get_children()

    # Tested
    def func_is_valid( self ):
        """
        Returns true if there is a command with both dependencies and products.
        
        * Return : Boolean
                   True indicates the Command has entries for command, dependencies, and products
        """
        
        return self.str_id and self.lstr_dependencies and self.lstr_products

    # Tested
    def func_to_dict( self ):
        """
        Translate the command to a dict representation.
        { Command.USTR_COMMAND_JSON: str_cur_command,
          Command.USTR_DEPENDENCIES_JSON: [{ Command.USTR_PATH:str_path,  Command.USTR_CLEAN: CLEAN }....],
          Command.USTR_PRODUCTS_JSON: [{ Command.USTR_PATH:str_path,  Command.USTR_CLEAN:CLEAN }...] }

        * return : Dict representation of Command as described above.
                 : Dict
        """

        dict_cur = {}
        # Add comamnd
        dict_cur[ STR_COMMAND_JSON ] = self.str_id
        # Add dependencies and clean levels
        if len( self.lstr_dependencies ) > 0:
            dict_cur[ STR_DEPENDENCIES_JSON ] = []
            for vtx_dep in self.lstr_dependencies:
                dict_cur[ STR_DEPENDENCIES_JSON ].append( { STR_PATH_JSON: vtx_dep.str_id, STR_CLEAN_JSON: DICT_CLEAN_TO_KEY[ vtx_dep.i_clean ] } )

        # Add products and clean levels
        if len( self.lstr_products ) > 0:
            dict_cur[ STR_PRODUCTS_JSON ] = []
            for vtx_prod in self.lstr_products:
                dict_cur[ STR_PRODUCTS_JSON ].append( { STR_PATH_JSON: vtx_prod.str_id, STR_CLEAN_JSON: DICT_CLEAN_TO_KEY[ vtx_prod.i_clean ] } )

        return( dict_cur )

    # Lightly tested
    @classmethod
    def func_dict_to_command( self, dict_convert ):
        """
        Change a dict of information to a command.
        The expected format is 
        { Command.USTR_COMMAND_JSON: str_cur_command,
          Command.USTR_DEPENDENCIES_JSON: { Command.USTR_PATHS_JSON:[ str_path ],  Command.USTR_CLEAN_JSON:[ CLEAN ] },
          Command.USTR_PRODUCTS_JSON: { Command.USTR_PATHS_JSON:[ str_path, str_path ],  Command.USTR_CLEAN_JSON:[ CLEAN, CLEAN ] } }

        * dict_convert : Dict of information to make into a command. Described above.
                       : Dict
        * return : Command or none on error/empty dict.
                 : Command
        """

        if not dict_convert:
            return None

        # If there is no command in the command object, disreguard, unimportant
        if not USTR_COMMAND_JSON in dict_convert:
            return None

        # Make command
        str_cur_command = dict_convert[ USTR_COMMAND_JSON ]
        # Get dependencies
        lstr_dependencies = dict_convert[ USTR_DEPENDENCIES_JSON ] if USTR_DEPENDENCIES_JSON in dict_convert else []
        lstr_dep_paths = [ dict_file[ USTR_PATH_JSON ] for dict_file in lstr_dependencies ]
        # Get products
        lstr_products = dict_convert[ USTR_PRODUCTS_JSON ] if USTR_PRODUCTS_JSON in dict_convert else []
        lstr_prod_paths = [ dict_file[ USTR_PATH_JSON ] for dict_file in lstr_products ]
        # Make command object
        vtx_cmd_cur = Command( str_cur_command=str_cur_command,
                               lstr_cur_dependencies=lstr_dep_paths,
                               lstr_cur_products=lstr_prod_paths )
        # Add dependencies clean level
        for dict_file in lstr_dependencies + lstr_products:
            lstr_file = [ dict_file[ USTR_PATH_JSON ] ]
            i_level = dict_file.get( USTR_CLEAN_JSON, DICT_CLEAN_TO_KEY[ Resource.CLEAN_DEFAULT ] ) 
            vtx_cmd_cur.func_set_resource_clean_level( lstr_file=lstr_file, i_level=i_level )
        return( vtx_cmd_cur )

    # Tested
    def func_set_dependency_level( self, lstr_file, i_level ):
        """
        Depricated, please use func_set_resource_clean_level().
        """
        return self.func_set_resource_clean_level( lstr_file, i_level )

    def func_set_resource_clean_level( self, lstr_file, i_level ):
        """
        Add a cleaning level for a list of files that are resources.

        * lstr_file : List of strings
                    : Paths to set to the given clean level
                    : Must be existing resources in the command
                    : If not absolute paths, will be given the current working dir as their prefix.

        * i_level : Int
                  : Clean level to set files to

        * return : Self
                 : This command.
        """

        if ( not lstr_file ) or ( i_level not in Resource.LSTR_CLEAN_LEVELS ) or ( not self.lstr_dependencies ):
            return self

        # Handle in case a string is accidently given
        if isinstance( lstr_file, basestring ):
            lstr_file = [ lstr_file ]

        # Make sure are absolute paths
        lstr_file = Resource.Resource.func_make_paths_absolute( lstr_file )

        # Allow all files to be added as long as they are known dependencies
        for vtx_file in self.lstr_dependencies + self.lstr_products:
            if vtx_file.str_id in lstr_file:
                vtx_file.i_clean=i_level
        return self

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
        if i_level not in Resource.LSTR_CLEAN_LEVELS:
            return []

        # Holds all products to clean
        lstr_dependencies_to_clean = []

        # Never return NEVER
        if i_level == Resource.CLEAN_NEVER:
            i_level += 1

        # Get all dependencies that are that level or greater
        # This does not include the defaults level
        for vtx_dependency in self.lstr_dependencies:
            if vtx_dependency.i_clean >= i_level:
                lstr_dependencies_to_clean.append( vtx_dependency )

        return set( lstr_dependencies_to_clean )

    # Used in testing
    def func_detail( self ):
        """
        Give a detailed and standardized view of the command. Mainly for detailed testing.
        """

        str_command = "Command: " + self.str_id
        str_dependencies = "Dependencies: " + ",".join( sorted ( [ str( rsc_dep ) for rsc_dep in self.lstr_dependencies ] ) )
        str_products = "Products: " + ",".join( sorted ( [ str( rsc_prod ) for rsc_prod in self.lstr_products ] ) )
        return( "; ".join( [ str_command, str_dependencies, str_products ] ) )

    # OK
    def __str__( self ):
        """
        String representation of the command.
        """
        
        return self.str_id

    # OK
    def __rep__( self ):
        """
        Represent command.
        """
        
        return self.str_id
