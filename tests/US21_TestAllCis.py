import unittest
import validation
import project as proj

class TestAllCis(unittest.TestCase):
  def generate_from_famlist(self, fam_list):
    fams, indis = {}, {}

    for fam in fam_list:
      fid = fam.pop('ID')
      fams[fid] = fam

      for par in ['HUSB', 'WIFE']:
        if fam[par] not in indis:
          indis[fam[par]] = {'FAMC': None, 'FAMS': []}
        indis[fam[par]]['FAMS'].append(fid)
        indis[fam[par]]['SEX'] = 'M' if par == 'HUSB' else 'F'

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
    output = validation.validate_gender_role(fams, indis)
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
    output = validation.validate_gender_role(fams, indis)
    self.assertEqual(output, [])

  def test_bad_gay(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    indis['I1']['SEX'] = 'F'
    output = validation.validate_gender_role(fams, indis)
    self.assertEqual(output, [('F1', f'Family id=F1 has a marriage where the husband id=I1 is not male')])

  def test_bad_nonbinary(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    indis['I1']['SEX'] = 'badaboom'
    indis['I2']['SEX'] = 'badabing'
    output = validation.validate_gender_role(fams, indis)
    self.assertEqual(output, [('F1', f'Family id=F1 has a marriage where the husband id=I1 is not male'),
                              ('F1', f'Family id=F1 has a marriage where the wife id=I2 is not female')])

  def test_ok_child(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    indis['I3']['SEX'] = 'somethingelse'
    output = validation.validate_gender_role(fams, indis)
    self.assertEqual(output, [])

if __name__ == '__main__':
  unittest.main()