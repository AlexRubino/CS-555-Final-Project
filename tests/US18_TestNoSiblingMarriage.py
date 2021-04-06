import sys
sys.path.append('../')
import unittest
import validation
import project as proj

class TestNoSiblingMarraige(unittest.TestCase):
  def generate_from_famlist(self, fam_list):
    fams, indis = {}, {}

    for fam in fam_list:
      fid = fam.pop('ID')
      fams[fid] = fam

      for par in ['HUSB', 'WIFE']:
        if fam[par] not in indis:
          indis[fam[par]] = {'FAMC': None, 'FAMS': []}
        indis[fam[par]]['FAMS'].append(fid)

      for cid in fam['CHIL']:
        if cid not in indis:
          indis[cid] = {'FAMC': None, 'FAMS': []}
        indis[cid]['FAMC'] = fid

    return fams, indis

  def test_ok_minimal(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_sibling_marriage(fams, indis)
    self.assertEqual(output, [])

  def test_ok_many_fam(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'F2',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6', 'I7']
      }, {
        'ID': 'F3',
        'HUSB': 'I4',
        'WIFE': 'I8',
        'CHIL': []
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_sibling_marriage(fams, indis)
    self.assertEqual(output, [])

  def test_bad_no_removed(self):
    fam_list = [
      {
        'ID': 'grandparents',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'parents1',
        'HUSB': 'I3',
        'WIFE': 'I4',
        'CHIL': ['I6']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_sibling_marriage(fams, indis)
    self.assertEqual(output, [('parents1', 'Siblings I3 and I4 should not marry.')])

  def test_bad_once_removed(self):
    fam_list = [
      {
        'ID': 'grandparents',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'parents1',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6']
      }, {
        'ID': 'parents2',
        'HUSB': 'I4',
        'WIFE': 'I7',
        'CHIL': ['I8']
      }, {
        'ID': 'F4',
        'HUSB': 'I3',
        'WIFE': 'I4',
        'CHIL': ['I10', 'I11']
      }, {
        'ID': 'F5',
        'HUSB': 'I6',
        'WIFE': 'I10',
        'CHIL': []
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_sibling_marriage(fams, indis)
    self.assertEqual(output, [('F4', 'Siblings I3 and I4 should not marry.'), ('F5', 'Siblings I6 and I10 should not marry.')])

  def test_bad_multiple_violation(self):
    fam_list = [
      {
        'ID': 'grandparents',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'parents1',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6']
      }, {
        'ID': 'parents2',
        'HUSB': 'I4',
        'WIFE': 'I7',
        'CHIL': ['I8']
      }, {
        'ID': 'F4',
        'HUSB': 'I6',
        'WIFE': 'I8',
        'CHIL': []
      }, {
        'ID': 'F5',
        'HUSB': 'I8',
        'WIFE': 'I9',
        'CHIL': ['I10', 'I11']
      }, {
        'ID': 'F6',
        'HUSB': 'I6',
        'WIFE': 'I10',
        'CHIL': []
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_sibling_marriage(fams, indis)
    self.assertEqual(len(output), 0)


if __name__ == '__main__':
  unittest.main()