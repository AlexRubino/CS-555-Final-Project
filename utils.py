from datetime import datetime, timedelta

def parse_date(str_date):
  return datetime.strptime(str_date, '%Y-%m-%d')

def current_date():
  return datetime.now()

# Returns a timedelta for the number of years provided
def yeardelta(years):
  return timedelta(days=365*years)

def get_age(birthday, today):
  ans = today.year - birthday.year
  if (today.month, today.day) < (birthday.month, birthday.day):
    ans -= 1
  return ans