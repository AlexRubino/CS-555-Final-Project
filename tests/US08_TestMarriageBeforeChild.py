import unittest
import validation
import project as proj

class MarriageBeforeChild(unittest.TestCase):
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

    def test_ok_order(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 2011')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_child(fams, indis)
        self.assertEqual(output, [])

    def test_bad_order(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 2009')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_child(fams, indis)
        self.assertEqual(output, [('F1', 'Child id=I1_3 has birthdate before marriage of parents')])

    def test_same_date(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 2010')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_marriage_before_child(fams, indis)
        self.assertEqual(output, [])

    def test_multi_family(self):
        ged1 = self.generate_fam_1(marriage='01 JAN 2000', birth='02 JAN 2000', id=1)
        ged2 = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 2009', id=2)

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_marriage_before_child(fams, indis)
        bad_fams = [o[0] for o in output]

        self.assertTrue('F2' in bad_fams)
        self.assertEqual(len(bad_fams), 1)

    def test_multi_bad_family(self):
        ged1 = self.generate_fam_1(marriage='01 JAN 2001', birth='02 JAN 2000', id=1)
        ged2 = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 2009', id=2)

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_marriage_before_child(fams, indis)
        bad_fams = [o[0] for o in output]

        self.assertTrue('F1' in bad_fams)
        self.assertTrue('F2' in bad_fams)
        self.assertEqual(len(bad_fams), 2)


if __name__ == '__main__':
    unittest.main()