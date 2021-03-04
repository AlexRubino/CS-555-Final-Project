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
  
