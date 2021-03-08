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
  US04:     Marriage Before Divorce
  Author:   Luke McEvoy
  Sprint:   1 (3/8/21)
  
  Story Description:
    Marriage should occur before divorce of spouses, and divorce can only occur after marriage
'''
def validate_marriage_before_divorce(fams, indis):
  # create list of invalid marriages to be returned
  invalid_marriages = []

  for fid in fams:
    # if married and divorced
    if fams[fid]['MARR'] is not None and fams[fid]['DIV'] is not None:

      # parse marriage and divorce date of husband and wife
      marriage_date = utils.parse_date(fams[fid]['MARR'])
      divorce_date = utils.parse_date(fams[fid]['DIV'])

      # if divorced before married
      if divorce_date < marriage_date:
        # add family to invalid marriage list
        invalid_marriages.append((fid, f'Family id={fid} has marriage after divorce'))

  return invalid_marriages

'''
  US05:     Marriage before Death
  Author:   Luke McEvoy
  Sprint:   1 (3/8/21)
  
  Story Description:
    Marriage should occur before death of either spouse
'''
def validate_marriage_before_death(fams, indis):
  # list of invalid marriages to be returned
  invalid_marriages = []

  for fid in fams:
    # if married
    if fams[fid]['MARR'] is not None:

      # parse marriage and death dates of husband and wife
      marriage = utils.parse_date(fams[fid]['MARR'])
      husbandID, wifeID = fams[fid]['HUSB'], fams[fid]['WIFE']
      husbandDeath, wifeDeath = indis[husbandID]['DEAT'], indis[wifeID]['DEAT']

      # if a partner has died
      if (wifeDeath or husbandDeath is not None):

        # create a list of dead partners (can be length of 1 or 2)
        dead_partners = []

        # if wife has died
        if wifeDeath is not None:
          wifeDeath = utils.parse_date(wifeDeath)
          # add wife's death date to list of dead partners 
          dead_partners.append(wifeDeath)

        # if husband has died
        if husbandDeath is not None:
          husbandDeath = utils.parse_date(husbandDeath)
          # add husband's death date to list of dead partners 
          dead_partners.append(husbandDeath)

        # find who died first (guarenteed at least one death between partners)
        # if partner who died first died before couple's marriage date
        if min(dead_partners) < marriage:
          # add family to invalid marriage list
          invalid_marriages.append((fid, f'Family id={fid} has marriage after death of partner'))
  
  return invalid_marriages

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
  US10:     Marriage after 14
  Author:   Luke McEvoy & Alex Rubino
  Sprint:   2 (3/22/21)
  
  Story Description:
    Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
'''
def validate_marriage_after_fourteen(fams, indis):
  invalid_marriages = []

  for fid in fams:
    # if married
    if fams[fid]['MARR'] is not None:
      marriage_date = utils.parse_date(fams[fid]['MARR'])

      husbandID, wifeID = fams[fid]['HUSB'], fams[fid]['WIFE']
      husband_birth, wife_birth = indis[husbandID]['BIRT'], indis[wifeID]['BIRT']

      ages = []
      if husband_birth is not None:
        husband_birth = utils.parse_date(husband_birth)
        husband_marriage_age = utils.get_age(husband_birth, marriage_date)
        ages.append(husband_marriage_age)

      if wife_birth is not None:
        wife_birth = utils.parse_date(wife_birth)
        wife_marriage_age = utils.get_age(wife_birth, marriage_date)
        ages.append(wife_marriage_age)

      if len(ages) > 0 and min(ages) < 14:
        invalid_marriages.append((fid, f'Family id={fid} has marriage before age 14'))

    return invalid_marriages
