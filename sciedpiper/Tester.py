"""
Runs the tests suites.
Test suites should be turned on here to run.
"""

__author__="Timothy Tickle"
__copyright__="Copyright 2014"
__credits__=["Timothy Tickle", "Brian Haas"]
__license__="MIT"
__maintainer__="Timothy Tickle"
__email__="ttickle@broadinstitute.org"
__status__="Development"


#import CommandlineTester
#import CommandTester
#import CompressionTester
#import DependencyGraphTester
#import DependencyTreeTester
import ResourceTester
#import FunctionalTester
#import GraphTester
#import JSONManagerTester
#import PipelineTester
import unittest


# Calls all unit tests as a regression suite.
suite=unittest.TestSuite()
#suite.addTest(ArgumentsTester.suite()) # 1 method
#suite.addTest(CommandlineTester.suite()) #Done
#suite.addTest(CommandTester.suite()) #Done
#suite.addTest(CompressionTester.suite()) #Done
#suite.addTest(ConfigMangerTester.suite()) # 8 methods
#suite.addTest(DependencyGraphTester.suite()) # Done
#suite.addTest(DependencyTreeTester.suite()) # 3 methods
#suite.addTest(DispatcherTester.suite()) # 5 methods
#suite.addTest(FunctionalTester.suite()) # Make sure func_run_commands istested for self organizing
#suite.addTest(GraphTester.suite()) # Done
#suite.addTest(JSONManagerTester.suite()) # 1 method
#suite.addTest(PipelineTester.suite()) # Make sure func_run_commands is tested for self organizing
suite.addTest(ResourceTester.suite()) # 1 test

runner = unittest.TextTestRunner()
runner.run(suite)
