import unittest
import validation
import project as proj

class TestMalesHaveSameLastName(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents
        and a child with a given marriage date and child birthdate.

        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, name1, name2, name3, name4, id=1):
        return [
            f'0 I{id}_1 INDI',
            f'1 NAME {name1}',
            f'1 SEX M',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 NAME {name2}',
            f'1 SEX F',
            f'1 FAMS F{id}',
            f'0 I{id}_3 INDI',
            f'1 NAME {name3}',
            f'1 SEX M',
            f'0 I{id}_4 INDI',
            f'1 NAME {name4}',
            f'1 SEX M',
            f'1 FAMC F{id}',
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            f'1 CHIL I{id}_3',
            f'1 CHIL I{id}_4',
        ]

    def test_ok_0(self):
        ged = self.generate_fam_1(
            name1 = "Luke McEvoy",
            name2 = "Nick McEvoy",
            name3 = "Hugh McEvoy",
            name4 = "Jackson McEvoy"
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_all_men_have_same_last_name(fams, indis)
        self.assertEqual(output, [])

    def test_ok_1(self):
        ged = self.generate_fam_1(
            name1 = "Luke McEvoy",
            name2 = "Nick Jannet",
            name3 = "Hugh McEvoy",
            name4 = "Jackson McEvoy"
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_all_men_have_same_last_name(fams, indis)
        self.assertEqual(output, [])

    def test_ok_2(self):
            ged = self.generate_fam_1(
                name1 = "Luke Maydof",
                name2 = "Nick Maydof",
                name3 = "Hugh Maydof",
                name4 = "Berney Maydof"
            )
            fams, indis = proj.parse_ged_data(ged)
            output = validation.validate_all_men_have_same_last_name(fams, indis)
            self.assertEqual(output, [])

    def test_fail_0(self):
            ged = self.generate_fam_1(
                name1 = "Luke Apples",
                name2 = "Nick Oranges",
                name3 = "Hugh Watermelon",
                name4 = "Berney Pineapple"
            )
            fams, indis = proj.parse_ged_data(ged)
            output = validation.validate_all_men_have_same_last_name(fams, indis)
            self.assertEqual(output, [('F1', f'Family id=F1 has males with a different last name')])

    def test_fail_1(self):
        ged = self.generate_fam_1(
            name1 = "Luke Apples",
            name2 = "Nick Dog",
            name3 = "Hugh Cat",
            name4 = "Berney Test"
        )
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_all_men_have_same_last_name(fams, indis)
        self.assertEqual(output, [('F1', f'Family id=F1 has males with a different last name')])

    def test_fail_2(self):
            ged = self.generate_fam_1(
                name1 = "Luke Apples",
                name2 = "Nick Porsche",
                name3 = "Hugh Watermelon",
                name4 = "Berney Tesla"
            )
            fams, indis = proj.parse_ged_data(ged)
            output = validation.validate_all_men_have_same_last_name(fams, indis)
            self.assertEqual(output, [('F1', f'Family id=F1 has males with a different last name')])


if __name__ == '__main__':
    unittest.main()