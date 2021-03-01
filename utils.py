from datetime import datetime

def parse_date(str_date):
  return datetime.strptime(str_date, '%Y-%m-%d')

def get_age(birthday, today):
  ans = today.year - birthday.year
  if (today.month, today.day) < (birthday.month, birthday.day):
    ans -= 1
  return ans