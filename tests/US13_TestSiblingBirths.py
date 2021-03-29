import unittest
import validation
import project as proj

class TestSiblingBirths(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents
        and a child with a given marriage date and child birthdate.

        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, birth1, birth2, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_3 INDI',
            '1 BIRT',
            f'2 DATE {birth1}',
            f'0 I{id}_4 INDI',
            '1 BIRT',
            f'2 DATE {birth2}',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'1 CHIL I{id}_4',
        ]

    def test1(self):
        ged = self.generate_fam_1('01 JAN 2010', '01 JAN 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_sibling_births(fams, indis)
        self.assertEqual(output, [])

    def test2(self):
        ged = self.generate_fam_1('01 JAN 2010', '01 NOV 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_sibling_births(fams, indis)
        self.assertEqual(output, [])

    def test3(self):
        ged = self.generate_fam_1('01 JAN 2010', '01 SEP 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_sibling_births(fams, indis)
        self.assertEqual(output, [('F1', 'Siblings with id=I1_3 and id=I1_4 in fid=F1 have birth dates more than one day and not less than eight months apart.')])

    def test4(self):
        ged = self.generate_fam_1('01 JAN 2010', '01 JAN 2011')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_sibling_births(fams, indis)
        self.assertEqual(output, [])

    # def test5(self):
    #     ged = self.generate_fam_1('31 DEC 2010', '28 FEB 2011')
    #     fams, indis = proj.parse_ged_data(ged)
    #     output = validation.validate_sibling_births(fams, indis)
    #     self.assertEqual(output, [('F1', "Siblings with id = I1_3 and id = I1_4 in fid = F1 have birth dates between three days and eight months apart.")])

if __name__ == '__main__':
    unittest.main()