import unittest
import validation
import project as proj

class TestNoUncleMarriage(unittest.TestCase):
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
    output = validation.validate_aunts_uncles(fams, indis)
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
    output = validation.validate_aunts_uncles(fams, indis)
    self.assertEqual(output, [])

  def test_bad_neice(self):
    fam_list = [
      {
        'ID': 'grandparents',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'goodfam',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6']
      }, {
        'ID': 'badfam',
        'HUSB': 'I4',
        'WIFE': 'I6',
        'CHIL': ['I7']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_aunts_uncles(fams, indis)
    self.assertEqual(output, [('badfam', f'Family id=badfam has a marriage between an uncle and their niece')])

  def test_bad_nephew(self):
    fam_list = [
      {
        'ID': 'grandparents',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'goodfam',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6']
      }, {
        'ID': 'badfam',
        'HUSB': 'I6',
        'WIFE': 'I4',
        'CHIL': ['I7']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_aunts_uncles(fams, indis)
    self.assertEqual(output, [('badfam', f'Family id=badfam has a marriage between an aunt and their nephew')])

  def test_bad_grand_nephew(self):
    fam_list = [
      {
        'ID': 'grandparents',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'goodfam1',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6']
      }, {
        'ID': 'goodfam2',
        'HUSB': 'I6',
        'WIFE': 'I7',
        'CHIL': ['I8']
      }, {
        'ID': 'badfam',
        'HUSB': 'I8',
        'WIFE': 'I4',
        'CHIL': ['I9']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_aunts_uncles(fams, indis)
    self.assertEqual(output, [('badfam', f'Family id=badfam has a marriage between an aunt and their nephew')])

if __name__ == '__main__':
  unittest.main()