import unittest
import validation
import project as proj

class TestCorrespondingEntries(unittest.TestCase):
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

  def test_ok_entries_simple(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_corresponding_entries(fams, indis)
    self.assertEqual(output, [])

  def test_ok_entries_multi(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'F2',
        'HUSB': 'I3',
        'WIFE': 'I4',
        'CHIL': ['I5', 'I6']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    output = validation.validate_corresponding_entries(fams, indis)

  def test_bad_entries_simple(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    indis['I1']['FAMS'] = []

    output = validation.validate_corresponding_entries(fams, indis)
    self.assertEqual(output, [('I1', 'Husband id=I1 in family id=F1 has incomplete FAMS entry')])

  def test_bad_entries_typo(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'F2',
        'HUSB': 'I5',
        'WIFE': 'I6',
        'CHIL': []
      },
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    indis['I2']['FAMS'] = ['F2']

    output = validation.validate_corresponding_entries(fams, indis)
    self.assertEqual(output, [('I2', 'Wife id=I2 in family id=F1 has incomplete FAMS entry'),
                              ('I2', 'Spouse id=I2 in family id=F2 is missing from HUSB/WIFE entry')])

  def test_bad_entries_multi(self):
    fam_list = [
      {
        'ID': 'F1',
        'HUSB': 'I1',
        'WIFE': 'I2',
        'CHIL': ['I3', 'I4']
      }, {
        'ID': 'F2',
        'HUSB': 'I5',
        'WIFE': 'I6',
        'CHIL': []
      },
    ]

    fams, indis = self.generate_from_famlist(fam_list)
    indis['I1']['FAMS'] = ['F2']
    indis['I4']['FAMC'] = 'F1'
    fams['F1']['CHIL'] = ['I4', 'I6']

    output = validation.validate_corresponding_entries(fams, indis)
    self.assertEqual(output, [('I1', 'Husband id=I1 in family id=F1 has incomplete FAMS entry'),
                              ('I6', 'Child id=I6 in family id=F1 has missing or incorrect FAMC entry'),
                              ('I1', 'Spouse id=I1 in family id=F2 is missing from HUSB/WIFE entry'),
                              ('I3', 'Child id=I3 in family id=F1 is missing from family CHIL list')])

if __name__ == '__main__':
  unittest.main()