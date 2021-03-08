import os
from prettytable import PrettyTable
import argparse
from datetime import datetime
import logging
import validation as validation
import utils as utils
import sys

logging.getLogger().setLevel(logging.INFO)
log_format = "%(levelname)s: %(message)s"
logging.basicConfig(stream=sys.stdout, level='DEBUG', format=log_format)

SUPPORTED_TAGS = {
  'comment': ['NOTE', 'HEAD', 'TRLR'],
  '0': ['INDI', 'FAM'],
  '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 
        'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'NAME'],
  '2': ['DATE']
}

DATE_TAGS = ['BIRT', 'DEAT', 'MARR', 'DIV']

INDI_PARAMS = ['ID', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
FAM_PARAMS =  ['ID', 'HUSB', 'WIFE', 'CHIL', 'MARR', 'DIV']

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
MONTH_NUM = {month : str(i+1).zfill(2) for i, month in enumerate(MONTHS)}

class GED_Node:
  # TODO: validate args based on tag
  def __init__(self, level, tag, args):
    self.level = level
    self.tag = tag
    self.args = args
    self.children = []

  def prnt(self, level=0):
    args = ','.join(self.args)
    ls = '\t' * level
    logging.debug(f'{ls}{{ {self.level}.{self.tag}[{args}] }}')
    for c in self.children:
      c.prnt(level+1)

  def add_child(self, nd):
    self.children.append(nd)  

  def needs_date_arg(self):
    return self.tag in DATE_TAGS

  def get_arg(self):
    if self.tag == 'DATE':
      if len(self.args) != 3:
        print(f'Error: DATE node has {len(self.args)} != 3 arguments')
        return None
      return self.args[2].zfill(4) + '-' + MONTH_NUM[self.args[1]] + '-' + self.args[0].zfill(2)
    elif self.tag == 'NAME':
      return ' '.join(self.args).replace('/','')
    elif self.needs_date_arg():
      for c in self.children:
        if c.tag == 'DATE':
          d = c.get_arg()        
          if d is not None:
            return d
      return None
    else:
      if len(self.args) == 0:
        logging.error(f'{self.type} node has 0 arguments where 1 was expected')
        return None
      if len(self.args) > 1:
        logging.warning(f'{self.type} node has {len(self.args)} arguments where 1 was expected')
      return self.args[0]

'''
Important assumption: "HEAD", "TRLR", and "NOTE" are not
allowed to be individual nor family IDs. This is because
it would create ambiguity in how to interpret:
0 NOTE INDI
Which could be
  1. An individual with ID = "NOTE"
  2. A note with comment = "INDI"
We assume the latter (2) is the intention.
'''

def build_ged_tree(lines):
  nodes = []
  for line in lines:
    line = line.strip()
    data = line.split()

    if len(data) < 2:
      logging.warning(f'invalid data \'{line}\'')
      continue

    level = data[0]
    tag = None
    valid = False
    args = None

    if level == '0':
      if data[1] in SUPPORTED_TAGS['comment']:
        tag = data[1]
        valid = True
        args = data[2:]
      elif len(data) == 3 and data[2] in SUPPORTED_TAGS[level]:
        tag = data[2]
        valid = True
        args = [data[1]]
    else:
      tag = data[1]
      if data[1] in SUPPORTED_TAGS[level]:
        valid = True
      args = data[2:]

    if tag is None or args is None:
      logging.warning(f'invalid data \'{line}\'')
    elif not valid:
      logging.warning(f'invalid tag \'{line}\'')
    else:
      nodes.append(GED_Node(int(level), tag, args))

  stk = []
  root_nodes = []
  for nd in nodes:
    while len(stk) > 0 and stk[-1].level >= nd.level:
      stk.pop()

    if len(stk) > 0:
      if stk[-1].level != nd.level - 1:
        logging.warning(f'level {nd.level} line follows level {stk[-1].level} level line')
      stk[-1].add_child(nd)
    else:
      root_nodes.append(nd)

    stk.append(nd)

  return root_nodes

def get_indis(root_nodes):
  indis = {}
  for root in root_nodes:
    if root.tag == 'INDI':
      indi_id = root.get_arg()
      if indi_id in indis:
        logging.error(f'duplicate INDI id {indi_id}')
        continue

      indi_data = { param: None for param in INDI_PARAMS }
      indi_data['FAMS'] = []
      indi_data['FAMC'] = []

      for nd in root.children:
        if nd.tag not in INDI_PARAMS:
          continue
        if nd.tag == 'FAMS' or nd.tag == 'FAMC':
          indi_data[nd.tag].append(nd.args[0])
        else:
          indi_data[nd.tag] = nd.get_arg()

      indis[indi_id] = indi_data
  return indis

def get_fams(root_nodes):
  fams = {}
  for root in root_nodes:
    if root.tag == 'FAM':
      fam_id = root.get_arg()
      if fam_id in fams:
        logging.error(f'duplicate FAM id {fam_id}')
        continue

      fam_data = { param: None for param in FAM_PARAMS }
      fam_data['CHIL'] = []
      fam_data['ID'] = root.args[0]

      for nd in root.children:
        if nd.tag not in FAM_PARAMS:
          continue
        if nd.tag == 'CHIL':
          fam_data[nd.tag].append(nd.args[0])
        else:
          fam_data[nd.tag] = nd.get_arg()

      fams[fam_id] = fam_data
  return fams

def parse_ged_data(lines):
  root_nodes = build_ged_tree(lines)
  fams = get_fams(root_nodes)
  indis = get_indis(root_nodes)
  return fams, indis

def parse_ged_data(lines):
  root_nodes = build_ged_tree(lines)
  fams = get_fams(root_nodes)
  indis = get_indis(root_nodes)
  return fams, indis

def print_tables(fams, indis):
  fam_table = PrettyTable()
  fam_table.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
  for fam_id in sorted(fams.keys()):
    fam_data = fams[fam_id]
    fam_table.add_row([fam_id, fam_data['MARR'] or 'NA', fam_data['DIV'] or 'NA', 
                       fam_data['HUSB'] or 'NA', indis[fam_data['HUSB']]['NAME'] or 'NA', 
                       fam_data['WIFE'] or 'NA', indis[fam_data['WIFE']]['NAME'] or 'NA',
                       fam_data['CHIL'] if len(fam_data['CHIL']) > 0 else 'NA' ])

  indi_table = PrettyTable()
  indi_table.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
  for indi_id in sorted(indis.keys()):
    indi_data = indis[indi_id]

    children = []
    spouse = None
    for fam_id in indi_data['FAMS']:
      children += fams[fam_id]['CHIL'] 
      if fams[fam_id]['DIV'] is None:
        if indi_data['SEX'] == 'M':
          spouse = fams[fam_id]['WIFE'] 
        else:
          spouse = fams[fam_id]['HUSB'] 

    age = None
    if indi_data['BIRT'] is not None:
      birthday = utils.parse_date(indi_data['BIRT'])
      age = utils.get_age(birthday)
      if age < 0:
        age = None
    alive = indi_data['DEAT'] is None
    indi_table.add_row([indi_id, indi_data['NAME'] or 'NA', indi_data['SEX'] or 'NA', 
                        indi_data['BIRT'] or 'NA', age or 'NA', alive, indi_data['DEAT'] or 'NA', 
                        children if len(children) > 0 else 'NA', spouse or 'NA'])

  print(indi_table)
  print(fam_table)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Parse a GED file to extract individuals and families.')
  parser.add_argument('file', type=str, help='the GED file')

  args = parser.parse_args()

  if not os.path.isfile(args.file):
    logging.critical(f'missing file {args.file} in cwd')
    exit(1)

  with open(args.file) as f:
    lines = f.readlines()

  fams, indis = parse_ged_data(lines)
  print_tables(fams, indis)

  for is_indi, id, reason in validation.validate_dates_before_current(fams, indis):
    logging.error(f'{"INDIVIDUAL" if is_indi else "FAMILY"}: US01: {id}: {reason}')
  for iid, reason in validation.validate_birth_before_marriage(fams, indis):
    logging.error(f'INDIVIDUAL: US02: {iid}: {reason}')
  for iid, reason in validation.validate_birth_before_death(fams, indis):
    logging.error(f'INDIVIDUAL: US03: {iid}: {reason}')
  for fid, reason in validation.validate_marriage_before_divorce(fams, indis):
    logging.error(f'FAMILY: US04: {fid}: {reason}')
  for fid, reason in validation.validate_marriage_before_death(fams, indis):
    logging.error(f'FAMILY: US05: {fid}: {reason}')
  for fid, reason in validation.validate_divorce_before_death(fams, indis):
    logging.error(f'FAMILY: US06: {fid}: {reason}')
  for iid, reason in validation.validate_reasonable_age(fams, indis):
    logging.warning(f'INDIVIDUAL: US07: {iid}: {reason}')
  for fid, reason in validation.validate_marriage_before_child(fams, indis):
    logging.warning(f'FAMILY: US08: {fid}: {reason}')
