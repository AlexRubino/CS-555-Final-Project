import unittest
import validation
import project as proj

class TestSingleLiving(unittest.TestCase):
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
        indis[fam[par]]['DEAT'] = None

      for cid in fam['CHIL']:
        if cid not in indis:
          indis[cid] = {'FAMC': None, 'FAMS': []}
        indis[cid]['FAMC'] = fid
        indis[cid]['DEAT'] = None

    return fams, indis

  def test_fam1(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': [],
        'DIV': None
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.list_single_living(fams, indis)
    self.assertEqual(output, [])

  def test_fam2(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4'],
        'DIV': None
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.list_single_living(fams, indis)
    self.assertEqual(output, ['I3', 'I4'])

  def test_fam3(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4'],
        'DIV': None
      }, {
        'ID': 'F2',
        'HUSB': 'I3',
        'WIFE': 'I5',
        'CHIL': ['I6', 'I7'],
        'DIV': None
      }, {
        'ID': 'F3',
        'HUSB': 'I4',
        'WIFE': 'I8',
        'CHIL': [],
        'DIV': None
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.list_single_living(fams, indis)
    self.assertEqual(output, ['I6', 'I7'])

  def test_fam4(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4'],
        'DIV': '12/1/2004'
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.list_single_living(fams, indis)
    self.assertEqual(output, ['I1', 'I2', 'I3', 'I4'])

if __name__ == '__main__':
  unittest.main()