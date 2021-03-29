from datetime import datetime
# from dateutil import *

def parse_date(str_date):
  return datetime.strptime(str_date, '%Y-%m-%d')

def stringify_date(date):
  return date.strftime("%Y-%m-%d")

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

'''
  Return a list of between 0 and 2 parents of the given individual id
'''
def get_parents(iid, fams, indis):
  if indis[iid]['FAMC'] is None:
    return []
  fid = indis[iid]['FAMC']

  return [fams[fid][par] for par in ['HUSB', 'WIFE'] if fams[fid][par] is not None]

'''
  Return all children in iid's FAM except for iid themself
'''
def get_siblings(iid, fams, indis):
  if indis[iid]['FAMC'] is None:
    return []

  ret = fams[indis[iid]['FAMC']]['CHIL']
  # this should always be the case with proper input data
  if iid in ret:
    idx = ret.index(iid)
    ret = ret[:idx] + ret[idx+1:]

  return ret

'''
  Return a boolean specifying if 'cid' (child id) is a descendant of 'aid' (ancestor id)
  True iff we can reach 'aid' via a series of 1 or more parent relationships from 'cid'
'''
def is_descendant(cid, aid, fams, indis):
  if cid == aid:
    return False

  stk = [cid]
  seen = set()

  while len(stk) > 0:
    iid = stk.pop()
    if iid == aid:
      return True

    if iid in seen:
      continue
    seen.add(iid)

    stk += get_parents(iid, fams, indis)

  return False

'''
  Return multi-line string representation of list where each line contains at most 25 chars (or one list item)
'''
def format_list(l):
  ret = ''
  cur = '['
  for i in range(len(l)):
    sx = f'\'{l[i]}\''
    delim = ', ' if i != len(l) - 1 else ']'

    if len(cur) <= 1 or len(cur) + len(sx) + len(delim) <= 24:
      cur += sx + delim
    else:
      ret += cur + '\n '
      cur = sx + delim

  return ret + cur