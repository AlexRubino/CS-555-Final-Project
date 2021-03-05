import utils as utils

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
  lifetime = utils.yeardelta(150)
  current_date = utils.current_date()
  
  for iid in indis:
    death_date = None
    if indis[iid]['DEAT'] is not None:
      # If the input date is outside the scope of a datetime object,
      # then return the error message
      if not utils.parseable_date(indis[iid]['DEAT']):
        ret_data.append((iid, f'Individual id={iid} is older than 150 years'))
        continue

      death_date = utils.parse_date(indis[iid]['DEAT'])
    else:
      death_date = current_date

    if indis[iid]['BIRT'] is not None:
      if not utils.parseable_date(indis[iid]['BIRT']):
        ret_data.append((iid, f'Individual id={iid} is older than 150 years'))
        continue

      birth_date = utils.parse_date(indis[iid]['BIRT'])
      if death_date - birth_date > lifetime:
        ret_data.append((iid, f'Individual id={iid} is older than 150 years'))
  
  return ret_data

'''
  Implements US08
  
  Returns a list pairs:
  [(id1, r1), (id2, r2), ...]
  
  Where the first item in the pair is the id of an
  invalid family and the second item is the reason.
  
  Note that a given family id may appear more than
  once if multiple invalid reasons are found.
'''
def validate_birth_marriage_order(fams, indis):
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
  
