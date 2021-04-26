import unittest
import utils
import project as proj

class TestCorrespondingEntries(unittest.TestCase):
  def test_standard_age(self):
    birt = utils.parse_date('2001-03-14')
    today = utils.parse_date('2005-12-25')
    age = utils.get_age(birt, today)
    self.assertEqual(age, 4)

  def test_birthday_age(self):
    birt = utils.parse_date('2001-03-14')
    today = utils.parse_date('2006-03-14')
    age = utils.get_age(birt, today)
    self.assertEqual(age, 5)

  def test_zero_age(self):
    birt = utils.parse_date('2001-03-14')
    today = utils.parse_date('2001-03-14')
    age = utils.get_age(birt, today)
    self.assertEqual(age, 0)

  # this is useful for us to detect anomalies
  def test_negative_age(self):
    birt = utils.parse_date('2001-03-14')
    today = utils.parse_date('1990-01-01')
    age = utils.get_age(birt, today)
    self.assertEqual(age, -12)

if __name__ == '__main__':
  unittest.main()