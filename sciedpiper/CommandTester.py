# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import os
import ParentPipelineTester
import Resource
import unittest

class CommandTester( ParentPipelineTester.ParentPipelineTester ):
    """
    Tests the Command object.
    """
    
    def func_clean_level_dict_to_string( self, dict_clean_level ):
        """
        Makes a clean level dictionary a string in a uniform way
        
        * dict_clean_level : Dictionary of lists of paths
                           : Dictionary of clean levels from a Command object instance
                           
        * Return : String
                 : String representation of the dictionaries
        """
        
        if not dict_clean_level:
            return "{}"
        
        str_return = "{"
        for i_key in sorted( dict_clean_level.keys() ):
            str_return += str( i_key ) + " : "
            str_return += str( dict_clean_level[ i_key ] )
        return str_return + "}"


    def func_command_dict_to_string( self, dict_command ):
        """
        Makes a command dictionary a string in a uniform way
        
        * dict_clean_level : Dictionary
                           : Command dictionary
                           
        * Return : String
                 : String representation of the dictionaries
        """
        
        if not dict_command:
            return "{}"
        lstr_return = []
        for str_key in sorted( dict_command.keys() ):
            x_value = dict_command[ str_key ]
            if isinstance( x_value, basestring ):
                lstr_return.append( str_key + " : " + x_value )
            else:
                lstr_path_info = []
                for dict_paths in x_value:
                    lstr_path_info.append( "{" + ",".join( sorted( [ str( str_dict_path_key ) + ":" + str( str_dict_path_value )
                                            for str_dict_path_key, str_dict_path_value in dict_paths.items() ] ) ) + "}" )
                lstr_return.append( str_key+":" + str( sorted( lstr_path_info ) ) )
        return "{" + ",".join( lstr_return ) + "}"


    def test_init_for_one_relative_paths( self ):
        """ Testing init for updating relative paths. """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        lstr_deps = [ str_path_one ]
        lstr_prods = [ str_path_two ]
        lstr_deps_answer = [ os.path.join( os.getcwd(), str_path_one ) ]
        lstr_prods_answer = [ os.path.join( os.getcwd(), str_path_two ) ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( sorted( [ str( str_dep ) for str_dep in cmd_test.lstr_dependencies ] +
                                  [ str( str_prod ) for str_prod in cmd_test.lstr_products ] ) )
        str_answer = "".join(["[\"PATH: "+os.getcwd()+"/This/is/a/path1, ",
                              "CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                              "\"PATH: "+os.getcwd()+"/This/is/a/path2, ",
                              "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\"]"])
        self.func_test_equals(str_answer, str_result)


    def test_init_for_two_relative_paths( self ):
        """ Testing init for updating 2 relative paths. """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        lstr_deps_answer = sorted( [ os.path.join( os.getcwd(), str_path_one ), os.path.join( os.getcwd(), str_path_three ) ] )
        lstr_prods_answer = sorted( [ os.path.join( os.getcwd(), str_path_two ), os.path.join( os.getcwd(), str_path_four ) ] )
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( sorted( [ str( str_dep ) for str_dep in cmd_test.lstr_dependencies ] +
                                  [ str( str_prod ) for str_prod in cmd_test.lstr_products ] ) )
        str_answer = "".join(["[\"PATH: "+os.getcwd()+"/This/is/a/path1,",
                     " CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                     "\"PATH: "+os.getcwd()+"/This/is/a/path2, ",
                     "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\", ",
                     "\"PATH: "+os.getcwd()+"/This/is/a/path3, ",
                     "CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                     "\"PATH: "+os.getcwd()+"/This/is/a/path4, ",
                     "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\"]"])
        self.func_test_equals(str_answer, str_result)
        
        
    def test_init_for_one_abs_paths( self ):
        """ Testing init for updating absolute paths. """

        str_command = "This is a command"
        str_path_one = os.path.sep + os.path.join( "This","is","a","path1" )
        str_path_two = os.path.sep + os.path.join( "This","is","a","path2" )
        lstr_deps = [ str_path_one ]
        lstr_prods = [ str_path_two ]
        lstr_deps_answer = [ str_path_one ]
        lstr_prods_answer = [ str_path_two ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( sorted( [ str( str_dep ) for str_dep in cmd_test.lstr_dependencies ] +
                                  [ str( str_prod ) for str_prod in cmd_test.lstr_products ] ) )
        str_answer = "".join(["[\"PATH: /This/is/a/path1, CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                     "\"PATH: /This/is/a/path2, CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\"]"])
        self.func_test_equals(str_answer, str_result)


    def test_init_for_two_abs_paths( self ):
        """ Testing init for updating 2 absolute paths. """

        str_command = "This is a command"
        str_path_one = os.path.sep + os.path.join( "This","is","a","path1" )
        str_path_two = os.path.sep + os.path.join( "This","is","a","path2" )
        str_path_three = os.path.sep + os.path.join( "This","is","a","path3" )
        str_path_four = os.path.sep + os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        lstr_deps_answer = sorted( [ str_path_one, str_path_three ] )
        lstr_prods_answer = sorted( [ str_path_two, str_path_four ] )
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( sorted( [ str( str_dep ) for str_dep in cmd_test.lstr_dependencies ] +
                                  [ str( str_prod ) for str_prod in cmd_test.lstr_products ] ) )
        str_answer = "".join(["[\"PATH: /This/is/a/path1, CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                              "\"PATH: /This/is/a/path2, CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\", ",
                              "\"PATH: /This/is/a/path3, CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                              "\"PATH: /This/is/a/path4, CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\"]"])
        self.func_test_equals(str_answer, str_result)


#    def test_init_for_none_in_path( self ):
#        """ Testing init for none in the product and dependency parameters. """
#
#        str_command = "This is a command"
#        str_path_one = os.path.sep + os.path.join( "This","is","a","path1" )
#        str_path_two = os.path.sep + os.path.join( "This","is","a","path2" )
#        lstr_deps = [ str_path_one, None, [] ]
#        lstr_prods = [ None, str_path_two, None ]
#        lstr_deps_answer = [ str_path_one ]
#        lstr_prods_answer = [ str_path_two ]
#        self.func_test_error( Command.Command( str_command, lstr_deps, lstr_prods ) )

    def test_init_for_three_mixed_paths( self ):
        """ Testing init for updating three mixed paths of absolute and relative. """

        str_command = "This is a command"
        str_path_one = os.path.sep + os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.sep + os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five ]
        lstr_prods = [ str_path_two, str_path_four, str_path_six ]
        lstr_deps_answer = [ str_path_one, os.path.join( os.getcwd(), str_path_three), str_path_five ]
        lstr_prods_answer = [ os.path.join( os.getcwd(), str_path_two ), str_path_four, str_path_six ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( sorted( [ str( str_dep ) for str_dep in cmd_test.lstr_dependencies ] +
                                  [ str( str_prod ) for str_prod in cmd_test.lstr_products ] ) )
        str_answer = "".join(["[\"PATH: /This/is/a/path1, CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                              "\"PATH: /This/is/a/path4, CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\", ",
                              "\"PATH: /This/is/a/path5, CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\", ",
                              "\"PATH: /This/is/a/path6, CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\", ",
                              "\"PATH: " + os.getcwd() + "/This/is/a/path2, ",
                              "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []\", ",
                              "\"PATH: " + os.getcwd() + "/This/is/a/path3, ",
                              "CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']\"]"])
        self.func_test_equals(str_answer, str_result)

    def test_init_for_command( self ):
        """ Testing init for the command itself, which hould not change. """

        str_command = "This is a command"
        str_path_one = os.path.sep + os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.sep + os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result=cmd_test.str_id
        str_answer = str_command
        self.func_test_equals(str_answer, str_result)

    def test_func_set_resource_clean_level_for_bad_level(self):
        """ Testing for adding a clean level when there is no dependency. """
        
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_answer = cmd_test.func_detail()
        cmd_test.func_set_resource_clean_level( lstr_prods, "INVALID" )
        str_result = cmd_test.func_detail()

        self.func_test_equals( str_answer, str_result )
 
    def test_func_set_resource_clean_level_for_bad_files(self):
        """ Testing for adding a clean level when there is a bad list of files. """
        
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_answer = cmd_test.func_detail()
        cmd_test.func_set_resource_clean_level( [], Resource.CLEAN_ALWAYS )
        str_result = cmd_test.func_detail()
        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_resource_clean_level_for_good_case_mult_files(self):
        """ Testing for adding a clean level in a good case with multiple files. """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( lstr_deps, Resource.CLEAN_ALWAYS )
        str_result = cmd_test.func_detail()
        str_answer = "".join(["Command: This is a command; ",
                              "Dependencies: PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path1, ",
                              "CLEAN: 3, Dependency PARENTS: [] CHILDREN: ['This is a command'],",
                              "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path3, ",
                              "CLEAN: 3, Dependency PARENTS: [] CHILDREN: ['This is a command']; ",
                              "Products: PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path2, ",
                              "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: [],",
                              "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path4, ",
                              "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []"])
        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_resource_clean_level_for_good_case_mult_files2(self):
        """ Testing for adding a clean level in a good case with multiple files, both absolute and relative. """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( lstr_deps, Resource.CLEAN_NEVER )
        str_result = cmd_test.func_detail()
        str_answer = "".join(["Command: This is a command; ",
                               "Dependencies: PATH: /This/is/a/path5, CLEAN: 1, Dependency ",
                               "PARENTS: [] CHILDREN: ['This is a command'],PATH: /This/is/a/path6, ",
                               "CLEAN: 1, Dependency PARENTS: [] CHILDREN: ['This is a command'],",
                               "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path1, ",
                               "CLEAN: 1, Dependency PARENTS: [] CHILDREN: ['This is a command'],",
                               "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path3, ",
                               "CLEAN: 1, Dependency PARENTS: [] CHILDREN: ['This is a command']; ",
                               "Products: PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path2, ",
                               "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: [],",
                               "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path4, ",
                               "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []"])

        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_resource_clean_level_for_good_case_mult_files3(self):
        """
        Testing for adding a clean level in a good case with multiple files, multiple clean levels. 
        Some strings, some lists. Some absolute.
        """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        str_result = cmd_test.func_detail()
        str_answer = "".join(["Command: This is a command; ",
                              "Dependencies: PATH: /This/is/a/path5, CLEAN: 2, Dependency ",
                              "PARENTS: [] CHILDREN: ['This is a command'],PATH: /This/is/a/path6, ",
                              "CLEAN: 3, Dependency PARENTS: [] CHILDREN: ['This is a command'],",
                              "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path1, ",
                              "CLEAN: 1, Dependency PARENTS: [] CHILDREN: ['This is a command'],",
                              "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path3, ",
                              "CLEAN: 2, Dependency PARENTS: [] CHILDREN: ['This is a command']; Products: ",
                              "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path2, ",
                              "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: [],",
                              "PATH: "+os.getcwd()+os.path.sep+"This"+os.path.sep+"is"+os.path.sep+"a"+os.path.sep+"path4, ",
                              "CLEAN: 2, Product PARENTS: ['This is a command'] CHILDREN: []"])
        self.func_test_equals( str_answer, str_result )

# Get dependencies
    def test_func_get_dependencies_to_clean_level_for_bad_case_invalid_level_0(self):
        """
        Testing for getting dependencies to a clean level. Using invalid level 0
        """
 
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( 0 )
        lstr_answer = []
        self.func_test_equals( str( lstr_answer), str( lstr_result ) )

    def test_func_get_dependencies_to_clean_level_for_bad_case_invalid_level_10(self):
        """
        Testing for getting dependencies to a clean level. Using invalid level 10
        """
 
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( 10 )
        lstr_answer = []
        self.func_test_equals( str( lstr_answer), str( lstr_result ) )

    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_temp(self):
        """
        Testing for getting dependencies to a clean level. All clean levels present. Level = Temp
        """
 
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Resource.CLEAN_AS_TEMP )
        lstr_answer = Resource.Resource.func_make_paths_absolute( [ str_path_three, str_path_five ] ) + Resource.Resource.func_make_paths_absolute( [ str_path_six ] )
        lstr_result = [ rsc_cur.str_id for rsc_cur in lstr_result ]
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )

    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_Never(self):
        """
        Testing for getting dependencies to a clean level. All clean levels present. Level = Never
        """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Resource.CLEAN_NEVER )
        lstr_answer = Resource.Resource.func_make_paths_absolute( [ str_path_three, str_path_five ] ) + Resource.Resource.func_make_paths_absolute( [ str_path_six ] )
        lstr_result = [ rsc_cur.str_id for rsc_cur in lstr_result ]
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )

    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_always(self):
        """
        Testing for getting dependencies to a clean level. All clean levels present. Level = Always
        """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Resource.CLEAN_ALWAYS )
        lstr_answer = Resource.Resource.func_make_paths_absolute( [ str_path_six ] )
        lstr_result = [ rsc_cur.str_id for rsc_cur in lstr_result ]
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )
        
    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_always_default(self):
        """
        Testing for getting dependencies to a clean level.
        All clean levels present.
        Level = Always
        With files that are not in the clean level and should be treated as default.
        """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        str_path_five = os.path.sep + os.path.join( "This","is","a","path5" )
        str_path_six = os.path.sep + os.path.join( "This","is","a","path6" )
        str_path_seven = os.path.join( "This","is","a","path7" )
        str_path_eight = os.path.sep + os.path.join( "This","is","a","path8" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six, str_path_seven, str_path_eight ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Resource.CLEAN_ALWAYS )
        lstr_answer = Resource.Resource.func_make_paths_absolute( [ str_path_six ] )
        lstr_result = [ rsc_cur.str_id for rsc_cur in lstr_result ]
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )

    def test_func_is_valid_for_valid( self ):
        """ Testing for a valid state """
        
        self.func_test_true( Command.Command( "OK", ["ok"],["ok"] ).func_is_valid() )
        
        
    def test_func_is_valid_for_invalid1( self ):
        """ Testing for a invalid state """
        
        self.func_test_true( not Command.Command( "", ["ok"],["ok"] ).func_is_valid() )
        

    def test_func_is_valid_for_invalid2( self ):
        """ Testing for a invalid state """
        
        self.func_test_true( not Command.Command( "OK", [],["ok"] ).func_is_valid() )


    def test_func_is_valid_for_invalid3( self ):
        """ Testing for a invalid state """
        
        self.func_test_true( not Command.Command( "OK", ["ok"],[] ).func_is_valid() )


    def test_func_is_valid_for_invalid4( self ):
        """ Testing for a invalid state """
        
        self.func_test_true( not Command.Command( "", [],[] ).func_is_valid() )

    def test_func_to_dict_for_good_case( self ):
        """ Test for making a dict for good case. """

        # Make command
        str_command = "This is a command"
        str_path_one = os.path.join( os.path.sep + "This","is","a","path1" )
        str_path_two = os.path.join( os.path.sep + "This","is","a","path2" )
        str_path_three = os.path.join( os.path.sep + "This","is","a","path3" )
        str_path_four = os.path.join( os.path.sep + "This","is","a","path4" )
        str_path_five = os.path.join( os.path.sep + "This","is","a","path5" )
        str_path_six = os.path.join( os.path.sep + "This","is","a","path6" )
        str_path_seven = os.path.join( os.path.sep + "This","is","a","path7" )
        str_path_eight = os.path.join( os.path.sep + "This","is","a","path8" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six, str_path_seven, str_path_eight ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )

        # Answer
        str_answer = "".join([ "{COMMAND : ",str_command,
            ",MAKES:[u'{CLEAN:TEMP,PATH:",str_path_two,
            "}', u'{CLEAN:TEMP,PATH:",str_path_four,
            "}'],NEEDS:[u'{CLEAN:ALWAYS,PATH:",str_path_six,
            "}', u'{CLEAN:NEVER,PATH:",str_path_one,
            "}', u'{CLEAN:TEMP,PATH:",str_path_three,
            "}', u'{CLEAN:TEMP,PATH:",str_path_five,
            "}', u'{CLEAN:TEMP,PATH:",str_path_seven,
            "}', u'{CLEAN:TEMP,PATH:",str_path_eight,"}']}" ] )
 
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        str_result = self.func_command_dict_to_string( cmd_test.func_to_dict() )
        self.func_test_equals( str_answer, str_result )

    def test_func_to_dict_for_good_case_noDep_prod( self ):
        """ Test for making a dict for good case with no dependnecies or products. """
 
        str_command = "This is a command"
        
        # Answer
        str_answer = "{COMMAND : " + str_command + "}"
        
        # Make command
        cmd_test = Command.Command( str_command, [], [] )
        str_result = self.func_command_dict_to_string( cmd_test.func_to_dict() )
        self.func_test_equals( str_answer, str_result )

    def test_func_to_dict_for_good_case_no_prod( self ):
        """ Test for making a dict for good case no products. """
 
        str_command = "This is a command"
        
        # Make command
        str_command = "This is a command"
        str_path_one = os.path.join( os.path.sep + "This","is","a","path1" )
        str_path_two = os.path.join( os.path.sep + "This","is","a","path2" )
        str_path_three = os.path.join( os.path.sep + "This","is","a","path3" )
        str_path_four = os.path.join( os.path.sep + "This","is","a","path4" )
        str_path_five = os.path.join( os.path.sep + "This","is","a","path5" )
        str_path_six = os.path.join( os.path.sep + "This","is","a","path6" )
        str_path_seven = os.path.join( os.path.sep + "This","is","a","path7" )
        str_path_eight = os.path.join( os.path.sep + "This","is","a","path8" )
        lstr_deps = [ str_path_one, str_path_three, str_path_five, str_path_six, str_path_seven, str_path_eight ]
        cmd_test = Command.Command( str_command, lstr_deps, [] )
        
        # Answer
        str_answer = "".join([ "{COMMAND : ",str_command,
            ",NEEDS:[u'{CLEAN:ALWAYS,PATH:",str_path_six,
            "}', u'{CLEAN:NEVER,PATH:",str_path_one,
            "}', u'{CLEAN:TEMP,PATH:",str_path_three,
            "}', u'{CLEAN:TEMP,PATH:",str_path_five,
            "}', u'{CLEAN:TEMP,PATH:",str_path_seven,
            "}', u'{CLEAN:TEMP,PATH:",str_path_eight,"}']}" ] )
 
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        str_result = self.func_command_dict_to_string( cmd_test.func_to_dict() )
        self.func_test_equals( str_answer, str_result )
        
    def test_func_to_dict_for_good_case_no_deps( self ):
        """ Test for making a dict for good case no dependencies. """
  
        # Make command
        str_command = "This is a command"
        str_path_one = os.path.join( os.path.sep + "This","is","a","path1" )
        str_path_two = os.path.join( os.path.sep + "This","is","a","path2" )
        str_path_three = os.path.join( os.path.sep + "This","is","a","path3" )
        str_path_four = os.path.join( os.path.sep + "This","is","a","path4" )
        str_path_five = os.path.join( os.path.sep + "This","is","a","path5" )
        str_path_six = os.path.join( os.path.sep + "This","is","a","path6" )
        str_path_seven = os.path.join( os.path.sep + "This","is","a","path7" )
        str_path_eight = os.path.join( os.path.sep + "This","is","a","path8" )
        
        # Answer
        str_answer = "".join([ "{COMMAND : ",str_command,
            ",MAKES:[u'{CLEAN:TEMP,PATH:",str_path_two,
            "}', u'{CLEAN:TEMP,PATH:",str_path_four,
            "}']}" ] )
 
        # Make command
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, [], lstr_prods )
        
        cmd_test.func_set_resource_clean_level( str_path_one, Resource.CLEAN_NEVER )
        cmd_test.func_set_resource_clean_level( [ str_path_three, str_path_five ], Resource.CLEAN_AS_TEMP )
        cmd_test.func_set_resource_clean_level( [ str_path_six ], Resource.CLEAN_ALWAYS )
        str_result = self.func_command_dict_to_string( cmd_test.func_to_dict() )
        self.func_test_equals( str_answer, str_result )

    def test_func_dict_to_command( self ):
      """ Tests the class method dict to command which makes a standard dict a command. """

      # Make dict
      str_command = "Test Command"
      str_path_1 = os.path.join( os.path.sep + "This","path","1" )
      str_path_2 = os.path.join( os.path.sep + "This","path","2" )
      str_path_3 = os.path.join( os.path.sep + "This","path","3" )
      str_path_4 = os.path.join( os.path.sep + "This","path","4" )
      dict_test = { Command.USTR_COMMAND_JSON: str_command,
        Command.USTR_DEPENDENCIES_JSON: [{ Command.USTR_CLEAN_JSON: Resource.CLEAN_NEVER,
                                                   Command.USTR_PATH_JSON: str_path_1 },
                                                 {  Command.USTR_CLEAN_JSON: Resource.CLEAN_ALWAYS,
                                                   Command.USTR_PATH_JSON: str_path_2 }],
        Command.USTR_PRODUCTS_JSON: [{ Command.USTR_CLEAN_JSON: Resource.CLEAN_AS_TEMP,
                                               Command.USTR_PATH_JSON: str_path_3 },
                                             { Command.USTR_PATH_JSON: str_path_4 }]}

      # Get string rep of command.
      cmd_answer = Command.Command( str_cur_command=str_command,
                                    lstr_cur_dependencies=[ str_path_1, str_path_2 ],
                                    lstr_cur_products=[ str_path_3, str_path_4 ] )
      for lstr_path in zip( [ str_path_1, str_path_2, str_path_3, str_path_4 ],
                            [ Resource.CLEAN_NEVER, Resource.CLEAN_ALWAYS, Resource.CLEAN_AS_TEMP, Resource.CLEAN_AS_TEMP ]  ):
        cmd_answer.func_set_resource_clean_level( lstr_file=lstr_path[ 0 ] , i_level=lstr_path[ 1 ] )
      str_answer = cmd_answer.func_detail()

      # Make result string
      str_received = Command.Command.func_dict_to_command( dict_test ).func_detail()

      # Compare
      self.func_test_equals( str_answer, str_received )


#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( CommandTester )
