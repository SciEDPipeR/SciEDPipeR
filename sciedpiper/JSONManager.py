
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import json


ARGUMENTS = "arguments"
COMMANDS = "commands"

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
             : dictionary { JSONManager.ARGUMENTS:[], JSONManager.COMMANDS:[] }
    """

    # Hold arguments and command seperately
    dict_arguments = {}
    list_commands = []

    # Check value of str_json
    if not str_json:
      return {}

    # Read in the json object
    json_read_data = json.loads( str_json )

    # Pull out global configuration
    for str_key in json_read_data:
        if not JSONManager.COMMANDS:
            dict_arguments[ str_key ] = json_read_data[ str_key ]

    # Iterate through commands
    for dict_command in json_read_data[ JSONManager.COMMANDS ]:
         list_commands.append( Command.Command.func_dict_to_Command() )

    return { JSONManager.COMMANDS: list_commands, JSONManager.ARGUMENTS: dict_arguments }


  @classmethod
  def func_pipeline_to_json( self, lcmd_commands, dict_args, str_file = None ):
    """
    Change a list of commands to a JSON object

    * lcmd_commands : List of commands to change to JSON
                    : List
    * dict_args : The parsed arguments for the pipeline
                : Dictionary
    * str_file : File to output the JSON string if given, either way the string is returned.
               : File path
    * returns : JSON representation of pipeline as a string
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
    dict_json[ JSONManager.COMMANDS ] = ldict_cmds

    # Make string nd return.
    # Write to file it requested.
    str_json = json.dumps( dict_json )
    if str_file:
        with open( str_file, "w" ) as hndl_out:
            hndl_out.write( str_json )
    return json.dumps( dict_json )
