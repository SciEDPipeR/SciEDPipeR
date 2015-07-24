from collections import deque

STR_TYPE_VERTEX = "VERTEX"

class Graph:
  """
  Bi-directional graph with root.
  Can represent any combination of DAGs and singleton groupings.
  Access to any vertex is through a look-up and is very efficient.
  """

  def __init__(self):
    self.vertices = {}
    """ All the vertices can be accessed through this dict """
    self.root = Vertex( "_i_am_Groot_" )
    """ Root hold all nodes that have no parents, this allows multiple DAGs and singletons without loosing them."""
    # Every graph has root ("Groot")
    self.func_add_vertex( vtx_new=self.root )

  def func_get_terminal_vertices( self ):
    """
    Turn vertices that are terminal.
    """

    for cur_vtx in self:
      if not cur_vtx.func_get_children(): 
        yield cur_vtx

  def func_get_vertex( self, str_id ):
    if str_id:
      return self.vertices.get( str_id, None)
    return None

  def func_get_graph_roots( self ):
    """
    Returns the roots of each subset graph in the data.
    """

    return self.root.get_children()

  def func_add_vertex( self, vtx_new ):
    """ Note will write over any existing vertex with the same key / id """

    self.vertices[ vtx_new.str_id ] = vtx_new

    # If the vertex has no parent and is not Groot, attach to Groot
    if not vtx_new.func_has_parent() and not vtx_new.str_id == self.root.str_id:
      self.func_add_edge( self.root, vtx_new )
      return self

  def __contains__( self , vtx_checking ):
    """ Overwrite the 'in' functionality """
    if not vtx_checking:
      return False
    return vtx_checking.str_id in self.vertices


  def func_add_edge( self, vtx_parent, vtx_child ):
    """ Both parents must be valid nodes, if they are not in the graph they will be added. """

    # Deny invalid nodes
    if not vtx_parent or not vtx_child:
      return False
    # Add parent to the graph if it does not exist
    if vtx_parent not in self:
      self.func_add_vertex( vtx_parent )
    # Add child to graph if it does not exist
    if vtx_child not in self:
      self.func_add_vertex( vtx_child )
    # Check for the case of the child being attached to the Groot
    # if it is, remove from Groot
    if len( vtx_child.dict_vtx_parents ) == 1 and ( self.root.str_id in vtx_child.dict_vtx_parents ):
      vtx_child.func_remove_parent( self.root )
      self.root.func_remove_child( vtx_child )
    # Double link vertex
    self.vertices[ vtx_parent.str_id ].func_add_child( self.vertices[ vtx_child.str_id ] )
    self.vertices[ vtx_child.str_id ].func_add_parent( self.vertices[ vtx_parent.str_id ] )
    return True    

  def func_delete_vertex( self, vtx_del ):
    lvtx_children = vtx_del.func_get_children()
    lvtx_parent = vtx_del.func_get_parents()
    for vtx_child in lvtx_children:
      vtx_child.func_remove_parent( vtx_del )
    for vtx_parent in lvtx_parents:
      vtx_parent.func_remove_child( vtx_del )
    del self.vertices[ vtx_del ]


  def func_merge_vertex( vtx_merge ):

    if vtx_merge not in self.graph_commands:
      self.graph_commands.func_add_vertex( vtx_merge )
    else:
      # If the dependency is already in the graph.
      # Give that dependency the links from this dependency and then del this vtx
      # get existing vertex
      vtx_cur_dep = self.graph_commands.func_get_vertex( vtx_merge.str_id )
      # Get linked vertices to move over
      lvtx_children = vtx_merge.func_get_children()
      lvtx_parents = vtx_merge.func_get_parents()
      # Delete vertex
      self.graph_commands.func_delete_vertex( vtx_merge )
      # Transfer links to already established vertex
      for vtx_dep_child in lvtx_children: 
        self.func_add_edge( vtx_cur_dep, vtx_dep_child )
      for vtx_parent in lvtx_parents:
        if not ( vtx_parent.str_id == self.graph_commands.root.str_id ):
          self.func_add_edge( vtx_parent, vtx_cur_dep )

#  def func_unlink_vertex( self, vtx_del ):
#    if vtx_del in self:
#      for vtx_del_parent in vtx_del.func_get_parents():
#        for vtx_del_child in vtx_del.func_get_children():
#          vtx_parent_parent.func_add_edge( vtx_del_parent, vtx_del_child )
#      del self.vertices[ vtx_del.str_id ]

  def __iter__( self ):
    """
    Generator performs a breadth-wise traversal.
    """

    dict_visited = { self.root: None }
    """ Indicate which nodes are visted """
    dq_cache = deque( [ self.root ] )
    """ Cache of nodes to vist """

    # Iterate through cache and add children to cache
    while len( dq_cache ):
      vtx_cur = dq_cache.popleft()
      # Add children to cache from current nodes and indicated visited
      for vtx_child in vtx_cur.func_get_children():
        # Make sure you did not already see the child
        if not vtx_child in dict_visited:
          # If this is the first time we see the vertex, add to cache and indicate it is visited.
          dq_cache.append( vtx_child )
          dict_visited[ vtx_child ] = None
      yield vtx_cur

  def __len__( self ):
    return len( self.vertices )

  def __str__( self ):
    return "Graph: " + str( len( self.vertices  )) + " vertices."

  def func_detail( self ):
    lstr_vertices = []
    for str_key in sorted( self.vertices.keys() ):
      lstr_vertices.append( self.vertices[ str_key ].func_detail() )
    return "Graph:" + ";".join( lstr_vertices )


class Vertex:

  def __init__( self, str_id ):
    """
    Init

    * str_id : Id for vertex
             : String but could be a numeric.
    """
    self.str_id = str_id
    self.dict_vtx_parents = {}
    self.dict_vtx_children = {}
    self.str_type = STR_TYPE_VERTEX

  def __id__( self ):
    return hash( self.str_id )

  def func_add_parent( self, vtx_parent ):
    """
    Add parent to the vertex.
    
    * vtx_parent : Parent vertex
               : vertex

    * return : void
    """
    if vtx_parent and vtx_parent.str_id:
      self.dict_vtx_parents[ vtx_parent.str_id ] = vtx_parent

  def func_remove_parent( self, vtx_parent ):
    del self.dict_vtx_parents[ vtx_parent ]

  def func_has_parent( self ):
    """
    Checks if the vertex has parents.

    * return : True indicates has parent.
             : boolean
    """
    return True if self.dict_vtx_parents else False


  def func_add_child( self, vtx_child ):
    """
    Add child to vertex.

    * vtx_child : Child vertex
                : Vertex
    * return : void
    """

    if vtx_child and vtx_child.str_id:
      self.dict_vtx_children[ vtx_child.str_id ] = vtx_child

  def func_has_child( self ):
    return True if self.dict_vtx_children else False

  def func_remove_child( self, vtx_child ):
    del self.dict_vtx_children[ vtx_child ]

  def func_get_parents( self ):
    return sorted( self.dict_vtx_parents.values() )

  def func_get_children( self ):
    return sorted( self.dict_vtx_children.values() )

  def func_remove_child( self, vtx_child ):
    if vtx_child.str_id in self.dict_vtx_children:
      del self.dict_vtx_children[ vtx_child.str_id ]

  def __str__( self ):
    return "".join([ "VERTEX{self.str_id, Parent count: ",
                     str(len(self.dict_vtx_parent)),
                     " Children count: ",
                     str(len(self.dict_vtx_children)) ])

  def func_detail( self ):
    return ";".join( [ "VERTEX{ ID=" + str( self.str_id ),
                       "Parents=" + str( sorted( self.dict_vtx_parents.keys() ) ),
                       "Children=" + str( sorted( self.dict_vtx_children.keys() ) ) + "}" ] )
