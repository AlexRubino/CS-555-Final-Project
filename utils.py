from datetime import datetime

def parse_date(str_date):
  return datetime.strptime(str_date, '%Y-%m-%d')

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