import unittest
import sys
import os

# include parent directory of test file
dirname = os.path.dirname
sys.path.append(dirname(dirname(__file__)))

import US09_TestBirthBeforeParentDeath as US09
import US10_TestMarriageAfterFourteen as US10
import US11_TestNoBigamy as US11

def sprint02_suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()

  suite.addTests(loader.loadTestsFromModule(US09))
  suite.addTests(loader.loadTestsFromModule(US10))
  suite.addTests(loader.loadTestsFromModule(US11))

  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner(verbosity=3)
  result = runner.run(sprint02_suite())