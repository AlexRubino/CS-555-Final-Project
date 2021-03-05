import sys
sys.path.append('../')
import unittest
import validation as validation
import project as proj

class TestBirthBeforeDeath(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents 
        and a child with a given birthdate and child deathdate. 
        
        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, birth, death, id=1):
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
            f'1 CHIL I{id}_3'
        ]
    
    def test1(self):
        ged = self.generate_fam_1(birth='01 JAN 2020', death='15 JAN 2021')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_death(fams, indis)
        self.assertEqual(output, [])

    def test2(self):
        ged = self.generate_fam_1(birth='01 JAN 2020', death='15 JAN 2020')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_death(fams, indis)
        self.assertEqual(output, [])

    def test3(self):
        ged = self.generate_fam_1(birth='15 JAN 2000', death='15 JAN 2000')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_death(fams, indis)
        self.assertEqual(output, [])

    def test4(self):
        ged = self.generate_fam_1(birth='15 JAN 2000', death='1 MAR 1900')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_death(fams, indis)
        self.assertEqual(output, [('I1_2', 'Person id = I1_2 has death before birth.')])
    
    def test5(self):
        ged = self.generate_fam_1(birth='15 APR 1962', death='3 MAY 1974')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_birth_before_death(fams, indis)
        self.assertEqual(output, [])

if __name__ == '__main__':
    unittest.main()