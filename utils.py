from datetime import datetime
# from dateutil import *

def parse_date(str_date):
  return datetime.strptime(str_date, '%Y-%m-%d')

def stringify_date(date):
  return date.strftime("%Y-%m-%d")

# Helper function for checking if a date is parsable or not
# Returns a boolean
def parseable_date(str_date):
  if str_date == None:
    return False
  if not isinstance(str_date, str):
    return False
  fields = str_date.split("-")
  if len(fields) != 3:
    return False
  year = int(fields[0])
  # The maximum year for a datetime object is 9999
  if year <= 0 or year >= 9999:
    return False
  return True

def current_date():
  return datetime.now()

def get_age(birthday, today=None):
  if today is None:
    today = current_date()

  ans = today.year - birthday.year
  if (today.month, today.day) < (birthday.month, birthday.day):
    ans -= 1
  return ans

'''
i1 and i2 are two intervals (a pair of dates)
A value of None indicates no start or end

Ex:
  i1 = (None, JAN 1 2020) ; i2 = (JAN 1 2019, None) --> true
  i1 = (JAN 1 2019, JAN 1 2020) ; i2 = (None, JAN 1 2018) --> false
'''
def interval_intersect(i1, i2):
  a, b = i1
  c, d = i2
  return (b is None or c is None or b >= c) and (a is None or d is None or d >= a)
