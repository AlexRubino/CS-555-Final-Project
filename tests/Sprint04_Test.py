import unittest
import sys
import os

# include parent directory of test file
dirname = os.path.dirname
sys.path.append(dirname(dirname(__file__)))

import US25_TestDifferentFirstnameBirthdayFamily as US25
import US26_TestCorrespondingEntries as US26
import US27_TestIndividualAges as US27
import US28_TestSortSiblings as US28
import US29_TestListDeceased as US29
import US32_TestListMultipleBirths as US32

def sprint04_suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()

  suite.addTests(loader.loadTestsFromModule(US25))
  suite.addTests(loader.loadTestsFromModule(US26))
  suite.addTests(loader.loadTestsFromModule(US27))
  suite.addTests(loader.loadTestsFromModule(US28))
  suite.addTests(loader.loadTestsFromModule(US29))
  suite.addTests(loader.loadTestsFromModule(US32))

  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner(verbosity=3)
  result = runner.run(sprint04_suite())