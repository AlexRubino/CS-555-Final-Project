import sys
sys.path.append('../')
import unittest
import validation
import project as proj

class TestUniqueIDs(unittest.TestCase):

    def generate_fam_1(self, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_3 INDI',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
        ]

    def generate_fam_2(self, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_3 INDI',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'1 CHIL I{id}_4',
            f'1 CHIL I{id}_5',
            f'1 CHIL I{id}_6',
            f'1 CHIL I{id}_7',
        ]

    def generate_fam_3(self, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'0 I{id}_2 INDI',
            f'0 I{id}_4 INDI',
            f'0 I{id}_4 INDI',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_4'
        ]

    def generate_fam_4(self, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'0 I{id}_2 INDI',
            f'0 I{id}_3 INDI',
            f'0 I{id}_4 INDI',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3'
        ]

    def generate_fam_5(self, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'0 I{id}_2 INDI',
            f'0 I{id}_3 INDI',
            f'0 I{id}_3 INDI',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3'
        ]


    def test_valid_unique_iid_fid_1(self):
        ged = self.generate_fam_1()
        fams, indis = proj.parse_ged_data_duplicates_allowed(ged)
        output = validation.validate_unique_ids(fams, indis)
        self.assertEqual(output, [])

    def test_valid_unique_iid_fid_2(self):
        ged = self.generate_fam_2()
        fams, indis = proj.parse_ged_data_duplicates_allowed(ged)
        output = validation.validate_unique_ids(fams, indis)
        self.assertEqual(output, [])

    def test_invalid_unique_iid_fid_3(self):
        ged = self.generate_fam_3()
        fams, indis = proj.parse_ged_data_duplicates_allowed(ged)
        output = validation.validate_unique_ids(fams, indis)
        self.assertEqual(output, [('I1_4', f'Individual iid=I1_4 is not unique')])

    def test_invalid_unique_iid_fid_4(self):
        ged = self.generate_fam_4()
        fams, indis = proj.parse_ged_data_duplicates_allowed(ged)
        output = validation.validate_unique_ids(fams, indis)
        self.assertEqual(output, [('F1', f'Family fid=F1 is not unique')])

    def test_invalid_unique_iid_fid_5(self):
        ged = self.generate_fam_5()
        fams, indis = proj.parse_ged_data_duplicates_allowed(ged)
        output = validation.validate_unique_ids(fams, indis)
        self.assertEqual(output, [('I1_3', 'Individual iid=I1_3 is not unique'), ('F1', f'Family fid=F1 is not unique')])

if __name__ == '__main__':
    unittest.main()