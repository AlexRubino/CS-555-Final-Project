import sys
sys.path.append('../')
import unittest
import validation
import project as proj

class TestDifferentNameBirthday(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents
        and a child with a given birthdate and child deathdate.

        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, birth1, name1, birth2, name2, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            '1 BIRT',
            f'2 DATE {birth1}',
            f'1 NAME {name1}',
            '1 BIRT',
            f'2 DATE {birth2}',
            f'1 NAME {name2}',
            f'0 I{id}_3 INDI',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3'
        ]

    def valid_test1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Smith',
            birth2='01 JAN 2000', name2='John Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_name_birthday(fams, indis)
        self.assertEqual(output, [])

    def valid_test2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='Matt Smith',
            birth2='01 JAN 2000', name2='Matt Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_name_birthday(fams, indis)
        self.assertEqual(output, [])

    def valid_test3(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 2000', name1='Alex Smith',
            birth2='01 JAN 2000', name2='Luke Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_name_birthday(fams, indis)
        self.assertEqual(output, [])

    def fail_test1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 2000', name1='Alex Apple',
            birth2='01 JAN 2000', name2='Alex Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_name_birthday(fams, indis)
        self.assertEqual(output, [])

    def fail_test2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 2000', name1='Luke Apple',
            birth2='01 JAN 2000', name2='Luke Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_different_name_birthday(fams, indis)
        self.assertEqual(output, [])

if __name__ == '__main__':
    unittest.main()