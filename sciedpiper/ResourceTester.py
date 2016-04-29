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

import Command
import DependencyTree
import Graph
import Resource
import os
import ParentPipelineTester
import unittest

class ResourceTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the Resource object.
    """

    def test_init_for_one_relative_path_product( self ):
        """ Testing init for updating relative path. """

        str_path_one = os.path.join( "This","is","a","path1" )
        str_answer = " ".join( [ "PATH:",os.path.join( os.getcwd(), str_path_one )+ ",",
                                 "CLEAN:",str( Resource.CLEAN_DEFAULT ) + ",",
                                 "Product","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)

    def test_init_for_one_relative_path_product_connected( self ):
        """ Testing init for resource with parents and children. """

        str_path_one = os.path.join( "This","is","a","path1" )
        str_answer = " ".join( [ "PATH:",os.path.join( os.getcwd(), str_path_one )+ ",",
                                 "CLEAN:",str( Resource.CLEAN_DEFAULT ) + ",",
                                 "Product","PARENTS: ['Parent'] CHILDREN: ['Child']" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True )
        rsc_test.func_add_child( Graph.Vertex( "Child" ) )
        rsc_test.func_add_parent( Graph.Vertex( "Parent" ) )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)

    def test_init_for_one_relative_path_dependency( self ):
        """ Testing init for updating relative path (dependency). """
 
        str_path_one = os.path.join( "This","is","a","path1" )
        str_answer = " ".join( [ "PATH:",os.path.join( os.getcwd(), str_path_one )+ ",",
                                 "CLEAN:",str( Resource.CLEAN_DEFAULT ) + ",",
                                 "Dependency","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=False )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)

    def test_init_for_one_abs_path_product( self ):
        """ Testing init for an absolute path. """
 
        str_path_one = os.path.join( os.getcwd(),"This","is","a","path1" )
        str_answer = " ".join( [ "PATH:", str_path_one + ",",
                                 "CLEAN:", str( Resource.CLEAN_DEFAULT ) + ",",
                                 "Product","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)

    def test_init_for_one_abs_path_dependency( self ):
        """ Testing init for an absolute path. """
        str_path_one = os.path.join( os.getcwd(),"This","is","a","path1" )
        str_answer = " ".join( [ "PATH:", str_path_one + ",",
                                 "CLEAN:", str( Resource.CLEAN_DEFAULT ) + ",",
                                 "Dependency","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=False, i_clean=Resource.CLEAN_DEFAULT )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)
 
#    def test_init_for_none_path_product( self ):
#        """ Testing init for a none path. """
# 
#        str_path_one = None
#        self.func_test_error( Resource.Resource( str_path=str_path_one, f_is_product=False ) )

#    def test_init_for_blank_path_product( self ):
#        """ Testing init for a blank path. """
# 
#        str_path_one = ""
#        self.func_test_error( Resource.Resource( str_path=str_path_one, f_is_product=True ) )

    def test_init_for_clean_3( self ):
        """ Testing init for cleaning level 3. """
 
        str_path_one = os.path.join( os.getcwd(),"This","is","a","path1" )
        str_answer = " ".join( [ "PATH:", str_path_one + ",",
                                 "CLEAN:", str( Resource.CLEAN_ALWAYS ) + ",",
                                 "Product","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_ALWAYS )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)
 
    def test_init_for_clean_2( self ):
        """ Testing init for cleaning level 2. """
 
        str_path_one = os.path.join( os.getcwd(),"This","is","a","path1" )
        str_answer = " ".join( [ "PATH:", str_path_one + ",",
                                 "CLEAN:", str( Resource.CLEAN_AS_TEMP ) + ",",
                                 "Product","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_AS_TEMP )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)
 
    def test_init_for_clean_1( self ):
        """ Testing init for cleaning level 1. """
 
        str_path_one = os.path.join( os.getcwd(),"This","is","a","path1" )
        str_answer = " ".join( [ "PATH:", str_path_one + ",",
                                 "CLEAN:", str( Resource.CLEAN_NEVER ) + ",",
                                 "Product","PARENTS: [] CHILDREN: []" ] )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_NEVER )
        str_result = str( rsc_test )
        self.func_test_equals(str_answer, str_result)

    def test_remove_temp_file( self ):
        """ Testing remove temp files from a list of temp files. """

        str_temp_dir = "dev"
        
        # Answer
        lstr_answer = [ os.path.sep + os.path.join( "This","is","a","path1" ),
                        os.path.join ( str_temp_dir, "This","is","a","path1" ),
                        os.path.sep + os.path.join( str_temp_dir+"_not", "This","is","a","path1" )  ]

        # Get result
        lstr_test_files = [ os.path.sep + os.path.join( str_temp_dir, "This","is","a","path1" ),
                       os.path.sep + os.path.join( str_temp_dir+"_not", "This","is","a","path1" ),
                       os.path.join( str_temp_dir, "This","is","a","path1" ),
                       os.path.sep + os.path.join( "This","is","a","path1" ) ]
        lstr_result_files = Resource.Resource.func_remove_temp_files( lstr_files=lstr_test_files )

        # Compare
        f_success = str( sorted( lstr_answer ) ) == str( sorted( lstr_result_files ) )
        self.func_test_equals( True, f_success )

    def test_remove_temp_file_empty( self ):
        """ Testing remove temp files from an empty list of temp files. """

        # Answer
        lstr_answer = []

        # Get result
        lstr_test_files = []
        lstr_result_files = Resource.Resource.func_remove_temp_files( lstr_files=lstr_test_files )

        # Compare
        f_success = str( sorted( lstr_answer ) ) == str( sorted( lstr_result_files ) )
        self.func_test_equals( True, f_success )

    def test_remove_temp_file_none( self ):
        """ Testing remove temp files from a list of none and empty temp files. """

        # Answer
        lstr_answer = []

        # Get result
        lstr_test_files = [ None, "" ]
        lstr_result_files = Resource.Resource.func_remove_temp_files( lstr_files=lstr_test_files )

        # Compare
        f_success = str( sorted( lstr_answer ) ) == str( sorted( lstr_result_files ) )
        self.func_test_equals( True, f_success )

    def test_func_is_dependency_clean_level_for_good_case_never(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = never
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_NEVER )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_NEVER )
        f_answer = True
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_good_case_never_false(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = never
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_NEVER )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_ALWAYS )
        f_answer = False
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_good_case_always(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = always
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_ALWAYS )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_ALWAYS )
        f_answer = True
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_good_case_always_false(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = always
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_ALWAYS )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_NEVER )
        f_answer = False
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_good_case_temp(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = temp
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_AS_TEMP )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_AS_TEMP )
        f_answer = True
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_good_case_temp(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = temp
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=Resource.CLEAN_AS_TEMP )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_NEVER )
        f_answer = False
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_bad_case_none(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = None
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=None )
        f_result = rsc_test.func_is_dependency_clean_level( Resource.CLEAN_AS_TEMP )
        f_answer = False
        self.func_test_equals( f_answer, f_result )

    def test_func_is_dependency_clean_level_for_bad_case_none(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Level = None
        """
        str_path_one = os.path.join( os.path.sep, "This","is","a","path1" )
        rsc_test = Resource.Resource( str_path=str_path_one, f_is_product=True, i_clean=None )
        f_result = rsc_test.func_is_dependency_clean_level( None )
        f_answer = False
        self.func_test_equals( f_answer, f_result )

    def test_func_make_paths_absolute_for_empty_list( self ):
        """ Test for taking an empty list. """

        lstr_paths = [ ]
        lstr_path_result = Resource.Resource.func_make_paths_absolute( lstr_paths)

        lstr_answer = [ ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )

    def test_func_make_paths_absolute_for_one_rel_path( self ):
        """ Test for making a simple relative path absolute. """
        
        str_path_one = os.path.join( "Test","Path", "One" )
        lstr_paths = [ str_path_one ]
        lstr_path_result = Resource.Resource.func_make_paths_absolute( lstr_paths)
        
        str_answer_one = os.path.join( os.getcwd(), str_path_one )
        lstr_answer = [ str_answer_one ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )

    def test_func_make_paths_absolute_for_two_rel_path( self ):
        """ Test for making two simple relative path absolute. """
        
        str_path_one = os.path.join( "Test","Path", "One" )
        str_path_two = os.path.join( "Test","Path", "Two" )
        lstr_paths = [ str_path_one, str_path_two ]
        lstr_path_result = Resource.Resource.func_make_paths_absolute( lstr_paths)
        
        str_answer_one = os.path.join( os.getcwd(), str_path_one )
        str_answer_two = os.path.join( os.getcwd(), str_path_two )
        lstr_answer = [ str_answer_one, str_answer_two ]
        
        self.func_test_equals( sorted( lstr_answer ), sorted( lstr_path_result ) )

    def test_func_make_paths_absolute_for_one_abs_path( self ):
        """ Test for making a simple absolute path absolute. """
        
        str_path_one = os.path.sep + os.path.join( "Test","Path", "One" )
        lstr_paths = [ str_path_one ]
        lstr_path_result = Resource.Resource.func_make_paths_absolute( lstr_paths)
        
        str_answer_one = str_path_one
        lstr_answer = [ str_answer_one ]
        
        self.func_test_equals( sorted( lstr_answer ), sorted( lstr_path_result ) )
        
    def test_func_make_paths_absolute_for_two_abs_path( self ):
        """ Test for making two simple absolute paths absolute. """
        
        str_path_one = os.path.sep + os.path.join( "Test","Path", "One" )
        str_path_two = os.path.sep + os.path.join( "Test","Path", "Two" )
        lstr_paths = [ str_path_one, str_path_two ]
        lstr_path_result = Resource.Resource.func_make_paths_absolute( lstr_paths)
        
        str_answer_one = str_path_one
        str_answer_two = str_path_two
        lstr_answer = [ str_answer_one, str_answer_two ]
        
        self.func_test_equals( sorted( lstr_answer ), sorted( lstr_path_result ) )

    def test_func_make_paths_absolute_for_mixture_of_path( self ):
        """ Test for making two absolute paths and two relative paths absolute. """
        
        str_path_one = os.path.sep + os.path.join( "Test","Path", "One" )
        str_path_two = os.path.join( "Test","Path", "Two" )
        str_path_three = os.path.sep + os.path.join( "Test","Path", "Three" )
        str_path_four = os.path.join( "Test","Path", "Four" )
        lstr_paths = [ str_path_one, str_path_two, str_path_three, str_path_four ]
        lstr_path_result = Resource.Resource.func_make_paths_absolute( lstr_paths)
        
        str_answer_one = str_path_one
        str_answer_two = os.path.join( os.getcwd(), str_path_two )
        str_answer_three = str_path_three
        str_answer_four = os.path.join( os.getcwd(), str_path_four )
        lstr_answer = [ str_answer_one, str_answer_two, str_answer_three, str_answer_four ]
        
        self.func_test_equals( sorted( lstr_answer ), sorted( lstr_path_result ) )

    def test_func_get_dependencies_for_no_dependency_one_parent_dependencies( self ):
        """
        Test for getting dependencies from a resource that has only one 
        command parent and no dependencies
        """
        str_path_one = os.path.sep + os.path.join( "test","path", "dep" )
        str_path_three = os.path.sep + os.path.join( "test","path", "dep_dep" )
        str_answer = ";".join([])
        cur_cmd = Command.Command( "test_func_get_dependencies_for_one_dependency_one_parent_dependencies_1", [ str_path_three ], [ str_path_one ] )
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd ] )
        cur_dep = dt_cur.graph_commands.func_get_vertex( str_path_three )
        lrsc_deps = cur_dep.func_get_dependencies()
        str_result = ";".join( sorted( [ cur_rsc.str_id for cur_rsc in lrsc_deps ]) )
        self.func_test_equals( str_answer, str_result )

    def test_func_get_dependencies_for_one_dependency_one_parent_dependencies( self ):
        """
        Test for getting dependencies from a resource that has only one 
        command parent and one dependency
        """
        str_path_one = os.path.sep + os.path.join( "test","path", "dep" )
        str_path_three = os.path.sep + os.path.join( "test","path", "dep_dep" )
        str_path_two = os.path.join( "test","path", "product" )
        str_answer = ";".join([ str_path_three ])
        cur_cmd = Command.Command( "test_func_get_dependencies_for_one_dependency_one_parent_dependencies_1", [ str_path_three ], [ str_path_one ] )
        cur_cmd2 = Command.Command( "test_func_get_dependencies_for_one_dependency_one_parent_dependencies_2", [ str_path_one ], [ str_path_two ] )
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd2 ] )
        cur_dep = dt_cur.graph_commands.func_get_vertex( str_path_one )
        lrsc_deps = cur_dep.func_get_dependencies()
        str_result = ";".join( sorted( [ cur_rsc.str_id for cur_rsc in lrsc_deps ]) )
        self.func_test_equals( str_answer, str_result )

    def test_func_get_dependencies_for_two_dependency_one_parent_dependencies( self ):
        """
        Test for getting dependencies from a resource that has only one 
        command parent and two dependencies
        """
        str_path_one = os.path.sep + os.path.join( "test","path", "dep" )
        str_path_three = os.path.sep + os.path.join( "test","path", "dep_dep" )
        str_path_four = os.path.sep + os.path.join( "test","path", "dep_dep_2" )
        str_path_two = os.path.join( "test","path", "product" )
        str_answer = ";".join([ str_path_three, str_path_four ])
        cur_cmd = Command.Command( "test_func_get_dependencies_for_two_dependency_one_parent_dependencies_1", [ str_path_three, str_path_four ], [ str_path_one ] )
        cur_cmd2 = Command.Command( "test_func_get_dependencies_for_two_dependency_one_parent_dependencies_2", [ str_path_one ], [ str_path_two ] )
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd2 ] )
        cur_dep = dt_cur.graph_commands.func_get_vertex( str_path_one )
        lrsc_deps = cur_dep.func_get_dependencies()
        str_result = ";".join( sorted( [ cur_rsc.str_id for cur_rsc in lrsc_deps ]) )
        self.func_test_equals( str_answer, str_result )

    def test_func_get_dependencies_for_four_dependency_two_parent_dependencies( self ):
        """
        Test for getting dependencies from a resource that has two
        command parents and four dependencies
        """
        str_path_one = os.path.sep + os.path.join( "test","path", "dep" )
        str_path_three = os.path.sep + os.path.join( "test","path", "dep_dep" )
        str_path_four = os.path.sep + os.path.join( "test","path", "dep_dep_2" )
        str_path_five = os.path.sep + os.path.join( "test","path", "dep_dep_3" )
        str_path_six = os.path.sep + os.path.join( "test","path", "dep_dep_4" )
        str_path_two = os.path.join( "test","path", "product" )
        str_path_seven = os.path.join( "test","path", "product_2" )
        str_answer = ";".join([ str_path_three, str_path_four, str_path_five, str_path_six ])
        cur_cmd = Command.Command( "test_func_get_dependencies_for_two_dependency_two_parent_dependencies_1", [ str_path_three, str_path_four ], [ str_path_one ] )
        cur_cmd1 = Command.Command( "test_func_get_dependencies_for_two_dependency_two_parent_dependencies_2", [ str_path_five, str_path_six ], [ str_path_one, str_path_seven ] )
        cur_cmd2 = Command.Command( "test_func_get_dependencies_for_two_dependency_two_parent_dependencies_3", [ str_path_one ], [ str_path_two ] )
        dt_cur = DependencyTree.DependencyTree( [ cur_cmd, cur_cmd1, cur_cmd2 ] )
        cur_dep = dt_cur.graph_commands.func_get_vertex( str_path_one )
        lrsc_deps = cur_dep.func_get_dependencies()
        str_result = ";".join( sorted( [ cur_rsc.str_id for cur_rsc in lrsc_deps ]) )
        self.func_test_equals( str_answer, str_result )

    def test_func_get_dependencies_for_one_dependency_one_parent_product( self ):
        """
        Test for getting dependencies from a resource that has only one 
        command parent and one dependencies in that command.
        """
        str_path_one = os.path.sep + os.path.join( "test","path", "dep" )
        str_path_two = os.path.join( "test","path", "product" )
        str_answer = ";".join([ str_path_one ])
        cur_cmd = Command.Command( "test_func_get_dependencies_for_one_dependency_one_parent_product", [ str_path_one ], [ str_path_two ] )
        lrsc_deps = cur_cmd.lstr_products[ 0 ].func_get_dependencies()
        str_result = ";".join([ cur_rsc.str_id for cur_rsc in sorted( lrsc_deps ) ])
        self.func_test_equals( str_answer, str_result )

    def test_func_get_dependencies_for_two_dependency_one_parent_product( self ):
        """
        Test for getting dependencies from a resource that has two 
        command parent and one dependencies in that command.
        """
        str_path_one = os.path.sep + os.path.join( "test","path", "dep" )
        str_path_three = os.path.sep + os.path.join( "test","path", "dep2" )
        str_path_two = os.path.join( "test","path", "product" )
        str_answer = ";".join( sorted( [ str_path_one, str_path_three ] ) )
        cur_cmd = Command.Command( "test_func_get_dependencies_for_two_dependency_one_parent_product", [ str_path_one, str_path_three ], [ str_path_two ] )
        lrsc_deps = cur_cmd.lstr_products[ 0 ].func_get_dependencies()
        str_result = ";".join( sorted( [ cur_rsc.str_id for cur_rsc in lrsc_deps ]))
        self.func_test_equals( str_answer, str_result )

    def test_func_get_dependencies_for_no_dependency_one_parent_product( self ):
        """
        Test for getting dependencies from a resource that has no
        command parent and one dependencies in that command.
        """
        str_path_two = os.path.join( "test","path", "product" )
        str_answer = ";".join([ ])
        cur_cmd = Command.Command( "test_func_get_dependencies_for_two_dependency_one_parent_product", [], [ str_path_two ] )
        lrsc_deps = cur_cmd.lstr_products[ 0 ].func_get_dependencies()
        str_result = ";".join([ cur_rsc.str_id for cur_rsc in sorted( lrsc_deps ) ])
        self.func_test_equals( str_answer, str_result )

    # Test func_get_size
    def test_func_get_size_for_empty_file(self):
        """
        Test get size for empty file.
        """
        str_file = os.path.join(self.str_test_directory, "test_func_get_size_for_empty_file.txt")
        str_answer = "0.0 B"
        self.func_make_dummy_dir(self.str_test_directory)
        self.func_make_dummy_file(str_file, "")
        str_size = Resource.Resource(str_path=str_file, f_is_product=True).func_get_size()
        self.func_remove_files([str_file])
        self.func_remove_dirs([self.str_test_directory])
        self.func_test_equals(str_answer, str_size)

    def test_func_get_size_for_a_sentence_file(self):
        """
        Test get size for a sentence file.
        """
        str_file = os.path.join(self.str_test_directory, "test_func_get_size_for_a_sentence_file.txt")
        str_answer = "55.0 B"
        self.func_make_dummy_dir(self.str_test_directory)
        self.func_make_dummy_file(str_file, "This is a sentence.")
        str_size = Resource.Resource(str_path=str_file, f_is_product=True).func_get_size()
        self.func_remove_files([str_file])
        self.func_remove_dirs([self.str_test_directory])
        self.func_test_equals(str_answer, str_size)

    def test_func_get_size_for_empty_dir(self):
        """
        Test get size for empty directories.
        """
        str_dir = os.path.join(self.str_test_directory, "test_func_get_size_for_empty_dir")
        str_answer = "68.0 B"
        self.func_make_dummy_dir(self.str_test_directory)
        self.func_make_dummy_dir(str_dir)
        str_size = Resource.Resource(str_path=str_dir, f_is_product=True).func_get_size()
        self.func_remove_dirs([str_dir, self.str_test_directory])
        self.func_test_equals(str_answer, str_size)

    def test_func_get_size_for_dir_one_file(self):
        """
        Test get size for empty directories.
        """
        str_dir = os.path.join(self.str_test_directory,
                               "test_func_get_size_for_dir_one_file")
        str_file = os.path.join(self.str_test_directory,
                               "test_func_get_size_for_dir_one_file",
                               "file_one.txt")
        str_answer = "150.0 B"
        self.func_make_dummy_dir(self.str_test_directory)
        self.func_make_dummy_dir(str_dir)
        self.func_make_dummy_file(str_file, "File_one.txt")
        str_size = Resource.Resource(str_path=str_dir, f_is_product=True).func_get_size()
        self.func_remove_files([str_file])
        self.func_remove_dirs([str_dir, self.str_test_directory])
        self.func_test_equals(str_answer, str_size)

    def test_func_get_size_for_dir_three_file(self):
        """
        Test get size for empty directories.
        """
        str_dir = os.path.join(self.str_test_directory,
                               "test_func_get_size_for_dir_three_file")
        str_file_1 = os.path.join(self.str_test_directory,
                               "test_func_get_size_for_dir_three_file",
                               "file_one.txt")
        str_file_2 = os.path.join(self.str_test_directory,
                               "test_func_get_size_for_dir_three_file",
                               "file_two.txt")
        str_file_3 = os.path.join(self.str_test_directory,
                               "test_func_get_size_for_dir_three_file",
                               "file_three.txt")
        str_answer = "316.0 B"
        self.func_make_dummy_dir(self.str_test_directory)
        self.func_make_dummy_dir(str_dir)
        self.func_make_dummy_file(str_file_1, "File_one.txt")
        self.func_make_dummy_file(str_file_2, "File_two.txt")
        self.func_make_dummy_file(str_file_3, "File_three.txt")
        str_size = Resource.Resource(str_path=str_dir, f_is_product=True).func_get_size()
        self.func_remove_files([str_file_1, str_file_2, str_file_3])
        self.func_remove_dirs([str_dir, self.str_test_directory])
        self.func_test_equals(str_answer, str_size)

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( ResourceTester )
