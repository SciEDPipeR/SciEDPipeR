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
import JSONManagerTester
import PipelineTester
import ResourceTester
import unittest


# Calls all unit tests as a regression suite.
suite=unittest.TestSuite()
suite.addTest(ArgumentsTester.suite())
suite.addTest(CommandlineTester.suite())
suite.addTest(CommandTester.suite()) # Running
suite.addTest(CompressionTester.suite())
suite.addTest(ConfigManagerTester.suite()) # 1 methods but ok for now.
suite.addTest(DependencyGraphTester.suite())
suite.addTest(DependencyTreeTester.suite())
##suite.addTest(DispatcherTester.suite()) # 5 methods, local works
#suite.addTest(FunctionalTester.suite()) # 3 methods but ok for now
suite.addTest(GraphTester.suite())
suite.addTest(JSONManagerTester.suite()) # 1 method, push Read JSON to parent script. Fix sort.
suite.addTest(PipelineTester.suite())
suite.addTest(ResourceTester.suite())

runner = unittest.TextTestRunner()
runner.run(suite)
