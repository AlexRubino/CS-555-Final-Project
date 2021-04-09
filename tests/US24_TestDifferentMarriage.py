import sys
sys.path.append('../')
import unittest
import validation
import project as proj

class TestDifferentMarriage(unittest.TestCase):
    def generate_fam_1(self, 
        husbandName1, wifeName1, marriage1, 
        husbandName2, wifeName2, marriage2, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 NAME {husbandName1}',
            f'1 FAMS F{id}_1',
            f'0 I{id}_2 INDI',
            f'1 NAME {wifeName1}',
            f'1 FAMS F{id}_1',
            f'0 F{id}_1 FAM',
            '1 MARR',
            f'2 DATE {marriage1}',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'0 I{id}_3 INDI',
            f'1 NAME {husbandName2}',
            f'1 FAMS F{id}_2',
            f'0 I{id}_4 INDI',
            f'1 NAME {wifeName2}',
            f'1 FAMS F{id}_2',
            f'0 F{id}_2 FAM',
            '1 MARR',
            f'2 DATE {marriage2}',
            f'1 HUSB I{id}_3',
            f'1 WIFE I{id}_4'
        ]

    def test_valid1(self):
        ged = self.generate_fam_1(
            husbandName1="Alex", wifeName1="Jill", marriage1="01 JAN 2000", 
            husbandName2="Luke", wifeName2="Sof", marriage2="02 JAN 2020",
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_marriage(fams, indis)
        self.assertEqual(output, [])

    def test_valid2(self):
        ged = self.generate_fam_1(
            husbandName1="Alex", wifeName1="Meg", marriage1="01 JAN 2000", 
            husbandName2="Luke", wifeName2="Lex", marriage2="02 JAN 2020",
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_marriage(fams, indis)
        self.assertEqual(output, [])

    def test_valid3(self):
        ged = self.generate_fam_1(
            husbandName1="Alex", wifeName1="Meg", marriage1="02 JAN 2020", 
            husbandName2="Luke", wifeName2="Meg", marriage2="02 JAN 2020",
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_marriage(fams, indis)
        self.assertEqual(output, [])

    def test_fail1(self):
        ged = self.generate_fam_1(
            husbandName1="Luke", wifeName1="Meg", marriage1="02 JAN 2020", 
            husbandName2="Luke", wifeName2="Meg", marriage2="02 JAN 2020",
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_marriage(fams, indis)
        self.assertEqual(output, [(('Luke', 'Meg', '2020-01-02'), 'Multiple families have the same names and marriage days.')])

    def test_fail2(self):
        ged = self.generate_fam_1(
            husbandName1="Alex", wifeName1="Meg", marriage1="02 JAN 2000", 
            husbandName2="Alex", wifeName2="Meg", marriage2="02 JAN 2000",
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_marriage(fams, indis)
        self.assertEqual(output, [(('Alex', 'Meg', '2000-01-02'), 'Multiple families have the same names and marriage days.')])

if __name__ == '__main__':
    unittest.main()