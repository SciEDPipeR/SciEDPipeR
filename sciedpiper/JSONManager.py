
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
C_STR_WORKFLOW_ID = "workflow_id"

# WDL key words
C_STR_CALL = "call"
C_STR_TASK = "task"
C_STR_COMMAND = "command"
C_STR_FILE = "File"
C_STR_INPUT = "input"
C_STR_OUTPUT = "output"
C_STR_WORKFLOW = "workflow"

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
  def func_pipeline_to_json( self, lcmd_commands, dict_args, str_file = None, f_pretty=False ):
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
    dict_json = dict_args

    # Go through the list and capture the json per command
    ldict_cmds = []
    for cmd_cur in lcmd_commands:
      #Check to make sure the list has something in it
      if not cmd_cur:
        continue
      ldict_cmds.append( cmd_cur.func_to_dict() )
    dict_json[ COMMANDS ] = ldict_cmds
    # Make string and return.
    # Write to file it requested.
    str_json = json.dumps( dict_json, sort_keys=True, indent=2 ) if f_pretty else json.dumps( dict_json )
    if str_file:
        with open( str_file, "w" ) as hndl_out:
            hndl_out.write( str_json )
    return str_json

  @classmethod
  def func_pipeline_to_wdl( self, lcmd_commands, str_workflow = "custom", str_file = None ):
    """
    Change a list of commands to a WDL output

    * lcmd_commands : List of commands to change to WDL
                    : List
    * str_file : File to output the wdl string if given, either way the string is returned.
               : File path
    * returns : WDL representation of pipeline as a string
              : String
    """

    # List of tasks for workflow
    # [ { name : name_value,
    #     products : { out1 : file_name, out2 : file_name },
    #     dependencies : {in1 : file_name, in2 : file_name } } ]
    ldict_tasks = []

    # List of dicts describing files used in the pipeline
    ldict_resources = {}

    # For each command.
    str_wdl = ""
    for cmd_cur in lcmd_commands:

      #Check to make sure the list has something in it
      if not cmd_cur:
        continue

      # Update tasks and extract data to a format useful.
      cur_command_dict = { "name" : cmd_cur.str_name, "products" : {}, "dependencies" : {}}
      i_product_count = 1
      i_dependency_count = 1
      for cur_prod in cmd_cur.lstr_products:
        cur_command_dict[ "products" ][ "out" + str( i_product_count ) ] = cur_prod.str_id
        i_product_count = i_product_count + 1
      for cur_dep in cmd_cur.lstr_dependencies:
        cur_command_dict[ "dependencies" ][ "in" + str( i_dependency_count ) ] = cur_dep.str_id
        i_dependency_count = i_dependency_count + 1
      ldict_tasks.append( cur_command_dict )

      # Add task to WDL
      str_wdl = str_wdl + C_STR_TASK + " " + cmd_cur.str_name + " {\n"

      # Add dependencies as inputs to WDL
      for str_file_count, str_file_name in cur_command_dict[ "dependencies" ].items():
        str_wdl = str_wdl + "  " + C_STR_FILE + " " + str_file_count + " " + str_file_name + "\n"

      # Add command to WDL
      str_wdl = str_wdl + "\n".join([ "  " + C_STR_COMMAND + " {",
                                      "    " + cmd_cur.str_id,
                                      "  }"])

      # Add products as outputs to WDL
      str_wdl = str_wdl + "  " + C_STR_OUTPUT + " {\n"
      for str_file_out_count, str_file_out_name in cur_command_dict[ "products" ].items():
        str_wdl = str_wdl + "    " + C_STR_OUTPUT + " " + str_file_out_count + " " + str_file_out_name
      str_wdl = str_wdl + "\n  }\n}\n"

    # Make workflow
    str_wdl = str_wdl + "\n" + C_STR_WORKFLOW  + " " + str_workflow + " {\n"
    for dict_cur_task in ldict_tasks:
      str_wdl = str_wdl + "  call " + dict_cur_task[ "name" ]

      # Add output
      if dict_cur_task[ "dependencies" ]:
        str_wdl = str_wdl + " { " + C_STR_INPUT + ": "
        lstr_workflow_inputs = []
        for str_dep_position, str_dep_value in dict_cur_task[ "dependencies" ].items():
          lstr_workflow_inputs.append( str_dep_position + "=" + str_dep_value )
        str_wdl = str_wdl + ", ".join( lstr_workflow_inputs ) + " }\n"
      else:
        str_wdl = str_wdl + "\n"
    str_wdl = str_wdl + "}"

    # Make string and return.
    # Write to file it requested.
    if str_file:
        with open( str_file, "w" ) as hndl_out:
            hndl_out.write( str_wdl )
    return str_wdl
