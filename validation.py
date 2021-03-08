import utils as utils

'''
  Implements US01: Dates before current date
'''
def validate_dates_before_current(root_nodes):
  ret_data = []
  today = utils.current_date()
  def check_dates(root):
    if root.tag == 'DATE':
      sdate = root.get_arg()
      date = utils.parse_date(sdate)
      if date > today:
        ret_data.append((sdate, 'Date is invalid - after present date'))

    for child in root.children:
      check_dates(child)

  for root in root_nodes:
    check_dates(root)

  return ret_data

'''
  Implements US02: Birth before marriage
  
  Returns a list pairs:
  [(id1, r1), (id2, r2), ...]
  
  Where the first item in the pair is the id of an
  invalid person and the second item is the reason.
'''
def validate_birth_before_marriage(fams, indis):
  return_data = []

  for cid in indis:
    if indis[cid]['BIRT'] is not None:
      birthday = utils.parse_date(indis[cid]['BIRT'])

      for fid in fams:
        if fams[fid]['MARR'] is not None:
          marriage_day = utils.parse_date(fams[fid]['MARR'])

          if marriage_day < birthday:
            return_data.append((cid, f'Person id = {cid} has marriage before birth.'))
      
  return return_data
  
'''
  Implements US03: Birth before death
  
  Returns a list pairs:
  [(id1, r1), (id2, r2), ...]
  
  Where the first item in the pair is the id of an
  invalid person and the second item is the reason.
'''
def validate_birth_before_death(fams, indis):
  return_data = []

  for cid in indis:
    if indis[cid]['BIRT'] is not None:
      birthday = utils.parse_date(indis[cid]['BIRT'])

      if indis[cid]['DEAT'] is not None:
        death_day = utils.parse_date(indis[cid]['DEAT'])

        if death_day < birthday:
          return_data.append((cid, f'Person id = {cid} has death before birth.'))
      
  return return_data

'''
  Implements US06
  Sprint 1
  Zack Schieberl
  A married couple cannot get divorced after one of them dies
'''
def validate_divorce_before_death(fams, indis):
  ret_data = []
  
  for fid in fams:
    if fams[fid]['DIV'] is not None:
      divorce_date = utils.parse_date(fams[fid]['DIV'])
      husband_id = fams[fid]['HUSB']
      wife_id = fams[fid]['WIFE']

      if indis[husband_id]['DEAT'] is not None:
        death_date = utils.parse_date(indis[husband_id]['DEAT'])
        if death_date < divorce_date:
          ret_data.append((husband_id, f'Individual id={husband_id} has a divorce after his death'))
      if indis[wife_id]['DEAT'] is not None:
        death_date = utils.parse_date(indis[wife_id]['DEAT'])
        if death_date < divorce_date:
          ret_data.append((wife_id, f'Individual id={wife_id} has a divorce after her death'))
  
  return ret_data

'''
  Implements US07
  Sprint 1
  Zack Schieberl
  An indiviual cannot be over 150 years old (alive or dead)
'''
def validate_reasonable_age(fams, indis):
  ret_data = []
  lifetime = 150
  current_date = utils.current_date()
  
  for iid in indis:
    death_date = None
    if indis[iid]['DEAT'] is not None:
      # If the input date is outside the scope of a datetime object,
      # then return the error message
      if not utils.parseable_date(indis[iid]['DEAT']):
        ret_data.append((iid, f'Individual id={iid} is older than {lifetime} years'))
        continue

      death_date = utils.parse_date(indis[iid]['DEAT'])
    else:
      death_date = current_date

    if indis[iid]['BIRT'] is not None:
      if not utils.parseable_date(indis[iid]['BIRT']):
        ret_data.append((iid, f'Individual id={iid} is older than {lifetime} years'))
        continue

      birth_date = utils.parse_date(indis[iid]['BIRT'])
      if utils.get_age(birth_date, death_date) > lifetime:
        ret_data.append((iid, f'Individual id={iid} is older than {lifetime} years'))
  
  return ret_data

'''
  Implements US08: Birth before marriage of parents
  
  Returns a list pairs:
  [(id1, r1), (id2, r2), ...]
  
  Where the first item in the pair is the id of an
  invalid family and the second item is the reason.
  
  Note that a given family id may appear more than
  once if multiple invalid reasons are found.
'''
def validate_marriage_before_child(fams, indis):
  ret_data = []
  
  for fid in fams:
    if fams[fid]['MARR'] is not None:
      marriage = utils.parse_date(fams[fid]['MARR'])
      
      for cid in fams[fid]['CHIL']:
        if indis[cid]['BIRT'] is not None:
          birth = utils.parse_date(indis[cid]['BIRT'])
          if birth < marriage:
            ret_data.append((fid, f'Child id={cid} has birthdate before marriage'))
  
  return ret_data
  
'''
  Implements US11: No bigamy
  
  Marriages are terminated by either divorce or death
  no unterminated marriages may intersect.
  
  Marriages without a MARR tag are ignored and marriages 
  without a DIV (or DEAT) tag are assumed to be ongoing.
'''
def validate_marriage_before_child(fams, indis):
  def intersect(int1, int2):
    a,b = int1
    c,d = int2
    return (d is None or d >= a) and (b is None or b >= c)
  
  ret_data = []
  
  # for a given id, give a list of their marriages
  marriages = {iid:[] for iid in indis}
  for iid in indis:
    for fid in indis[iid]['FAMS']:
      if any(fams[fid][tag] is None for tag in ['HUSB','WIFE','MARR']):
        continue
      
      begin_date = utils.parse_date(fams[fid]['MARR'])
      end_date = None
      if indis[fams[fid]['HUSB']]['DEAT'] is not None:
        deat = utils.parse_date(indis[fams[fid]['HUSB']]['DEAT'])
        end_date = (deat if end_date is None else min(end_date, deat))
      if indis[fams[fid]['WIFE']]['DEAT'] is not None:
        deat = utils.parse_date(indis[fams[fid]['WIFE']]['DEAT'])
        end_date = (deat if end_date is None else min(end_date, deat))
      if fams[fid]['DIV'] is not None:
        div = utils.parse_date(fams[fid]['DIV'])
        end_date = (div if end_date is None else min(end_date, div))
      
      marriages[iid].append((begin_date, end_date))
    marriages[iid].sort()
    
    for i in range(len(marriages[iid]) - 1):
      int1 = marriages[iid][i]  
      int2 = marriages[iid][i+1]  
      
      if intersect(int1, int2):
        ret_data.append((iid, f'Individual id={iid} was in two or more marriages at the same time'))
        break
    
  return ret_data