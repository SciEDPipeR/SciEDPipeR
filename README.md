# SciEDPipeR

Scientific Environment for the Development of Pipeline Resources

## Quick Start

SciEDPipeR is a development environment focused on making scientific pipelines easy. For now you need to know python to use SciEDPipeR. For those who know python the good news is that you can use any language feature when making pipelines; for those that do not program in python we are working on ways to leverage the pipelining system without it :-)

To make a script see the ExampleScript.py:

To run the example
```
python ExamplePython.py
```

## What can SciEDPipeR do?

- **Manage running commands**
  - Tracks dependencies and products of commands (optional).
  - Tracked items can be files or folders
  - All tracked products from an errored command are automatically deleted so partial files are not used. 
  - Waits for the creation of products incase of network lag in distributed environments.
  - Pipelines can be ran as serial bsub commands.
  - Paths to pipeline tools can be set through command line to match installation environment
- **Self-documents**
  - Automatically logs to stdout or a log file
  - Commands can be ran as a test run, documenting what will be performed when ran.
- **Manages input files**
  - Automatically uncompresses files before use (optional).
- **Reduces storage foot-prints**
  - Automated deletion of intermediary files which are no longer needed in analysis (optional).
  - Products from commands be individually set be to deleted as intermediary files, as always, or as never.
