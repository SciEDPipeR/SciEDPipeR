
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
import Resource
import unittest


class DependencyTreeTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the DependencyTree object.
    """


    def test_init_for_no_command( self ):
        """ Test initialization with no commands """
       
        str_answer = "\n".join( [ "Graph{ Graph:VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }}",
                                  "Products{ []}",
                                  "Dependencies{ []}",
                                  "Inputs{ []}",
                                  "Terminal_Products{ []}" ] )
        dt_tree = DependencyTree.DependencyTree()
        self.func_test_equals( str_answer, dt_tree.func_detail() )


    def test_init_for_one_command( self ):
        """ Test initialization for one command """

        str_env = os.path.join( self.str_test_directory, "test_init_for_one_command" ) + os.path.sep
        str_answer = "\n".join([ "".join([
           "Graph{ Graph:VERTEX{ ID=" + str_env + "Dependency_1;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
           "VERTEX{ ID=" + str_env + "Dependency_2;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
           "VERTEX{ ID=" + str_env + "Product_1;Parents=['Command_1'];Children=[];Type=RESOURCE };Command: Command_1; Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1'],PATH: " + str_env + "Dependency_2, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: " + str_env + "Product_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [];",
           "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['" + str_env + "Dependency_1', '" + str_env + "Dependency_2'];Type=VERTEX }}" ] ),
           "Products{ ['" + str_env + "Product_1']}",
           "Dependencies{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}",
           "Inputs{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}",
           "Terminal_Products{ ['" + str_env + "Product_1']}" ])

        lcmd_commands = [ Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ str_env + "Dependency_1",
                                                                     str_env + "Dependency_2" ],
                                           lstr_cur_products = [ str_env + "Product_1" ] ) ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( str_answer, dt_tree.func_detail() )
 

    def test_init_for_three_duplicate_commands( self ):
        """ Test initialization for three duplicate commands. """

        str_env = os.path.join( self.str_test_directory, "test_init_for_three_duplicate_commands" ) + os.path.sep
        str_answer = "\n".join([ "".join([
           "Graph{ Graph:VERTEX{ ID=" + str_env + "Dependency_1;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
           "VERTEX{ ID=" + str_env + "Dependency_2;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
           "VERTEX{ ID=" + str_env + "Product_1;Parents=['Command_1'];Children=[];Type=RESOURCE };Command: Command_1;",
           " Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2,",
           " Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1'],PATH: " + str_env + "Dependency_2, CLEAN: 2,",
           " Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: " + str_env + "Product_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [];",
           "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['" + str_env + "Dependency_1', '" + str_env + "Dependency_2'];Type=VERTEX }}" ] ),
           "Products{ ['" + str_env + "Product_1']}",
           "Dependencies{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}",
           "Inputs{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}",
           "Terminal_Products{ ['" + str_env + "Product_1']}" ])

        cmd_cur = Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ str_env + "Dependency_1", str_env + "Dependency_2" ],
                                           lstr_cur_products = [ str_env + "Product_1" ] )
        lcmd_commands = [ cmd_cur, cmd_cur, cmd_cur ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( str_answer, dt_tree.func_detail() )


    def test_init_for_two_commands( self ):
        """ Test initialization for two command """

        str_env = os.path.join( self.str_test_directory, "test_init_for_two_commands" ) + os.path.sep
        str_answer = "".join([ "Graph{ Graph:",
                               "VERTEX{ ID=" + str_env + "Dependency_1;Parents=['_i_am_Groot_'];Children=['Command_1', 'Command_2'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Dependency_2;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_1;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_2;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_3;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_4;Parents=['Command_2'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_5;Parents=['Command_2'];Children=[];Type=RESOURCE };",
                               "Command: Command_1; Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, ",
                                       "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2'],",
                                   "PATH: " + str_env + "Dependency_2, CLEAN: 2, ",
                                       "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; ",
                                   "Products: PATH: " + str_env + "Product_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [],",
                                            "PATH: " + str_env + "Product_2, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [],",
                                            "PATH: " + str_env + "Product_3, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [];",
                               "Command: Command_2; Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, ",
                                       "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2']; ",
                                   "Products: PATH: " + str_env + "Product_4, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: [],",
                                             "PATH: " + str_env + "Product_5, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: [];",
                               "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['" + str_env + "Dependency_1', '" + str_env + "Dependency_2'];Type=VERTEX }}\n",
                               "Products{ ['" + str_env + "Product_1', '" + str_env + "Product_2', '" + str_env + "Product_3', '" + str_env + "Product_4', '" + str_env + "Product_5']}\n",
                               "Dependencies{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}\n",
                               "Inputs{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}\n",
                               "Terminal_Products{ ['" + str_env + "Product_1', '" + str_env + "Product_2', '" + str_env + "Product_3', '" + str_env + "Product_4', '" + str_env + "Product_5']}" ])

        lcmd_commands = [ Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ str_env + "Dependency_1", 
                                                                    str_env + "Dependency_2" ],
                                           lstr_cur_products = [ str_env + "Product_1",
                                                                str_env + "Product_2", 
                                                                str_env + "Product_3" ] ),
                         Command.Command( str_cur_command = "Command_2",
                                           lstr_cur_dependencies = [ str_env + "Dependency_1" ],
                                           lstr_cur_products = [ str_env + "Product_4",
                                                                str_env + "Product_5" ] ) ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( str_answer, dt_tree.func_detail() )

    def test_init_for_three_commands( self ):
        """ Test initialization for one command """

        str_env = os.path.join( self.str_test_directory, "test_init_for_three_commands" ) + os.path.sep
        str_answer = "".join([ "Graph{ Graph:VERTEX{ ID=" + str_env + "Dependency_1;Parents=['_i_am_Groot_'];",
                               "Children=['Command_1', 'Command_2'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Dependency_2;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_1;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_2;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_3;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_4;Parents=['Command_2'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_5;Parents=['Command_2'];Children=['Command_3'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_6;Parents=['Command_3'];Children=[];Type=RESOURCE };",
                               "Command: Command_1; Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, ",
                                   "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2'],PATH: " + str_env + "Dependency_2, CLEAN: 2, ",
                                   "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: " + str_env + "Product_1, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_1'] CHILDREN: [],PATH: " + str_env + "Product_2, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_1'] CHILDREN: [],PATH: " + str_env + "Product_3, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_1'] CHILDREN: [];",
                               "Command: Command_2; Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, ",
                                   "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2']; Products: PATH: " + str_env + "Product_4, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_2'] CHILDREN: [],PATH: " + str_env + "Product_5, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_2'] CHILDREN: ['Command_3'];",
                               "Command: Command_3; Dependencies: PATH: " + str_env + "Product_5, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_2'] CHILDREN: ['Command_3']; Products: PATH: " + str_env + "Product_6, CLEAN: 2, ",
                                   "Product PARENTS: ['Command_3'] CHILDREN: [];",
                               "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['" + str_env + "Dependency_1', '" + str_env + "Dependency_2'];Type=VERTEX }}\n",
                               "Products{ ['" + str_env + "Product_1', '" + str_env + "Product_2', '" + str_env + "Product_3', '" + str_env + "Product_4', '" + str_env + "Product_5', '" + str_env + "Product_6']}\n",
                               "Dependencies{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2', '" + str_env + "Product_5']}\n",
                               "Inputs{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2']}\n",
                               "Terminal_Products{ ['" + str_env + "Product_1', '" + str_env + "Product_2', '" + str_env + "Product_3', '" + str_env + "Product_4', '" + str_env + "Product_6']}" ])

        lcmd_commands = [ Command.Command( str_cur_command = "Command_1",
                                           lstr_cur_dependencies = [ str_env + "Dependency_1", 
                                                                     str_env + "Dependency_2"],
                                           lstr_cur_products = [ str_env + "Product_1",
                                                                 str_env + "Product_2", 
                                                                 str_env + "Product_3" ] ),
                         Command.Command( str_cur_command = "Command_2",
                                           lstr_cur_dependencies = [ str_env + "Dependency_1" ],
                                           lstr_cur_products = [ str_env + "Product_4",
                                                                 str_env + "Product_5" ] ),
                         Command.Command( str_cur_command = "Command_3",
                                           lstr_cur_dependencies = [ str_env + "Product_5" ],
                                           lstr_cur_products = [ str_env + "Product_6" ] ) ]
        dt_tree = DependencyTree.DependencyTree( lcmd_commands )
        self.func_test_equals( str_answer, dt_tree.func_detail() )

# func_add_command
    def test_func_add_command_for_invalid_command( self ):
        """ Test adding commands when an invalid command is given. """
        cmd_test = Command.Command( "", [], [] )
        dt_tree = DependencyTree.DependencyTree()
        f_result = dt_tree._DependencyTree__func_add_command( cmd_test )
        self.func_test_true( not f_result )


    def test_func_add_command_for_new_command( self ):
        """ Test adding commands when a new command is given. """
        str_env = os.path.join( self.str_test_directory, "test_func_add_command_for_new_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ], 
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        f_result = dt_tree._DependencyTree__func_add_command( cmd_test )
        self.func_test_true( f_result )


    def test_func_add_command_for_known_command( self ):
        """ Test adding commands when a command already in the DependencyTree are given. """
        str_env = os.path.join( self.str_test_directory, "test_func_add_command_for_known_command" )
        cmd_test = Command.Command( "Command_1", [ os.path.join( str_env, "Dependencies_1" ) ],
                                    [ os.path.join( str_env, "Products_1" ) ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree._DependencyTree__func_add_command( cmd_test )
        f_result = dt_tree._DependencyTree__func_add_command( cmd_test )
        self.func_test_true( not f_result )

    def test_func_add_command_for_invalid_command_detail( self ):
        """ Test adding commands when an invalid command is given. """
        str_answer = "\n".join([ "Graph{ Graph:VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }}",
                                 "Products{ []}",
                                 "Dependencies{ []}",
                                 "Inputs{ []}",
                                 "Terminal_Products{ []}" ])
        cmd_test = Command.Command( "", [], [] )
        dt_tree = DependencyTree.DependencyTree()
        str_result = dt_tree.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_func_add_command_for_new_command_detail( self ):
        """ Test adding commands when an invalid command is given. """

        str_env = os.path.join( self.str_test_directory, "test_init_for_three_commands" ) + os.path.sep
        str_answer = "\n".join([ "Graph{ Graph:VERTEX{ ID=/Dependencies_1;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };VERTEX{ ID=" + os.path.sep + "Products_1;Parents=['Command_1'];Children=[];Type=RESOURCE };Command: Command_1; Dependencies: PATH: " + os.path.sep + "Dependencies_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: " + os.path.sep + "Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [];VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['" + os.path.sep + "Dependencies_1'];Type=VERTEX }}",
                                  "Products{ ['" + os.path.sep + "Products_1']}",
                                  "Dependencies{ ['" + os.path.sep + "Dependencies_1']}",
                                  "Inputs{ ['" + os.path.sep + "Dependencies_1']}",
                                  "Terminal_Products{ ['" + os.path.sep + "Products_1']}" ])
        cmd_test = Command.Command( "Command_1", [ os.path.sep + "Dependencies_1" ], [ os.path.sep + "Products_1" ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree._DependencyTree__func_add_command( cmd_test )
        str_result = dt_tree.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_func_add_command_for_2_new_command_detail( self ):
        """ Test adding 2 commands. """

        str_env = os.path.join( self.str_test_directory, "test_func_add_command_for_2_new_command_detail" ) + os.path.sep
        str_answer = "".join( [ "Graph{ Graph:",
                               "VERTEX{ ID=" + str_env + "Dependencies_1;Parents=['_i_am_Groot_'];Children=['Command_1', 'Command_2'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Products_1;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Products_2;Parents=['Command_2'];Children=[];Type=RESOURCE };",
                               "Command: Command_1; Dependencies: PATH: " + str_env + "Dependencies_1, CLEAN: 2, ",
                                   "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2']; ",
                                   "Products: PATH: " + str_env + "Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [];Command: Command_2; ",
                                   "Dependencies: PATH: " + str_env + "Dependencies_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2']; ",
                                   "Products: PATH: " + str_env + "Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: [];",
                               "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['" + str_env + "Dependencies_1'];Type=VERTEX }}\n",
                               "Products{ ['" + str_env + "Products_1', '" + str_env + "Products_2']}\n",
                               "Dependencies{ ['" + str_env + "Dependencies_1']}\n",
                               "Inputs{ ['" + str_env + "Dependencies_1']}\n",
                               "Terminal_Products{ ['" + str_env + "Products_1', '" + str_env + "Products_2']}" ] )

        cmd_test = Command.Command( "Command_1", [ str_env + "Dependencies_1" ], 
                                    [ str_env + "Products_1"] )
        cmd_test2 = Command.Command( "Command_2", [ str_env + "Dependencies_1" ], 
                                    [ str_env + "Products_2" ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree._DependencyTree__func_add_command( cmd_test )
        dt_tree._DependencyTree__func_add_command( cmd_test2 )
        str_result = dt_tree.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_func_add_command_for_5_new_command_detail( self ):
        """

        Test adding 5 commands, making a small graph.

        i_am_groot
        |             |                     |
        Dependency_1  Dependency_2          Dependency_3
        |             /       |             |
        Command_1             Command_2     Command_3
        |   |   |             |             |
        Product_1,2,3         Product_4     Product_5
        |            \        |             |
        Command_4             Command_5     Command_6
        |                     |             |
        Product_6             Product_7     Product_8
        
        """

        str_env = os.path.join( self.str_test_directory, "test_func_add_command_for_5_new_command_detail" ) + os.path.sep
        str_answer = "".join([ "Graph{ Graph:",
                               "VERTEX{ ID=" + str_env + "Dependency_1;Parents=['_i_am_Groot_'];Children=['Command_1'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Dependency_2;Parents=['_i_am_Groot_'];Children=['Command_1', 'Command_2'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Dependency_3;Parents=['_i_am_Groot_'];Children=['Command_3'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_1;Parents=['Command_1'];Children=['Command_4'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_2;Parents=['Command_1'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_3;Parents=['Command_1'];Children=['Command_5'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_4;Parents=['Command_2'];Children=['Command_5'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_5;Parents=['Command_3'];Children=['Command_6'];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_7;Parents=['Command_5'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Product_8;Parents=['Command_6'];Children=[];Type=RESOURCE };",
                               "VERTEX{ ID=" + str_env + "Products_6;Parents=['Command_4'];Children=[];Type=RESOURCE };",
                               "Command: Command_1; Dependencies: ",
                                   "PATH: " + str_env + "Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1'],",
                                   "PATH: " + str_env + "Dependency_2, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2']; ",
                               "Products: ",
                                   "PATH: " + str_env + "Product_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_4'],",
                                   "PATH: " + str_env + "Product_2, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: [],",
                                   "PATH: " + str_env + "Product_3, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_5'];",
                               "Command: Command_2; Dependencies: ",
                                   "PATH: " + str_env + "Dependency_2, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1', 'Command_2']; Products: ",
                                   "PATH: " + str_env + "Product_4, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_5'];",
                               "Command: Command_3; Dependencies: ",
                                   "PATH: " + str_env + "Dependency_3, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_3']; ",
                               "Products: ",
                                   "PATH: " + str_env + "Product_5, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_6'];",
                               "Command: Command_4; Dependencies: ",
                                   "PATH: " + str_env + "Product_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_4']; ",
                               "Products: ",
                                   "PATH: " + str_env + "Products_6, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: [];",
                               "Command: Command_5; Dependencies: ",
                                   "PATH: " + str_env + "Product_3, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_5'],",
                                   "PATH: " + str_env + "Product_4, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_5']; ",
                               "Products: ",
                                   "PATH: " + str_env + "Product_7, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: [];",
                               "Command: Command_6; Dependencies: ",
                                   "PATH: " + str_env + "Product_5, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_6']; ",
                               "Products: ",
                                   "PATH: " + str_env + "Product_8, CLEAN: 2, Product PARENTS: ['Command_6'] CHILDREN: [];",
                               "VERTEX{ ID=_i_am_Groot_;Parents=[];",
                                   "Children=['" + str_env + "Dependency_1', '" + str_env + "Dependency_2', '" + str_env + "Dependency_3'];Type=VERTEX }}\n",
                                   "Products{ ['" + str_env + "Product_1', '" + str_env + "Product_2', '" + str_env + "Product_3', '" + str_env + "Product_4', '" + str_env + "Product_5', '" + str_env + "Product_7', '" + str_env + "Product_8', '" + str_env + "Products_6']}\n",
                                   "Dependencies{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2', '" + str_env + "Dependency_3', '" + str_env + "Product_1', '" + str_env + "Product_3', '" + str_env + "Product_4', '" + str_env + "Product_5']}\n",
                                   "Inputs{ ['" + str_env + "Dependency_1', '" + str_env + "Dependency_2', '" + str_env + "Dependency_3']}\n",
                                   "Terminal_Products{ ['" + str_env + "Product_2', '" + str_env + "Product_7', '" + str_env + "Product_8', '" + str_env + "Products_6']}" ])

        cmd_test = Command.Command( "Command_1", 
                                    [ str_env + "Dependency_1", str_env + "Dependency_2" ], 
                                    [ str_env + "Product_1", str_env + "Product_2", str_env + "Product_3"] )
        cmd_test2 = Command.Command( "Command_2", [ str_env + "Dependency_2" ], [ str_env + "Product_4" ] )
        cmd_test3 = Command.Command( "Command_3", [ str_env + "Dependency_3" ], [ str_env + "Product_5" ] )
        cmd_test4 = Command.Command( "Command_4", [ str_env + "Product_1" ], [ str_env + "Products_6" ] )
        cmd_test5 = Command.Command( "Command_5", [ str_env + "Product_3", str_env + "Product_4" ], 
                                                  [ str_env + "Product_7" ] )
        cmd_test6 = Command.Command( "Command_6", [ str_env + "Product_5" ], [ str_env + "Product_8" ] )
        dt_tree = DependencyTree.DependencyTree()
        dt_tree._DependencyTree__func_add_command( cmd_test )
        dt_tree._DependencyTree__func_add_command( cmd_test2 )
        dt_tree._DependencyTree__func_add_command( cmd_test3 )
        dt_tree._DependencyTree__func_add_command( cmd_test4 )
        dt_tree._DependencyTree__func_add_command( cmd_test5 )
        dt_tree._DependencyTree__func_add_command( cmd_test6 )
        str_result = dt_tree.func_detail()
        self.func_test_equals( str_answer, str_result )

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
        str_initial_state_answer = os.getcwd()+os.path.sep+ "test"+os.path.sep+ "test_complete_command_for_one_in_one_command"+os.path.sep+ "Dependencies_1.txt, "+os.getcwd()+os.path.sep+ "test"+os.path.sep+ "test_complete_command_for_one_in_one_command"+os.path.sep+ "Dependencies_2.txt"
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
        str_initial_state = dt_tree.func_show_active_dependencies()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        f_internal_state = str_initial_state == str_initial_state_answer
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
        str_dependencies_before = ", ".join( sorted( [ str_dependency_1, str_dependency_2, str_product_1, str_product_2, str_product_3, str_product_4 ] ) )
        str_dependencies_after = ", ".join( sorted( [ str_product_1, str_product_2, str_product_3, str_product_4 ] ) )
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
        str_dependencies_before_result = dt_tree.func_show_active_dependencies()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_cur = cmd_test_1 )
        str_dependencies_after_result = dt_tree.func_show_active_dependencies()
        f_internal_state = str_dependencies_before == str_dependencies_before_result
        f_internal_dep_state = str_dependencies_after == str_dependencies_after_result
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
        str_dependencies_before = ", ".join( sorted( [ str_dependency_1, str_dependency_2, str_product_1, str_product_2 ] ) )
        str_dependencies_after = ", ".join( sorted( [ str_product_1, str_product_2 ] ) )
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
        str_dependencies_before_result = dt_tree.func_show_active_dependencies()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        str_dependencies_after_result = dt_tree.func_show_active_dependencies()
        f_internal_state = str_dependencies_before == str_dependencies_before_result
        f_internal_dep_state = str_dependencies_after == str_dependencies_after_result
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
        str_dependencies_before = ", ".join( sorted( [ str_dependency_1, str_dependency_2, str_product_1, str_product_2 ] ) )
        str_dependencies_after = ", ".join( sorted( [ ] ) )
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
        str_dependencies_before_result = dt_tree.func_show_active_dependencies()
        dt_tree.func_remove_wait()
        f_success = dt_tree.func_complete_command( cmd_test_1 )
        f_success = f_success and dt_tree.func_complete_command( cmd_test_2 )
        str_dependencies_after_result = dt_tree.func_show_active_dependencies()
        f_internal_state = str_dependencies_before == str_dependencies_before_result
        f_internal_dep_state = str_dependencies_after == str_dependencies_after_result
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
    def test_is_used_intermediate_file_for_empty_dependency_tree_good_data( self ):
        """ Check return for good data with an empty dependency tree. """

        str_product_one = os.path.sep + "Product_1"
        dt_tree = DependencyTree.DependencyTree( [  ] )
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_one, True ) ) )
    
    
    def test_is_used_intermediate_file_for_simple_good_case( self ):
        """ Check to see if one file is recognized as intermediary """

        str_dependency_one = os.path.sep + "Dependency_1"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies = {}
        self.func_test_true( dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_one, True ) ) )

    
    def test_is_used_intermediary_file_for_multiple_good_case( self ):
        """ Check to see if multiple files are recognized as intermediary. """

        str_dependency_one = os.path.sep + "Dependency_1"
        str_dependency_two = os.path.sep + "Dependency_2"
        str_dependency_three = os.path.sep + "Dependency_3"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        str_product_three = os.path.sep + "Product_3"
        str_product_four = os.path.sep + "Product_4"
        str_product_five = os.path.sep + "Product_5"
        str_product_six = os.path.sep + "Product_6"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies = {}
        self.func_test_true( dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_one, True ) ) 
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_two, True ) )
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_three, True ) ) )
    
    
    def test_is_used_intermediary_file_for_one_not_product( self ):
        """ Check to see if a file is recognized as not a product. """

        str_dependency_one = os.path.sep +  "Dependency_1"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies = {}
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( Resource.Resource( str_dependency_one, False ) ) )
    
    
    def test_is_used_intermediary_file_for_mult_not_product( self ):
        """ Check to see if mult files are recognized as not a product. """

        str_dependency_one = os.path.sep + "Dependency_1"
        str_dependency_two = os.path.sep + "Dependency_2"
        str_dependency_three = os.path.sep + "Dependency_3"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        str_product_three = os.path.sep + "Product_3"
        str_product_four = os.path.sep + "Product_4"
        str_product_five = os.path.sep + "Product_5"
        str_product_six = os.path.sep + "Product_6"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies = {}
        self.func_test_true( not ( dt_tree.func_is_used_intermediate_file( Resource.Resource( str_dependency_one, False ) )
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_dependency_two, False ) )
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_dependency_three, False ) ) ) )

    
    def test_is_used_intermediary_file_for_one_terminal( self ):
        """ Check to see if a file is recognized as terminal. """
        str_dependency_one = os.path.sep + "Dependency_1"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies = {}
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( Resource.Resource( str_dependency_one, False ) ) )
        
    
    def test_is_used_intermediary_file_for_mult_terminal( self ):
        """ Check to see if mult files are recognized as terminal. """

        str_dependency_one = os.path.sep + "Dependency_1"
        str_dependency_two = os.path.sep + "Dependency_2"
        str_dependency_three = os.path.sep + "Dependency_3"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        str_product_three = os.path.sep + "Product_3"
        str_product_four = os.path.sep + "Product_4"
        str_product_five = os.path.sep + "Product_5"
        str_product_six = os.path.sep + "Product_6"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies[ str_product_four ] = [ "Command2" ]
        self.func_test_true( not( dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_four, True ) )
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_five, True ) )
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_six, True ) ) ) )

    
    def test_is_used_intermediary_file_for_one_needed( self ):
        """ Check to see if a file is recognized as needed. """

        str_dependency_one = os.path.sep + "Dependency_1"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one ], [str_product_one ] ),
                                                  Command.Command( "Command2", [ str_product_one ], [ str_product_two ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = [ "Command2" ]
        self.func_test_true( not dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_one, True ) ) )

    
    def test_is_used_intermediary_file_for_mult_needed( self ):
        """ Check to see if mult files are recognized as needed. """

        str_dependency_one = os.path.sep + "Dependency_1"
        str_dependency_two = os.path.sep + "Dependency_2"
        str_dependency_three = os.path.sep + "Dependency_3"
        str_product_one = os.path.sep + "Product_1"
        str_product_two = os.path.sep + "Product_2"
        str_product_three = os.path.sep + "Product_3"
        str_product_four = os.path.sep + "Product_4"
        str_product_five = os.path.sep + "Product_5"
        str_product_six = os.path.sep + "Product_6"
        dt_tree = DependencyTree.DependencyTree( [ Command.Command( "Command1", [ str_dependency_one,str_dependency_two,str_dependency_three ],
                                                                    [ str_product_one,str_product_two,str_product_three ] ),
                                                  Command.Command( "Command2", [ str_product_one,str_product_two,str_product_three ], 
                                                                [ str_product_four,str_product_five,str_product_six ] ) ] )
        dt_tree.dict_dependencies[ str_product_one ] = [ "Command2" ]
        dt_tree.dict_dependencies[ str_product_two ] = [ "Command2" ]
        dt_tree.dict_dependencies[ str_product_three ] = [ "Command2" ]
        self.func_test_true( not ( dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_one, True ) )
                             and dt_tree.func_is_used_intermediate_file( Resource.Resource( str_product_two, True ) )
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
        str_commands = "Graph{8}"
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
        str_dependencies = str_env+os.path.sep+ "Products_1, "+str_env+os.path.sep+ "Products_2"
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
        str_dependencies = str_env+os.path.sep+ "Products_2"
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
        cmd_test_1 = Command.Command( "Command_1", [ os.path.join( str_env, "Dependency_1" ) ], [ os.path.join( str_env, "Products_1" ) ] )
        cmd_test_2 = Command.Command( "Command_2", [ os.path.join( str_env, "Products_1" ) ], [ os.path.join( str_env, "Products_2" ) ] )
        cmd_test_3 = Command.Command( "Command_3", [ os.path.join( str_env, "Products_2" ) ], [ os.path.join( str_env, "Products_3" ) ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        f_initial_load = len( [ str_dep for str_dep in dt_tree.dict_dependencies ] ) == 3
        dt_tree.func_remove_dependency_relationships( cmd_test_1 )
        dt_tree.func_remove_dependency_relationships( cmd_test_2 )
        dt_tree.func_remove_dependency_relationships( cmd_test_3 )
        f_dependencies_removed = "[]" == str( sorted( [ str_dep for str_dep in dt_tree.dict_dependencies ] ) )
        self.func_test_equals( f_initial_load, f_dependencies_removed )


    def test_func_remove_dependency_relationships_for_one_in_multiple_times( self ):
        """ Tests removing relationships on a command when removed a second time. """

        str_env = os.path.join( self.str_test_directory, "test_func_remove_dependency_relationships_for_one_in_multiple_times" )
        str_dependencies = str_env+os.path.sep+ "Products_1, "+str_env+os.path.sep+ "Products_2"
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


    def test_func_get_commands_no_command( self ):
        """ Tests the commands returned when no command is in the graph """

        str_env = os.path.join( self.str_test_directory, "test_func_get_commmands_no_command" ) + os.path.sep
        str_answer = "[]"
        dt_tree = DependencyTree.DependencyTree( [ ] )
        str_result = str([ cmd_cur.func_detail() for cmd_cur in dt_tree.func_get_commands() ])
        self.func_test_equals( str_answer, str_result )
    

    def test_func_get_commands_one_command( self ):
        """ Tests the commands returned when one command is in the graph """

        str_env = os.path.join( self.str_test_directory, "test_func_get_commmands_one_command" ) + os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_product_1 = str_env + "Products_1"
        str_answer = "".join([ "[\"Command: Command_1; ",
                                  "Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; ",
                                  "Products: PATH: " + str_env + "Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: []\"]" ])
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ], [ str_product_1 ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1 ] )
        str_result = str([ cmd_cur.func_detail() for cmd_cur in dt_tree.func_get_commands() ])
        self.func_test_equals( str_answer, str_result )


    def test_func_get_commands_three_command( self ):
        """ Tests the order of the commands returned when three commmands are in the graph. """

        str_env = os.path.join( self.str_test_directory, "test_func_get_commands_three_command" ) + os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_product_1 = str_env + "Products_1"
        str_product_2 = str_env + "Products_2"
        str_product_3 = str_env + "Products_3"
        str_answer = "".join([ "[\"Command: Command_1; ",
                                    "Dependencies: PATH: " + str_env + "Dependency_1, CLEAN: 2, ",
                                    "Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; ",
                                    "Products: PATH: " + str_env + "Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2']\", ",
                                "\"Command: Command_2; ",
                                    "Dependencies: PATH: " + str_env + "Products_1, CLEAN: 2, ",
                                    "Product PARENTS: ['Command_1'] CHILDREN: ['Command_2']; ",
                                    "Products: PATH: " + str_env + "Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_3']\",",
                               " \"Command: Command_3; ",
                                    "Dependencies: PATH: " + str_env + "Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_3']; ",
                                    "Products: PATH: " + str_env + "Products_3, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: []\"]" ])
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ],
                                      [ str_product_1 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_product_1 ],
                                      [ str_product_2 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_2 ],
                                      [ str_product_3 ] )
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3 ] )
        str_result = str([ cmd_cur.func_detail() for cmd_cur in dt_tree.func_get_commands() ])
        self.func_test_equals(str_answer, str_result)


    def test_func_get_commands_six_command_1( self ):
        """ 
        Tests the order of the commands returned when six commands are in a graph as shown below.  
          1      2
          |      |
          3      4
          |      |
          5      6
        """ 
        str_env = os.path.join( self.str_test_directory, "test_func_get_commands_six_command_1" ) + os.path.sep
        str_env = os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_dependency_2 = str_env + "Dependency_2"
        str_product_1 = str_env + "Products_1"
        str_product_2 = str_env + "Products_2"
        str_product_3 = str_env + "Products_3"
        str_product_4 = str_env + "Products_4"
        str_product_5 = str_env + "Products_5"
        str_product_6 = str_env + "Products_6"
        str_cmd_1_answer = "Command: Command_1; Dependencies: PATH: /Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']"
        str_cmd_2_answer = "Command: Command_2; Dependencies: PATH: /Dependency_2, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_2']; Products: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']"
        str_cmd_3_answer = "Command: Command_3; Dependencies: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']; Products: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']"
        str_cmd_4_answer = "Command: Command_4; Dependencies: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']; Products: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: ['Command_6']"
        str_cmd_5_answer = "Command: Command_5; Dependencies: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']; Products: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: []"
        str_cmd_6_answer = "Command: Command_6; Dependencies: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: ['Command_6']; Products: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_6'] CHILDREN: []"
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ], [ str_product_1 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_dependency_2 ], [ str_product_2 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_1 ], [ str_product_3 ] )
        cmd_test_4 = Command.Command( "Command_4", [ str_product_2 ], [ str_product_4 ] )
        cmd_test_5 = Command.Command( "Command_5", [ str_product_3 ], [ str_product_5 ] )
        cmd_test_6 = Command.Command( "Command_6", [ str_product_4 ], [ str_product_6 ] )
        lstr_cmd_1 = [ str_cmd_1_answer, str_cmd_2_answer ]
        lstr_cmd_2 = [ str_cmd_3_answer, str_cmd_4_answer ]
        lstr_cmd_3 = [ str_cmd_5_answer, str_cmd_6_answer ]
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ] )
        itr_cmd = iter( dt_tree.func_get_commands() )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        self.func_test_true( True )


    def test_func_get_commands_six_command_2( self ):
        """ 
        Tests the order of the commands returned when six commands are in a graph as shown below.  
          1   2
           \ /
            3
           / \
          4   5
              |
              6
        """ 
        str_env = os.path.join( self.str_test_directory, "test_func_get_commands_six_command_2" ) + os.path.sep
        str_env = os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_dependency_2 = str_env + "Dependency_2"
        str_product_1 = str_env + "Products_1"
        str_product_2 = str_env + "Products_2"
        str_product_3 = str_env + "Products_3"
        str_product_4 = str_env + "Products_4"
        str_product_5 = str_env + "Products_5"
        str_product_6 = str_env + "Products_6"
        str_product_7 = str_env + "Products_7"
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ], [ str_product_1 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_dependency_2 ], [ str_product_2 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_1, str_product_2 ], [ str_product_3, str_product_4 ] )
        cmd_test_4 = Command.Command( "Command_4", [ str_product_3 ], [ str_product_7 ] )
        cmd_test_5 = Command.Command( "Command_5", [ str_product_4 ], [ str_product_5 ] )
        cmd_test_6 = Command.Command( "Command_6", [ str_product_5 ], [ str_product_6 ] )
        str_cmd_1_answer = "Command: Command_1; Dependencies: PATH: /Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']"
        str_cmd_2_answer = "Command: Command_2; Dependencies: PATH: /Dependency_2, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_2']; Products: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_3']"
        str_cmd_3_answer = "Command: Command_3; Dependencies: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3'],PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_3']; Products: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_4'],PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']"
        str_cmd_4_answer = "Command: Command_4; Dependencies: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_4']; Products: PATH: /Products_7, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: []"
        str_cmd_5_answer = "Command: Command_5; Dependencies: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']; Products: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']"
        str_cmd_6_answer = "Command: Command_6; Dependencies: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']; Products: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_6'] CHILDREN: []"
        lstr_cmd_1 = [ str_cmd_1_answer, str_cmd_2_answer ]
        lstr_cmd_2 = [ str_cmd_3_answer ]
        lstr_cmd_3 = [ str_cmd_4_answer, str_cmd_5_answer ]
        lstr_cmd_4 = [ str_cmd_6_answer ]
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ] )
        itr_cmd = iter( dt_tree.func_get_commands() )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_4:
            self.func_test_true( False )
        self.func_test_true( True )


    def test_func_get_commands_six_command_3( self ):
        """ 
        Tests the order of the commands returned when six commands are in a graph as shown below.  
          1
          |
          2
          |\
          3 4
          |/
          5
          |
          6
        """ 
        str_env = os.path.join( self.str_test_directory, "test_func_get_commands_six_command_3" ) + os.path.sep
        str_env = os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_product_1 = str_env + "Products_1"
        str_product_2 = str_env + "Products_2"
        str_product_3 = str_env + "Products_3"
        str_product_4 = str_env + "Products_4"
        str_product_5 = str_env + "Products_5"
        str_product_6 = str_env + "Products_6"
        str_product_7 = str_env + "Products_7"
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ], [ str_product_1 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_product_1 ], [ str_product_2, str_product_3 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_2 ], [ str_product_4 ] )
        cmd_test_4 = Command.Command( "Command_4", [ str_product_3 ], [ str_product_5 ] )
        cmd_test_5 = Command.Command( "Command_5", [ str_product_4, str_product_5 ], [ str_product_6 ] )
        cmd_test_6 = Command.Command( "Command_6", [ str_product_6 ], [ str_product_7 ] )
        str_cmd_1_answer = "Command: Command_1; Dependencies: PATH: /Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2']"
        str_cmd_2_answer = "Command: Command_2; Dependencies: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2']; Products: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_3'],PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']"
        str_cmd_3_answer = "Command: Command_3; Dependencies: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_3']; Products: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']"
        str_cmd_4_answer = "Command: Command_4; Dependencies: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']; Products: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: ['Command_5']"
        str_cmd_5_answer = "Command: Command_5; Dependencies: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5'],PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: ['Command_5']; Products: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']"
        str_cmd_6_answer = "Command: Command_6; Dependencies: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']; Products: PATH: /Products_7, CLEAN: 2, Product PARENTS: ['Command_6'] CHILDREN: []"
        lstr_cmd_1 = [ str_cmd_1_answer ]
        lstr_cmd_2 = [ str_cmd_2_answer ]
        lstr_cmd_3 = [ str_cmd_3_answer, str_cmd_4_answer ]
        lstr_cmd_4 = [ str_cmd_5_answer ]
        lstr_cmd_5 = [ str_cmd_6_answer ]
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ] )
        itr_cmd = iter( dt_tree.func_get_commands() )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_4:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_5:
            self.func_test_true( False )
        self.func_test_true( True )


    def test_func_get_commands_six_command_4( self ):
        """ 
        Tests the order of the commands returned when six commands are in a graph as shown below.  
          1
          |\
          2 3
          | |
          4 5
          |/
          6
        """ 
        str_env = os.path.join( self.str_test_directory, "test_func_get_commands_six_command_4" ) + os.path.sep
        str_env = os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_product_1 = str_env + "Products_1"
        str_product_2 = str_env + "Products_2"
        str_product_3 = str_env + "Products_3"
        str_product_4 = str_env + "Products_4"
        str_product_5 = str_env + "Products_5"
        str_product_6 = str_env + "Products_6"
        str_product_7 = str_env + "Products_7"
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ], [ str_product_1, str_product_2 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_product_1 ], [ str_product_3 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_2 ], [ str_product_4 ] )
        cmd_test_4 = Command.Command( "Command_4", [ str_product_3 ], [ str_product_5 ] )
        cmd_test_5 = Command.Command( "Command_5", [ str_product_4 ], [ str_product_6 ] )
        cmd_test_6 = Command.Command( "Command_6", [ str_product_5, str_product_6 ], [ str_product_7 ] )
        str_cmd_1_answer = "Command: Command_1; Dependencies: PATH: /Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2'],PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']"
        str_cmd_2_answer = "Command: Command_2; Dependencies: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2']; Products: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']"
        str_cmd_3_answer = "Command: Command_3; Dependencies: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']; Products: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']"
        str_cmd_4_answer = "Command: Command_4; Dependencies: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']; Products: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: ['Command_6']"
        str_cmd_5_answer = "Command: Command_5; Dependencies: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']; Products: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']"
        str_cmd_6_answer = "Command: Command_6; Dependencies: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_4'] CHILDREN: ['Command_6'],PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']; Products: PATH: /Products_7, CLEAN: 2, Product PARENTS: ['Command_6'] CHILDREN: []"
        lstr_cmd_1 = [ str_cmd_1_answer ]
        lstr_cmd_2 = [ str_cmd_2_answer, str_cmd_3_answer ]
        lstr_cmd_3 = [ str_cmd_4_answer, str_cmd_5_answer ]
        lstr_cmd_4 = [ str_cmd_6_answer ]
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ] )
        itr_cmd = iter( dt_tree.func_get_commands() )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_4:
            self.func_test_true( False )
        self.func_test_true( True )


    def test_func_get_commands_six_command_5( self ):
        """ 
        Tests the order of the commands returned when six commands are in a graph as shown below.  
          1
          |\
          2 3
          |/ \
          4   5
            \ |
              6
        """ 
        str_env = os.path.join( self.str_test_directory, "test_func_get_commands_six_command_5" ) + os.path.sep
        str_env = os.path.sep
        str_dependency_1 = str_env + "Dependency_1"
        str_product_1 = str_env + "Products_1"
        str_product_2 = str_env + "Products_2"
        str_product_3 = str_env + "Products_3"
        str_product_4 = str_env + "Products_4"
        str_product_5 = str_env + "Products_5"
        str_product_6 = str_env + "Products_6"
        str_product_7 = str_env + "Products_7"
        str_product_8 = str_env + "Products_8"
        cmd_test_1 = Command.Command( "Command_1", [ str_dependency_1 ], [ str_product_1, str_product_2 ] )
        cmd_test_2 = Command.Command( "Command_2", [ str_product_1 ], [ str_product_3 ] )
        cmd_test_3 = Command.Command( "Command_3", [ str_product_2 ], [ str_product_4, str_product_5 ] )
        cmd_test_4 = Command.Command( "Command_4", [ str_product_3, str_product_4 ], [ str_product_6 ] )
        cmd_test_5 = Command.Command( "Command_5", [ str_product_5 ], [ str_product_6, str_product_7 ] )
        cmd_test_6 = Command.Command( "Command_6", [ str_product_6, str_product_7 ], [ str_product_8 ] )
        str_cmd_1_answer = "Command: Command_1; Dependencies: PATH: /Dependency_1, CLEAN: 2, Dependency PARENTS: ['_i_am_Groot_'] CHILDREN: ['Command_1']; Products: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2'],PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']"
        str_cmd_2_answer = "Command: Command_2; Dependencies: PATH: /Products_1, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_2']; Products: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4']"
        str_cmd_3_answer = "Command: Command_3; Dependencies: PATH: /Products_2, CLEAN: 2, Product PARENTS: ['Command_1'] CHILDREN: ['Command_3']; Products: PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_4'],PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']"
        str_cmd_4_answer = "Command: Command_4; Dependencies: PATH: /Products_3, CLEAN: 2, Product PARENTS: ['Command_2'] CHILDREN: ['Command_4'],PATH: /Products_4, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_4']; Products: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_4', 'Command_5'] CHILDREN: ['Command_6']"
        str_cmd_5_answer = "Command: Command_5; Dependencies: PATH: /Products_5, CLEAN: 2, Product PARENTS: ['Command_3'] CHILDREN: ['Command_5']; Products: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_4', 'Command_5'] CHILDREN: ['Command_6'],PATH: /Products_7, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']"
        str_cmd_6_answer = "Command: Command_6; Dependencies: PATH: /Products_6, CLEAN: 2, Product PARENTS: ['Command_4', 'Command_5'] CHILDREN: ['Command_6'],PATH: /Products_7, CLEAN: 2, Product PARENTS: ['Command_5'] CHILDREN: ['Command_6']; Products: PATH: /Products_8, CLEAN: 2, Product PARENTS: ['Command_6'] CHILDREN: []"
        lstr_cmd_1 = [ str_cmd_1_answer ]
        lstr_cmd_2 = [ str_cmd_2_answer, str_cmd_3_answer ]
        lstr_cmd_3 = [ str_cmd_4_answer, str_cmd_5_answer ]
        lstr_cmd_4 = [ str_cmd_6_answer ]
        dt_tree = DependencyTree.DependencyTree( [ cmd_test_1, cmd_test_2, cmd_test_3, cmd_test_4, cmd_test_5, cmd_test_6 ] )
        itr_cmd = iter( dt_tree.func_get_commands() )
        if not itr_cmd.next().func_detail() in lstr_cmd_1:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_2:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_3:
            self.func_test_true( False )
        if not itr_cmd.next().func_detail() in lstr_cmd_4:
            self.func_test_true( False )
        self.func_test_true( True )


#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( DependencyTreeTester )
