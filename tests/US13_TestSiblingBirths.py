import sys
sys.path.append('../')
import unittest
import validation as validation
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

    def generate_fam_2(self, husband, wife, marriage, id=1):
        h_birth, h_death = husband
        w_birth, w_death = wife
        marr_date, div_date = marriage
        ret =  [
            f'0 I{id}_1 INDI',
            '1 BIRT' if h_birth is not None else '',
            f'2 DATE {h_birth}' if h_birth is not None else '',
            '1 DEAT' if h_death is not None else '',
            f'2 DATE {h_death}' if h_death is not None else '',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            '1 BIRT' if w_birth is not None else '',
            f'2 DATE {w_birth}' if w_birth is not None else '',
            '1 DEAT' if w_death is not None else '',
            f'2 DATE {w_death}' if w_death is not None else '',
            f'1 FAMS F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            '1 MARR' if marr_date is not None else '',
            f'2 DATE {marr_date}' if marr_date is not None else '',
            '1 DIV' if div_date is not None else '',
            f'2 DATE {div_date}' if div_date is not None else ''
        ]
        # This removes all the empty lines
        return [i for i in ret if i]
    
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
        ged = self.generate_fam_1('01 JAN 2010', '16 JUN 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_sibling_births(fams, indis)
        self.assertEqual(output, [('F1', "Siblings with id = I1_3 and id = I1_4 in fid = F1 have birth dates between three days and eight months apart.")])

#     def test4(self):
#         ged = self.generate_fam_2(
#             husband=('01 JAN 2011', '01 MAR 2013'), 
#             wife=('01 FEB 2009', '01 MAR 2013'), 
#             marriage=('01 JAN 2010', '01 JUN 2012')
#         )   
#         fams, indis = proj.parse_ged_data(ged)
#         output = validation.validate_birth_before_marriage(fams, indis)
#         self.assertEqual(output, [('I1_1', 'Person id = I1_1 in family id = F1 has marriage before birth.')])
    
#     def test5(self):
#         ged = self.generate_fam_2(
#             husband=('01 JAN 2011', '01 MAR 2013'), 
#             wife=('01 FEB 2010', '01 MAR 2013'), 
#             marriage=('01 JAN 2010', '01 JUN 2012')
#         )   
#         fams, indis = proj.parse_ged_data(ged)
#         output = validation.validate_birth_before_marriage(fams, indis)
#         self.assertEqual(output, [('I1_1', 'Person id = I1_1 in family id = F1 has marriage before birth.'), ('I1_2', 'Person id = I1_2 in family id = F1 has marriage before birth.')])

if __name__ == '__main__':
    unittest.main()