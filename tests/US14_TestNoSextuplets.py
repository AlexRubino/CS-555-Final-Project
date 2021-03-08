import sys
sys.path.append('../')
import unittest
import validation as validation
import project as proj

class TheseNoSextuplets(unittest.TestCase):
    '''
        Helper function which generates a minimal family of two parents 
        and a child with a given marriage date and child birthdate. 
        
        Optionally takes in the family ID (which is used to generate
        individual IDs as well).
    '''
    def generate_fam_1(self, marriage, births, id=1):
        child_births = []
        child_ids = []

        for index, child in enumerate(births):
            child_births += [
                 f'0 I{id}_{index + 3} INDI',
                '1 BIRT',
                f'2 DATE {child}',
                f'1 FAMC F{id}'
            ]
            child_ids += [
                f'1 CHIL I{id}_{index + 3}',
            ]

        #insert arrays into ret
        return [
            f'0 I{id}_1 INDI',
            f'1 FAMS F{id}',
            f'0 I{id}_2 INDI',
            f'1 FAMS F{id}',
            *child_births,
            f'0 F{id} FAM',
            f'1 HUSB I{id}_1',
            f'1 WIFE I{id}_2',
            *child_ids,
            '1 MARR',
            f'2 DATE {marriage}'
        ]
    
    def test_ok_2(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "19 JUL 2023"
            ]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [])

    def test_none(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [])

    def test_bad_6(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020"
            ]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has more than 5 children born together')])

    def test_ok_6(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2021",
                "25 DEC 2022",
                "25 DEC 2023",
                "25 DEC 2024",
                "25 DEC 2025"
            ]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [])

    def test_bad_25(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=["25 DEC 2020" for _ in range(25)]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has more than 5 children born together')])

    def test_bad_7(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020"
            ]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has more than 5 children born together')])

    def test_bad_8(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020",
                "27 DEC 2020",
                "27 DEC 2020",
                "27 DEC 2020"
            ]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has more than 5 children born together')])

    def test_ok_duo6(self):
        ged1 = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2021",
                "25 DEC 2022",
                "25 DEC 2023",
                "25 DEC 2024",
                "25 DEC 2025"
            ]
        )
        ged2 = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2021",
                "25 DEC 2022",
                "25 DEC 2023",
                "25 DEC 2024",
                "25 DEC 2025"
            ],
            id=2
        )

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [])

    def test_bad_duo6(self):
        ged1 = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020"
            ]
        )
        ged2 = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020",
                "25 DEC 2020"
            ],
            id=2
        )

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_no_sextuples(fams, indis)
        self.assertEqual(output, [('F1', 'Family id=F1 has more than 5 children born together'), 
                                  ('F2', 'Family id=F2 has more than 5 children born together')])


if __name__ == '__main__':
    unittest.main()