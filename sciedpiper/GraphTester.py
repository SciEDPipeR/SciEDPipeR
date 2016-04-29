# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Graph
import os
import ParentPipelineTester
import unittest

class GraphTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the Graph and Vertex Objects.
    """

# Graph building functions
    def func_make_one_cycle_graph( self ):

      cur_graph = Graph.Graph()
      vtx_22 = Graph.Vertex( 22 )
      vtx_23 = Graph.Vertex( 23 )
      vtx_24 = Graph.Vertex( 24 )
      vtx_21 = Graph.Vertex( 21 )
      cur_graph.func_add_edge( vtx_22, vtx_24 )
      cur_graph.func_add_edge( vtx_23, vtx_24 )
      cur_graph.func_add_edge( vtx_21, vtx_22 )
      cur_graph.func_add_edge( vtx_21, vtx_23 )
      return cur_graph

    def func_make_complex_graph(self):
      """
      Test creating a graph as such:

      One
       |
      Two
       |     |
      Three Four
       |     |    |
      Five  Six Seven
             |
           Eight

             21
              |
          22     23
              |
             24

      33

      All three structures attached to Groot
      """
 
      cur_graph = Graph.Graph()
      vtx_one = Graph.Vertex( "One" )
      cur_graph.func_add_vertex( vtx_one )
      vtx_two = Graph.Vertex( "Two" )
      cur_graph.func_add_vertex( vtx_two )
      vtx_three = Graph.Vertex( "Three" )
      cur_graph.func_add_vertex( vtx_three )
      vtx_four = Graph.Vertex( "Four" )
      cur_graph.func_add_vertex( vtx_four )
      vtx_five = Graph.Vertex( "Five" )
      cur_graph.func_add_vertex( vtx_five )
      vtx_six = Graph.Vertex( "Six" )
      cur_graph.func_add_vertex( vtx_six )
      vtx_seven = Graph.Vertex( "Seven" )
      cur_graph.func_add_vertex( vtx_seven )
      vtx_eight = Graph.Vertex( "Eight" )
      cur_graph.func_add_vertex( vtx_eight )
      vtx_21 = Graph.Vertex( 21 )
      cur_graph.func_add_vertex( vtx_21 )
      vtx_22 = Graph.Vertex( 22 )
      cur_graph.func_add_vertex( vtx_22 )
      vtx_23 = Graph.Vertex( 23 )
      cur_graph.func_add_vertex( vtx_23 )
      vtx_24 = Graph.Vertex( 24 )
      cur_graph.func_add_vertex( vtx_24 )
      vtx_33 = Graph.Vertex( 33 )
      cur_graph.func_add_vertex( vtx_33 )

      cur_graph.func_add_edge( vtx_one, vtx_two )
      cur_graph.func_add_edge( vtx_four, vtx_six )
      cur_graph.func_add_edge( vtx_four, vtx_seven )
      cur_graph.func_add_edge( vtx_two, vtx_four )
      cur_graph.func_add_edge( vtx_six, vtx_eight )
      cur_graph.func_add_edge( vtx_two, vtx_three )
      cur_graph.func_add_edge( vtx_three, vtx_five )

      cur_graph.func_add_edge( vtx_22, vtx_24 )
      cur_graph.func_add_edge( vtx_23, vtx_24 )
      cur_graph.func_add_edge( vtx_21, vtx_22 )
      cur_graph.func_add_edge( vtx_21, vtx_23 )
      return cur_graph

    ##### Vertex Testing
# init
    def test_init_vertex_for_good_case(self):
        """ Testing init for good case. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

# Add parent
    def test_add_parent_for_good_case(self):
        """ Testing add parent for good case. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[\'Parent1\'];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent1" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_add_parent_for_multiple_parents(self):
        """ Testing add parent for multiple parents. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[\'Parent01\', \'Parent09\', \'Parent10\'];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent09" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent01" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent10" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_add_parents_for_good_and_bad(self):
        """ Testing add parent for multiple parents add some bad. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[\'Parent01\', \'Parent09\', \'Parent10\'];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent09" ) )
        cur_vertex.func_add_parent( Graph.Vertex( None ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent01" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent10" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_add_parent_for_none_vertex(self):
        """ Testing add parent for none vertex. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( None ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_add_parent_for_bad_id(self):
        """ Testing add parent for bad id. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

# str
    def test_str_vertex_for_good_case(self):
        """ Testing str for good case. """
        
        str_answer = "VERTEX{ ID, Parent count: 0, Children count: 0 }"
        cur_vertex = Graph.Vertex( "ID" )
        str_result = str( cur_vertex )
        self.func_test_equals( str_answer, str_result )

    def test_str_vertex_for_mult_child_parent_case(self):
        """ Testing str for mult child parent case. """
        
        str_answer = "VERTEX{ ID, Parent count: 3, Children count: 2 }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent1" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child1" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent2" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent3" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child2" ) )
        str_result = str( cur_vertex )
        self.func_test_equals( str_answer, str_result )

# func_remove_parent
    def test_remove_parent_for_no_parents(self):
        """ Testing remove parent for no parents. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_remove_parent( Graph.Vertex("NOT_HERE") )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_remove_parent_for_one_parent(self):
        """ Testing remove parent for one parent. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent1" ) )
        cur_vertex.func_remove_parent( Graph.Vertex( "Parent1" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_remove_one_parent_for_multiple_parents(self):
        """ Testing removing one parent with a vertex with multiple parents. """
         
        str_answer = "VERTEX{ ID=ID;Parents=[\'Parent09\', \'Parent10\'];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent09" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent01" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent10" ) )
        cur_vertex.func_remove_parent( Graph.Vertex( "Parent01" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_remove_multiple_parent_for_multiple_parents(self):
        """ Testing removing multiple parents with a vertex with multiple parents. """
         
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent09" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent01" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent10" ) )
        cur_vertex.func_remove_parent( Graph.Vertex( "Parent09" ) )
        cur_vertex.func_remove_parent( Graph.Vertex( "Parent10" ) )
        cur_vertex.func_remove_parent( Graph.Vertex( "Parent01" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

# func_remove_child
    def test_remove_child_for_no_children(self):
        """ Testing remove child for no children. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_remove_child( Graph.Vertex("NOT_HERE") )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_remove_child_for_one_child(self):
        """ Testing remove child for one child. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child1" ) )
        cur_vertex.func_remove_child( Graph.Vertex( "Child1" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_remove_one_child_for_multiple_children(self):
        """ Testing removing one child with a vertex with multiple children. """
         
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[\'Child09\', \'Child10\'];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child09" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child01" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child10" ) )
        cur_vertex.func_remove_child( Graph.Vertex( "Child01" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_remove_multiple_child_for_multiple_children(self):
        """ Testing removing multiple children with a vertex with multiple children. """
         
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child09" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child01" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child10" ) )
        cur_vertex.func_remove_child( Graph.Vertex( "Child09" ) )
        cur_vertex.func_remove_child( Graph.Vertex( "Child10" ) )
        cur_vertex.func_remove_child( Graph.Vertex( "Child01" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

# func get parents
    def test_get_parents_for_no_parent(self):
        """ Testing get parent with a vertex with one parent. """
         
        str_answer = "[]"
        cur_vertex = Graph.Vertex( "ID" )
        str_result = str( [ vtx_parent.str_id for vtx_parent in cur_vertex.func_get_parents() ] )
        self.func_test_equals( str_answer, str_result )
 
    def test_get_parents_for_one_parent(self):
        """ Testing get parents with a vertex with one parent. """
         
        str_answer = "[\'Parent09\']"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent09" ) )
        str_result = str( [ vtx_parent.str_id for vtx_parent in cur_vertex.func_get_parents() ] )
        self.func_test_equals( str_answer, str_result )
 
    def test_get_parent_for_multiple_parents(self):
        """ Testing get parent with a vertex with multiple parents. """
         
        str_answer = str( sorted( [ 'Parent09', 'Parent01', 'Parent10'] ) )
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent09" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent01" ) )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent10" ) )
        str_result = str( sorted( [ vtx_parent.str_id for vtx_parent in cur_vertex.func_get_parents() ] ) )
        self.func_test_equals( str_answer, str_result )

# func get children
    def test_get_children_for_no_child(self):
        """ Testing get children with a vertex with one child. """
         
        str_answer = "[]"
        cur_vertex = Graph.Vertex( "ID" )
        str_result = str( [ vtx_child.str_id for vtx_child in cur_vertex.func_get_children() ] )
        self.func_test_equals( str_answer, str_result )
 
    def test_get_children_for_one_child(self):
        """ Testing get children with a vertex with one child. """
         
        str_answer = "[\'Child09\']"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child09" ) )
        str_result = str( [ vtx_child.str_id for vtx_child in cur_vertex.func_get_children() ] )
        self.func_test_equals( str_answer, str_result )
 
    def test_get_children_for_multiple_children(self):
        """ Testing get children with a vertex with multiple children. """
         
        str_answer = str( sorted( ['Child09', 'Child01', 'Child10'] ) )
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child09" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child01" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child10" ) )
        str_result = str( sorted( [ vtx_child.str_id for vtx_child in cur_vertex.func_get_children() ] ) )
        self.func_test_equals( str_answer, str_result )

# func_add_child
    def test_add_child_for_good_case(self):
        """ Testing add child for good case. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=['Child1'];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child1" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_add_children_for_multiple_children(self):
        """ Testing add child for multiple children. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[\'Child01\', \'Child09\', \'Child10\'];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child09" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child01" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child10" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_add_children_for_good_and_bad(self):
        """ Testing add child for multiple children add some bad. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[\'Child01\', \'Child09\', \'Child10\'];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child09" ) )
        cur_vertex.func_add_child( Graph.Vertex( None ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child01" ) )
        cur_vertex.func_add_child( Graph.Vertex( "" ) )
        cur_vertex.func_add_child( Graph.Vertex( "Child10" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

    def test_add_child_for_none_vertex(self):
        """ Testing add child for none vertex. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( None ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )
 
    def test_add_child_for_bad_id(self):
        """ Testing init for bad id. """
        
        str_answer = "VERTEX{ ID=ID;Parents=[];Children=[];Type=VERTEX }"
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "" ) )
        str_result = cur_vertex.func_detail()
        self.func_test_equals( str_answer, str_result )

# func_has_child
    def test_has_child_for_true(self):
        """ Testing add child for true. """
        
        str_answer = True
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child" ) )
        str_result = cur_vertex.func_has_child()
        self.func_test_equals( str_answer, str_result )
 
    def test_has_child_for_false(self):
        """ Testing add child for false. """
        
        str_answer = False
        cur_vertex = Graph.Vertex( "ID" )
        str_result = cur_vertex.func_has_child()
        self.func_test_equals( str_answer, str_result )
 
    def test_has_child_for_false(self):
        """ Testing add child for false, has parent not child. """
        
        str_answer = False
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent" ) )
        str_result = cur_vertex.func_has_child()
        self.func_test_equals( str_answer, str_result )

    def test_has_parent_for_true(self):
        """ Testing add parent for true. """
        
        str_answer = True
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_parent( Graph.Vertex( "Parent" ) )
        str_result = cur_vertex.func_has_parent()
        self.func_test_equals( str_answer, str_result )
 
    def test_has_parent_for_false(self):
        """ Testing add parent for false. """
        
        str_answer = False
        cur_vertex = Graph.Vertex( "ID" )
        str_result = cur_vertex.func_has_parent()
        self.func_test_equals( str_answer, str_result )
 
    def test_has_parent_for_false(self):
        """ Testing add parent for false, has child not parent. """
        
        str_answer = False
        cur_vertex = Graph.Vertex( "ID" )
        cur_vertex.func_add_child( Graph.Vertex( "Child" ) )
        str_result = cur_vertex.func_has_parent()
        self.func_test_equals( str_answer, str_result )

    ###### Graph

# init
    def test_init_graph(self):
      """ Test init for graph. """
 
      str_answer = "Graph:VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }"
      cur_graph = Graph.Graph()
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

# add vertex
    def test_add_vertex_with_no_parent(self):
      """ Test test adding a vertex with no parent. """
 
      str_answer = "Graph:VERTEX{ ID=One;Parents=[\'_i_am_Groot_'];Children=[];Type=VERTEX };VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[\'One\'];Type=VERTEX }"
      cur_graph = Graph.Graph()
      cur_graph.func_add_vertex( Graph.Vertex( "One" ) )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_add_multiple_vertices(self):
      """ Test test adding multiple vertices with no parent. """
 
      str_answer = "".join([ "Graph:VERTEX{ ID=One;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX };",
                             "VERTEX{ ID=Three;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX };",
                             "VERTEX{ ID=Two;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX };",
                             "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['One', 'Three', 'Two'];Type=VERTEX }" ])
      cur_graph = Graph.Graph()
      cur_graph.func_add_vertex( Graph.Vertex( "One" ) )
      cur_graph.func_add_vertex( Graph.Vertex( "Two" ) )
      cur_graph.func_add_vertex( Graph.Vertex( "Three" ) )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_add_vertex_with_parent_linear(self):
      """ Test adding a vertex with no parent. """
 
      str_answer = "".join([ "Graph:VERTEX{ ID=One;Parents=['Two'];Children=[];Type=VERTEX };",
                             "VERTEX{ ID=Two;Parents=['_i_am_Groot_'];Children=['One'];Type=VERTEX };",
                             "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['Two'];Type=VERTEX }" ])
      cur_graph = Graph.Graph()
      vtx_one = Graph.Vertex( "One" )
      cur_graph.func_add_vertex( vtx_one )
      cur_graph.func_add_edge( Graph.Vertex( "Two" ), vtx_one )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_add_vertex_with_parents_dag(self):
      """
      Test creating a complex dag with add vertex.
      """
 
      str_answer = "".join([
                      "Graph:VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22, 23];Type=VERTEX };",
                      "VERTEX{ ID=22;Parents=[21];Children=[24];Type=VERTEX };",
                      "VERTEX{ ID=23;Parents=[21];Children=[24];Type=VERTEX };",
                      "VERTEX{ ID=24;Parents=[22, 23];Children=[];Type=VERTEX };",
                      "VERTEX{ ID=33;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX };",
                      "VERTEX{ ID=Eight;Parents=['Six'];Children=[];Type=VERTEX };",
                      "VERTEX{ ID=Five;Parents=['Three'];Children=[];Type=VERTEX };",
                      "VERTEX{ ID=Four;Parents=['Two'];Children=['Seven', 'Six'];Type=VERTEX };",
                      "VERTEX{ ID=One;Parents=['_i_am_Groot_'];Children=['Two'];Type=VERTEX };",
                      "VERTEX{ ID=Seven;Parents=['Four'];Children=[];Type=VERTEX };",
                      "VERTEX{ ID=Six;Parents=['Four'];Children=['Eight'];Type=VERTEX };",
                      "VERTEX{ ID=Three;Parents=['Two'];Children=['Five'];Type=VERTEX };",
                      "VERTEX{ ID=Two;Parents=['One'];Children=['Four', 'Three'];Type=VERTEX };",
                      "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21, 33, 'One'];Type=VERTEX }" ])

      cur_graph = self.func_make_complex_graph()
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

# _iter_
    def test_iter_for_empty_graph( self ):
      """ 
      Iter should give a breadth first traversal across all graphs.
      """
 
      str_answer = "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }"
      cur_graph = Graph.Graph()
      lstr_traversal = []
      for vtx_node in cur_graph:
        lstr_traversal.append( vtx_node.func_detail() )
      str_result = "\n".join( lstr_traversal )
      self.func_test_equals( str_answer, str_result )
    
    def test_iter_for_one_vertex_graph( self ):
      """ 
      Iter should give a breadth first traversal across all graphs.
      """
 
      str_answer = "\n".join([ "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[33];Type=VERTEX }",
                             "VERTEX{ ID=33;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX }" ])
      cur_graph = Graph.Graph()
      vtx_33 = Graph.Vertex( 33 )
      cur_graph.func_add_vertex( vtx_33 )
      lstr_traversal = []
      for vtx_node in cur_graph:
        lstr_traversal.append( vtx_node.func_detail() )
      str_result = "\n".join( lstr_traversal )
      self.func_test_equals( str_answer, str_result )

    def test_iter_for_one_cycle_graph( self ):
      """ 
      Iter should give a breadth first traversal across all graphs.
      """
 
      str_answer = "\n".join( sorted( [ "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21];Type=VERTEX }",
                              "VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22, 23];Type=VERTEX }",
                              "VERTEX{ ID=22;Parents=[21];Children=[24];Type=VERTEX }",
                              "VERTEX{ ID=23;Parents=[21];Children=[24];Type=VERTEX }",
                              "VERTEX{ ID=24;Parents=[22, 23];Children=[];Type=VERTEX }" ] ) )
      cur_graph = self.func_make_one_cycle_graph()
      lstr_traversal = []
      for vtx_node in cur_graph:
        lstr_traversal.append( vtx_node.func_detail() )
      str_result = "\n".join( sorted( lstr_traversal ) )
      self.func_test_equals( str_answer, str_result )

# _str_
    def test_str_for_empty_graph( self ):
      """
      Test str for empty graph
      """
      str_answer = "Graph: 1 vertices." 
      cur_graph = Graph.Graph()
      str_result = str( cur_graph )
      self.func_test_equals( str_answer, str_result )

    def test_str_for_4_vertex_graph( self ):
      """
      Test str for graph for 4 vertices
      """
      str_answer = "Graph: 5 vertices." 
      cur_graph = self.func_make_one_cycle_graph()
      str_result = str( cur_graph )
      self.func_test_equals( str_answer, str_result )

    def test_str_for_complex_vertex_graph( self ):
      """
      Test str for complex graph of 13  vertices
      """
      str_answer = "Graph: 14 vertices." 
      cur_graph = self.func_make_complex_graph()
      str_result = str( cur_graph )
      self.func_test_equals( str_answer, str_result )

# _len_
    def test_len_for_empty_graph( self ):
      """
      Test len for empty graph
      """
      str_answer = "1" 
      cur_graph = Graph.Graph()
      str_result = str( len( cur_graph ) )
      self.func_test_equals( str_answer, str_result )

    def test_len_for_4_vertex_graph( self ):
      """
      Test len for graph for 4 vertices
      """
      str_answer = "5" 
      cur_graph = self.func_make_one_cycle_graph()
      str_result = str( len( cur_graph ) )
      self.func_test_equals( str_answer, str_result )

    def test_len_for_complex_vertex_graph( self ):
      """
      Test len for complex graph of 13  vertices
      """
      str_answer = "14" 
      cur_graph = self.func_make_complex_graph()
      str_result = str( len( cur_graph ) )
      self.func_test_equals( str_answer, str_result )

# Contains
    def test_contains_for_empty_graph( self ):
      """
      Test contains for empty graph
      """
      str_answer = "False" 
      cur_graph = Graph.Graph()
      cur_vtx = Graph.Vertex( "NOT" )
      str_result = str( cur_vtx in cur_graph )
      self.func_test_equals( str_answer, str_result )

    def test_contains_for_4_vertex_graph( self ):
      """
      Test contains for graph for false
      """
      str_answer = "False" 
      cur_graph = self.func_make_one_cycle_graph()
      cur_vtx = Graph.Vertex( "NOT" )
      str_result = str( cur_vtx in cur_graph )
      self.func_test_equals( str_answer, str_result )

    def test_contains_for_complex_vertex_graph( self ):
      """
      Test contains for true
      """
      str_answer = "True" 
      cur_graph = self.func_make_one_cycle_graph()
      cur_vtx = Graph.Vertex( 22 )
      str_result = str( cur_vtx in cur_graph )
      str_result = str( len( cur_graph ) )

# get vertex
    def test_get_vertex_in_empty_graph( self ):
      """
      Test get for empty graph
      """
      str_answer = "None" 
      cur_graph = Graph.Graph()
      str_result = str( cur_graph.func_get_vertex( "NOT" ) )
      self.func_test_equals( str_answer, str_result )

    def test_get_vertex_in_4_vertex_graph_false( self ):
      """
      Test get for graph for false
      """
      str_answer = "None" 
      cur_graph = self.func_make_one_cycle_graph()
      str_result = str( cur_graph.func_get_vertex( "NOT" ) )
      self.func_test_equals( str_answer, str_result )

    def test_get_vertex_in_4_vertex_graph_true( self ):
      """
      Test get for graph for false
      """
      str_answer = "VERTEX{ ID=22;Parents=[21];Children=[24];Type=VERTEX }" 
      cur_graph = self.func_make_one_cycle_graph()
      str_result = cur_graph.func_get_vertex( 22 ).func_detail()
      self.func_test_equals( str_answer, str_result )

# Get graph roots
    def test_get_graph_roots_in_empty_graph( self ):
      """
      Test get roots for empty graph
      """
      str_answer = "[]" 
      cur_graph = Graph.Graph()
      str_result = str( cur_graph.func_get_graph_roots() )
      self.func_test_equals( str_answer, str_result )

    def test_get_graph_roots_in_4_vertex_graph( self ):
      """
      Test get roots for 1 root
      """
      str_answer = "[\'VERTEX{ 21, Parent count: 1, Children count: 2 }\']" 
      cur_graph = self.func_make_one_cycle_graph()
      str_result = str([ str( vtx_root ) for vtx_root in cur_graph.func_get_graph_roots() ])
      self.func_test_equals( str_answer, str_result )

    def test_get_graph_roots_in_complex_graph( self ):
      """
      Test get roots for 3 root
      """

      lstr_answer = sorted( [ "VERTEX{ One, Parent count: 1, Children count: 1 }",
                     "VERTEX{ 21, Parent count: 1, Children count: 2 }",
                     "VERTEX{ 33, Parent count: 1, Children count: 0 }" ] )

      str_answer = "".join( lstr_answer )

      cur_graph = self.func_make_complex_graph()
      str_result = "".join(sorted([ str( vtx_root ) for vtx_root in cur_graph.func_get_graph_roots() ]))
      self.func_test_equals( str_answer, str_result )

# Get terminal vertices
    def test_get_terminal_vertices_in_empty_graph( self ):
      """
      Test terminal_vertices for empty graph
      """
      str_answer = "[]" 
      cur_graph = Graph.Graph()
      str_result = str([ str( vtx_root ) for vtx_root in cur_graph.func_get_terminal_vertices() ])
      self.func_test_equals( str_answer, str_result )

    def test_terminal_vertices_in_4_vertex_graph( self ):
      """
      Test terminal_vertices for 1 root
      """
      str_answer = "[\'VERTEX{ 24, Parent count: 2, Children count: 0 }\']" 
      cur_graph = self.func_make_one_cycle_graph()
      str_result = str([ str( vtx_root ) for vtx_root in cur_graph.func_get_terminal_vertices() ])
      self.func_test_equals( str_answer, str_result )

    def test_terminal_vertices_in_complex_graph( self ):
      """
      Test terminal_vertices for complex graph
      """
      str_answer = "".join([ "[",
                             "\'VERTEX{ 24, Parent count: 2, Children count: 0 }\', ",
                             "\'VERTEX{ 33, Parent count: 1, Children count: 0 }\', ",
                             "\'VERTEX{ Eight, Parent count: 1, Children count: 0 }\', ",
                             "\'VERTEX{ Five, Parent count: 1, Children count: 0 }\', ",
                             "\'VERTEX{ Seven, Parent count: 1, Children count: 0 }\'",
                              "]" ])
      cur_graph = self.func_make_complex_graph()
      str_result = str(sorted([ str( vtx_root ) for vtx_root in cur_graph.func_get_terminal_vertices() ]))
      self.func_test_equals( str_answer, str_result )

# Delete vertices
    def test_delete_vertex_in_empty_graph( self ):
      """
      Test delete vertex for empty graph
      """
      str_answer = "Graph:VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }" 
      cur_graph = Graph.Graph()
      cur_graph.func_delete_vertex( Graph.Vertex( "Not" ) )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_delete_vertices_in_4_vertex_graph_1_del( self ):
      """
      Test delete vertices in a 4 vertex graph deleting 1 vtx
      """
      str_answer = "\n".join( sorted( [ "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21];Type=VERTEX }",
                               "VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22, 23];Type=VERTEX }",
                               "VERTEX{ ID=22;Parents=[21];Children=[];Type=VERTEX }",
                               "VERTEX{ ID=23;Parents=[21];Children=[];Type=VERTEX }" ] ) )
      cur_graph = self.func_make_one_cycle_graph()
      cur_vtx = cur_graph.func_get_vertex( 24 )
      cur_graph.func_delete_vertex( cur_vtx )
      str_result = "\n".join( sorted( [ vtx_root.func_detail() for vtx_root in cur_graph ] ) )
      self.func_test_equals( str_answer, str_result )

    def test_delete_vertices_in_4_vertex_graph_2_del( self ):
      """
      Test delete vertices in a 4 vertex graph deleting 2 vtx
      """
      str_answer = str( "\n".join( [ "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21];Type=VERTEX }",
                              "VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22];Type=VERTEX }",
                              "VERTEX{ ID=22;Parents=[21];Children=[];Type=VERTEX }" ]))
      cur_graph = self.func_make_one_cycle_graph()
      cur_vtx = cur_graph.func_get_vertex( 24 )
      cur_graph.func_delete_vertex( cur_vtx )
      cur_vtx = cur_graph.func_get_vertex( 23 )
      cur_graph.func_delete_vertex( cur_vtx )
      str_result = "\n".join([ vtx_root.func_detail() for vtx_root in cur_graph ])
      self.func_test_equals( str_answer, str_result )

    def test_delete_vertices_in_4_vertex_graph_1_del_mid( self ):
      """
      Test delete vertices in a 4 vertex graph deleting 1 vtx in the middle
      """
      str_answer = str( "\n".join( [ "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }" ]))
      cur_graph = self.func_make_one_cycle_graph()
      cur_vtx = cur_graph.func_get_vertex( 21 )
      cur_graph.func_delete_vertex( cur_vtx )
      str_result = "\n".join([ vtx_root.func_detail() for vtx_root in cur_graph ])
      self.func_test_equals( str_answer, str_result )

# Merge Vertex
    def test_merge_vertex_empty_graph_none_vertex( self ):
      """
      Test merging a none vertex with an empty graph
      """
      str_answer = "Graph:VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[];Type=VERTEX }"
      cur_graph = Graph.Graph()
      cur_graph.func_merge_vertex( None )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_merge_vertex_empty_graph_simple_vertex( self ):
      """
      Test merging a simple vertex with an empty graph
      """
      str_answer = ";".join(sorted([ "Graph:VERTEX{ ID=Test;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['Test'];Type=VERTEX }" ]))
                               
      cur_graph = Graph.Graph()
      cur_graph.func_merge_vertex( Graph.Vertex( "Test" ) )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_merge_vertex_empty_graph_complex_vertex( self ):
      """
      Test merging a vertex with children and parents with an empty graph
      """
      str_answer = ";".join(sorted([ 
                                     "Graph:VERTEX{ ID=Child1;Parents=['Test'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Child2;Parents=['Test'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Parent1;Parents=['_i_am_Groot_'];Children=['Test'];Type=VERTEX }",
                                     "VERTEX{ ID=Test;Parents=['Parent1'];Children=['Child1', 'Child2'];Type=VERTEX }",
                                     "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=['Parent1'];Type=VERTEX }"
                                   ]))
                               
      cur_graph = Graph.Graph()
      cur_vertex = Graph.Vertex( "Test" )
      cur_vertex.func_add_parent( Graph.Vertex( "Parent1" ) )
      cur_vertex.func_add_child( Graph.Vertex( "Child1" ) )
      cur_vertex.func_add_child( Graph.Vertex( "Child2" ) )
      cur_graph.func_merge_vertex( cur_vertex )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_merge_vertex_graph_none_vertex( self ):
      """
      Test merging a none vertex with a graph with existing parents and children
      """
      str_answer = ";".join(sorted([ 
                                     "Graph:VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22, 23];Type=VERTEX }",
                                     "VERTEX{ ID=22;Parents=[21];Children=[24];Type=VERTEX }",
                                     "VERTEX{ ID=23;Parents=[21];Children=[24];Type=VERTEX }",
                                     "VERTEX{ ID=24;Parents=[22, 23];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=33;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Eight;Parents=['Six'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Five;Parents=['Three'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Four;Parents=['Two'];Children=['Seven', 'Six'];Type=VERTEX }",
                                     "VERTEX{ ID=One;Parents=['_i_am_Groot_'];Children=['Two'];Type=VERTEX }",
                                     "VERTEX{ ID=Seven;Parents=['Four'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Six;Parents=['Four'];Children=['Eight'];Type=VERTEX }",
                                     "VERTEX{ ID=Three;Parents=['Two'];Children=['Five'];Type=VERTEX }",
                                     "VERTEX{ ID=Two;Parents=['One'];Children=['Four', 'Three'];Type=VERTEX }",
                                     "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21, 33, 'One'];Type=VERTEX }"
                                   ]))

      cur_graph = Graph.Graph()                               
      cur_graph = self.func_make_complex_graph()
      cur_graph.func_merge_vertex( None )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_merge_vertex_graph_simple_orthogonal_vertex( self ):
      """
      Test merging a vertex not contained in the graph with a graph with existing parents and children
      """
      str_answer = ";".join(sorted([ 
                                     "Graph:VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22, 23];Type=VERTEX }",
                                     "VERTEX{ ID=22;Parents=[21];Children=[24];Type=VERTEX }",
                                     "VERTEX{ ID=23;Parents=[21];Children=[24];Type=VERTEX }",
                                     "VERTEX{ ID=24;Parents=[22, 23];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=33;Parents=['_i_am_Groot_'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Child1;Parents=['Test'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Child2;Parents=['Test'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Eight;Parents=['Six'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Five;Parents=['Three'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Four;Parents=['Two'];Children=['Seven', 'Six'];Type=VERTEX }",
                                     "VERTEX{ ID=One;Parents=['_i_am_Groot_'];Children=['Two'];Type=VERTEX }",
                                     "VERTEX{ ID=Parent1;Parents=['_i_am_Groot_'];Children=['Test'];Type=VERTEX }",
                                     "VERTEX{ ID=Seven;Parents=['Four'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Six;Parents=['Four'];Children=['Eight'];Type=VERTEX }",
                                     "VERTEX{ ID=Test;Parents=['Parent1'];Children=['Child1', 'Child2'];Type=VERTEX }",
                                     "VERTEX{ ID=Three;Parents=['Two'];Children=['Five'];Type=VERTEX }",
                                     "VERTEX{ ID=Two;Parents=['One'];Children=['Four', 'Three'];Type=VERTEX }",
                                     "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21, 33, 'One', 'Parent1'];Type=VERTEX }"
                                   ]))

      cur_graph = self.func_make_complex_graph()
      cur_vertex = Graph.Vertex( "Test" )
      cur_vertex.func_add_parent( Graph.Vertex( "Parent1" ) )
      cur_vertex.func_add_child( Graph.Vertex( "Child1" ) )
      cur_vertex.func_add_child( Graph.Vertex( "Child2" ) )
      cur_graph.func_merge_vertex( cur_vertex )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

    def test_merge_vertex_graph_overlapping_vertex( self ):
      """
      Test merging a vertex contained in the graph with a graph with existing parents and children
      """
      str_answer = ";".join(sorted([ 
                                     "Graph:VERTEX{ ID=21;Parents=['_i_am_Groot_'];Children=[22, 23];Type=VERTEX }",
                                     "VERTEX{ ID=22;Parents=[21, 'Test'];Children=[24];Type=VERTEX }",
                                     "VERTEX{ ID=23;Parents=[21];Children=[24];Type=VERTEX }",
                                     "VERTEX{ ID=24;Parents=[22, 23];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=33;Parents=['Test'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Eight;Parents=['Six'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Five;Parents=['Three'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Four;Parents=['Two'];Children=['Seven', 'Six'];Type=VERTEX }",
                                     "VERTEX{ ID=One;Parents=['_i_am_Groot_'];Children=['Two'];Type=VERTEX }",
                                     "VERTEX{ ID=Seven;Parents=['Four'];Children=[];Type=VERTEX }",
                                     "VERTEX{ ID=Six;Parents=['Four'];Children=['Eight', 'Test'];Type=VERTEX }",
                                     "VERTEX{ ID=Test;Parents=['Six'];Children=[22, 33];Type=VERTEX }",
                                     "VERTEX{ ID=Three;Parents=['Two'];Children=['Five'];Type=VERTEX }",
                                     "VERTEX{ ID=Two;Parents=['One'];Children=['Four', 'Three'];Type=VERTEX }",
                                     "VERTEX{ ID=_i_am_Groot_;Parents=[];Children=[21, 'One'];Type=VERTEX }"
                                   ]))

      cur_graph = self.func_make_complex_graph()
      cur_vertex = Graph.Vertex( "Test" )
      cur_vertex.func_add_parent( Graph.Vertex( "Six" ) )
      cur_vertex.func_add_child( Graph.Vertex( 33 ) )
      cur_vertex.func_add_child( Graph.Vertex( 22 ) )
      cur_graph.func_merge_vertex( cur_vertex )
      str_result = cur_graph.func_detail()
      self.func_test_equals( str_answer, str_result )

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( GraphTester )
