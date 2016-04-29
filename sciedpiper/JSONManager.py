# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import Command
import json
import os
import ParentScript
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

  def __init__(self, **args):
    self.__dict__.update(args)


  def __str__(self):
     """
     Returns a string with the internal items alphanumerically sorted by name.
 
     * return: String representation of the internal dict, sorted
               alphanumerically by keys
             : String
     """

     # Sort keys and make string
     return("{" + ", ".join([": ".join([str(str_key),
                             str(self.__dict__[str_key])]) for str_key in
                             sorted(self.__dict__.keys())]) + "}")


class JSONManager(object):
  """
  Takes a list of commands and converts them to JSON representation or
  takes a JSON repsresentation and converts it to a list of commands.
  """

  # Tested
  @classmethod
  def func_json_to_commands(self, str_json):
    """
    Change a json file to a list of commands.

    * str_json: String which represents a json object
              : String
    * return: Both a list of commands and a dict of global settings if provided.
            : dictionary { JSONManager.ARGUMENTS:[], JSONManager.COMMANDS:[] }
    """

    # Hold arguments and command seperately
    dict_arguments = {}
    list_commands = []

    # Check value of str_json
    if not str_json:
      return {}

    # Read in the json object
    # Unicode is left in the strings as is, argument names are normalized
    # because they will eventually be variable names.
    json_read_data = json.loads(str_json)
    # Pull out global configuration
    for str_key in json_read_data:
       if not str_key == COMMANDS:
            dict_arguments[unicodedata.normalize("NFKD", str_key).encode("ascii","ignore")] = json_read_data[str_key]

    # Iterate through commands
    if COMMANDS in json_read_data:
        for dict_command in json_read_data[COMMANDS]:
            list_commands.append(Command.Command.func_dict_to_command(dict_command))

    return({COMMANDS: list_commands,
            ARGUMENTS: Struct(**dict_arguments)})


  #Tested
  @classmethod
  def func_pipeline_to_json(self,
                            lcmd_commands,
                            dict_args,
                            str_file=None,
                            f_pretty=False):
    """
    Change a list of commands to a JSON object

    * lcmd_commands: List of commands to change to JSON
                   : List
    * dict_args: The parsed arguments for the pipeline
               : Dictionary
    * str_file: File to output the JSON string if given, either way the 
                string is returned.
              : File path
    * returns: JSON representation of pipeline as a string
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
      ldict_cmds.append(cmd_cur.func_to_dict())
    dict_json[COMMANDS] = ldict_cmds
    # Make string and return.
    # Write to file it requested.
    str_json = json.dumps(dict_json, sort_keys=True, indent=4) if f_pretty else json.dumps(dict_json)
    if str_file:
        with open(str_file, "w") as hndl_out:
            hndl_out.write(str_json)
    return str_json


  # TODO Test and 4 space
  @classmethod
  def func_pipeline_to_wdl(self,
                           dt_tree_graph,
                           str_file,
                           args_pipe,
                           str_workflow="custom"):
    """
    Change a list of commands to a WDL output

    * lcmd_commands: List of commands to change to WDL
                   : List
    * str_file: File to output the wdl string if given, either way the
                string is returned.
              : File path
    * returns: WDL representation of pipeline as a string
             : String
    """

    str_output_dir_variable = "${" + ParentScript.C_STR_OUTPUT_DIR + "}"

    # Simple JSON file for inputs
    lstr_json_input = []

    # Periods are used as a special character in WDL, make sure the
    # Script name has no period in it.
    str_workflow = str_workflow.replace(".","_")

    # Workflow
    lstr_workflow = []
    lstr_workflow_inputs = []

    # List of tasks for workflow
    # [{ name : name_value,
    #     products : { out1 : file_name, out2 : file_name },
    #     dependencies : {in1 : file_name, in2 : file_name } }]
    ldict_tasks = []

    # The original arguments as a dict
    dict_original_arguments = vars(args_pipe)

    # List of dicts describing files used in the pipeline
    # Changes the product name to the variable name in the WDL pipeline
    dict_resources = {}

    # Global increment for dependencies
    i_dependency_count = 1

    # Get the paths of the inputs and outputs to the dependency tree.
    lstr_terminal_inputs = [rsc_cur.str_id for rsc_cur in
                            dt_tree_graph.graph_commands.func_get_input_files()]
    lstr_terminal_products = [rsc_cur.str_id for rsc_cur in
                              dt_tree_graph.graph_commands.func_get_terminal_products()]

    # Arguments that are used in any commands
    set_used_arguments = set()

    # For each command.
    str_wdl = ""
    for cmd_cur in dt_tree_graph.func_get_commands():

      #Check to make sure the list has something in it
      if not cmd_cur:
        continue

      lstr_task_inputs = []
      lstr_cur_used_args = []

      # Make a WDL comamnd that will be updated when products and
      # dependecies are updated.
      # Add command to WDL
      str_cur_cmd_wdl = "\n".join(["  " + C_STR_COMMAND + " {",
                                    "    " + cmd_cur.str_id,
                                    "  }"])

      # Check for used arguments
      for str_arg in dict_original_arguments.keys():
          if "${" + str_arg + "}" in str_cur_cmd_wdl:
              lstr_cur_used_args.append(str_arg)
      

      # Indicate if the command has either inputs or outputs
      f_has_prod_dep = 0 < (len(cmd_cur.lstr_products) + 
                            len(cmd_cur.lstr_dependencies))
      lstr_workflow.append("  call " + cmd_cur.str_name + (" { input: " if f_has_prod_dep else ""))

      # Update tasks and extract data to a format useful.
      cur_command_dict = {"name": cmd_cur.str_name,
                          "products": {},
                          "dependencies": {}}
      i_product_count = 1
      for cur_prod in cmd_cur.lstr_products:
        str_prod_token = "out" + str(i_product_count)
        cur_command_dict["products"][str_prod_token] = "${" + "prod" + str(i_product_count) + "}"
        str_cur_cmd_wdl = str_cur_cmd_wdl.replace(cur_prod.str_id,
                                                  str_output_dir_variable + os.path.sep + "${" + "prod" + str(i_product_count) + "}")
        lstr_json_input.append("  \""+str_workflow+"."+cmd_cur.str_name+"." + "prod" + str(i_product_count) + "\"" + "=\""+cur_prod.str_id+"\"")
        dict_resources[cur_prod.str_id] = "${" + cmd_cur.str_name + "." + str_prod_token + "}"
        i_product_count = i_product_count + 1
      for cur_dep in cmd_cur.lstr_dependencies:
        str_dep_token = "in" + str(i_dependency_count)
        cur_command_dict["dependencies"]["input_" + str(i_dependency_count)] = cur_dep.str_id
        if cur_dep.str_id in lstr_terminal_inputs:
          lstr_workflow_inputs.append("  File dependency_" + str(i_dependency_count) + " " + str_output_dir_variable + os.path.sep + "${" + str_dep_token + "}")
          lstr_json_input.append("  \""+str_workflow+"." + str_dep_token + "\"" + "=\""+cur_dep.str_id+"\"")
          dict_resources[cur_dep.str_id] = "${dependency_" + str(i_dependency_count) + "}"
        lstr_task_inputs.append("    " + "input_" + str(i_dependency_count) + "=" + dict_resources.get(cur_dep.str_id, cur_dep.str_id))
        str_cur_cmd_wdl = str_cur_cmd_wdl.replace(cur_dep.str_id, "input_" + str(i_dependency_count))
        i_dependency_count = i_dependency_count + 1

      # Add arguments to task inputs
      lstr_task_inputs.extend(["    " + str_used_arg + "=" + str_used_arg for str_used_arg in lstr_cur_used_args])
      

      lstr_workflow.append(",\n".join(lstr_task_inputs))
      if f_has_prod_dep:
          lstr_workflow.append("  }")
      # Add task to WDL
      str_wdl = str_wdl + C_STR_TASK + " " + cmd_cur.str_name + " {\n"

      # Add dependencies as inputs to WDL
      for str_file_count, str_file_name in cur_command_dict["dependencies"].items():
        str_wdl = str_wdl + "  " + C_STR_FILE + " " + str_file_count + "\n"

      # Add updated command.
      str_wdl = str_wdl + str_cur_cmd_wdl

      # Add products as outputs to WDL
      str_wdl = str_wdl + "  " + C_STR_OUTPUT + " {\n"
      for str_file_out_count, str_file_out_name in cur_command_dict["products"].items():
        str_wdl = str_wdl + "    " + C_STR_FILE + " " + str_file_out_count + " " + str_file_out_name
      str_wdl = str_wdl + "\n  }\n}\n"

      # Update globaly used arguments
      set_used_arguments = set_used_arguments or set(lstr_cur_used_args)

    # Add workflow
    str_wdl = str_wdl + C_STR_WORKFLOW  + " " + str_workflow + " {\n\n  "
    str_wdl = str_wdl + ",\n  ".join([arg_key for arg_key, arg_value in dict_original_arguments.items() if arg_key in set_used_arguments])
    str_wdl = str_wdl + "\n" + "\n".join(lstr_workflow_inputs) + "\n"
    str_wdl = str_wdl + "\n" + "\n".join(lstr_workflow)

    # Add JSON file
    str_wdl = str_wdl + "\n\n{\n"
    str_wdl = str_wdl + ",\n".join(["  \"" + str_workflow + "." + arg_key + "\"" + "=\"" + str(arg_value) + "\""
                                      for arg_key, arg_value in dict_original_arguments.items() if arg_key in set_used_arguments])
    if (len(dict_original_arguments) > 0) and (len(list(set_used_arguments)) > 0):
        str_wdl = str_wdl + ","
    str_wdl = str_wdl + "\n" + ",\n".join(lstr_json_input).replace(str_output_dir_variable + os.path.sep, "") + "\n}"

    # Make string and return.
    # Write to file it requested.
    if str_file:
        with open(str_file, "w") as hndl_out:
            hndl_out.write(str_wdl)
    return str_wdl
