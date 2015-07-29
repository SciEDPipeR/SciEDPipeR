__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Graph
import Resource

class DependencyGraph( Graph.Graph ):
  """
  Graph that contains functions related to dependency trees and not a generic graph.
  """

  def __init__(self):
    Graph.Graph.__init__( self )


  # Tested
  def func_get_terminal_products( self ):
    """
    Turn vertices that are terminal products.
    """

    for vtx_terminal in self.func_get_terminal_vertices():
      if vtx_terminal.str_type == Resource.STR_TYPE:
        yield vtx_terminal

  # Tested
  def func_get_input_files( self ):
    for vtx_input in self.func_get_graph_roots():
      if vtx_input.str_type == Resource.STR_TYPE:
        yield vtx_input 

  # Tested
  def func_get_dependencies( self ):
    for vtx_cur in self:
      if not ( vtx_cur.str_type == Resource.STR_TYPE ):
        continue
      if vtx_cur.func_has_child():
        yield vtx_cur

  #Tested
  def func_get_products( self ):
    for vtx_cur in self:
      if not ( vtx_cur.str_type ==  Resource.STR_TYPE ):
        continue
      if vtx_cur.func_has_parent() and ( not self.root in vtx_cur.func_get_parents()):
        yield vtx_cur
