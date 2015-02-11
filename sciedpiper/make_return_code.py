__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle", "Brian Haas" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import argparse

prsr_arguments = argparse.ArgumentParser( prog = "make_return_code.py", description = "Quick script used in testing that returns the requested return code, that is it.", conflict_handler="resolve", formatter_class = argparse.ArgumentDefaultsHelpFormatter )
prsr_arguments.add_argument( "-r", "--return_code", metavar = "Return_Code", type=int, dest = "i_return_code", default = 0, help = "The code for this script to return." )
prsr_arguments.add_argument( "-e", "--exception", dest = "f_throw_exception", default = False, action = "store_true", help = "This flag is given to indicate an exception should be thrown not a return code." )

args_cur = prsr_arguments.parse_args()

# Check to throw exception
if args_cur.f_throw_exception:
    raise Exception( "make_return_code raised an exception, as requested." )

exit( args_cur.i_return_code )
