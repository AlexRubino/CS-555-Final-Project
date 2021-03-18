import unittest
import validation as validation
import project as proj

class BirthBeforeParentDeath(unittest.TestCase):
    def generate_fam_4(self, husb_deat, wife_deat, child_birt, id=1):
        ret = [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            '1 DEAT' if husb_deat is not None else '',
            f'2 DATE {husb_deat}' if husb_deat is not None else '',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            '1 DEAT' if wife_deat is not None else '',
            f'2 DATE {wife_deat}' if wife_deat is not None else '',
            f'0 I{id}_3 INDI',
            f'1 FAMC F{id}',
            '1 BIRT' if child_birt is not None else '',
            f'2 DATE {child_birt}' if child_birt is not None else '',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
        ]
        return [i for i in ret if i]

    def test_ok_1(self):
        ged = self.generate_fam_4(husb_deat='01 JAN 2010',
                                  wife_deat='01 JAN 2011',
                                  child_birt='01 JAN 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_parent_death(fams, indis)
        self.assertEqual(output, [])

    def test_ok_2(self):
        ged = self.generate_fam_4(husb_deat=None,
                                  wife_deat=None,
                                  child_birt='01 JAN 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_parent_death(fams, indis)
        self.assertEqual(output, [])

    def test_bad_wife(self):
        ged = self.generate_fam_4(husb_deat='10 JAN 2010',
                                  wife_deat='01 JAN 2010',
                                  child_birt='05 JAN 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_parent_death(fams, indis)
        self.assertEqual(output, [('I1_3', 'Individual I1_3 was born after parent I1_2 death')])

    def test_bad_both(self):
        ged = self.generate_fam_4(husb_deat='01 JAN 2008',
                                  wife_deat='01 JAN 2010',
                                  child_birt='05 JAN 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_parent_death(fams, indis)
        self.assertEqual(len(output), 2)
        self.assertTrue(any('I1_1' in reason for _,reason in output))
        self.assertTrue(any('I1_2' in reason for _,reason in output))

    def test_bad_multiple_fams(self):
        ged1 = self.generate_fam_4(husb_deat='01 FEB 2010',
                                  wife_deat='01 JAN 2010',
                                  child_birt='05 MAR 2010', id=1)
        ged2 = self.generate_fam_4(husb_deat='01 JAN 2008',
                                  wife_deat='01 JAN 2011',
                                  child_birt='05 JAN 2010', id=2)
        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_birth_before_parent_death(fams, indis)
        self.assertEqual(len(output), 2)
        self.assertTrue(any(iid == 'I1_3' for iid, _ in output))
        self.assertTrue(any(iid == 'I2_3' for iid, _ in output))


if __name__ == '__main__':
    unittest.main()