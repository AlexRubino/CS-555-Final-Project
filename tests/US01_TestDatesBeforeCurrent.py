import unittest
import validation as validation
import project as proj
import utils as utils
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
        root_nodes = proj.build_ged_tree(ged)
        output = validation.validate_dates_before_current(root_nodes)
        self.assertEqual(output, [])
    
    def test_bad_date(self):
        ged = self.generate_fam_1(marriage='01 JAN 4010', birth='01 JAN 2011')
        root_nodes = proj.build_ged_tree(ged)
        output = validation.validate_dates_before_current(root_nodes)
        self.assertEqual(output, [('4010-01-01', 'Date is invalid - after present date')])
        
    def test_bad_dates(self):
        ged = self.generate_fam_1(marriage='01 JAN 4010', birth='07 FEB 2102')
        root_nodes = proj.build_ged_tree(ged)
        output = validation.validate_dates_before_current(root_nodes)
        bad_dates = [date for date,_ in output]
        self.assertEqual(len(bad_dates), 2)
        self.assertTrue('4010-01-01' in bad_dates)
        self.assertTrue('2102-02-07' in bad_dates)

    def test_many_bad_dates(self):
        ged1 = self.generate_fam_1(marriage='25 DEC 2101', birth='31 OCT 2102', id=1)
        ged2 = self.generate_fam_1(marriage='31 DEC 2104', birth='14 FEB 2103', id=2)
        
        root_nodes = proj.build_ged_tree(ged1 + ged2)
        output = validation.validate_dates_before_current(root_nodes)
        bad_dates = [date for date,_ in output]
        self.assertEqual(len(bad_dates), 4)
        self.assertTrue('2101-12-25' in bad_dates)
        self.assertTrue('2102-10-31' in bad_dates)
        self.assertTrue('2103-02-14' in bad_dates)
        self.assertTrue('2104-12-31' in bad_dates)
    
    def test_today_tomorrow(self):
        today = datetime.date.today()
        ged_stoday = today.strftime("%d %b %Y").upper()
        stoday = utils.stringify_date(today)
        
        tomorrow = today + datetime.timedelta(days=1)
        ged_stomorrow = tomorrow.strftime("%d %b %Y").upper()
        stomorrow = utils.stringify_date(tomorrow)
        
        ged = self.generate_fam_1(marriage=ged_stoday, birth=ged_stomorrow, id=1)
        
        root_nodes = proj.build_ged_tree(ged)
        output = validation.validate_dates_before_current(root_nodes)
        bad_dates = [date for date,_ in output]
        self.assertEqual(len(bad_dates), 1)
        self.assertTrue(stomorrow in bad_dates)


if __name__ == '__main__':
    unittest.main()