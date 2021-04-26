import unittest
import validation
import project as proj

class TestListMultipleBirths(unittest.TestCase):
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
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [])

    def test_none(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
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
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [('F1', ['I1_3', 'I1_4', 'I1_5', 'I1_6', 'I1_7', 'I1_8'])])

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
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [])

    def test_bad_25(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=["25 DEC 2020" for _ in range(25)]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0][0], 'F1')
        self.assertEqual(len(output[0][1]), 25)

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
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [('F1', ['I1_3', 'I1_4', 'I1_5', 'I1_6', 'I1_7', 'I1_8', 'I1_9'])])

    def test_bad_8(self):
        ged = self.generate_fam_1(
            marriage="01 JAN 2000",
            births=[
                "25 DEC 2020",
                "25 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020",
                "26 DEC 2020",
                "29 DEC 2020",
                "29 DEC 2020",
                "29 DEC 2020"
            ]
        )

        fams, indis = proj.parse_ged_data(ged)
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [('F1', ['I1_3', 'I1_4', 'I1_5', 'I1_6', 'I1_7']),
                                  ('F1', ['I1_8', 'I1_9', 'I1_10'])])

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
        output = validation.list_all_multiple_births(fams, indis)
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
        output = validation.list_all_multiple_births(fams, indis)
        self.assertEqual(output, [('F1', ['I1_3', 'I1_4', 'I1_5', 'I1_6', 'I1_7', 'I1_8']),
                                  ('F2', ['I2_3', 'I2_4', 'I2_5', 'I2_6', 'I2_7', 'I2_8'])])


if __name__ == '__main__':
    unittest.main()