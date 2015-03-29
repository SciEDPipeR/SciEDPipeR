
__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import json
import unicodedata

# Constants
ARGUMENTS = "arguments"
COMMANDS = "commands"
    
class Struct:
  """
  Using this to turn a dict to a class.
  Nice solution given by Eli
  http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
  """

  def __init__( self, **args ):
    self.__dict__.update( args )

  def __str__( self ):
     """
     Returns a string with the internal items alphanumerically sorted by name.
 
     * return : String representation of the internal dict, sorted alphanumerically by keys
              : String
     """

     # Sort keys and make string
     return( "{" + ", ".join([ ": ".join([ str( str_key ), str( self.__dict__[ str_key ])]) for str_key in sorted(self.__dict__.keys()) ]) + "}" )


class JSONManager( object ):
  """
  Takes a list of commands and converts them to JSON representation or takes a JSON repsresentation and converts it to a list of commands.
  """

  # Tested
  @classmethod
  def func_json_to_commands( self, str_json ):
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
    # Unicode is left in the strings as is, argument names are normalized because they will eventually be variable names.
    json_read_data = json.loads( str_json )
    # Pull out global configuration
    for str_key in json_read_data:
        if not str_key == COMMANDS:
            dict_arguments[ unicodedata.normalize( "NFKD", str_key ).encode("ascii","ignore") ] = json_read_data[ str_key ]

    # Iterate through commands
    if COMMANDS in json_read_data:
        for dict_command in json_read_data[ COMMANDS ]:
            list_commands.append( Command.Command.func_dict_to_command( dict_command ) )

    return { COMMANDS: list_commands, ARGUMENTS: Struct( **dict_arguments ) }


  #Tested
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
    dict_json[ COMMANDS ] = ldict_cmds

    # Make string nd return.
    # Write to file it requested.
    str_json = json.dumps( dict_json )
    if str_file:
        with open( str_file, "w" ) as hndl_out:
            hndl_out.write( str_json )
    return json.dumps( dict_json )
