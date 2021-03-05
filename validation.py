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