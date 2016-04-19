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


import ArgumentsTester
import CommandlineTester
import CommandTester
import CompressionTester
import ConfigManagerTester
import DependencyGraphTester
import DependencyTreeTester
#import Dispatcher
import FunctionalTester
import GraphTester
#import JSONManagerTester
import PipelineTester
import ResourceTester
import unittest


# Calls all unit tests as a regression suite.
suite=unittest.TestSuite()
#suite.addTest(ArgumentsTester.suite()) # Running
#suite.addTest(CommandlineTester.suite()) # Running
#suite.addTest(CommandTester.suite()) # Running
#suite.addTest(CompressionTester.suite()) # Running
#suite.addTest(ConfigManagerTester.suite()) # 1 methods ok for now.
#suite.addTest(DependencyGraphTester.suite()) # Running
#suite.addTest(DependencyTreeTester.suite()) # Running
##suite.addTest(DispatcherTester.suite()) # 5 methods
suite.addTest(FunctionalTester.suite()) # 10 functions
#suite.addTest(GraphTester.suite()) # Running
##suite.addTest(JSONManagerTester.suite()) # 1 method, push Read JSON to parent script. ok for now.
#suite.addTest(PipelineTester.suite()) # Running
#suite.addTest(ResourceTester.suite()) # Running

runner = unittest.TextTestRunner()
runner.run(suite)
