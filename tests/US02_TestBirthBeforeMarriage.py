import sys
sys.path.append('../')
import unittest
import validation as validation
import project as proj

class TestBirthBeforeMarriage(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents 
        and a child with a given marriage date and child birthdate. 
        
        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, birth, marriage, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_3 INDI',
            '1 BIRT',
            f'2 DATE {birth}',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            '1 MARR',
            f'2 DATE {marriage}'
        ]
    
    def test1(self):
        ged = self.generate_fam_1(birth='01 JAN 2020', marriage='15 JAN 2021')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_marriage(fams, indis)
        self.assertEqual(output, [])

    def test2(self):
        ged = self.generate_fam_1(birth='01 JAN 2020', marriage='15 JAN 2020')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_marriage(fams, indis)
        self.assertEqual(output, [])

    def test3(self):
        ged = self.generate_fam_1(birth='15 JAN 2000', marriage='15 JAN 2000')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_marriage(fams, indis)
        self.assertEqual(output, [])

    def test4(self):
        ged = self.generate_fam_1(birth='15 JAN 2000', marriage='1 MAR 1900')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_marriage(fams, indis)
        self.assertEqual(output, [('I1_3', 'Person id = I1_3 has marriage before birth.')])
    
    def test5(self):
        ged = self.generate_fam_1(birth='15 APR 1962', marriage='15 MAY 1974')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_marriage(fams, indis)
        self.assertEqual(output, [])

if __name__ == '__main__':
    unittest.main()