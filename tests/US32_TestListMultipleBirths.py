import unittest
import validation
import project as proj

class TestListMultipleBirths(unittest.TestCase):
    def generate_fam_1(self, birth1, birth2, birth3, birth4, id=1):
        return [
            f'0 I{id}_1 INDI',
            '1 BIRT',
            f'2 DATE {birth1}',
            f'0 I{id}_2 INDI',
            '1 BIRT',
            f'2 DATE {birth2}',
            f'0 I{id}_3 INDI',
            '1 BIRT',
            f'2 DATE {birth3}',
            f'0 I{id}_4 INDI',
            '1 BIRT',
            f'2 DATE {birth4}',
        ]


    def test_valid1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900',
            birth2='01 JAN 2000',
            birth3='01 JAN 2000',
            birth4='01 JAN 2000',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, ['2000-01-01'])


    def test_valid2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900',
            birth2='01 JAN 1900',
            birth3='01 JAN 2000',
            birth4='01 JAN 2000',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, ['1900-01-01','2000-01-01'])

    def test_valid3(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900',
            birth2='01 JAN 1900',
            birth3='01 JAN 2000',
            birth4='01 JAN 2001',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, ['1900-01-01'])

    def test_valid4(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1902',
            birth2='01 JAN 1900',
            birth3='01 JAN 2000',
            birth4='01 JAN 2001',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [])

if __name__ == '__main__':
    unittest.main()