import unittest
import validation
import project as proj

class TestDivorceBeforeDeath(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents
        and a child with a given marriage date and child birthdate.

        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, marriage, birth, id=1):
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

    def test_ok_age(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 2010', '01 JAN 2013'),
            wife=('01 JAN 2010', '01 JAN 2013'),
            marriage=(None, None)
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_reasonable_age(fams, indis)
        self.assertEqual(output, [])

    def test_husband_over(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 2010', '01 JAN 2213'),
            wife=('01 JAN 2010', '01 JAN 2013'),
            marriage=(None, None)
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_reasonable_age(fams, indis)
        self.assertEqual(output, [('I1_1', 'Individual id=I1_1 is older than 150 years')])

    def test_wife_over(self):
        ged = self.generate_fam_2(
            husband=('11 JUL 2010', '06 DEC 2013'),
            wife=('22 DEC 2010', '31 MAR 2213'),
            marriage=(None, None)
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_reasonable_age(fams, indis)
        self.assertEqual(output, [('I1_2', 'Individual id=I1_2 is older than 150 years')])

    def test_both_over(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 2010', '01 JAN 9999'),
            wife=('22 DEC 1', '31 MAR 2213'),
            marriage=(None, None)
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_reasonable_age(fams, indis)
        self.assertEqual(output, [('I1_1', 'Individual id=I1_1 is older than 150 years'),
                                  ('I1_2', 'Individual id=I1_2 is older than 150 years')])

    def test_ok_live(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 2010', None),
            wife=('01 JAN 2010', None),
            marriage=(None, None)
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_divorce_before_death(fams, indis)
        self.assertEqual(output, [])

    def test_bad_live(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 1577', None),
            wife=('22 DEC 2010', None),
            marriage=(None, None)
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_reasonable_age(fams, indis)
        self.assertEqual(output, [('I1_1', 'Individual id=I1_1 is older than 150 years')])


if __name__ == '__main__':
    unittest.main()