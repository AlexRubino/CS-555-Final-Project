import unittest
import validation
import project as proj

class TestListDeceased(unittest.TestCase):
    def generate_fam_1(self, birth1, death1, birth2, death2, birth3, death3, birth4, death4, id=1):
        data = [(birth1, death1), (birth2, death2), (birth3, death3), (birth4, death4)]
        ret = []

        for i, (birth, death) in enumerate(data):
            ret.append(f'0 I{id}_{i+1} INDI')
            if birth is not None:
                ret.append('1 BIRT')
                ret.append(f'2 DATE {birth}')
            if death is not None:
                ret.append('1 DEAT')
                ret.append(f'2 DATE {death}')

        return ret


    def test_valid1(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', death1='01 JAN 2100',
            birth2='01 JAN 2000', death2='01 JAN 2100',
            birth3='01 JAN 2000', death3=None,
            birth4='01 JAN 2000', death4='01 JAN 2100',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_deceased(fams, indis)
        self.assertEqual(output, ['I1_1', 'I1_2', 'I1_4'])


    def test_valid2(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', death1='01 JAN 2100',
            birth2='01 JAN 2000', death2=None,
            birth3='01 JAN 2000', death3=None,
            birth4='01 JAN 2000', death4='01 JAN 2100',
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_deceased(fams, indis)
        self.assertEqual(output, ['I1_1', 'I1_4'])


    def test_valid3(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', death1='01 JAN 2100',
            birth2='01 JAN 2000', death2=None,
            birth3='01 JAN 2000', death3=None,
            birth4='01 JAN 2000', death4=None,
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_deceased(fams, indis)
        self.assertEqual(output, ['I1_1'])

    def test_valid4(self):
        ged = self.generate_fam_1(
            birth1='01 JAN 1900', death1=None,
            birth2='01 JAN 2000', death2=None,
            birth3='01 JAN 2000', death3=None,
            birth4='01 JAN 2000', death4=None,
            )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_deceased(fams, indis)
        self.assertEqual(output, [])


if __name__ == '__main__':
    unittest.main()