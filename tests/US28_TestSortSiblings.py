import unittest
import validation
import project as proj

class TestDifferentFirstnameBirthdayFamily(unittest.TestCase):
    def generate_fam_1(self, birth1, name1, birth2, name2, birth3, name3, birth4, name4, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 NAME {name1}',
            f'1 FAMS F{id}',
            '1 BIRT',
            f'2 DATE {birth1}',
            f'0 I{id}_2 INDI',
            f'1 NAME {name2}',
            f'1 FAMS F{id}',
            '1 BIRT',
            f'2 DATE {birth2}',
            f'0 I{id}_3 INDI',
            f'1 NAME {name3}',
            f'1 FAMC F{id}',
            '1 BIRT',
            f'2 DATE {birth3}',
            f'0 F{id} FAM',
            f'0 I{id}_4 INDI',
            f'1 NAME {name4}',
            f'1 FAMC F{id}',
            '1 BIRT',
            f'2 DATE {birth4}',
            f'0 F{id} FAM',
            '1 MARR',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'1 CHIL I{id}_4'
        ]


    def test_valid1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Smith',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2012', name3='John e',
            birth4='01 JAN 2222', name4='John z',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.sort_siblings_decreasing_age(fams, indis)
        self.assertEqual(output, {'F1':['I1_3', 'I1_4']})

    def test_valid2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 2002', name1='John Apple',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2022', name3='John Apple',
            birth4='01 JAN 2012', name4='John Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.sort_siblings_decreasing_age(fams, indis)
        self.assertEqual(output, {'F1':['I1_4', 'I1_3']})

    def test_valid3(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', name1='John Apple',
            birth2='01 JAN 2000', name2='John Apple',
            birth3='01 JAN 2012', name3='John Apple',
            birth4='01 JAN 2012', name4='Matt Apple',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.sort_siblings_decreasing_age(fams, indis)
        self.assertEqual(output, {'F1':['I1_3', 'I1_4']})

    def test_multifam(self):
        ged1 = self.generate_fam_1(
            birth1='01 JAN 1900', name1='A A',
            birth2='01 JAN 2000', name2='A A',
            birth3='01 JAN 2011', name3='A A',
            birth4='01 JAN 2012', name4='A A',
            )
        ged2 = self.generate_fam_1(
            birth1='01 JAN 2900', name1='B B',
            birth2='01 JAN 2900', name2='B B',
            birth3='01 APR 3012', name3='B B',
            birth4='01 FEB 3012', name4='B B',
            id=2)

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.sort_siblings_decreasing_age(fams, indis)
        self.assertEqual(output, {'F1': ['I1_3', 'I1_4'], 'F2': ['I2_4', 'I2_3']})


if __name__ == '__main__':
    unittest.main()