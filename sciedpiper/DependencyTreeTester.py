
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import DependencyTree
import ParentPipelineTester
import os
import unittest


class DependencyTreeTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the DependencyTree object.
    """
    
    
    def test_init_for_no_command( self ):
        """ Test initialization with no commands """
        
        dt_tree = DependencyTree.DependencyTree()
        self.func_test_equals( dt_tree, "" )
        
    
    def test_init_for_one_command( self ):
        """ Test initialization for one command """

        str_env = os.path.join( self.str_test_directory, "test_init_for_one_command" )
        str_answer = "\n".join( [ "Command: Command_1",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_1\', \'"+
                                  str_env+os.path.sep+"Dependency_2\']",
                                  "Products: [\'"+str_env+os.path.sep+"Product_1\']" ] )
        lcmd_commands = [ Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ os.path.join( str_env, "Dependency_1" ),
                                                                    os.path.join( str_env, "Dependency_2" ) ],
                                           lstr_cur_products = [ os.path.join( str_env, "Product_1" ) ] ) ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( dt_tree, str_answer )
        

    def test_init_for_three_duplicate_commands( self ):
        """ Test initialization for three duplicate commands. """

        str_env = os.path.join( self.str_test_directory, "test_init_for_three_duplicate_commands" )
        str_answer = "\n".join( [ "Command: Command_1",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_1\', \'"+
                                  str_env+os.path.sep+"Dependency_2\']",
                                  "Products: [\'"+str_env+os.path.sep+"Product_1\']" ] )
        cmd_cur = Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ os.path.join( str_env, "Dependency_1" ),
                                                                    os.path.join( str_env, "Dependency_2" ) ],
                                           lstr_cur_products = [ os.path.join( str_env, "Product_1" ) ] )
        lcmd_commands = [ cmd_cur, cmd_cur, cmd_cur ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( dt_tree, str_answer )


    def test_init_for_three_commands( self ):
        """ Test initialization for one command """

        str_env = os.path.join( self.str_test_directory, "test_init_for_three_commands" )
        str_answer = "\n".join( [ "Command: Command_1",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_1\', \'"+
                                  str_env+os.path.sep+"Dependency_2\']",
                                  "Products: [\'"+str_env+os.path.sep+"Product_1\', \'"+
                                  str_env+os.path.sep+"Product_2\', \'"+
                                  str_env+os.path.sep+"Product_3\']",
                                  "Command: Command_2",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_1\']",
                                  "Products: [\'"+str_env+os.path.sep+"Product_1\', \'"+
                                  str_env+os.path.sep+"Product_2\']",
                                  "Command: Command_3",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_1\']",
                                  "Products: [\'"+str_env+os.path.sep+"Product_1\']" ] )
        lcmd_commands = [ Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ os.path.join( str_env, "Dependency_1" ), 
                                                                    os.path.join( str_env, "Dependency_2" )],
                                           lstr_cur_products = [ os.path.join( str_env, "Product_1" ),
                                                                os.path.join( str_env, "Product_2" ), 
                                                                os.path.join( str_env, "Product_3" ) ] ),
                         Command.Command( str_cur_command = "Command_2",
                                           lstr_cur_dependencies = [ os.path.join( str_env, "Dependency_1" ) ],
                                           lstr_cur_products = [ os.path.join( str_env, "Product_1" ),
                                                                os.path.join( str_env, "Product_2" ) ] ),
                         Command.Command( str_cur_command = "Command_3",
                                           lstr_cur_dependencies = [ os.path.join( str_env, "Dependency_1" ) ],
                                           lstr_cur_products = [ os.path.join( str_env, "Product_1" ) ] ) ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( dt_tree, str_answer )


# func_add_command
    def test_func_add_command_for_invalid_command( self ):
        """ Test adding commands when an invalid command is given. """
        
        cmd_test = Command.Command( "", [], [] )
        dt_tree = DependencyTree.DependencyTree()
        f_result = dt_tree.func_add_command( cmd_test )
        self.func_test_true( not f_result )


    def test_func_add_command_for_new_command( self ):
        """ Test adding commands when a new command is given. """

        str_env = os.path.join( self.str_test_directory, "test_func_add_command_for_new_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ], 
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_result = dt_tree.func_add_command( cmd_test )
        self.func_test_true( f_result )


    def test_func_add_command_for_known_command( self ):
        """ Test adding commands when a command already in the DependencyTree are given. """

        str_env = os.path.join( self.str_test_directory, "test_func_add_command_for_known_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ],
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_add_command( cmd_test )
        f_result = dt_tree.func_add_command( cmd_test )
        self.func_test_true( not f_result )


# func_complete_command
    def test_complete_command_for_unknown_command( self ):
        """ Test attempting to complete a command that is not in the dependency tree."""
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_unknown_command" )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ],
                                      [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Dependencies_2" ) ],
                                      [ os.path.join( str_env, "Products_2" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        dt_tree.func_remove_wait()
        self.func_test_true( not dt_tree.func_complete_command( cmd_test_2 ) )
        
        
    def test_complete_command_for_empty_dependency_tree( self ):
        """ Test attempting to complete a command with an empty dependency tree."""
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_empty_dependency_tree" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ],
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        self.func_test_true( not dt_tree.func_complete_command( cmd_test ) )
        

    def test_complete_command_for_one_in_one_command_dependencies_not_made( self ):
        """
        Test attempting to complete a command when there is only one command.
        But the dependencies are not made so the complete will not occur.
        """
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_one_in_one_command_dependencies_not_made" )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ],
                                      [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        dt_tree.func_remove_wait()
        self.func_test_true( not dt_tree.func_complete_command( cmd_test_1 ) )


    def test_complete_command_for_one_in_one_command_one_product_not_made( self ):
        """
        Test attempting to complete a command when there is only one command.
        And one product is not made so the complete will not occur.
        """
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_one_in_one_command_one_product_not_made" )
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        cmd_test_1 = Command.Command( "Command_1", 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1, str_product_2 ] )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_product_1 )

        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        self.func_remove_files( [ str_dependency_1, str_dependency_2, str_product_1 ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( not f_success )


    def test_complete_command_for_one_in_one_command( self ):
        """
        Test attempting to complete a command when there is only one command.
        Checks both return value and internal state.
        """
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_one_in_one_command" )
        str_dependencies = ""
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        str_commands = "\n".join( [ "Command: Command_1",
                                  "Dependencies: "+str( [ str_dependency_1, str_dependency_2 ] ),
                                  "Products: "+str( [ str_product_1, str_product_2 ] ) ] )
        cmd_test_1 = Command.Command( "Command_1", 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1, str_product_2 ] )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_2 )

        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        f_internal_state = str_commands == str( dt_tree )
        f_internal_dep_state = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_remove_files( [ str_dependency_1, str_dependency_2, str_product_1, str_product_2 ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( f_success and f_internal_state and f_internal_dep_state )


    def test_complete_command_for_one_in_three_command( self ):
        """
        Test attempting to complete a command when there is one in two commands.
        Checks both return value and internal state.
        """

        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_one_in_three_command" )
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        str_product_3 = os.path.join( str_env, "Products_3.txt" )
        str_product_4 = os.path.join( str_env, "Products_4.txt" )
        str_product_5 = os.path.join( str_env, "Products_5.txt" )
        str_product_6 = os.path.join( str_env, "Products_6.txt" )
        str_dependencies = ", ".join( [ str_product_1, str_product_2,
                                       str_product_3, str_product_4 ] )
        str_commands = "\n".join( [ "Command: Command_1",
                                  "Dependencies: "+str( [ str_dependency_1, str_dependency_2 ] ),
                                  "Products: "+str( [ str_product_1, str_product_2 ] ),
                                  "Command: Command_2",
                                  "Dependencies: "+str( [ str_product_1, str_product_2 ] ),
                                  "Products: "+str( [ str_product_3, str_product_4 ] ),
                                  "Command: Command_3",
                                  "Dependencies: "+str( [ str_product_3, str_product_4 ] ),
                                  "Products: "+str( [ str_product_5, str_product_6 ] ) ] )
        cmd_test_1 = Command.Command( "Command_1", 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1, str_product_2 ] )
        cmd_test_2 = Command.Command( "Command_2", 
                                      [ str_product_1, str_product_2 ],
                                      [ str_product_3, str_product_4 ] )
        cmd_test_3 = Command.Command( "Command_3", 
                                      [ str_product_3, str_product_4 ],
                                      [ str_product_5, str_product_6 ] )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_3 )
        self.func_make_dummy_file( str_product_4 )
        self.func_make_dummy_file( str_product_5 )
        self.func_make_dummy_file( str_product_6 )

        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_cur = cmd_test_1 )
        f_internal_state = str_commands == str( dt_tree )
        f_internal_dep_state = str_dependencies == dt_tree.func_show_active_dependencies()

        self.func_remove_files( [ str_dependency_1, str_dependency_2, str_product_1, str_product_2,
                                 str_product_3, str_product_4, str_product_5, str_product_6 ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( f_success and f_internal_state and f_internal_dep_state )


    def test_complete_command_for_one_in_two_commands( self ):
        """
        Test attempting to complete a command when there is one in two commands.
        Checks both return value and internal state.
        """
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_one_in_two_commands" )
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        str_product_3 = os.path.join( str_env, "Products_3.txt" )
        str_product_4 = os.path.join( str_env, "Products_4.txt" )
        str_dependencies = ", ".join( [ str_product_1, str_product_2 ] )
        str_commands = "\n".join( [ "Command: Command_1",
                                  "Dependencies: "+str( [ str_dependency_1, str_dependency_2 ] ),
                                  "Products: "+str( [ str_product_1, str_product_2 ] ),
                                  "Command: Command_2",
                                  "Dependencies: "+str( [ str_product_1, str_product_2 ] ),
                                  "Products: "+str( [ str_product_3, str_product_4 ] ) ] )
        cmd_test_1 = Command.Command( "Command_1", 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1, str_product_2 ] )
        cmd_test_2 = Command.Command( "Command_2", 
                                      [ str_product_1, str_product_2 ],
                                      [ str_product_3, str_product_4 ] )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_3 )
        self.func_make_dummy_file( str_product_4 )

        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2 ] )
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        f_internal_state = str_commands == str( dt_tree )
        f_internal_dep_state = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_remove_files( [ str_dependency_1, str_dependency_2, 
                                 str_product_1, str_product_2,  
                                 str_product_3, str_product_4 ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( f_success and f_internal_state and f_internal_dep_state )


    def test_complete_command_for_two_in_two_commands( self ):
        """
        Test attempting to complete a command when there is one in two commands.
        Checks both return value and internal state.
        """
        
        str_env = os.path.join( self.str_test_directory, "test_complete_command_for_two_in_two_commands" )
        str_dependency_1 = os.path.join( str_env, "Dependencies_1.txt" )
        str_dependency_2 = os.path.join( str_env, "Dependencies_2.txt" )
        str_product_1 = os.path.join( str_env, "Products_1.txt" )
        str_product_2 = os.path.join( str_env, "Products_2.txt" )
        str_product_3 = os.path.join( str_env, "Products_3.txt" )
        str_product_4 = os.path.join( str_env, "Products_4.txt" )
        str_dependencies = ", ".join( [ ] )
        str_commands = "\n".join( [ "Command: Command_1",
                                  "Dependencies: "+str( [ str_dependency_1, str_dependency_2 ] ),
                                  "Products: "+str( [ str_product_1, str_product_2 ] ),
                                  "Command: Command_2",
                                  "Dependencies: "+str( [ str_product_1, str_product_2 ] ),
                                  "Products: "+str( [ str_product_3, str_product_4 ] ) ] )
        cmd_test_1 = Command.Command( "Command_1", 
                                      [ str_dependency_1, str_dependency_2 ],
                                      [ str_product_1, str_product_2 ] )
        cmd_test_2 = Command.Command( "Command_2", 
                                      [ str_product_1, str_product_2 ],
                                      [ str_product_3, str_product_4 ] )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_dependency_1 )
        self.func_make_dummy_file( str_dependency_2 )
        self.func_make_dummy_file( str_product_1 )
        self.func_make_dummy_file( str_product_2 )
        self.func_make_dummy_file( str_product_3 )
        self.func_make_dummy_file( str_product_4 )

        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2 ] )
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        f_success = f_success and dt_tree.func_complete_command( cmd_test_2 )
        f_internal_state = str_commands == str( dt_tree )
        f_internal_dep_state = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_remove_files( [ str_dependency_1, str_dependency_2, 
                                 str_product_1, str_product_2,  
                                 str_product_3, str_product_4 ] )
        self.func_remove_dirs( str_env )
        self.func_test_true( f_success and f_internal_state and f_internal_dep_state )


# func_dependencies_are_made
    def test_dependencies_are_made_for_no_dependencies( self ):
        """ Test checking for dependencies when there are none in the command """
        
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_no_dependencies" )
        cmd_test = Command.Command( "Command_1", [], [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_test_true( not f_success )


    def test_dependencies_are_made_for_nonexisting_file( self ):
        """ Test checking that a dependency is made which is a file which does not exist. """
        
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_nonexisting_file" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        self.func_test_true( not dt_tree.func_dependencies_are_made( cmd_test ) )


    def test_dependencies_are_made_for_existing_file( self ):
        """ Test checking that a dependency is made which is a file. """

        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_existing_file" )
        str_file_name = "dependency_1.txt"
        str_file = os.path.join( str_env, str_file_name )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file )
        
        # Test
        cmd_test = Command.Command( "Command_1", [str_file], [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_remove_files( [ str_file ] )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success )


    def test_dependencies_are_made_for_existing_files( self ):
        """ Test checking that a dependency is made which are 3 files. """

        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_existing_files" )
        str_file_name_1 = "dependency_1.txt"
        str_file_name_2 = "dependency_2.txt"
        str_file_name_3 = "dependency_3.txt"
        lstr_dependencies = [ os.path.join( str_env, str_file_name ) 
                             for str_file_name in [str_file_name_1, str_file_name_2, str_file_name_3 ] ]
        self.func_make_dummy_dir( str_env )
        for str_dep in lstr_dependencies:
            self.func_make_dummy_file( str_dep )
        
        # Test
        cmd_test = Command.Command( "Command_1", lstr_dependencies, [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_remove_files( lstr_dependencies )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success )


    def test_dependencies_are_made_for_existing_folder( self ):
        """ Test checking that a dependency is made which is a folder. """

        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_existing_folder" )
        str_folder_name = "dependency_1"
        str_folder = os.path.join( str_env, str_folder_name )
        self.func_make_dummy_dir( str_folder )
        self.func_make_dummy_file( os.path.join( str_folder, "test.txt" ) )
        
        # Test
        cmd_test = Command.Command( "Command_1", [str_folder], [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_remove_files( [ os.path.join( str_folder, "test.txt" ) ] )
        self.func_remove_dirs( [ str_folder ] )
        self.func_test_true( f_success )
        

    def test_dependencies_are_made_for_existing_empty_folder( self ):
        """ Test checking that a dependency is made which is an empty folder. """

        # Set up environment
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_existing_empty_folder" )
        str_folder_name = "dependency_1"
        str_folder = os.path.join( str_env, str_folder_name )
        self.func_make_dummy_dir( str_folder )
        
        # Test
        cmd_test = Command.Command( "Command_1", [str_folder], [ os.path.join( str_env, "Products_1") ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_remove_dirs( [ str_folder ] )
        self.func_test_true( not f_success )

        
    def test_dependencies_are_made_for_existing_folders( self ):
        """ Test checking that a dependency is made which is 2 folders. """  

        # Set up environment
        str_folder_name_1 = "dependency_1"
        str_folder_name_2 = "dependency_2"
        str_folder_name_3 = "dependency_3"
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_existing_folders" )
        lstr_dependencies = [ os.path.join( str_env, str_name ) 
                             for str_name in [ str_folder_name_1, str_folder_name_2, str_folder_name_3 ] ]
        for str_dep in lstr_dependencies:
            self.func_make_dummy_dir( str_dep )
            self.func_make_dummy_file( os.path.join( str_dep, "test.txt" ) )
        
        # Test
        cmd_test = Command.Command( "Command_1", lstr_dependencies, [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_remove_files( [ os.path.join( str_path, "test.txt" ) for str_path in lstr_dependencies ] )
        self.func_remove_dirs( lstr_dependencies )
        self.func_test_true( f_success )
        
        
    def test_dependencies_are_made_for_existing_empty_folders( self ):
        """ Test checking that a dependency is made which is 2 folders, one empty. """  

        # Set up environment
        str_folder_name_1 = "dependency_1"
        str_folder_name_2 = "dependency_2"
        str_folder_name_3 = "dependency_3"
        str_env = os.path.join( self.str_test_directory, "test_dependencies_are_made_for_existing_empty_folders" )
        lstr_dependencies = [ os.path.join( str_env, str_name ) 
                             for str_name in [ str_folder_name_1, str_folder_name_2, str_folder_name_3 ] ]
        for str_dep in lstr_dependencies:
            self.func_make_dummy_dir( str_dep )
            self.func_make_dummy_file( os.path.join( str_dep, "test.txt" ) )
        self.func_remove_files( [ os.path.join( str_env, str_folder_name_2, "test.txt" ) ] )
        
        # Test
        cmd_test = Command.Command( "Command_1", lstr_dependencies, [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_success = dt_tree.func_dependencies_are_made( cmd_test )
        self.func_remove_files( [ os.path.join( str_path, "test.txt" ) for str_path in lstr_dependencies ] )
        self.func_remove_dirs( lstr_dependencies )
        self.func_test_true( not f_success )


# func_dependency_is_needed
    def test_func_dependency_is_needed_for_empty_dependency_tree( self ):
        """ Tests behavior when the dependency tree is empty."""

        str_env = os.path.join( self.str_test_directory, "test_func_dependency_is_needed_for_empty_dependency_tree" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Product_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        self.func_test_true( not dt_tree.func_dependency_is_needed( cmd_test.lstr_dependencies[ 0 ] ) )


    def test_func_dependency_is_needed_for_not_needed_dependency_one_command( self ):
        """ Tests behavior when the dependency is not needed and the dependency tree has one command """

        str_env = os.path.join( self.str_test_directory, "test_func_dependency_is_needed_for_not_needed_dependency_one_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Product_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Dependency_2" ) ],
                                      [ os.path.join( str_env, "Product_2" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_2 ] )
        self.func_test_true( not dt_tree.func_dependency_is_needed( cmd_test.lstr_dependencies[ 0 ] ) )


    def test_func_dependency_is_needed_for_not_needed_dependency_three_command( self ):
        """ Tests behavior when the dependency is not needed and the dependency tree has three commands """

        str_env = os.path.join( self.str_test_directory, "test_func_dependency_is_needed_for_not_needed_dependency_three_command" )
        cmd_test = Command.Command( "Command_0", [ os.path.join( str_env, "Dependency_0" ) ],
                                    [ os.path.join( str_env, "Product_0" ) ] )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Product_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Product_1" ) ],
                                      [ os.path.join( str_env, "Product_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Product_2" ) ],
                                      [ os.path.join( str_env, "Product_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        self.func_test_true( not dt_tree.func_dependency_is_needed( cmd_test.lstr_dependencies[ 0 ] ) )


    def test_func_dependency_is_needed_for_needed_dependency_one_command( self ):
        """ Tests behavior when the dependency is needed and is a part of the only command."""

        str_env = os.path.join( self.str_test_directory, "test_func_dependency_is_needed_for_needed_dependency_one_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Product_1" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test ] )
        self.func_test_true( dt_tree.func_dependency_is_needed( cmd_test.lstr_dependencies[ 0 ] ) )


    def test_func_dependency_is_needed_for_needed_dependency_three_command( self ):
        """ Tests behavior when the dependency is needed and is a part of one of three commands."""

        str_env = os.path.join( self.str_test_directory, "test_func_dependency_is_needed_for_needed_dependency_three_command" )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Product_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Product_1" ) ],
                                      [ os.path.join( str_env, "Product_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Product_2" ) ],
                                      [ os.path.join( str_env, "Product_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        self.func_test_true( dt_tree.func_dependency_is_needed( cmd_test_2.lstr_dependencies[ 0 ] ) )


# func_is_used_intermediate_file
    def test_is_used_intermediate_file_for_empty_dependency_tree_bad_data( self ):
        """ Check return for bad data with an empty dependency tree """
    
        dt_tree = DependencyTree.DependencyTree( [] )
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( "" ) )
        
    
    def test_is_used_intermediate_file_for_empty_dependency_tree_good_data( self ):
        """ Check return for good data with an empty dependency tree. """

        str_product_one = os.path.abspath( "Product_1" )
        dt_tree = DependencyTree.DependencyTree( [  ] )
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( str_product_one ) )
    
    
    def test_is_used_intermediate_file_for_simple_good_case( self ):
        """ Check to see if one file is recognized as intermediary """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = []
        self.func_test_true( dt_tree.func_is_used_intermediate_file( str_product_one ) )

    
    def test_is_used_intermediary_file_for_multiple_good_case( self ):
        """ Check to see if multiple files are recognized as intermediary. """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_dependency_two = os.path.abspath( "Dependency_2" )
        str_dependency_three = os.path.abspath( "Dependency_3" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        str_product_three = os.path.abspath( "Product_3" )
        str_product_four = os.path.abspath( "Product_4" )
        str_product_five = os.path.abspath( "Product_5" )
        str_product_six = os.path.abspath( "Product_6" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = []
        dt_tree.dict_dependencies[ str_product_two ] = []
        dt_tree.dict_dependencies[ str_product_three ] = []
        self.func_test_true( dt_tree.func_is_used_intermediate_file( str_product_one ) 
                             and dt_tree.func_is_used_intermediate_file( str_product_two )
                             and dt_tree.func_is_used_intermediate_file( str_product_three ) )
    
    
    def test_is_used_intermediary_file_for_one_not_product( self ):
        """ Check to see if a file is recognized as not a product. """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = []
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( str_dependency_one ) )
    
    
    def test_is_used_intermediary_file_for_mult_not_product( self ):
        """ Check to see if mult files are recognized as not a product. """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_dependency_two = os.path.abspath( "Dependency_2" )
        str_dependency_three = os.path.abspath( "Dependency_3" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        str_product_three = os.path.abspath( "Product_3" )
        str_product_four = os.path.abspath( "Product_4" )
        str_product_five = os.path.abspath( "Product_5" )
        str_product_six = os.path.abspath( "Product_6" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = []
        dt_tree.dict_dependencies[ str_product_three ] = []
        self.func_test_true( not ( dt_tree.func_is_used_intermediate_file( str_dependency_one )
                             and dt_tree.func_is_used_intermediate_file( str_dependency_two )
                             and dt_tree.func_is_used_intermediate_file( str_dependency_three ) ) )

    
    def test_is_used_intermediary_file_for_one_terminal( self ):
        """ Check to see if a file is recognized as terminal. """
        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = []
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( str_dependency_one ) )
        
    
    def test_is_used_intermediary_file_for_mult_terminal( self ):
        """ Check to see if mult files are recognized as terminal. """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_dependency_two = os.path.abspath( "Dependency_2" )
        str_dependency_three = os.path.abspath( "Dependency_3" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        str_product_three = os.path.abspath( "Product_3" )
        str_product_four = os.path.abspath( "Product_4" )
        str_product_five = os.path.abspath( "Product_5" )
        str_product_six = os.path.abspath( "Product_6" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = []
        dt_tree.dict_dependencies[ str_product_three ] = []
        self.func_test_true( not( dt_tree.func_is_used_intermediate_file( str_product_four )
                             and dt_tree.func_is_used_intermediate_file( str_product_five )
                             and dt_tree.func_is_used_intermediate_file( str_product_six ) ) )

    
    def test_is_used_intermediary_file_for_one_needed( self ):
        """ Check to see if a file is recognized as needed. """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = [ str_product_two ]
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( str_product_one ) )

    
    def test_is_used_intermediary_file_for_mult_needed( self ):
        """ Check to see if mult files are recognized as needed. """

        str_dependency_one = os.path.abspath( "Dependency_1" )
        str_dependency_two = os.path.abspath( "Dependency_2" )
        str_dependency_three = os.path.abspath( "Dependency_3" )
        str_product_one = os.path.abspath( "Product_1" )
        str_product_two = os.path.abspath( "Product_2" )
        str_product_three = os.path.abspath( "Product_3" )
        str_product_four = os.path.abspath( "Product_4" )
        str_product_five = os.path.abspath( "Product_5" )
        str_product_six = os.path.abspath( "Product_6" )
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = [ str_product_four ]
        dt_tree.dict_dependencies[ str_product_two ] = [ str_product_five ]
        dt_tree.dict_dependencies[ str_product_three ] = [ str_product_six ]
        self.func_test_true( not ( dt_tree.func_is_used_intermediate_file( str_product_one )
                             and dt_tree.func_is_used_intermediate_file( str_product_two )
                             and dt_tree.func_is_used_intermediate_file( str_product_three ) ) )
        
# func_products_are_made
    def test_products_are_made_for_no_dependencies( self ):
        """ Test checking for products when there are none in the command """

        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_no_dependencies" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], [] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_test_true( not f_success )


    def test_products_are_made_for_nonexisting_file( self ):
        """ Test checking that a product is made which is a file which does not exist. """

        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_nonexisting_file" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( self.str_test_directory, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        self.func_test_true( not dt_tree.func_products_are_made( cmd_test ) )


    def test_products_are_made_for_existing_file( self ):
        """ Test checking that a product is made which is a file. """

        # Set up environment
        str_file_name = "product_1.txt"
        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_existing_file" )
        str_file = os.path.join( str_env, str_file_name )
        self.func_make_dummy_dir( str_env )
        self.func_make_dummy_file( str_file )
        
        # Test
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], [ str_file ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_remove_files( [str_file] )
        self.func_remove_dirs( [ os.path.join( str_env ) ] )
        self.func_test_true( f_success )


    def test_products_are_made_for_existing_files( self ):
        """ Test checking that a product is made which are 3 files. """

        # Set up environment
        str_file_name_1 = "product_1.txt"
        str_file_name_2 = "product_2.txt"
        str_file_name_3 = "product_3.txt"
        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_existing_files" )
        lstr_products = [ os.path.join( str_env, str_file_name ) 
                             for str_file_name in [str_file_name_1, str_file_name_2, str_file_name_3 ] ]
        self.func_make_dummy_dir( str_env )
        for str_prod in lstr_products:
            self.func_make_dummy_file( str_prod )
        
        # Test
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env,"Dependency_1" ) ], lstr_products )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_remove_files( lstr_products )
        self.func_remove_dirs( [ str_env ] )
        self.func_test_true( f_success )


    def test_products_are_made_for_existing_folder( self ):
        """ Test checking that a product is made which is a folder. """

        # Set up environment
        str_test_env = "test_products_are_made_for_existing_folder"
        str_folder_name = "product_1"
        str_folder = os.path.join( self.str_test_directory, str_test_env, str_folder_name )
        str_dependency = os.path.join( self.str_test_directory, str_test_env,"Dependency_1" )
        self.func_make_dummy_dir( os.path.join( self.str_current_dir, str_folder ) )
        self.func_make_dummy_file( os.path.join( self.str_current_dir, str_folder, "test.txt" ) )
        
        # Test
        cmd_test = Command.Command( "Command_1", [ str_dependency ], [ str_folder ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_remove_files( [ os.path.join( self.str_current_dir, str_folder, "test.txt" ) ] )
        self.func_remove_dirs( [ os.path.join( self.str_current_dir, str_folder ) ] )
        self.func_test_true( f_success )
        
    
    def test_products_are_made_for_existing_empty_folder( self ):
        """ Test checking that a product is made which is an empty folder. """

        # Set up environment
        str_folder_name = "product_1"
        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_existing_empty_folder" )
        str_folder = os.path.join( str_env, str_folder_name )
        self.func_make_dummy_dir( str_folder )
        
        # Test
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], [ str_folder ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_remove_dirs( [ str_folder ] )
        self.func_test_true( not f_success )
        
        
    def test_products_are_made_for_existing_folders( self ):
        """ Test checking that a product is made which is 2 folders. """  

        # Set up environment
        str_folder_name_1 = "product_1"
        str_folder_name_2 = "product_2"
        str_folder_name_3 = "product_3"
        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_existing_folders" )
        lstr_products = [ os.path.join( str_env, str_name ) 
                             for str_name in [ str_folder_name_1, str_folder_name_2, str_folder_name_3 ] ]
        for str_prod in lstr_products:
            self.func_make_dummy_dir( str_prod )
            self.func_make_dummy_file( os.path.join( str_prod, "test.txt" ) )
        self.func_remove_files( [ os.path.join( str_env, str_folder_name_2, "test.txt" ) ] )
        
        # Test
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], lstr_products )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_remove_files( [ os.path.join( str_path, "test.txt" ) for str_path in lstr_products ] )
        self.func_remove_dirs( lstr_products )
        self.func_test_true( not f_success )
        
    
    def test_products_are_made_for_existing_empty_folders( self ):
        """ Test checking that a product is made which is 2 folders, one empty. """  

        # Set up environment
        str_folder_name_1 = "product_1"
        str_folder_name_2 = "product_2"
        str_folder_name_3 = "product_3"
        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_existing_empty_folders" )
        lstr_products = [ os.path.join( str_env, str_name ) 
                             for str_name in [ str_folder_name_1, str_folder_name_2, str_folder_name_3 ] ]
        for str_prod in lstr_products:
            self.func_make_dummy_dir( str_prod )
            self.func_make_dummy_file( os.path.join( str_prod, "test.txt" ) )
        
        # Test
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], lstr_products )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_products_are_made( cmd_test )
        self.func_remove_files( [ os.path.join( str_path, "test.txt" ) for str_path in lstr_products ] )
        self.func_remove_dirs( lstr_products )
        self.func_test_true( f_success )


# func_product_is_terminal
    def test_func_product_is_terminal_for_empty_dependency_tree( self ):
        """ Test if a dependency is terminal when the dependency tree is empty. """
        
        str_env = os.path.join( self.str_current_dir, "test_func_product_is_terminal_for_empty_dependency_tree" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Product_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        self.func_test_true( not dt_tree.func_product_is_terminal( cmd_test.lstr_products[ 0 ] ) )

        
    def test_func_product_is_terminal_for_unknown_dependency( self ):
        """ Test if a dependency is terminal when it is actually unknown. """

        str_env = os.path.join( self.str_current_dir, "test_func_product_is_terminal_for_unknown_dependency" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Product_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Dependency_2" ) ],
                                      [ os.path.join( str_env, "Product_2" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test ] )
        self.func_test_true( not dt_tree.func_product_is_terminal( cmd_test_2.lstr_products[ 0 ] ) )

        
    def test_func_product_is_terminal_for_one_command( self ):
        """ Test if a dependency is terminal when there is only one command. So must be terminal. """

        str_env = os.path.join( self.str_current_dir, "test_func_product_is_terminal_for_one_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Product_1" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test ] )
        self.func_test_true( dt_tree.func_product_is_terminal( cmd_test.lstr_products[ 0 ] ) )


    def test_func_product_is_terminal_for_false_with_three_commands( self ):
        """ Test if a dependency is terminal when there are three commands and it is NOT terminal """

        str_env = os.path.join( self.str_current_dir, "test_func_product_is_terminal_for_false_with_three_commands" )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Product_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Product_1" ) ],
                                      [ os.path.join( str_env, "Product_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Product_2" ) ],
                                      [ os.path.join( str_env, "Product_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        self.func_test_true( not dt_tree.func_product_is_terminal( cmd_test_2.lstr_products[ 0 ] ) )


    def test_func_product_is_terminal_for_true_with_three_commands( self ):
        """ Test if a dependency is terminal when there are three commands and it is terminal """

        str_env = os.path.join( self.str_current_dir, "test_func_product_is_terminal_for_true_with_three_commands" )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Product_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Product_1" ) ],
                                      [ os.path.join( str_env, "Product_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Product_2" ) ],
                                      [ os.path.join( str_env, "Product_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        self.func_test_true( dt_tree.func_product_is_terminal( cmd_test_3.lstr_products[ 0 ] ) )
 

# func_remove_dependency_relationships
    def test_func_remove_dependency_relationships_for_empty_tree( self ):
        """ Tests removing relationships on an empty dependency tree """

        str_env = os.path.join( self.str_test_directory, "test_products_are_made_for_existing_empty_folders" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        self.func_test_true( not dt_tree.func_remove_dependency_relationships( cmd_test ) )


    def test_func_remove_dependency_relationships_for_unknown_dependency( self ):
        """ Tests removing relationships on a dependency that does not exist """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_unknown_dependency" )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], 
                                      [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ],
                                      [ os.path.join( str_env, "Products_2" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_2 ] )
        self.func_test_true( not dt_tree.func_remove_dependency_relationships( cmd_test_1 ) )


    def test_func_remove_dependency_relationships_for_one_in_one_commands( self ):
        """ Tests removing relationships on a command when it is the only one """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_one_in_one_commands" )
        str_dependencies = ""
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], 
                                      [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        f_removal = dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_internal_state_matches = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_test_true( f_removal and f_internal_state_matches )
        

    def test_func_remove_dependency_relationships_for_one_in_one_with_mult_dep( self ):
        """ 
        Tests removing relationships on a command when is only one command but that command
        has multiple dependencies to remove
        """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_one_in_one_with_mult_dep" )
        str_commands = "\n".join( [ "Command: Command_11",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_11\', \'"+
                                  str_env+os.path.sep+"Dependency_12\', \'"+
                                  str_env+os.path.sep+"Dependency_13\']",
                                  "Products: [\'"+str_env+os.path.sep+
                                  "Products_11\', \'"+str_env+os.path.sep+
                                  "Products_12\', \'"+str_env+os.path.sep+
                                  "Products_13\']" ] )
        str_dependencies = ""
        cmd_test_1 = Command.Command( "Command_11", [ os.path.join( str_env, "Dependency_11" ),
                                                     os.path.join( str_env, "Dependency_12" ),
                                                     os.path.join( str_env, "Dependency_13" )  ],
                                      [ os.path.join( str_env, "Products_11" ),
                                       os.path.join( str_env, "Products_12" ),
                                       os.path.join( str_env, "Products_13" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_command_state = str_commands == str( dt_tree )
        f_dependency_state = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_test_true( f_command_state and f_dependency_state )


    def test_func_remove_dependency_relationships_for_one_in_three_commands( self ):
        """ Tests removing relationships on a command when there are three """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_one_in_three_commands" )
        str_dependencies = str_env+os.path.sep+"Products_1, "+str_env+os.path.sep+"Products_2"
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ],
                                      [ os.path.join( str_env, "Products_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Products_2" ) ],
                                      [ os.path.join( str_env, "Products_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        f_removal = dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_internal_state_matches = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_test_true( f_removal and f_internal_state_matches )
        

    def test_func_remove_dependency_relationships_for_two_in_three_commands( self ):
        """ Tests removing relationships on a command when there are three """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_two_in_three_commands" )
        str_dependencies = str_env+os.path.sep+"Products_2"
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ],
                                      [ os.path.join( str_env, "Products_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Products_2" ) ],
                                      [ os.path.join( str_env, "Products_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        f_removal = dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_removal = f_removal and dt_tree.func_remove_dependency_relationships( cmd_test_2 )
        f_internal_state_matches = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_test_true( f_removal and f_internal_state_matches )


    def test_func_remove_dependency_relationships_for_three_in_three_commands( self ):
        """ Tests removing relationships on a command when there are three """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_three_in_three_commands" )
        str_dependencies = ""
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ],
                                      [ os.path.join( str_env, "Products_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Products_2" ) ],
                                      [ os.path.join( str_env, "Products_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        f_removal = dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_removal = f_removal and dt_tree.func_remove_dependency_relationships( cmd_test_2 )
        f_removal = f_removal and dt_tree.func_remove_dependency_relationships( cmd_test_3 )
        f_internal_state_matches = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_test_true( f_removal and f_internal_state_matches )
        

    def test_func_remove_dependency_relationships_for_three_in_three_commands_dictcommands( self ):
        """ 
        Tests removing relationships on a command when there are three that the internal
        information about the commands is not modified, just the dependencies between them
        and documents
        """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_three_in_three_commands_dictcommands" )
        str_commands = "\n".join( [ "Command: Command_1",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Dependency_1\']",
                                  "Products: [\'"+str_env+os.path.sep+"Products_1\']",
                                  "Command: Command_2",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Products_1\']",
                                  "Products: [\'"+str_env+os.path.sep+"Products_2\']",
                                  "Command: Command_3",
                                  "Dependencies: [\'"+str_env+os.path.sep+"Products_2\']",
                                  "Products: [\'"+str_env+os.path.sep+"Products_3\']" ] )
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ], [ os.path.join( str_env, "Products_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Products_2" ) ], [ os.path.join( str_env, "Products_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        dt_tree.func_remove_dependency_relationships( cmd_test_2 )
        dt_tree.func_remove_dependency_relationships( cmd_test_3 )
        self.func_test_equals( str_commands, str( dt_tree ) )


    def test_func_remove_dependency_relationships_for_one_in_multiple_times( self ):
        """ Tests removing relationships on a command when removed a second time. """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_one_in_multiple_times" )
        str_dependencies = str_env+os.path.sep+"Products_1, "+str_env+os.path.sep+"Products_2"
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ],
                                      [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ],
                                      [ os.path.join( str_env, "Products_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Products_2" ) ],
                                      [ os.path.join( str_env, "Products_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        f_removal = dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_removal = f_removal and not dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        f_internal_state_matches = str_dependencies == dt_tree.func_show_active_dependencies()
        self.func_test_true( f_removal and f_internal_state_matches )


# func_show_active_dependencies
    def test_func_show_active_dependencies_none( self ):
        """ Tests the results of an empty dependency tree """

        str_answer = ""
        dt_tree = DependencyTree.DependencyTree( [ ] )
        str_result = dt_tree.func_show_active_dependencies()
        self.func_test_equals(str_answer, str_result)
    

    def test_func_show_active_dependencies_one( self ):
        """ Tests the results of a dependency tree with one active dependency """

        str_env = os.path.join( self.str_test_directory, "test_func_show_active_dependencies_one" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1" )
        str_product_1 = os.path.join( str_env, "Products_1" )
        str_product_2 = os.path.join( str_env, "Products_2" )
        str_product_3 = os.path.join( str_env, "Products_3" )
        str_answer = ", ".join( sorted( [ str_dependency_1, str_product_1, str_product_2 ]) )
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ],
                                      [ str_product_1 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_product_1 ],
                                      [ str_product_2 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_2 ],
                                      [ str_product_3 ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        str_result = dt_tree.func_show_active_dependencies()
        self.func_test_equals(str_answer, str_result)
    

    def test_func_show_active_dependencies_many( self ):
        """ Tests the results of a dependency tree with 3 active dependency """

        str_env = os.path.join( self.str_test_directory, "test_func_show_active_dependencies_many" )
        str_dependency_1 = os.path.join( str_env, "Dependency_1" )
        str_product_1 = os.path.join( str_env, "Products_1" )

        str_answer = ", ".join( sorted( [ str_dependency_1 ]) )
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ],
                                      [ str_product_1 ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        str_result = dt_tree.func_show_active_dependencies()
        self.func_test_equals(str_answer, str_result)


#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( DependencyTreeTester )
