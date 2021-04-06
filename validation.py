from datetime import timedelta
import utils

'''
  Implements US01: Dates before current date
'''
def validate_dates_before_current(fams, indis):
  ret_data = []

  def check(date_str, is_indi, oid, date_type):
    if utils.parse_date(date_str) > utils.current_date():
      ret_data.append((oid, f'{date_type} {date_str} occurs in the future'))

  for iid in indis:
    if indis[iid]['BIRT'] is not None:
      check(indis[iid]['BIRT'], True, iid, 'Birthday')
    if indis[iid]['DEAT'] is not None:
      check(indis[iid]['DEAT'], True, iid, 'Death')

  for fid in fams:
    if fams[fid]['MARR'] is not None:
      check(fams[fid]['MARR'], False, fid, 'Marriage')
    if fams[fid]['DIV'] is not None:
      check(fams[fid]['DIV'], False, fid, 'Divorce')

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
        return_data.append((husband_id, f'Husband id={husband_id} in family id={fid} has marriage before birth.'))

      if marriage_day < wife_birthday:
        return_data.append((wife_id, f'Wife id={wife_id} in family id={fid} has marriage before birth.'))

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
          return_data.append((cid, f'Person id={cid} has death before birth.'))

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
      husband_id=fams[fid]['HUSB']
      wife_id=fams[fid]['WIFE']

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

  for iid in indis:
    if indis[iid]['BIRT'] is not None:
      birth_date = utils.parse_date(indis[iid]['BIRT'])
      death_date = utils.current_date()

      if indis[iid]['DEAT'] is not None:
        death_date = utils.parse_date(indis[iid]['DEAT'])

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
            ret_data.append((fid, f'Child id={cid} has birthdate before marriage of parents'))

  return ret_data

'''
  Implements US09: Birth before death of parents

  We enforce
  - child birth <= mother death
  - child birth <= father death + 1 year
'''
def validate_birth_before_parent_death(fams, indis):
  ret_data = []

  for iid in indis:
    if indis[iid]['FAMC'] is None or indis[iid]['BIRT'] is None:
      continue
    fid = indis[iid]['FAMC']
    birthdate = utils.parse_date(indis[iid]['BIRT'])

    for par in ['HUSB', 'WIFE']:
      if fams[fid][par] is None or indis[fams[fid][par]]['DEAT'] is None:
        continue
      par_deat = utils.parse_date(indis[fams[fid][par]]['DEAT'])
      if par == 'WIFE' and par_deat < birthdate or \
         par == 'HUSB' and par_deat + timedelta(days=365) < birthdate:
        ret_data.append((iid, f'Individual {iid} was born after parent {fams[fid][par]} death'))

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

'''
  Implements US11: No bigamy

  Marriages are terminated by either divorce or death
  no unterminated marriages may intersect.

  Marriages without a MARR tag are ignored and marriages
  without a DIV (or DEAT) tag are assumed to be ongoing.
'''
def validate_no_bigamy(fams, indis):
  ret_data = []

  for iid in indis:
    marriages = []
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

      marriages.append((begin_date, end_date))
    marriages.sort()
    for i in range(len(marriages) - 1):
      int1 = marriages[i]
      int2 = marriages[i+1]

      if utils.interval_intersect(int1, int2):
        ret_data.append((iid, f'Individual id={iid} was in two or more marriages at the same time'))
        break

  return ret_data

'''
  Implements US12
  Sprint 2
  Alex Rubino
  Mother should be less than 60 years older than her children and father should be less than 80 years older than his children.
'''
def validate_parent_age(fams, indis):
  return_data = []

  for fid in fams:
    if fams[fid]['HUSB'] is not None:
      husband_id = fams[fid]['HUSB']
      husband_birth = indis[husband_id]['BIRT']
      if husband_birth is not None:
        husband_birthday = utils.parse_date(husband_birth)

    if fams[fid]['WIFE'] is not None:
      wife_id = fams[fid]['WIFE']
      wife_birth = indis[wife_id]['BIRT']
      if wife_birth is not None:
        wife_birthday = utils.parse_date(wife_birth)

    for cid in fams[fid]['CHIL']:
      if indis[cid]['BIRT'] is not None:
        child_birthday = utils.parse_date(indis[cid]['BIRT'])

        if husband_birthday is not None:
          husband_age = utils.get_age(husband_birthday, child_birthday)
          if husband_age > 80:
            return_data.append((husband_id, f'Husband id={husband_id} in family id={fid} was born over 80 years before child id={cid}.'))

        if wife_birthday is not None:
          wife_age = utils.get_age(wife_birthday, child_birthday)
          if wife_age > 60:
            return_data.append((wife_id, f'Wife id={wife_id} in family id={fid} was born over 60 years before child id={cid}.'))

  return return_data

'''
  Implements US13
  Sprint 2
  Luke McEvoy & Alex Rubino
  Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)

  Function will reject siblings that have birthdays satisfying both conditions:
  - more than 1 day apart
  - not less than 8 months (248 days) apart
'''
def validate_sibling_births(fams, indis):
  return_data = []
  one_day = timedelta(days=1)
  eight_mons = timedelta(days=248)

  for fid in fams:
    births = []

    # Appends every child's birthday into the array
    for cid in fams[fid]['CHIL']:
      if indis[cid]['BIRT'] is not None:
        births.append((cid, utils.parse_date(indis[cid]['BIRT'])))

    for i in range(len(births)):
      for j in range(i+1, len(births)):
        delta = abs(births[i][1] - births[j][1])

        if one_day < delta <= eight_mons:
          return_data.append((fid, f'Siblings with id={births[i][0]} and id={births[j][0]} in fid={fid} have birth dates more than one day and not less than eight months apart.'))

  return return_data

'''
  Implements US14
  Sprint 2
  Zack Schieberl + Ben Mirtchouk
  A family cannot give birth to sextuplets
  Only return an error if there are more than 5 kids born on two consecutive days
'''
def validate_no_sextuples(fams, indis):
  one_day = timedelta(days=1)

  ret_data = []
  for fid in fams:
    child_births = [indis[cid]['BIRT'] for cid in fams[fid]['CHIL'] if indis[cid]['BIRT'] is not None]
    if len(child_births) <= 5:
      continue

    birth_freq = {}
    for birth in child_births:
      if birth not in birth_freq:
        birth_freq[birth] = 0
      birth_freq[birth] += 1

    dates = sorted(birth_freq.keys())
    parsed_dates = [utils.parse_date(d) for d in dates]
    for i in range(len(dates)):
      count = birth_freq[dates[i]]
      if i + 1 < len(dates) and parsed_dates[i+1] - parsed_dates[i] == one_day:
        count = birth_freq[dates[i]] + birth_freq[dates[i+1]]

      if count > 5:
        ret_data.append((fid, f'Family id={fid} has more than 5 children born together'))
        break

  return ret_data

'''
  Implements US15
  Sprint 2
  Zack Schieberl
  There cannot be more than 14 siblings in one family
'''
def validate_no_excessive_siblings(fams, indis):
  MAX_SIB = 14
  ret_data = []

  for fid in fams:
    if len(fams[fid]['CHIL']) > MAX_SIB:
      ret_data.append((fid, f'Family id={fid} has more than {MAX_SIB} siblings'))

  return ret_data

'''
  Implements US16
  Sprint 2
  Luke McEvoy
  All male members of a family should have the same last name
'''
def validate_all_men_have_same_last_name(fams, indis):
  retData = []
  for fid in fams:
    familyMen = []

    # Add all male children
    for cid in fams[fid]['CHIL']:
      if indis[cid]['SEX'] == 'M':
        lastName = indis[cid]['NAME'].split()[-1]
        familyMen.append(lastName)

    # Add husband
    if fams[fid]['HUSB'] is not None:
      lastName = indis[fams[fid]['HUSB']]['NAME'].split()[-1]
      familyMen.append(lastName)

    if len(set(familyMen)) > 1:
      retData.append((fid, f'Family id={fid} has males with a different last name'))

  return retData

'''
  Implements US17: No marriages to descendants

  A is a descendant of B iff we can reach B from A via a
  series of one or more parent relationships
'''
def validate_no_descendant_marriage(fams, indis):
  ret_data = []

  for fid in fams:
    if fams[fid]['HUSB'] is None or fams[fid]['WIFE'] is None:
      continue
    husb = fams[fid]['HUSB']
    wife = fams[fid]['WIFE']

    for desc, ance in [(husb, wife), (wife, husb)]:
      if utils.is_descendant(desc, ance, fams, indis):
        ret_data.append((fid, f'Family fid={fid} is a marriage of ancestor id={ance} and descendant id={desc}'))
        break

  return ret_data

'''
  Implements US18
  Sprint 3
  Alex Rubino
  Siblings should not marry
'''
def validate_no_sibling_marriage(fams, indis):
  return_data = []

  for fid in fams:
    if fams[fid]['HUSB'] is None or fams[fid]['WIFE'] is None:
      continue
    
    husband = fams[fid]['HUSB']
    wife = fams[fid]['WIFE']

    # for id1, id2 in [(husband, wife), (wife, husband)]:
    #   parents_id1 = set(utils.get_parents(id1, fams, indis))
    #   parents_id2 = set(utils.get_parents(id2, fams, indis))

    for id1, id2 in [(husband, wife)]:
      parents_id1 = set(utils.get_parents(id1, fams, indis))
      parents_id2 = set(utils.get_parents(id2, fams, indis))


      parents_both = parents_id1.union(parents_id2)

      parents_flag = (len(parents_both) == len(parents_id1) + len(parents_id2))

      if (not parents_flag):
        return_data.append((fid, f'Siblings {id1} and {id2} should not marry.'))      

  return return_data

'''
  Implements US19: First cousins should not marry

  - A is a first cousin of B <-> A is a descendant of B's aunt/uncle
                              OR B is a descendant of A's aunt/uncle
  - A is the uncle of B      <-> one of B's parents is a sibling of A
  - A is a sibling of B      <-> A and B CHIL tags appear in the same FAM
'''
def validate_no_cousin_marriage(fams, indis):
  ret_data = []

  for fid in fams:
    if fams[fid]['HUSB'] is None or fams[fid]['WIFE'] is None:
      continue
    husb = fams[fid]['HUSB']
    wife = fams[fid]['WIFE']

    for id1, id2 in [(husb, wife), (wife, husb)]:
      id1_parents = utils.get_parents(id1, fams, indis)
      # this includes aunts as well
      id1_uncles = [iid for pid in id1_parents for iid in utils.get_siblings(pid, fams, indis)]

      if any(utils.is_descendant(id2, uncle, fams, indis) for uncle in id1_uncles):
        ret_data.append((fid, f'Family fid={fid} is a marriage of first cousins id={husb} and id={wife}'))
        break

  return ret_data

'''
  Implements US22
  Sprint 3
  Alex Rubino
  All individual IDs should be unique and all family IDs should be unique
'''
def validate_unique_ids(fams, indis):
  return_data = []
  family_ids = []
  individual_ids = []
  family_flag = 0
  individual_flag = 0

  for fid in fams:
    family_ids.append(fid)

  for iid in indis:
    individual_ids.append(iid)

  family_flag = (len(set(family_ids)) == len(family_ids))
  individual_flag = (len(set(individual_ids)) == len(individual_ids))
  print("--> ", individual_flag, individual_ids, set(individual_ids))

  if (not family_flag):
    return_data.append((fid, f'Family fid={fid} is not unique'))

  if (not individual_flag):
    return_data.append((iid, f'Individual iid={iid} is not unique'))

  print("-->", individual_ids)
  return return_data

'''
  Implements US23
  Sprint 3
  Luke McEvoy
  No more than one individual with the same name and birth date should appear in a GEDCOM file
'''
def validate_different_name_birthday(fams, indis):
  return_data = []

  individual_ids = []
  individual_flag = 0

  for iid in indis:
    name = indis[iid]['NAME']
    birth = indis[iid]['BIRT']
    if (name is not None) and (birth is not None):
      birthday = utils.parse_date(birth)
      individual_ids.append([name, birthday])

  unique_data = [list(x) for x in set(tuple(x) for x in individual_ids)]

  if (not unique_data):
    return_data.append([name, birthday], f'Multiple individuals have the same name and birthday {[name, birthday]}.')

  return return_data

'''
  Implements US24
  Sprint 3
  Luke McEvoy
  No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
'''
def validate_different_marriage(fams, indis):
  return_data = []

  family_ids = []
  
  for fid in fams:
    if fams[fid]['MARR'] is not None:
      marriage_day = utils.parse_date(fams[fid]['MARR'])

      husband_id = fams[fid]['HUSB']
      wife_id = fams[fid]['WIFE']

      husband_name = indis[husband_id]['NAME']
      wife_name = indis[wife_id]['NAME']

      if (husband_name is not None) and (wife_name is not None) and (marriage_day is not None):
        family_ids.append([husband_name, wife_name, marriage_day])

      unique_data = [list(x) for x in set(tuple(x) for x in family_ids)]

      if (not unique_data):
        return_data.append([husband_name, wife_name, marriage_day], f'Multiple families have the same names and marriage days {[husband_name, wife_name, marriage_day]}.')

  return return_data