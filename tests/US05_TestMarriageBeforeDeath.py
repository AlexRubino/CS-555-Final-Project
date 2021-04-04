import unittest
import validation
import project as proj

class TestMarriageBeforeDeath(unittest.TestCase):

    def generate_fam_1(self, marriage, birth, divorce, death, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            '1 BIRT',
            f'2 DATE {birth}',
            '1 DEAT Y',
            f'2 DATE {death}',
            f'0 I{id}_3 INDI',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            '1 MARR',
            f'2 DATE {marriage}',
            '1 DIV',
            f'2 DATE {divorce}'
        ]

    def test_married_before_death_1(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 2040')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_death(fams, indis)
        self.assertEqual(output, [])

    def test_married_before_death_2(self):
        ged = self.generate_fam_1(marriage='01 JAN 1990', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 2040')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_death(fams, indis)
        self.assertEqual(output, [])

    def test_married_before_death_3(self):
        ged = self.generate_fam_1(marriage='01 JAN 1970', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 2040')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_death(fams, indis)
        self.assertEqual(output, [])

    def test_married_after_death_1(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 1970')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_death(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has marriage after death of partner')])

    def test_married_after_death_2(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_death(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has marriage after death of partner')])

    def test_married_after_death_3(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='31 DEC 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_death(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has marriage after death of partner')])

if __name__ == '__main__':
    unittest.main()