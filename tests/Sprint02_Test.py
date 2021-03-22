import unittest
import sys
import os

# include parent directory of test file
dirname = os.path.dirname
sys.path.append(dirname(dirname(__file__)))

import US09_TestBirthBeforeParentDeath as US09
import US10_TestMarriageAfterFourteen as US10
import US11_TestNoBigamy as US11
import US12_TestParentAge as US12
import US13_TestSiblingBirths as US13
import US14_TestNoSextuplets as US14
import US15_TestNoExcessiveSiblings as US15
import US17_TestNoDescendantMarriage as US17
import US19_TestNoCousinMarriage as US19

def sprint02_suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()

  suite.addTests(loader.loadTestsFromModule(US09))
  suite.addTests(loader.loadTestsFromModule(US10))
  suite.addTests(loader.loadTestsFromModule(US11))
  suite.addTests(loader.loadTestsFromModule(US12))
  suite.addTests(loader.loadTestsFromModule(US13))
  suite.addTests(loader.loadTestsFromModule(US14))
  suite.addTests(loader.loadTestsFromModule(US15))
  suite.addTests(loader.loadTestsFromModule(US17))
  suite.addTests(loader.loadTestsFromModule(US19))

  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner(verbosity=3)
  result = runner.run(sprint02_suite())