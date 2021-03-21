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

def year_difference(date1, date2):
  fields1 = date1.split("-")
  fields2 = date2.split("-")
  year1 = int(fields1[0])
  year2 = int(fields2[0])
  year_difference = abs(year1 - year2)
  return year_difference

def month_difference(date1, date2):
  fields1 = date1.split("-")
  fields2 = date2.split("-")
  month1 = int(fields1[1])
  month2 = int(fields2[1])
  month_difference = abs(month1 - month2)
  # month_difference = dateutil.relativedelta(date2, date1).months
  return month_difference

def day_difference(date1, date2):
  fields1 = date1.split("-")
  fields2 = date2.split("-")
  day1 = int(fields1[2])
  day2 = int(fields2[2])
  day_difference = abs(day1 - day2)
  return day_difference

# def date_difference(date1, date2):
#   difference = abs(date1 - date2)
#   return difference

# def month_difference(d1, d2):
#     d1 = datetime.timedelta(d1, "%Y-%m-%d")
#     d2 = datetime.strptime(d2, "%Y-%m-%d")
#     return abs((d2 - d1).months)

#     # use_date = use_date+relativedelta(months=+1)
