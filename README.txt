SciEDPipeR

Scientific Environment for the Development of Pipeline Resources


Quick Start

SciEDPipeR is a development environment focused on making scientific pipelines easy. For now you need to know python to use SciEDPipeR. For those who know python the good news is that you can use any language feature when making pipelines; for those that do not program in python we are working on ways to leverage the pipelining system without it :-)


To install:

Download the code

git clone https://github.com/SciEDPipeR/SciEDPipeR.git

Move into the downloaded directory

cd SciEDPipeR

Install SciEDPipeR (linux / Mac)

python setup.py install

Install SciEDPipeR (Windows)

setup.py install

Install SciEDPipeR without root priviledges (in your local user space)
Modify the above setup.py command with the following
( Linux /Mac )

python setup.py install --user

(OpenSUSE and RedHat may need the following additional argument)

python setup.py install --user --prefix==

( Windows )

setup.py install --user


To make a script:

see the bin/ExampleScript.py:


To run the example (from the directory it is in):

python ExamplePython.py


What can SciEDPipeR do?

Manage running commands
   Tracks dependencies and products of commands (optional).
   Tracked items can be files or folders
   All tracked products from an errored command are automatically deleted so partial files are not used. 
   Waits for the creation of products incase of network lag in distributed environments.
   Pipelines can be ran as serial bsub commands.
   Paths to pipeline tools can be set through command line to match installation environment
Self-documents
   Automatically logs to stdout or a log file
   Commands can be ran as a test run, documenting what will be performed when ran.
Manages input files
   Automatically uncompresses files before use (optional).
Reduces storage foot-prints
   Automated deletion of intermediary files which are no longer needed in analysis (optional).
   Products from commands be individually set be to deleted as intermediary files, as always, or as never.
   After completion of a command, intermediary files no longer needed in analysis that are not cleaned can be compressed (zip, gz, bz2).
   After completion of the pipeline, the resulting output directory can be compressed (several modes available).
Manages output directory
  The resulting output directory (which is optionally compressed) can be copied to mutltiple locations.
  The resulting output directory can also be moved to a location (to free up space in your working directory).
    Multiple copy commands and a move command can be combined on uncompressed or compressed modes.

What happens behind-the-scenes when I give the SciedPiper a list of commands (run mode not test mode)?

SciedPiper attempts to perform the follow when executing commands (in this order).
 Create the output directory for the run.
 Create directories indicated by user to make.
 Create a log file.
 Go through the list of user defined commands and do the following:
   Check to see if the product(s) made by the command are already made.
     If made, check to see if the product was made without error.
       If made without error, skip command.
       If made with error, delete product and move forward to remake product.
     If products are not made.
       Run command locally or using bsub (dependent on command line).
       Wait for completion of command (handle lag on cluster)
       If the command errored, remove products made, log, and stop
       If the command ran without error. Store that it finished successfully and log.
         Clean up files if cleaning is turned on (dependent on command line).
     Update internal state tracking dependencies and products.
   Compress any files no longer in use that were not cleaned (optional).
 Compress the output directory (optional)
 Copy output directory to one or more locations.
 Move output directory to a location.
