
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Graph
import logging
import os
import Resource
import time

class DependencyTree:
    """
    This object manages dependencies tracking for command line.

    graph_commands is a graph that holds the commands and how they relate to each other.
    
    dict_dependencies is a dictionary that holds dependencies and their related commands
    { string_dependency: [ str_command, str_command,...] }
    
    lstr_products is a list of products added (helps determine currently terminal files).
    
    lstr_dependencies is a list of dependencies add (help determine currently terminal files).
    
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
        
        self.graph_commands = DependencyGraph.DependencyGraph()
        """ Graph holds the relationship between commands. """

        # Load any initial commands
        if lcmd_inital_commands:
            for cmd_cur in lcmd_inital_commands:
                self.func_add_command( cmd_cur )
 
        self.li_waits_for_products = [ 5, 15, 40 ]

        self.lstr_products = self.graph_commands.func_get_products()
        """ History of products added to the pipeline. """
        
        self.lstr_dependencies = self.graph_commands.func_get_dependencies()
        """ History of the dependencies add to the pipeline """

        self.__lstr_inputs = self.graph_commands.func_get_input_files()
        """ A list of input files. """

        self.__lstr_terminal_products = self.graph_commands.func_get_terminal_vertices()
        """ A list of terminal products for the pipeline ( should never be deleted ). """
        

    @property
    def lstr_inputs( self ):
        """
        Calculate input files.
        """
        
        if self.__lstr_inputs is None:
            # Remake inputs
            self.__lstr_inputs = self.graph_commands.func_get_inputs_files()
        return self.__lstr_inputs

    @property
    def lstr_products( self ):
        """
        Calculate the products if needed and return
        """

        if self.__lstr_products is None:
            self.__lstr_products = self.graph_commands.func_get_dependencies()
        return self.__lstr_products

    @property
    def lstr_dependencies( self ):
        """
        Calculate the dependencies if needed and return
        """

        if self.__lstr_dependencies is None:
            self.__lstr_products = self.graph_commands.func_get_products()
        return self.__lstr_dependencies

    @property
    def lstr_terminal_products( self ):
        """
        Calculate terminal products if needed and return.
        """
        
        if self.__lstr_terminal_products is None:
            self.__lstr_terminal_products = self.graph_commands.func_get_terminal_products()
        return self.__lstr_terminal_products
        
    
    # Tested
    # Edited
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
            if cmd_cur in self.graph_commands:
                return False
            
            # Add command (each should be unique so this is not wrtting over)
            self.graph_commands.func_add_vertex( cmd_cur )

            # Add dependencies
            for vtx_dependency in cmd_cur.lstr_dependencies:
                self.graph_commands.func_merge_vertex( vtx_dependency )
            # Add products
            for vtx_product in cmd_cur.lstr_products:
                self.graph_commands.func_merge_vertex( vtx_product )
 
            # Indicate the terminal, dependencies, and products need to be recalculated 
            self.__lstr_terminal_products = None
            self.__lstr_dependencies = None
            self.__lstr_products = None
            self.__lstr_inputs = None

            return True
        return False


    # Tested
    # Compat
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
                # Update the products
                for rsc_prod in cmd_cur.func_get_children():
                    rsc_prod.str_status = Resource.STR_MADE
                cmd_cur.str_status = Command.STR_ERROR
                return False

            # Completed cleaning return true
            # Update the products
            for rsc_prod in cmd_cur.func_get_children():
                rsc_prod.str_status = Resource.STR_MADE
            cmd_cur.str_status = Command.STR_COMPLETE 
            return True

        # Return false indicating the command state was invalid for completing.
        self.logr_logger.info( "DependencyTree.func_complete_command: Products were not created." )
        # If error update the files were made on an error run and indicate the command was an error.
        for rsc_prod in cmd_cur.func_get_children():
            rsc_prod.str_status = Resource.STR_ERROR
        cmd_cur.str_status = Command.ERROR
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
    # Update
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
    # Compat
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
        
    # Used in testing
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
            for rsc_file in lstr_files:
                str_file = rsc_file.str_id
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
    # Compat
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
    

    def func_remove_wait( self ):
        """
        Turn off the wait for looking for products.
        """
        
        self.li_waits_for_products = [0]
        

#    # Tested
#    def func_show_active_dependencies( self ):
#        """
#        Show the dependencies that are still active.
#        
#        * Return : String
#                   A list of dependencies still needed in the pipeline.
#        """
#        
#        return ", ".join( sorted( self.dict_dependencies.keys() ) )            

    def __str__( self ):
        return "Graph{" + str( len( self.graph_commands ) ) + "}"

    def func_detail( self ):
        """
        String representation of the internal state of the object.
        
        * Return : String
                   String representation of the relationship between the 
                   commands and products/dependents
        """
       
        return "\n".join([ "Graph{ " + self.graph_commands.func_detail() + "}", 
                           "Products{ " + str( sorted( [ rsc_products.str_id for rsc_product in self.lstr_products ] ) ) + "}", 
                           "Dependencies{ " + str( sorted( [ rsc_dep.str_id for rsc_dep in self.lstr_dependencies ] ) ) + "}", 
                           "Inputs{ " + str( sorted( [ rsc_in.str_id for rsc_in in self.__lstr_inputs ] ) ) + "}", 
                           "Terminal_Products{ " + str(sorted([ vtx_product.str_id for vtx_product in self.__lstr_terminal_products ])) + "}"] )

         
#        lstr_return = []
#        for vtx_command in self.graph_commands:
#            lls_dep_prods = self.graph_commands.get( str_command, ["",""] )
#            lstr_return.append( "".join( [ "Command: ", str_command,
#                                 "\nDependencies: ", str( lls_dep_prods[ self.C_INT_DEPENDENCIES_INDEX ] ),
#                                 "\nProducts: ", str( lls_dep_prods[ self.C_INT_PRODUCTS_INDEX ] ) ] ) )
#        return "\n".join( lstr_return )
