import sys
sys.path.append('../')
import unittest
import validation
import project as proj

class TestDifferentFirstnameBirthdayFamily(unittest.TestCase):
    def generate_fam_1(self, birth1, name1, birth2, name2, birth3, name3, birth4, name4, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 NAME {name1}',
            f'1 FAMS F1',
            '1 BIRT',
            f'2 DATE {birth1}',
            f'0 I{id}_2 INDI',
            f'1 NAME {name2}',
            f'1 FAMS F1',
            '1 BIRT',
            f'2 DATE {birth2}',
            f'0 I{id}_3 INDI',
            f'1 NAME {name3}',
            f'1 FAMC F{id}',
            '1 BIRT',
            f'2 DATE {birth3}',
            f'0 F1 FAM',
            f'0 I{id}_4 INDI',
            f'1 NAME {name4}',
            f'1 FAMC F{id}',
            '1 BIRT',
            f'2 DATE {birth4}',
            f'0 F1 FAM',
            '1 MARR',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'1 CHIL I{id}_4'
        ]

    def generate_fam_2(self, birth1, name1, birth2, name2, birth3, name3, birth4, name4,id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 NAME {name1}',
            f'1 FAMS F1',
            '1 BIRT',
            f'2 DATE {birth1}',
            f'0 I{id}_2 INDI',
            f'1 NAME {name2}',
            f'1 FAMS F1',
            '1 BIRT',
            f'2 DATE {birth2}',
            f'0 F1 FAM',
            '1 MARR',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            
            f'0 I{id}_3 INDI',
            f'1 NAME {name3}',
            f'1 FAMS F2',
            '1 BIRT',
            f'2 DATE {birth3}',
            f'0 I{id}_4 INDI',
            f'1 NAME {name4}',
            f'1 FAMS F2',
            '1 BIRT',
            f'2 DATE {birth4}',
            f'0 F2 FAM',
            '1 MARR',
            f'1 HUSB I{id}_3',
            f'1 WIFE I{id}_4',
        ]

    def test_valid1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Smith',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2012', name3='John e',
            birth4='01 JAN 2222', name4='John z',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_firstname_birthday_family(fams, indis)
        self.assertEqual(output, [])

    def test_valid2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Apple',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2012', name3='John Apple',
            birth4='01 JAN 2222', name4='John Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_firstname_birthday_family(fams, indis)
        self.assertEqual(output, [])

    def test_valid3(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Apple',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2012', name3='John Apple',
            birth4='01 JAN 2012', name4='Matt Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_firstname_birthday_family(fams, indis)
        self.assertEqual(output, [])

    def test_fail1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Apple',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2012', name3='John Apple',
            birth4='01 JAN 2012', name4='John Dice',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_firstname_birthday_family(fams, indis)
        self.assertEqual(output, [('I1_3','Individual id=I1_3 shares name and birth date with individual id=I1_4')])

    def test_fail2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Apple',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2000', name3='John Apple',
            birth4='01 JAN 2022', name4='John Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_firstname_birthday_family(fams, indis)
        self.assertEqual(output, [('I1_3','Individual id=I1_3 shares name and birth date with individual id=I1_4')])

if __name__ == '__main__':
    unittest.main()