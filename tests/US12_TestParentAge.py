import unittest
import validation
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

    def generate_fam_2(self, husband, wife, child, id=1):
        h_birth, h_death = husband
        w_birth, w_death = wife
        c_birth, c_death = child
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
            '1 MARR',
            f'1 CHIL I{id}_3',
            f'1 FAMS F{id}',
            f'0 I{id}_3 INDI',
            '1 BIRT' if c_birth is not None else '',
            f'2 DATE {c_birth}' if c_birth is not None else '',
        ]
        # This removes all the empty lines
        return [i for i in ret if i]

    def test1(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 2000', None),
            wife=('01 JAN 2010', None),
            child=('01 JAN 2050', None)
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_parent_age(fams, indis)
        self.assertEqual(output, [])

    def test2(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 1900', None),
            wife=('01 JAN 2010', None),
            child=('01 JAN 2050', None)
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_parent_age(fams, indis)
        self.assertEqual(output, [('I1_1', 'Husband id=I1_1 in family id=F1 was born over 80 years before child id=I1_3.')])

    def test3(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 2000', None),
            wife=('01 JAN 1910', None),
            child=('01 JAN 2050', None)
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_parent_age(fams, indis)
        self.assertEqual(output, [('I1_2', 'Wife id=I1_2 in family id=F1 was born over 60 years before child id=I1_3.')])

    def test4(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 1900', None),
            wife=('01 JAN 1910', None),
            child=('01 JAN 2050', None)
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_parent_age(fams, indis)
        self.assertEqual(output, [(('I1_1', 'Husband id=I1_1 in family id=F1 was born over 80 years before child id=I1_3.')), ('I1_2', 'Wife id=I1_2 in family id=F1 was born over 60 years before child id=I1_3.')])

    def test5(self):
        ged = self.generate_fam_2(
            husband=('01 JAN 1900', None),
            wife=('01 JAN 1910', None),
            child=('01 JAN 1981', None)
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_parent_age(fams, indis)
        self.assertEqual(output, [(('I1_1', 'Husband id=I1_1 in family id=F1 was born over 80 years before child id=I1_3.')), ('I1_2', 'Wife id=I1_2 in family id=F1 was born over 60 years before child id=I1_3.')])

if __name__ == '__main__':
    unittest.main()