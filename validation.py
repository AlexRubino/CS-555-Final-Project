import utils as utils

'''
  Input:
    fams
      dictionary of families with 
      key   ->  fam id
      value ->  object {  'ID': _, 
                          'HUSB': _, 
                          'WIFE': _, 
                          'CHIL': [_], 
                          'MARR': _, 
                          'DIV': _  }
    indis
      dictionary of individuals with 
      key   ->  indiv id
      value ->  object {  'ID': _,
                          'NAME': _,
                          'SEX': _, 
                          'BIRT': _, 
                          'DEAT': _, 
                          'FAMC': [_],
                          'FAMS': [_] }

  Output:
    [(fam1, err1), (fam2, err2)]

    fam_  ->  id of invalid family
    err_  ->  error message
'''


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
    # if married
    if fams[fid]['MARR'] is not None:

      # parse marriage and divorce date of husband and wife
      marriage_date = utils.parse_date(fams[fid]['MARR'])
      divorce_date = utils.parse_date(fams[fid]['DIV'])
      print(marriage_date, "divorce: ", divorce_date, type(marriage_date), type(divorce_date))

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

            husband_birth = utils.parse_date(husband_birth)
            wife_birth = utils.parse_date(wife_birth)
            
            # both partners are born
            if (husband_birth and wife_birth is not None):
              # if husband + wife were 14 and above when married
              husband_marriage_age = utils.get_age(husband_birth, marriage_date)
              wife_marriage_age = utils.get_age(wife_birth, marriage_date)

              if (husband_marriage_age < 14) or (wife_marriage_age < 14):
                    invalid_marriages.append((fid, f'Family id={fid} has marriage before age 14'))

    return invalid_marriages

