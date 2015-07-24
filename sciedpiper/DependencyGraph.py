
class DependencyGraph( Graph ):
  """
  Graph that contains functions related to dependency trees and not a generic graph.
  """

  def __init__(self):
    Graph.__init__( self )


  def func_get_terminal_products( self ):
    """
    Turn vertices that are terminal products.
    """

    for vtx_terminal in self.func_get_terminal_vertices():
      if vtx_terminal.str_type == Resource.STR_TYPE:
        yield vtx_terminal


  def func_get_input_files( self ):
    for vtx_input in self.func_get_graph_roots():
      if vtx_input.str_type == Resource.STR_TYPE:
        yield vtx_input 


  def func_get_dependencies( self ):
    for vtx_cur in self:
      if not ( vtx_cur.str_type == Resource.STR_TYPE ):
        continue
      if vtx_cur.func_has_child():
        yield


  def func_get_products( self ):
    for vtx_cur in self:
      if not ( vtx_cur.str_type ==  Reosurce.STR_TYPE ):
        continue
      if vtx_cur.has_parent()
        yield
