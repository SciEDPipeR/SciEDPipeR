
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
        str_result = str( [ cmd_test.lstr_dependencies, cmd_test.lstr_products ] )
        str_answer = str( [ lstr_deps_answer, lstr_prods_answer ] )
        
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
        lstr_deps_answer = [ os.path.join( os.getcwd(), str_path_one ), os.path.join( os.getcwd(), str_path_three ) ]
        lstr_prods_answer = [ os.path.join( os.getcwd(), str_path_two ), os.path.join( os.getcwd(), str_path_four ) ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( [ cmd_test.lstr_dependencies, cmd_test.lstr_products ] )
        str_answer = str( [ lstr_deps_answer, lstr_prods_answer ] )
        
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
        str_result = str( [ cmd_test.lstr_dependencies, cmd_test.lstr_products ] )
        str_answer = str( [ lstr_deps_answer, lstr_prods_answer ] )
        
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
        lstr_deps_answer = [ str_path_one, str_path_three ]
        lstr_prods_answer = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( [ cmd_test.lstr_dependencies, cmd_test.lstr_products ] )
        str_answer = str( [ lstr_deps_answer, lstr_prods_answer ] )
        
        self.func_test_equals(str_answer, str_result)


    def test_init_for_none_in_path( self ):
        """ Testing init for none in the product and dependency parameters. """

        str_command = "This is a command"
        str_path_one = os.path.sep + os.path.join( "This","is","a","path1" )
        str_path_two = os.path.sep + os.path.join( "This","is","a","path2" )
        lstr_deps = [ str_path_one, None, [] ]
        lstr_prods = [ None, str_path_two, None ]
        lstr_deps_answer = [ str_path_one ]
        lstr_prods_answer = [ str_path_two ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        str_result = str( [ cmd_test.lstr_dependencies, cmd_test.lstr_products ] )
        str_answer = str( [ lstr_deps_answer, lstr_prods_answer ] )
        
        self.func_test_equals(str_answer, str_result)


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
        str_result = str( [ cmd_test.lstr_dependencies, cmd_test.lstr_products ] )
        str_answer = str( [ lstr_deps_answer, lstr_prods_answer ] )
        
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
        str_result = cmd_test.str_command
        str_answer = str_command
        
        self.func_test_equals(str_answer, str_result)


    def test_func_set_dependency_clean_level_for_no_dependencies(self):
        """ Testing for adding a clean level when there is no dependency. """
        
        str_command = "This is a command"
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_dependency_clean_level( lstr_prods, Command.CLEAN_AS_TEMP )
        str_result = str( cmd_test.dict_clean_level )
        str_answer = "{}"

        self.func_test_equals( str_answer, str_result )


    def test_func_set_dependency_clean_level_for_bad_level(self):
        """ Testing for adding a clean level when there is no dependency. """
        
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_dependency_clean_level( lstr_prods, "INVALID" )
        str_result = str( cmd_test.dict_clean_level )
        str_answer = "{}"

        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_dependency_clean_level_for_bad_files(self):
        """ Testing for adding a clean level when there is a bad list of files. """
        
        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        cmd_test.func_set_dependency_clean_level( [], Command.CLEAN_AS_TEMP )
        str_result = str( cmd_test.dict_clean_level )
        str_answer = "{}"

        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_dependency_clean_level_for_good_case_mult_files(self):
        """ Testing for adding a clean level in a good case with multiple files. """

        str_command = "This is a command"
        str_path_one = os.path.join( "This","is","a","path1" )
        str_path_two = os.path.join( "This","is","a","path2" )
        str_path_three = os.path.join( "This","is","a","path3" )
        str_path_four = os.path.join( "This","is","a","path4" )
        lstr_deps = [ str_path_one, str_path_three ]
        lstr_prods = [ str_path_two, str_path_four ]
        cmd_test = Command.Command( str_command, lstr_deps, lstr_prods )
        lstr_abs_deps = cmd_test.func_make_paths_absolute( lstr_deps )
        cmd_test.func_set_dependency_clean_level( lstr_abs_deps, Command.CLEAN_AS_TEMP )
        str_result = self.func_clean_level_dict_to_string( cmd_test.dict_clean_level )
        str_answer = self.func_clean_level_dict_to_string( {Command.CLEAN_AS_TEMP: lstr_abs_deps} )
        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_dependency_clean_level_for_good_case_mult_files2(self):
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
        cmd_test.func_set_dependency_clean_level( lstr_deps, Command.CLEAN_AS_TEMP )
        lstr_abs_deps = cmd_test.func_make_paths_absolute( lstr_deps )
        str_result = self.func_clean_level_dict_to_string( cmd_test.dict_clean_level )
        str_answer = self.func_clean_level_dict_to_string( {Command.CLEAN_AS_TEMP: lstr_abs_deps} )

        self.func_test_equals( str_answer, str_result )
        
        
    def test_func_set_dependency_clean_level_for_good_case_mult_files3(self):
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        str_result = self.func_clean_level_dict_to_string( cmd_test.dict_clean_level )
        str_answer = self.func_clean_level_dict_to_string( { Command.CLEAN_NEVER: cmd_test.func_make_paths_absolute( [ str_path_one ] ),
                                                             Command.CLEAN_AS_TEMP: cmd_test.func_make_paths_absolute( [ str_path_three, str_path_five ] ),
                                                             Command.CLEAN_ALWAYS: cmd_test.func_make_paths_absolute( [ str_path_six ] ) } )
        self.func_test_equals( str_answer, str_result )
        

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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_AS_TEMP )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_three, str_path_five ] ) + cmd_test.func_make_paths_absolute( [ str_path_six ] )
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_NEVER )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_three, str_path_five ] ) + cmd_test.func_make_paths_absolute( [ str_path_six ] )
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_ALWAYS )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_six ] )
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_ALWAYS )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_six ] )
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )

            
    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_never_default(self):
        """
        Testing for getting dependencies to a clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
        """
        
        i_original_default = Command.CLEAN_DEFAULT
        Command.CLEAN_DEFAULT = Command.CLEAN_NEVER
        
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_NEVER )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_three, str_path_five, str_path_six ] )
        Command.CLEAN_DEFAULT = i_original_default
        
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )
        
        
    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_never_default2(self):
        """
        Testing for getting dependencies to a clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = Temp
        """

        i_original_default = Command.CLEAN_DEFAULT
        Command.CLEAN_DEFAULT = Command.CLEAN_AS_TEMP

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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_NEVER )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_three, str_path_five, str_path_six, str_path_seven, str_path_eight ] )
        Command.CLEAN_DEFAULT = i_original_default
        
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )


    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_temp_default(self):
        """
        Testing for getting dependencies to a clean level.
        All clean levels present.
        Level = Temp
        With files that are not in the clean level and should be treated as default.
        Default = Temp
        """

        i_original_default = Command.CLEAN_DEFAULT
        Command.CLEAN_DEFAULT = Command.CLEAN_AS_TEMP

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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_AS_TEMP )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_three, str_path_five, str_path_six, str_path_seven, str_path_eight ] )
        Command.CLEAN_DEFAULT = i_original_default
        
        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )
        

    def test_func_get_dependencies_to_clean_level_for_good_case_mult_levels_always_default2(self):
        """
        Testing for getting dependencies to a clean level.
        All clean levels present.
        Level = ALways
        With files that are not in the clean level and should be treated as default.
        Default = Temp
        """

        i_original_default = Command.CLEAN_DEFAULT
        Command.CLEAN_DEFAULT = Command.CLEAN_AS_TEMP

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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        lstr_result = cmd_test.func_get_dependencies_to_clean_level( Command.CLEAN_ALWAYS )
        lstr_answer = cmd_test.func_make_paths_absolute( [ str_path_six ] )
        Command.CLEAN_DEFAULT = i_original_default

        self.func_test_equals( sorted( lstr_answer) , sorted( lstr_result ) )


    def test_func_is_dependency_clean_level_for_bad_case_mult_levels_bad_level(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Bad clean level
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_one,
                                                            i_clean_level = -1 )
        f_answer = False
        self.func_test_equals( f_answer , f_result )
        

    def test_func_is_dependency_clean_level_for_bad_case_mult_levels_bad_path(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        Bad path
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = "",
                                                            i_clean_level = Command.CLEAN_NEVER )
        f_answer = False
        self.func_test_equals( f_answer , f_result )
        

    def test_func_is_dependency_clean_level_for_good_case_mult_levels_never_true(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_one,
                                                            i_clean_level = Command.CLEAN_NEVER )
        f_answer = True
        self.func_test_equals( f_answer , f_result )
        
        
    def test_func_is_dependency_clean_level_for_good_case_mult_levels_never_false(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_eight,
                                                            i_clean_level = Command.CLEAN_NEVER )
        f_answer = False
        self.func_test_equals( f_answer , f_result )


    def test_func_is_dependency_clean_level_for_good_case_mult_levels_tmp_true(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_three,
                                                            i_clean_level = Command.CLEAN_AS_TEMP )
        f_answer = True
        self.func_test_equals( f_answer , f_result )
        
        
    def test_func_is_dependency_clean_level_for_good_case_mult_levels_tmp_false(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_six,
                                                            i_clean_level = Command.CLEAN_AS_TEMP )
        f_answer = False
        self.func_test_equals( f_answer , f_result )


    def test_func_is_dependency_clean_level_for_good_case_mult_levels_always_true(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_six,
                                                            i_clean_level = Command.CLEAN_ALWAYS )
        f_answer = True
        self.func_test_equals( f_answer , f_result )
        
        
    def test_func_is_dependency_clean_level_for_good_case_mult_levels_always_false(self):
        """
        Testing for indicating if the dependency is a certain clean level.
        All clean levels present.
        Level = never
        With files that are not in the clean level and should be treated as default.
        Default = NEVER
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
        cmd_test.func_set_dependency_clean_level( str_path_one, Command.CLEAN_NEVER )
        cmd_test.func_set_dependency_clean_level( [ str_path_three, str_path_five ], Command.CLEAN_AS_TEMP )
        cmd_test.func_set_dependency_clean_level( [ str_path_six ], Command.CLEAN_ALWAYS )
        f_result = cmd_test.func_is_dependency_clean_level( str_dependency = str_path_two,
                                                            i_clean_level = Command.CLEAN_ALWAYS )
        f_answer = False
        self.func_test_equals( f_answer , f_result )


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


    def test_func_make_paths_absolute_for_empty_list( self ):
        """ Test for taking an empty list. """

        lstr_paths = [ ]
        lstr_path_result = Command.Command("",[],[]).func_make_paths_absolute( lstr_paths)

        lstr_answer = [ ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )


    def test_func_make_paths_absolute_for_one_rel_path( self ):
        """ Test for making a simple relative path absolute. """
        
        str_path_one = os.path.join( "Test","Path", "One" )
        lstr_paths = [ str_path_one ]
        lstr_path_result = Command.Command("",[],[]).func_make_paths_absolute( lstr_paths)
        
        str_answer_one = os.path.join( os.getcwd(), str_path_one )
        lstr_answer = [ str_answer_one ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )


    def test_func_make_paths_absolute_for_two_rel_path( self ):
        """ Test for making two simple relative path absolute. """
        
        str_path_one = os.path.join( "Test","Path", "One" )
        str_path_two = os.path.join( "Test","Path", "Two" )
        lstr_paths = [ str_path_one, str_path_two ]
        lstr_path_result = Command.Command("",[],[]).func_make_paths_absolute( lstr_paths)
        
        str_answer_one = os.path.join( os.getcwd(), str_path_one )
        str_answer_two = os.path.join( os.getcwd(), str_path_two )
        lstr_answer = [ str_answer_one, str_answer_two ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )
        

    def test_func_make_paths_absolute_for_one_abs_path( self ):
        """ Test for making a simple absolute path absolute. """
        
        str_path_one = os.path.sep + os.path.join( "Test","Path", "One" )
        lstr_paths = [ str_path_one ]
        lstr_path_result = Command.Command("",[],[]).func_make_paths_absolute( lstr_paths)
        
        str_answer_one = str_path_one
        lstr_answer = [ str_answer_one ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )
        
        
    def test_func_make_paths_absolute_for_two_abs_path( self ):
        """ Test for making two simple absolute paths absolute. """
        
        str_path_one = os.path.sep + os.path.join( "Test","Path", "One" )
        str_path_two = os.path.sep + os.path.join( "Test","Path", "Two" )
        lstr_paths = [ str_path_one, str_path_two ]
        lstr_path_result = Command.Command("",[],[]).func_make_paths_absolute( lstr_paths)
        
        str_answer_one = str_path_one
        str_answer_two = str_path_two
        lstr_answer = [ str_answer_one, str_answer_two ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )


    def test_func_make_paths_absolute_for_mixture_of_path( self ):
        """ Test for making two absolute paths and two relative paths absolute. """
        
        str_path_one = os.path.sep + os.path.join( "Test","Path", "One" )
        str_path_two = os.path.join( "Test","Path", "Two" )
        str_path_three = os.path.sep + os.path.join( "Test","Path", "Three" )
        str_path_four = os.path.join( "Test","Path", "Four" )
        lstr_paths = [ str_path_one, str_path_two, str_path_three, str_path_four ]
        lstr_path_result = Command.Command("",[],[]).func_make_paths_absolute( lstr_paths)
        
        str_answer_one = str_path_one
        str_answer_two = os.path.join( os.getcwd(), str_path_two )
        str_answer_three = str_path_three
        str_answer_four = os.path.join( os.getcwd(), str_path_four )
        lstr_answer = [ str_answer_one, str_answer_two, str_answer_three, str_answer_four ]
        
        self.func_test_equals( lstr_answer, lstr_path_result )
        

#Creates a suite of tests
def suite():
    return unittest.TestLoader().loadTestsFromTestCase( CommandTester )