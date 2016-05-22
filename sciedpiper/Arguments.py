# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import re

"""
Utility functions working with arguments.
"""

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = ["Timothy Tickle", "Brian Haas"]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


# Constants
C_STR_CHOICES = "choices"
C_STR_DEFAULT = "default"
C_STR_OPTION_STRINGS = "option_strings"
C_STR_TYPE = "type"
C_STR_VARIABLE_NAME = "var_name"
C_STR_POSITIONAL_ARGUMENTS = "__positional_arguments__"

# Constants Types
C_STR_INT_TYPE = "<type 'int'>"
C_STR_LIST_TYPE = "<type 'list'>"
C_STR_FLOAT_TYPE = "<type 'float'>"
C_STR_STRING_TYPE = "<type 'str'>"
C_STR_BOOL_TYPE = "<type 'bool'>"

# Arguments
C_STR_OUTPUT_DIR = "str_out_dir"
C_STR_NO_PIPELINE_CONFIG_ARG = "--no_pipeline_config"
C_STR_PIPELINE_CONFIG_FILE_ARG = "--pipeline_config_file"
C_STR_SAMPLE_FILE_ARG = "--sample_file"
C_STR_SAMPLE_FILE_DEST = "str_sample_file"

# Locked arguments (can not be updated by the pipeline config file.
# Make sure to include all flags and move argparse to the correct group.
C_LSTR_LOCKED_ARGS = ["--out_dir",
                      C_STR_SAMPLE_FILE_ARG,
                      "--concurrent_jobs"]

# These arguments do not show up in the help due to being
# sciedpiper specific
HIDDEN_ARGS = ["--clean", "--copy", "--dot_file",
               "--log", "--json_out", "--max_bsub_memory", "--move",
               "--test", "--graph_ordered_commands", "--timestamp",
               "--update_command", "--compress", "--wait",
               C_STR_SAMPLE_FILE_ARG, "--concurrent_jobs",
               "--job_system", "--job_memory", "--job_queue",
               "--job_misc", C_STR_NO_PIPELINE_CONFIG_ARG,
               C_STR_PIPELINE_CONFIG_FILE_ARG, "--resources"]
# Use this to tag sciedpiper argument group descriptions to hid them.
C_STR_SCIEDPIPER_ARG_GROUP = "(SciEDPipeR)"

class PipelineDefaultHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """ Formats the help so SciEDPiper builtins are not listed. """

    # Remove arguments from the detail section but not the argument
    # group descriptions.
    def add_arguments(self, actions):
        for action in actions:
            if action.option_strings:
                if(sum([opt in HIDDEN_ARGS
                        for opt in action.option_strings])>0):
                    return
            self.add_argument(action)

    # Allows us to hide argument groups.
    def start_section(self, heading):
        # Only scipt things with C_STR_SCIEDPIPER_ARG_GROUP in them
        if(not C_STR_SCIEDPIPER_ARG_GROUP.lower() in heading.lower()):
            super(argparse.ArgumentDefaultsHelpFormatter,
                  self).start_section(heading)
        else:
            # Mange indenting and return blank help string.
            self._indent()
            section = self._Section(self, self._current_section, heading)
            self._add_item(lambda: "", [])
            self._current_section = section

    # The overwritting here removes sciedpiper arguments from the
    # usage summary section.
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = 'usage: '

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=self._prog)

        # if optionals and positionals are available, calculate usage
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)

            # split optionals from positionals
            optionals = []
            positionals = []
            for action in actions:
                if action.option_strings:
                    if (sum([opt in HIDDEN_ARGS
                             for opt in action.option_strings])==0):
                        optionals.append(action)
                else:
                    positionals.append(action)

            # build full usage string
            format = self._format_actions_usage
            action_usage = format(optionals + positionals, groups)
            usage = ' '.join([s for s in [prog, action_usage] if s])

            # wrap the usage parts if it's too long
            text_width = self._width - self._current_indent
            if len(prefix) + len(usage) > text_width:

                # break usage into wrappable parts
                part_regexp = r'\(.*?\)+|\[.*?\]+|\S+'
                opt_usage = format(optionals, groups)
                pos_usage = format(positionals, groups)
                opt_parts = re.findall(part_regexp, opt_usage)
                pos_parts = re.findall(part_regexp, pos_usage)
                assert ' '.join(opt_parts) == opt_usage
                assert ' '.join(pos_parts) == pos_usage

                # helper for wrapping lines
                def get_lines(parts, indent, prefix=None):
                    lines = []
                    line = []
                    if prefix is not None:
                        line_len = len(prefix) - 1
                    else:
                        line_len = len(indent) - 1
                    for part in parts:
                        if line_len + 1 + len(part) > text_width:
                            lines.append(indent + ' '.join(line))
                            line = []
                            line_len = len(indent) - 1
                        line.append(part)
                        line_len += len(part) + 1
                    if line:
                        lines.append(indent + ' '.join(line))
                    if prefix is not None:
                        lines[0] = lines[0][len(indent):]
                    return lines

                # if prog is short, follow it with optionals or positionals
                if len(prefix) + len(prog) <= 0.75 * text_width:
                    indent = ' ' * (len(prefix) + len(prog) + 1)
                    if opt_parts:
                        lines = get_lines([prog] + opt_parts, indent, prefix)
                        lines.extend(get_lines(pos_parts, indent))
                    elif pos_parts:
                        lines = get_lines([prog] + pos_parts, indent, prefix)
                    else:
                        lines = [prog]

                # if prog is long, put it on its own line
                else:
                    indent = ' ' * len(prefix)
                    parts = opt_parts + pos_parts
                    lines = get_lines(parts, indent)
                    if len(lines) > 1:
                        lines = []
                        lines.extend(get_lines(opt_parts, indent))
                        lines.extend(get_lines(pos_parts, indent))
                    lines = [prog] + lines

                # join lines into usage
                usage = '\n'.join(lines)

        # prefix with 'usage:'
        return '%s%s\n\n' % (prefix, usage)

class Arguments(object):
    """
    Consolidates code involving arguments.
    """

    # Tested 3-21-2016 6 tests
    @classmethod
    def func_extract_argument_info(cls, args):
        """
        Extract information from parsed arguments and return
            a dict of argument information.

        * args : Namespace
                 Parsed arguments.

        * returns : Dict
                    Dictionary of argument information
                    (both positional and optional.
        """

        if not args:
            return {}

        dict_argument_info = {}

        # Extract
        for _, str_arg_value in args._optionals._option_string_actions.items():
            str_long_flag = str_arg_value.option_strings[0]
            for str_flag in str_arg_value.option_strings:
                if (str_flag[0:2] == "--") and (not str_long_flag[0:2] == "--"):
                    str_long_flag = str_flag
                    break

            dict_argument_info[str_long_flag] = {}
            dict_argument_info[str_long_flag][C_STR_OPTION_STRINGS] = str_arg_value.option_strings

            # Find the name of the destination variable
            dict_argument_info[str_long_flag][C_STR_VARIABLE_NAME] = str_arg_value.dest

            # Find the argument type.
            dict_argument_info[str_long_flag][C_STR_TYPE] = str_arg_value.type
            if not dict_argument_info[str_long_flag][C_STR_TYPE]:
                if str_arg_value.nargs == 0:
                    dict_argument_info[str_long_flag][C_STR_TYPE] = C_STR_BOOL_TYPE
                elif str_arg_value.nargs > 1:
                    dict_argument_info[str_long_flag][C_STR_TYPE] = C_STR_LIST_TYPE
                else:
                    dict_argument_info[str_long_flag][C_STR_TYPE] = C_STR_STRING_TYPE

            # Set default for flags
            dict_argument_info[str_long_flag][C_STR_DEFAULT] = str_arg_value.default

            # Set choices for flags
            dict_argument_info[str_long_flag][C_STR_CHOICES] = str_arg_value.choices

        # Add in positionals
        dict_pos = {C_STR_TYPE:C_STR_LIST_TYPE,
                    C_STR_VARIABLE_NAME:[stract_pos.dest for stract_pos
                                         in args._get_positional_actions()],
                    C_STR_OPTION_STRINGS:[],
                    C_STR_CHOICES:[]}
        dict_argument_info[C_STR_POSITIONAL_ARGUMENTS] = dict_pos

        return dict_argument_info
