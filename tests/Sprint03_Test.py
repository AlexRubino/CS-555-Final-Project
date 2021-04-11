import unittest
import sys
import os

# include parent directory of test file
dirname = os.path.dirname
sys.path.append(dirname(dirname(__file__)))

import US17_TestNoDescendantMarriage as US17
import US18_TestNoSiblingMarriage as US18
import US19_TestNoCousinMarriage as US19
import US22_TestUniqueIDs as US22
import US23_TestDifferentNameBirthday as US23
import US24_TestDifferentMarriage as US24

def sprint03_suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()

  suite.addTests(loader.loadTestsFromModule(US17))
  suite.addTests(loader.loadTestsFromModule(US18))
  suite.addTests(loader.loadTestsFromModule(US19))
  suite.addTests(loader.loadTestsFromModule(US22))
  suite.addTests(loader.loadTestsFromModule(US23))
  suite.addTests(loader.loadTestsFromModule(US24))

  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner(verbosity=3)
  result = runner.run(sprint03_suite())