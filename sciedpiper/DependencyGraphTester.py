
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import DependencyGraph
import Graph
import ParentPipelineTester
import Resource
import os
import unittest


class DependencyGraphTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the DependencyGraph object.
    """

# Test graphs
    def func_make_simple_graph( self ):
        """
         -----R1------
        |      |      |
        2      3      4
        |     | |     |
        R5    R6  R7 R8
        """
        vtx_one = Resource.Resource( "/R1", False )
        vtx_two = Graph.Vertex( 2 )
        vtx_three = Graph.Vertex( 3 )
        vtx_four = Graph.Vertex( 4 )
        vtx_two.str_type = Command.STR_TYPE
        vtx_three.str_type = Command.STR_TYPE
        vtx_four.str_type = Command.STR_TYPE
        vtx_five = Resource.Resource( "/R5", True )
        vtx_six = Resource.Resource( "/R6", True )
        vtx_seven = Resource.Resource( "/R7", True )
        vtx_eight = Resource.Resource( "/R8", True )
        graph_dep = DependencyGraph.DependencyGraph()
        graph_dep.func_add_vertex( vtx_one )
        graph_dep.func_add_vertex( vtx_two )
        graph_dep.func_add_vertex( vtx_three )
        graph_dep.func_add_vertex( vtx_four )
        graph_dep.func_add_vertex( vtx_five )
        graph_dep.func_add_vertex( vtx_six )
        graph_dep.func_add_vertex( vtx_seven )
        graph_dep.func_add_vertex( vtx_eight )
        graph_dep.func_add_edge( vtx_one, vtx_two )
        graph_dep.func_add_edge( vtx_one, vtx_three )
        graph_dep.func_add_edge( vtx_one, vtx_four )
        graph_dep.func_add_edge( vtx_two, vtx_five )
        graph_dep.func_add_edge( vtx_three, vtx_six )
        graph_dep.func_add_edge( vtx_three, vtx_seven )
        graph_dep.func_add_edge( vtx_four, vtx_eight )
        return graph_dep

    def func_make_complex_graph( self ):
        """
         -----R1------
        |      |      |
        2      3      4
        |     | |     |
        R5    R6  R7 R8

        R9
        |
        10
        |
        R11

        R12
        |    |
        13   14
        |    |
        R15  R16
          | |
           17
           |
          R18
        
        """
        vtx_one = Resource.Resource( "/R1", False )
        vtx_two = Graph.Vertex( 2 )
        vtx_three = Graph.Vertex( 3 )
        vtx_four = Graph.Vertex( 4 )
        vtx_five = Resource.Resource( "/R5", True )
        vtx_six = Resource.Resource( "/R6", True )
        vtx_seven = Resource.Resource( "/R7", True )
        vtx_eight = Resource.Resource( "/R8", True )
        vtx_nine = Resource.Resource( "/R9", True )
        vtx_ten = Graph.Vertex( 10 )
        vtx_eleven = Resource.Resource( "/R11", True )
        vtx_twelve = Resource.Resource( "/R12", True )
        vtx_thirteen = Graph.Vertex( 13 )
        vtx_fourteen = Graph.Vertex( 14 )
        vtx_fifteen = Resource.Resource( "/R15", True )
        vtx_sixteen = Resource.Resource( "/R16", True )
        vtx_seventeen = Graph.Vertex( 17 )
        vtx_eighteen = Resource.Resource( "/R18", True )
        graph_dep = DependencyGraph.DependencyGraph()
        vtx_two.str_type = Command.STR_TYPE
        vtx_three.str_type = Command.STR_TYPE
        vtx_four.str_type = Command.STR_TYPE
        vtx_ten.str_type = Command.STR_TYPE
        vtx_thirteen.str_type = Command.STR_TYPE
        vtx_fourteen.str_type = Command.STR_TYPE
        vtx_seventeen.str_type = Command.STR_TYPE

        for vtx_add in [ vtx_one, vtx_two, vtx_three, vtx_four,
                         vtx_five, vtx_six, vtx_seven, vtx_eight,
                         vtx_nine, vtx_ten, vtx_eleven, vtx_twelve,
                         vtx_thirteen, vtx_fourteen, vtx_fifteen,
                         vtx_sixteen, vtx_seventeen, vtx_eighteen ]:
          graph_dep.func_add_vertex( vtx_add )

        graph_dep.func_add_edge( vtx_one, vtx_two )
        graph_dep.func_add_edge( vtx_one, vtx_three )
        graph_dep.func_add_edge( vtx_one, vtx_four )
        graph_dep.func_add_edge( vtx_two, vtx_five )
        graph_dep.func_add_edge( vtx_three, vtx_six )
        graph_dep.func_add_edge( vtx_three, vtx_seven )
        graph_dep.func_add_edge( vtx_four, vtx_eight )
        graph_dep.func_add_edge( vtx_nine, vtx_ten )
        graph_dep.func_add_edge( vtx_ten, vtx_eleven )
        graph_dep.func_add_edge( vtx_twelve, vtx_thirteen )
        graph_dep.func_add_edge( vtx_thirteen, vtx_fifteen )
        graph_dep.func_add_edge( vtx_twelve, vtx_fourteen )
        graph_dep.func_add_edge( vtx_fourteen, vtx_sixteen )
        graph_dep.func_add_edge( vtx_fifteen, vtx_seventeen )
        graph_dep.func_add_edge( vtx_sixteen, vtx_seventeen )
        graph_dep.func_add_edge( vtx_seventeen, vtx_eighteen )
        return graph_dep

# Init 
    def test_init_for_no_command( self ):
        """ Test initialization with no commands """
        str_answer = "Graph:VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }" 
        graph_dep = DependencyGraph.DependencyGraph()
        str_result = graph_dep.func_detail()
        self.func_test_equals( str_answer, str_result )

# Get Commands
    def test_get_command_for_empty_graph( self ):
        """ Test get commands for empty Dependency graph. """
        str_answer = "[]" 
        graph_dep = DependencyGraph.DependencyGraph()
        str_result = str( sorted( [ vtx_cur.str_id for vtx_cur in graph_dep.func_get_commands() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_commands_for_simple_graph( self ):
        """ Test get terminal products for simple DependencyGraph """
        str_answer = str(sorted([2,3,4]))
        graph_dep = self.func_make_simple_graph()
        str_result = str( sorted( [ vtx_cur.str_id for vtx_cur in graph_dep.func_get_commands() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_commands_for_complex_graph( self ):
        """ Test get commands for a complex DependencyGraph """
        str_answer = str(sorted([2,3,4,10,13,14,17]))
        graph_dep = self.func_make_complex_graph()
        str_result = str( sorted( [ vtx_cur.str_id for vtx_cur in graph_dep.func_get_commands() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    # TODO this test works fine by itself wbut will periodically fail when added to the
    # complete regression suite.
    def fixtest_get_commands_for_order_in_complex_graph( self ):
        """ Test get commands for the complex DependencyGraph, checking to make sure the order is right. """
        itr_commands = iter( self.func_make_complex_graph().func_get_commands() )
        lstr_commands_group_1 = [ 2, 3, 4 ]
        lstr_commands_group_2 = [ 10 ]
        lstr_commands_group_3 = [ 13, 14 ]
        lstr_commands_group_4 = [ 17 ]
        for i_cmd in lstr_commands_group_1:
            cmd_cur = itr_commands.next()
            if not cmd_cur.str_id in lstr_commands_group_1:
                self.func_test_true( False )
        cmd_cur = itr_commands.next()
        if not cmd_cur.str_id in lstr_commands_group_2:
            self.func_test_true( False )
        cmd_cur = itr_commands.next()
        if not cmd_cur.str_id in lstr_commands_group_3:
            self.func_test_true( False )
        cmd_cur = itr_commands.next()
        if not cmd_cur.str_id in lstr_commands_group_3:
            self.func_test_true( False )
        cmd_cur = itr_commands.next()
        if not cmd_cur.str_id in lstr_commands_group_4:
            self.func_test_true( False )
        self.func_test_true( True )

# Get terminal products
    def test_get_terminal_products_for_empty_graph( self ):
        """ Test get terminal products for an empty DependencyGraph """
        str_answer = "[]" 
        graph_dep = DependencyGraph.DependencyGraph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_terminal_products() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_terminal_products_for_simple_graph( self ):
        """ Test get terminal products for simple DependencyGraph """
        str_answer = "['VERTEX{ ID=/R5;Parents=[2];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R6;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R7;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R8;Parents=[4];Children=[];Type=RESOURCE }']" 
        graph_dep = self.func_make_simple_graph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_terminal_products() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_terminal_products_for_complex_graph( self ):
        """ Test get terminal products for a complex DependencyGraph """
        str_answer = "['VERTEX{ ID=/R11;Parents=[10];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R18;Parents=[17];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R5;Parents=[2];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R6;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R7;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R8;Parents=[4];Children=[];Type=RESOURCE }']" 
        graph_dep = self.func_make_complex_graph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_terminal_products() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

# Get input files
    def test_get_input_files_for_empty_graph( self ):
        """ Test get input files for an empty DependencyGraph """
        str_answer = "[]" 
        graph_dep = DependencyGraph.DependencyGraph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_input_files() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_input_files_for_simple_graph( self ):
        """ Test get input_files for an empty DependencyGraph """
        str_answer = "[\"VERTEX{ ID=/R1;Parents=['_i_am_Groot_'];Children=[2, 3, 4];Type=RESOURCE }\"]" 
        graph_dep = self.func_make_simple_graph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_input_files() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_input_files_for_complex_graph( self ):
        """ Test get input files for a complex DependencyGraph """
        str_answer = "[\"VERTEX{ ID=/R12;Parents=['_i_am_Groot_'];Children=[13, 14];Type=RESOURCE }\", \"VERTEX{ ID=/R1;Parents=['_i_am_Groot_'];Children=[2, 3, 4];Type=RESOURCE }\", \"VERTEX{ ID=/R9;Parents=['_i_am_Groot_'];Children=[10];Type=RESOURCE }\"]" 
        graph_dep = self.func_make_complex_graph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_input_files() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

# Get dependencies
    def test_get_dependencies_for_empty_graph( self ):
        """ Test get dependencies for an empty DependencyGraph """
        str_answer = "[]" 
        graph_dep = DependencyGraph.DependencyGraph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_dependencies() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_dependencies_for_simple_graph( self ):
        """ Test get dependencies for an empty DependencyGraph """
        str_answer = "[\"VERTEX{ ID=/R1;Parents=['_i_am_Groot_'];Children=[2, 3, 4];Type=RESOURCE }\"]" 
        str_answer = "[\'/R1\']"
        graph_dep = self.func_make_simple_graph()
        str_result = str( sorted( [ vtx_cur for vtx_cur in graph_dep.func_get_dependencies() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_dependencies_for_complex_graph( self ):# R1, R9, R12, R15, R16
        """ Test get dependencies for a complex DependencyGraph """
        graph_dep = self.func_make_complex_graph()
        str_result = str( sorted( [ vtx_cur for vtx_cur in graph_dep.func_get_dependencies() if vtx_cur] ) )
        str_answer = "[\'/R1\', \'/R12\', \'/R15\', \'/R16\', \'/R9\']"
        self.func_test_equals( str_answer, str_result )

# Get products
    def test_get_products_for_empty_graph( self ):
        """ Test get products for an empty DependencyGraph """
        str_answer = "[]" 
        graph_dep = DependencyGraph.DependencyGraph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_products() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result ) 

    def test_get_products_for_simple_graph( self ):
        """ Test get products for an empty DependencyGraph """
        str_answer = "['VERTEX{ ID=/R5;Parents=[2];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R6;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R7;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R8;Parents=[4];Children=[];Type=RESOURCE }']" 
        graph_dep = self.func_make_simple_graph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_products() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

    def test_get_products_for_complex_graph( self ):
        """ Test get products for an complex DependencyGraph """
        str_answer = "['VERTEX{ ID=/R11;Parents=[10];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R15;Parents=[13];Children=[17];Type=RESOURCE }', 'VERTEX{ ID=/R16;Parents=[14];Children=[17];Type=RESOURCE }', 'VERTEX{ ID=/R18;Parents=[17];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R5;Parents=[2];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R6;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R7;Parents=[3];Children=[];Type=RESOURCE }', 'VERTEX{ ID=/R8;Parents=[4];Children=[];Type=RESOURCE }']" 
        graph_dep = self.func_make_complex_graph()
        str_result = str( sorted( [ vtx_cur.func_detail() for vtx_cur in graph_dep.func_get_products() if vtx_cur] ) )
        self.func_test_equals( str_answer, str_result )

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( DependencyGraphTester )
