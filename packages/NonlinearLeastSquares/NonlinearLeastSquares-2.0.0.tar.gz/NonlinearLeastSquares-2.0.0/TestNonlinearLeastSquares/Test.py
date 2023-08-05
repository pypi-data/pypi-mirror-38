#!/usr/bin/env python

import unittest
import TestNonlinearLeastSquaresCalculation

class NonlinearLeastSquaresTestCase( unittest.TestCase ):
    def checkVersion(self):
        import NonlinearLeastSquares

testSuites = [unittest.makeSuite(NonlinearLeastSquaresTestCase, 'test')] 

for test_type in [
            TestNonlinearLeastSquaresCalculation,
    ]:
    testSuites.append(test_type.getTestSuites('test'))


def getTestDirectory():
    try:
        return os.path.abspath(os.path.dirname(__file__))
    except:
        return '.'

import os
os.chdir(getTestDirectory())

runner = unittest.TextTestRunner()
runner.run(unittest.TestSuite(testSuites))
