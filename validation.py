import utils as utils

'''
  Implements US02: Birth before marriage
  
  Returns a list pairs:
  [(id1, r1), (id2, r2), ...]
  
  Where the first item in the pair is the id of an
  invalid person and the second item is the reason.
'''
def validate_birth_before_marriage(fams, indis):
  return_data = []

  for fid in fams:
    if fams[fid]['MARR'] is not None:
      marriage_day = utils.parse_date(fams[fid]['MARR'])

      husband_id = fams[fid]['HUSB']
      wife_id = fams[fid]['WIFE']

      husband_birth = indis[husband_id]['BIRT']
      wife_birth = indis[wife_id]['BIRT']

      if husband_birth is not None:
        husband_birthday = utils.parse_date(husband_birth)

      if wife_birth is not None:
        wife_birthday = utils.parse_date(wife_birth)

      if marriage_day < husband_birthday:
        return_data.append((husband_id, f'Husband id = {husband_id} in family id = {fid} has marriage before birth.'))

      if marriage_day < wife_birthday:
        return_data.append((wife_id, f'Wife id = {wife_id} in family id = {fid} has marriage before birth.'))

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

'''
  Implements US13
  Sprint 2
  Luke McEvoy & Alex Rubino
  Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day).
'''

def validate_sibling_births(fams, indis):
  return_data = []

  for fid in fams:
    children_birthdays = []

    for cid in fams[fid]['CHIL']:
      # Appends every child's birthday into the array
      children_birthdays.append((cid, utils.parse_date(indis[cid]['BIRT'])))
    

    for i in range(0, len(children_birthdays)):

      for j in range(i + 1, len(children_birthdays)):

        difference = utils.date_difference(children_birthdays[i][1], children_birthdays[j][1])

        if difference.days > 1:
          print(difference.days)
          print(difference.days / 30)
          if (difference.days / 30) < 9:
            return_data.append((fid, f'Siblings with id = {children_birthdays[i][0]} and id = {children_birthdays[j][0]} in fid = {fid} have birth dates between three days and eight months apart.'))
      
        # if abs(children_birthdays[i][1].date().year - children_birthdays[j][1].date().year) <= 1:
        #   if abs(children_birthdays[i][1].date().month - children_birthdays[j][1].date().month) == 0:

        # if (abs(children_birthdays[i][1].date().month - children_birthdays[j][1].date().month) <= 8): 
        #   return_data.append((fid, f'Siblings with id = {children_birthdays[i][0]} and id = {children_birthdays[j][0]} in fid = {fid} have birth dates between eight months apart.'))
        # elif (abs(children_birthdays[i][1].date().year - children_birthdays[j][1].date().year) == 0) and (abs(children_birthdays[i][1].date().month - children_birthdays[j][1].date().month) == 0) and (abs(children_birthdays[i][1].date().day - children_birthdays[j][1].date().day) >= 2):
        #   return_data.append((fid, f'Siblings with id = {children_birthdays[i][0]} and id = {children_birthdays[j][0]} in fid = {fid} have birth dates between three days and eight months apart.'))

  return return_data