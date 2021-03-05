import utils as utils

'''
  US04:     Marriage Before Death
  Author:   Luke McEvoy
  Sprint:   1 (3/8/21)
  
  Story Description:
    Marriage should occur before death of either spouse
  
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

def divorce_before_death(fams, indis):
  invalid_marriages = []

  for familyID in fams:
    if fams[familyID]['MARR'] is not None:
      marriage = utils.parse_date(fams[familyID]['MARR'])

      husbandID, wifeID = fams[familyID]['HUSB'], fams[familyID]['WIFE']
      husbandDeath, wifeDeath = indis[husbandID]['DEAT'], indis[wifeID]['DEAT']

      # revise this logic for Project 04
      if husbandDeath is not None:
        husbandDeath = utils.parse_date(husbandDeath)

      # revise this logic for Project 04
      if wifeDeath is not None:
        wifeDeath = utils.parse_date(wifeDeath)

      # revise this logic for Project 04
      if (wifeDeath or husbandDeath is not None):
        if wifeDeath is not None:
          tmp = wifeDeath
        if husbandDeath is not None:
          tmp = husbandDeath
        if tmp < marriage:
          invalid_marriages.append((familyID, f'Family id={familyID} has marriage after death of partner'))
  
  return invalid_marriages


'''
  US05:     Marriage Before Death
  Author:   Luke McEvoy
  Sprint:   1 (3/8/21)
  
  Story Description:
    Marriage should occur before death of either spouse
  
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

def marriage_before_death(fams, indis):
  invalid_marriages = []

  for familyID in fams:
    if fams[familyID]['MARR'] is not None:
      marriage = utils.parse_date(fams[familyID]['MARR'])

      husbandID, wifeID = fams[familyID]['HUSB'], fams[familyID]['WIFE']
      husbandDeath, wifeDeath = indis[husbandID]['DEAT'], indis[wifeID]['DEAT']

      # revise this logic for Project 04
      if husbandDeath is not None:
        husbandDeath = utils.parse_date(husbandDeath)

      # revise this logic for Project 04
      if wifeDeath is not None:
        wifeDeath = utils.parse_date(wifeDeath)

      # revise this logic for Project 04
      if (wifeDeath or husbandDeath is not None):
        if wifeDeath is not None:
          tmp = wifeDeath
        if husbandDeath is not None:
          tmp = husbandDeath
        if tmp < marriage:
          invalid_marriages.append((familyID, f'Family id={familyID} has marriage after death of partner'))
  
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

'''
    for cid in indis:
        # check if birthed
        if indis[cid]['BIRT'] is not None:
            # marriage date of form '%Y-%m-%d'
            birthday = utils.parse_date(indis[cid]['BIRT'])

            for fid in fams:
                if fams[fid]['MARR'] is not None:
                    marriage_day = utils.parse_date(fams[fid]['MARR'])

                    # L:    2005
                    # R:    2008
                    # Marr: 2015
                    # 16 (13) 
                    if marriage_day < (birthday + 14):
                        continue

            # get IDs of husband + wife through indis
'''
