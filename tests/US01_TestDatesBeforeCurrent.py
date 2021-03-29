import unittest
import validation
import project as proj
import utils
import datetime

class DatesBeforeCurrent(unittest.TestCase):
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

    def test_ok_dates(self):
        ged = self.generate_fam_1(marriage='01 JAN 2010', birth='01 JAN 2011')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_dates_before_current(fams, indis)
        self.assertEqual(output, [])

    def test_bad_date(self):
        ged = self.generate_fam_1(marriage='01 JAN 4010', birth='01 JAN 2011')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_dates_before_current(fams, indis)
        self.assertEqual(output, [('F1', 'Marriage 4010-01-01 occurs in the future')])

    def test_bad_dates(self):
        ged = self.generate_fam_1(marriage='01 JAN 4010', birth='07 FEB 2102')
        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_dates_before_current(fams, indis)
        self.assertEqual(output, [('I1_3', 'Birthday 2102-02-07 occurs in the future'), ('F1', 'Marriage 4010-01-01 occurs in the future')])

    def test_many_bad_dates(self):
        ged1 = self.generate_fam_1(marriage='25 DEC 2101', birth='31 OCT 2102', id=1)
        ged2 = self.generate_fam_1(marriage='31 DEC 2104', birth='14 FEB 2103', id=2)

        fams, indis = proj.parse_ged_data(ged1 + ged2)
        output = validation.validate_dates_before_current(fams, indis)
        self.assertEqual(output, [('I1_3', 'Birthday 2102-10-31 occurs in the future'), ('I2_3', 'Birthday 2103-02-14 occurs in the future'), ('F1', 'Marriage 2101-12-25 occurs in the future'), ('F2', 'Marriage 2104-12-31 occurs in the future')])


    def test_today_tomorrow(self):
        today = datetime.date.today()
        ged_stoday = today.strftime("%d %b %Y").upper()
        stoday = utils.stringify_date(today)

        tomorrow = today + datetime.timedelta(days=1)
        ged_stomorrow = tomorrow.strftime("%d %b %Y").upper()
        stomorrow = utils.stringify_date(tomorrow)

        ged = self.generate_fam_1(marriage=ged_stoday, birth=ged_stomorrow, id=1)

        fams, indis = proj.parse_ged_data(ged)
        output = validation.validate_dates_before_current(fams, indis)
        self.assertEqual(output, [('I1_3', f'Birthday {stomorrow} occurs in the future')])


if __name__ == '__main__':
    unittest.main()