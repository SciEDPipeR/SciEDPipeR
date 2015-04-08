#!/usr/bin/env python


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse
import sciedpiper.JSONManager as JSONManager
import sciedpiper.ParentScript as ParentScript

class RunJSON( ParentScript.ParentScript ):
    """
    Runs JSON objects (read from files) as pipelines 
    """
   
    def func_update_arguments(self, arg_raw ):
        """
        Updates to the arg parser, command line options
        
        * arg_raw : Arguments ( not yet parsed )
                  : Arguments
        * return  : Updated Arguments
                  : Arguments
        """

        arg_raw = argparse.ArgumentParser( prog = "runJSON.py", description = "Runs JSON onjects (read from files) as pipelines.",
                                                  conflict_handler="resolve", formatter_class = argparse.ArgumentDefaultsHelpFormatter )
        arg_raw.add_argument( dest="str_json_in", default=None, help="File that holds the json object." )        
        return( arg_raw )

    def func_make_commands( self, args_parsed, cur_pipeline ):
        """
        Set commands from JSON file.
        """

        # Read in json file
        str_json = None
        with open( args_parsed.str_json_in, "r" ) as hndl_in:
            str_json = hndl_in.read()

        # Get the json file
        dict_json_return = JSONManager.JSONManager.func_json_to_commands( str_json )
        arg_parsed = dict_json_return[ JSONManager.ARGUMENTS ]
        return dict_json_return[ JSONManager.COMMANDS ]

    def func_make_arguments_readable( self, args_raw ):
        """

        """
    
if __name__ == "__main__":

    # Needed to run, calls the script
    RunJSON().func_run_pipeline()
