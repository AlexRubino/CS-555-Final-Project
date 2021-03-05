import sys
sys.path.append('../')
import unittest
import validation as validation
import project as proj

class TestMarriageBeforeDeath(unittest.TestCase):

    def generate_fam_1(self, marriage, birth, divorce, death, id=1):
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
            f'1 CHIL I{id}_3',
            '1 MARR',
            f'2 DATE {marriage}',
            '1 DIV',
            f'2 DATE {divorce}'
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

    def test_marriage_before_divorce_1(self):
        ged = self.generate_fam_2(
            husband = ('01 JAN 2000','01 JAN 2032'),
            wife = ('01 JAN 2001','01 JAN 2032'),
            marriage = ('01 JAN 2021','01 JAN 2031')
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_divorce(fams, indis)
        self.assertEqual(output, [])

    def test_marriage_before_divorce_2(self):
        ged = self.generate_fam_2(
            husband = ('01 JAN 2000',None),
            wife = ('01 JAN 2001',None),
            marriage = ('01 JAN 2021',None)
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_divorce(fams, indis)
        self.assertEqual(output, [])

    def test_marriage_before_divorce_3(self):
        ged = self.generate_fam_2(
            husband = ('01 JAN 2000',None),
            wife = ('01 JAN 2001','01 JAN 2080'),
            marriage = ('01 JAN 2021','01 MAR 2060')
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_divorce(fams, indis)
        self.assertEqual(output, [])
'''
    def test_married_after_death_1(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 1970')
        fams, indis = proj.parse_ged_data(ged)
        output = proj.marriage_before_death(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has marriage after death of partner')])

    def test_married_after_death_2(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='01 JAN 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = proj.marriage_before_death(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has marriage after death of partner')])

    def test_married_after_death_3(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 1950', divorce='05 JAN 2020', death='31 DEC 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = proj.marriage_before_death(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has marriage after death of partner')])
'''
if __name__ == '__main__':
    unittest.main() 