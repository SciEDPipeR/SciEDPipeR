
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import json


class JSONManager( object ):
  """
  Takes a list of commands and converts them to JSON representation or takes a JSON repsresentation and converts it to a list of commands.
  """
    
  @classmethod
  def func_json_to_command( self, str_json ):
    """
    Change a json file to a list of commands.

    * str_json : String which represents a json object
               : String
    * return : Both a list of commands and a dict of global settings if provided.
             : dictionary { commands:[], settings:[] }
    """

    # Check value of str_json
    if not str_json:
      return {}

    # Read in the json object
    json_read_data = json.loads( str_json )

    # Pull out global configuration

    # Iterate through commands

    return 

  @classmethod
  def func_pipeline_to_json( self, lcmd_commands, dict_args ):
    """
    Change a list of commands to a JSON object

    * lcmd_commands : List of commands to change to JSON
                    : List
    * dict_args : The parsed arguments for the pipeline
                : Dictionary
    * returns : JSON represenation of pipeline as a string
              : String
    """

    # Dict for the object
    # Capture global settings
    dict_json = dict( dict_args )

    # Go through the list and capture the json per command
    ldict_cmds = []
    for cmd_cur in lcmd_commands:
      #Check to make sure the list has something in it
      if not cmd_cur:
        continue
      ldict_cmds.append( cmd_cur.func_to_dict() )
    dict_json[ "commands" ] = ldict_cmds

    return json.dumps( dict_json )
