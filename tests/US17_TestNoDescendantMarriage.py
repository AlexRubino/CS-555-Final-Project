import unittest
import validation
import project as proj

class TestNoDescendantMarriage(unittest.TestCase):
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
    output = validation.validate_no_descendant_marriage(fams, indis)
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
    output = validation.validate_no_descendant_marriage(fams, indis)
    self.assertEqual(output, [])

  def test_bad_child_marriage(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'F2',
        'HUSB': 'I3',
        'WIFE': 'I2',
        'CHIL': ['I5']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_descendant_marriage(fams, indis)
    self.assertEqual(output, [('F2', 'Family fid=F2 is a marriage of ancestor id=I2 and descendant id=I3')])

  def test_bad_grandchild_marriage(self):
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
        'HUSB': 'I1',
        'WIFE': 'I7',
        'CHIL': []
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_descendant_marriage(fams, indis)
    self.assertEqual(output, [('F3', 'Family fid=F3 is a marriage of ancestor id=I1 and descendant id=I7')])

  def test_bad_multiple_violation(self):
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
        'HUSB': 'I1',
        'WIFE': 'I7',
        'CHIL': ['I8']
      }, {
        'ID': 'F4',
        'HUSB': 'I6',
        'WIFE': 'I5',
        'CHIL': ['I9', 'I10']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_no_descendant_marriage(fams, indis)
    self.assertEqual(len(output), 2)
    self.assertTrue(any(fid=='F3' for fid,_ in output))
    self.assertTrue(any(fid=='F4' for fid,_ in output))


if __name__ == '__main__':
  unittest.main()