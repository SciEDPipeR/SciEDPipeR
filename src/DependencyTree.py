
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import logging
import os
import time


class DependencyTree:
    """
    This object manages dependencies tracking for command line.

    dict_commands is a dictionary that holds the commands and the related dependencies and products.
    { string_command: [ [str_dependency,str_dependency,...], [str_product,str_product,...] }
    
    dict_dependencies is a dictionary that holds dependencies and their related commands
    { string_dependency: [ str_command, str_command,...] }
    
    lstr_products is a list of products added (helps determine currently terminal files.
    
    lstr_dependencies is a list of dependencies add (help determine currently terminal files
    
    lstr_terminal_products is a list of terminal products given current graph state.
    """
    
    C_INT_DEPENDENCIES_INDEX = 0
    C_INT_PRODUCTS_INDEX = 1


    # Tested
    def __init__( self, lcmd_inital_commands = None, logr_cur = None ):
        """
        Initializer
        
        * lcmd_iniital_commands : List strings
                                : List of commands to run
        * logr_cur : Logger
                   : A logger to use
        """
        
        self.logr_logger = logging.getLogger() if not logr_cur else logr_cur
        """ Logger, uses the default logger. """
        
        self.dict_commands = {}
        """ Holds the relationship between commands and their dependencies and products hashed by command. """
        
        self.dict_dependencies = {}
        """ Holds the relationship between dependencies and their commands. """

        self.lstr_products = []
        """ History of products added to the pipeline. """
        
        self.lstr_dependencies = []
        """ History of the dependencies add to the pipeline """

        self.__lstr_inputs = None
        """ A list of input files. """

        self.__lstr_terminal_products = None
        """ A list of terminal products for the pipeline ( should never be deleted ). """
        
        # Load any initial commands
        if lcmd_inital_commands:
            for cmd_cur in lcmd_inital_commands:
                self.func_add_command( cmd_cur )
                
        self.li_waits_for_products = [ 5, 15, 40 ]


    @property
    def lstr_inputs( self ):
        """
        Calculate input files.
        """
        
        if self.__lstr_inputs is None:
            # Remake inputs
            self.__lstr_inputs = list( set( self.lstr_dependencies ) - set( self.lstr_products ) )
        return self.__lstr_inputs


    @property
    def lstr_terminal_products( self ):
        """
        Calculate terminal products if needed and return.
        """
        
        if self.__lstr_terminal_products is None:
            # Remake terminal products
            self.__lstr_terminal_products = list( set( self.lstr_products ) - set( self.lstr_dependencies ) )
        return self.__lstr_terminal_products
        
    
    # Tested
    def func_add_command( self, cmd_cur ):
        """
        Adds a command and outputs to the dependency tree.
        
        * cmd_cur : Command
                    Command to add to the dependency tree.
                    
        * Return : Boolean
                   True indicates the command was successfully added.
        """
        
        # Only allow complete commands with product, dependencies, and commands to be handled.
        if cmd_cur.func_is_valid():
            # Each command should be unique
            if cmd_cur.str_command in self.dict_commands:
                return False
            
            # Add command
            self.dict_commands[ cmd_cur.str_command ] = [ cmd_cur.lstr_dependencies, cmd_cur.lstr_products ]
            
            # Also add into a dict that keeps tract of dependencies between commands and files
            for str_dependency in cmd_cur.lstr_dependencies:
                # Update command and dependency relationship
                lstr_commands = self.dict_dependencies.setdefault( str_dependency, [] )
                if not cmd_cur.str_command in lstr_commands:
                    lstr_commands.append( cmd_cur.str_command )
                if str_dependency not in self.lstr_dependencies:
                    self.lstr_dependencies.append( str_dependency )

            # Add product to the product list for check checking
            for str_product in cmd_cur.lstr_products:
                if not str_product in self.lstr_products:
                    self.lstr_products.append( str_product )
                    
            # Indicate the terminal need to be recalculated 
            self.__lstr_terminal_products = None

            return True
        return False


    # Tested
    def func_complete_command( self, cmd_cur, f_wait = None, f_test = False ):
        """
        Checks that the products are made for the command and then
        retains that the command is completed. This helps resolve if dependencies are not longer
        needed to make targets. If a directory is a product, the directory must not be empty
        or it is not considered a completed command.
        
        * cmd_cur : Command
                    The command which will have products checked for existence
                                 
        * f_test : Boolean
                   Enables a testing mode. False indicates only logging occurs
        
        * Return  : Boolean
                    True indicates the command was completed.
                    This means dependency relationships are removed for the 
                    completed command.
        """

        # If both products and dependencies exist
        # Remove the dependency relationships for the command
        self.logr_logger.debug( "DependencyTree.func_complete_command: Checking products" )
        if self.func_products_are_made( cmd_cur, f_wait = f_wait ) or f_test:
            self.logr_logger.info( "DependencyTree.func_complete_command: Products are made" )
            
            # Update the dependency relationships
            if not self.func_remove_dependency_relationships( cmd_cur ):
                self.logr_logger.error( "DependencyTree.func_complete_command: Could not update dependency relationships." )
                return False

            # Completed cleaning return true
            return True

        # Return false indicating the command state was invalid for completing.
        self.logr_logger.info( "DependencyTree.func_complete_command: Products were not created." )
        return False

    
    # Tested
    def func_dependencies_are_made( self, cmd_cur ):
        """ 
        Check to make sure each dependency exists. These dependencies are expected to be files.
        
        * cmd_cur : Command
                    Command to check that it's dependencies exist.
                    
        * Return : Boolean
                   True indicates all dependencies exist.
        """

        return self.func_paths_made( cmd_cur.lstr_dependencies )

    
    # Tested
    def func_dependency_is_needed( self, str_dependency ):
        """
        Checks to see if a dependency is needed to create a product.
        
        * str_dependency : String
                           Path to dependency to be checked.
                           
        * Return : Boolean
                   True indicates the dependency is still needed for other commands.
        """

        if str_dependency:

            # Return if the length of the commands associated with the dependency is greater than 1
            # Which would indicate those commands have not been completed yet and the
            # dependency is still needed.
            return len( self.dict_dependencies.get( str_dependency, [] ) ) > 0
        return False


    # Tested
    def func_is_used_intermediate_file( self, str_path ):
        """
        Returns if a file is an intermediate file that has already been used
        and is no longer needed.
        
        * str_path : String
                   : path to file
                   
        * Return : Boolean
                 : True indicates is an intermediate file that is used.
        """
        
        f_is_product = str_path in self.lstr_products
        f_is_terminal = self.func_product_is_terminal( str_path )
        f_is_needed = self.func_dependency_is_needed( str_path )
        if( f_is_product and ( not f_is_terminal ) and ( not f_is_needed ) ):
            return True
        return False
        
        
    def func_paths_made( self, lstr_files ):
        """
        Check to see if paths are made, could be a folder or a file.
        
        * lstr_Files : List of strings
                       Paths to files/folders to check and see if they exist.
                       
        * Return : Boolean
                   True indicates they all exist.
        """

        if lstr_files:
            self.logr_logger.info(" ".join( [ "DependencyTree.func_paths_made: Currently at ", os.getcwd() ] ) )
            for str_file in lstr_files:
                self.logr_logger.info( "".join( [ "DependencyTree.func_paths_made: Checking that ", str_file, " was made." ] ) )
                if not os.path.exists( str_file ):
                    self.logr_logger.info( "DependencyTree.func_paths_made: Does not exist." )
                    # Return false of not existent path
                    return False
                if os.path.isdir( str_file ) and not os.listdir( str_file ):
                    self.logr_logger.info( "DependencyTree.func_paths_made: This folder is empty." )
                    # Return false for an empty directory
                    return False
            # Return true for a file or directory that contains things
            self.logr_logger.info( "DependencyTree.func_paths_made: Files were made." )
            return True
        # Return false for bad file names
        return False 
    
    
    # Tested
    def func_products_are_made( self, cmd_cur, f_wait = True ):
        """
        Check to see if products are made.
        This assumes a product may just have been made and could be subject to lag.
        A wait is incorporated into the check, by default 3 attempts occur at progressively
        more wait.
        
        * cmd_cur : Command
                    Command to check that it's products exist.
                    
        * Return : Boolean
                   True indicates all products exist.
        """

        # Try a tiered approach to checking for products
        # Sometimes products are made but there is a lag on the server / cluster
        # Check and then on failure try in 5 seconds, 15 seconds and 40 seconds then fail.
        for i_wait_in_seconds in self.li_waits_for_products if f_wait else [0]:
            if self.func_paths_made( cmd_cur.lstr_products ):
                return True
            time.sleep( i_wait_in_seconds )
        return False


    # Tested
    def func_product_is_terminal( self, str_product ):
        """
        Returns if the product is terminal in the commands.
        Terminal here means no command uses the product as a dependency.
        
        * str_product : String
                        Path to file to check if it is terminal in the dependency tree.
                        
        * Return : Boolean
                   True indicates that the product is terminal.
        """
        
        # Handle the case where the dependencies are empty
        return str_product in self.lstr_terminal_products
    
    
    # Tested
    def func_remove_dependency_relationships( self, cmd_cur):
        """
        Indicates that the dependencies for the command no longer need to be built.
        
        * cmd_cur : Command
                    Command containing dependencies to indicate they are not needed.
                    
        * Return : Boolean
                   True indicates all dependencies were indicates to be stale and not needed
        """

        # Return false on where there are no dependencies
        if not len( self.dict_dependencies ):
            return False
        
        if cmd_cur.func_is_valid():
            # For every dependency
            # Remove the command from the dependency as an association
            # If this reduces the dependency to having no commands left
            # It is stale and not needed and so remove the dependency from the DependencyTree
            for str_dependency in cmd_cur.lstr_dependencies:
                lstr_commands = self.dict_dependencies.get( str_dependency, [] )
                # The dependency should exist with at least the current command.
                # So this state is an error
                if not len( lstr_commands ):
                    self.logr_logger.info( "DependencyTree.func_remove_dependency_relationships: No dependencies found ." )
                    self.logr_logger.info( " ".join( [ "DepenencyTree.func_remove_dependency_relationships: Dependency=", str_dependency ] ) )
                    self.logr_logger.debug( str( self.dict_dependencies ) )
                    return False
                # Remove the command for the dependency
                if cmd_cur.str_command in lstr_commands:
                    lstr_commands.remove( cmd_cur.str_command )
                # If the dependency has no other command interested in it, now that the current is removed, then remove it as a dependency
                if not self.dict_dependencies.get( str_dependency, [] ):
                    self.dict_dependencies.pop( str_dependency, False )
            return True
        else:
            self.logr_logger.info( " ".join( [ "DependencyTree.func_remove_dependency_relationships: Command not valid. Command =", str( cmd_cur ) ] ) )
        return False


    def func_remove_wait( self ):
        """
        Turn off the wait for looking for products.
        """
        
        self.li_waits_for_products = [0]
        

    # Tested
    def func_show_active_dependencies( self ):
        """
        Show the dependencies that are still active.
        
        * Return : String
                   A list of dependencies still needed in the pipeline.
        """
        
        return ", ".join( sorted( self.dict_dependencies.keys() ) )            


    def __str__( self ):
        """
        String representation of the internal state of the object.
        
        * Return : String
                   String representation of the relationship between the 
                   commands and products/dependents
        """
        
        lstr_return = []
        for str_command in sorted( self.dict_commands.keys() ):
            lls_dep_prods = self.dict_commands.get( str_command, ["",""] )
            lstr_return.append( "".join( [ "Command: ", str_command,
                                 "\nDependencies: ", str( lls_dep_prods[ self.C_INT_DEPENDENCIES_INDEX ] ),
                                 "\nProducts: ", str( lls_dep_prods[ self.C_INT_PRODUCTS_INDEX ] ) ] ) )
        return "\n".join( lstr_return )
