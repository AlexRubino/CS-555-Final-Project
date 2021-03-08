import unittest
import sys
import os

# include parent directory of test file
dirname = os.path.dirname
sys.path.append(dirname(dirname(__file__)))

import US01_TestDatesBeforeCurrent as US01
import US02_TestBirthBeforeMarriage as US02
import US03_TestBirthBeforeDeath as US03
import US04_TestMarriageBeforeDivorce as US04
import US05_TestMarriageBeforeDeath as US05
import US06_TestDivorceBeforeDeath as US06
import US07_TestReasonableAge as US07
import US08_TestMarriageBeforeChild as US08

def sprint01_suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  
  suite.addTests(loader.loadTestsFromModule(US01))
  suite.addTests(loader.loadTestsFromModule(US02))
  suite.addTests(loader.loadTestsFromModule(US03))
  suite.addTests(loader.loadTestsFromModule(US04))
  suite.addTests(loader.loadTestsFromModule(US05))
  suite.addTests(loader.loadTestsFromModule(US06))
  suite.addTests(loader.loadTestsFromModule(US07))
  suite.addTests(loader.loadTestsFromModule(US08))
  
  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner(verbosity=3)
  result = runner.run(sprint01_suite())