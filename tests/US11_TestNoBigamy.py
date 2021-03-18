import sys
sys.path.append('../')
import unittest
import validation as validation
import project as proj

class NoBigamy(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two
        married individuals
    '''
    def generate_fam_2(self, husband, wife, marriage, id=1, define_husband=True, husb_fams=[]):
        h_id, h_birth, h_death = husband
        husb_fams.append(id)
        w_id, w_birth, w_death = wife
        marr_date, div_date = marriage
        ret = [
            f'0 {w_id} INDI',
            '1 BIRT' if w_birth is not None else '',
            f'2 DATE {w_birth}' if w_birth is not None else '',
            '1 DEAT' if w_death is not None else '',
            f'2 DATE {w_death}' if w_death is not None else '',
            f'1 FAMS F{id}',
            f'0 F{id} FAM',
            f'1 HUSB {h_id}',
            f'1 WIFE {w_id}',
            '1 MARR' if marr_date is not None else '',
            f'2 DATE {marr_date}' if marr_date is not None else '',
            '1 DIV' if div_date is not None else '',
            f'2 DATE {div_date}' if div_date is not None else ''
        ]

        if define_husband:
            ret += [
                f'0 {h_id} INDI',
                '1 BIRT' if h_birth is not None else '',
                f'2 DATE {h_birth}' if h_birth is not None else '',
                '1 DEAT' if h_death is not None else '',
                f'2 DATE {h_death}' if h_death is not None else '',
                *[f'1 FAMS F{fid}' for fid in husb_fams]
            ]
        # This removes all the empty lines
        return [i for i in ret if i]

    def test_single_fam(self):
        ged = self.generate_fam_2(
            husband=('I1', '01 JAN 2010', '01 JAN 2013'),
            wife=('I2', '01 JAN 2010', '01 JAN 2013'),
            marriage=('01 JAN 2011', '01 JAN 2012'),
            husb_fams=[]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_bigamy(fams, indis)
        self.assertEqual(output, [])

    def test_multi_fam_good(self):
        ged1 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I2', None, None),
            marriage=('01 JAN 2011', '01 JAN 2012'),
            id=1,
            husb_fams=[2]
        )
        ged2 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I3', None, None),
            marriage=('01 JAN 2013', '01 JAN 2014'),
            id=2,
            define_husband=False
        )
        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_no_bigamy(fams, indis)
        self.assertEqual(output, [])

    def test_multi_fam_bad_divorce(self):
        ged1 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I2', None, None),
            marriage=('01 JAN 2011', '01 JAN 2012'),
            id=1,
            husb_fams=[2]
        )
        ged2 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I3', None, None),
            marriage=('01 JUL 2011', '01 JAN 2014'),
            id=2,
            define_husband=False
        )
        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_no_bigamy(fams, indis)
        self.assertEqual(output, [('I1', 'Individual id=I1 was in two or more marriages at the same time')])

    def test_multi_fam_bad_death(self):
        ged1 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I2', None, '01 JAN 2012'),
            marriage=('01 JAN 2011', None),
            id=1,
            husb_fams=[2]
        )
        ged2 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I3', None, None),
            marriage=('01 JUL 2011', '01 JAN 2014'),
            id=2,
            define_husband=False
        )
        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_no_bigamy(fams, indis)
        self.assertEqual(output, [('I1', 'Individual id=I1 was in two or more marriages at the same time')])

    def test_multi_fam_good_death(self):
        ged1 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I2', None, '01 JAN 2012'),
            marriage=('01 JAN 2011', None),
            id=1,
            husb_fams=[2]
        )
        ged2 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I3', None, None),
            marriage=('01 JUL 2013', '01 JAN 2014'),
            id=2,
            define_husband=False
        )

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_no_bigamy(fams, indis)
        self.assertEqual(output, [])

    def test_super_polygamy(self):
        ged1 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I2', None, None),
            marriage=('01 JAN 2011', None),
            id=1,
            husb_fams=[2,3]
        )
        ged2 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I3', None, None),
            marriage=('02 JAN 2011', None),
            id=2,
            define_husband=False
        )
        ged3 = self.generate_fam_2(
            husband=('I1', None, None),
            wife=('I4', None, None),
            marriage=('03 JAN 2011', None),
            id=3,
            define_husband=False
        )
        fams, indis = proj.parse_ged_data(ged1 + ged2 + ged3)
        output = validation.validate_no_bigamy(fams, indis)
        self.assertEqual(output, [('I1', 'Individual id=I1 was in two or more marriages at the same time')])

if __name__ == '__main__':
    unittest.main()