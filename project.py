import argparse
import os
import logging
import sys
from prettytable import PrettyTable
import validation
import utils

logging.getLogger().setLevel(logging.INFO)
LOG_FORMAT = "%(levelname)s: %(message)s"
logging.basicConfig(stream=sys.stdout, level='DEBUG', format=LOG_FORMAT)

SUPPORTED_TAGS = {
  'comment': ['NOTE', 'HEAD', 'TRLR'],
  '0': ['INDI', 'FAM'],
  '1': ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS',
        'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'],
  '2': ['DATE']
}

DATE_TAGS = ['BIRT', 'DEAT', 'MARR', 'DIV']

INDI_PARAMS = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
FAM_PARAMS =  ['HUSB', 'WIFE', 'CHIL', 'MARR', 'DIV']

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
MONTH_NUM = {month : str(i+1).zfill(2) for i, month in enumerate(MONTHS)}

class GEDNode:
  # TODO: validate args based on tag
  def __init__(self, level, tag, args):
    self.level = level
    self.tag = tag
    self.args = args
    self.children = []

  def prnt(self, level=0):
    args = ','.join(self.args)
    ls = '\t' * level
    logging.debug('%s{ %d.%s[%s] }', ls, self.level, self.tag, args)
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

    if self.tag == 'NAME':
      return ' '.join(self.args).replace('/','')

    if self.needs_date_arg():
      for c in self.children:
        if c.tag == 'DATE':
          d = c.get_arg()
          if d is not None:
            return d
      return None

    if len(self.args) == 0:
      logging.error('%s node has 0 arguments where 1 was expected', self.tag)
      return None
    if len(self.args) > 1:
      logging.warning('%s node has %d arguments where 1 was expected', self.tag, len(self.args))
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
    if not line:
      continue
    data = line.split()

    if len(data) < 2:
      logging.warning('invalid data \'%s\'', line)
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
      logging.warning('invalid data \'%s\'', line)
    elif not valid:
      logging.warning('invalid tag \'%s\'', line)
    else:
      nodes.append(GEDNode(int(level), tag, args))

  stk = []
  root_nodes = []
  for nd in nodes:
    while len(stk) > 0 and stk[-1].level >= nd.level:
      stk.pop()

    if len(stk) > 0:
      if stk[-1].level != nd.level - 1:
        logging.warning('level %d line follows level %d level line', nd.level, stk[-1].level)
      stk[-1].add_child(nd)
    else:
      root_nodes.append(nd)

    stk.append(nd)

  return root_nodes

def get_indis_raw(root_nodes):
  indis = {}
  for root in root_nodes:
    if root.tag == 'INDI':
      indi_id = root.get_arg()
      indi_data = { param: None for param in INDI_PARAMS }
      indi_data['FAMS'] = []

      for nd in root.children:
        if nd.tag not in INDI_PARAMS:
          continue
        if nd.tag == 'FAMS':
          indi_data[nd.tag].append(nd.get_arg())
        else:
          indi_data[nd.tag] = nd.get_arg()

      indis[indi_id] = indi_data
  return indis

def get_fams_raw(root_nodes):
  fams = {}
  for root in root_nodes:
    if root.tag == 'FAM':
      fam_id = root.get_arg()
      fam_data = { param: None for param in FAM_PARAMS }
      fam_data['CHIL'] = []

      for nd in root.children:
        if nd.tag not in FAM_PARAMS:
          continue
        if nd.tag == 'CHIL':
          fam_data[nd.tag].append(nd.args[0])
        else:
          fam_data[nd.tag] = nd.get_arg()

      fams[fam_id] = fam_data
  return fams


def get_indis(root_nodes):
  indis = {}
  for root in root_nodes:
    if root.tag == 'INDI':
      indi_id = root.get_arg()
      if indi_id in indis:
        logging.error('duplicate INDI id %s', indi_id)
        continue

      indi_data = { param: None for param in INDI_PARAMS }
      indi_data['FAMS'] = []

      for nd in root.children:
        if nd.tag not in INDI_PARAMS:
          continue
        if nd.tag == 'FAMS':
          indi_data[nd.tag].append(nd.get_arg())
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
        logging.error('duplicate FAM id %s', fam_id)
        continue

      fam_data = { param: None for param in FAM_PARAMS }
      fam_data['CHIL'] = []

      for nd in root.children:
        if nd.tag not in FAM_PARAMS:
          continue
        if nd.tag == 'CHIL':
          fam_data[nd.tag].append(nd.args[0])
        else:
          fam_data[nd.tag] = nd.get_arg()

      fams[fam_id] = fam_data
  return fams

def parse_ged_data_raw(lines):
  root_nodes = build_ged_tree(lines)
  fams = get_fams_raw(root_nodes)
  indis = get_indis_raw(root_nodes)
  return fams, indis

def parse_ged_data(lines):
  root_nodes = build_ged_tree(lines)
  fams = get_fams(root_nodes)
  indis = get_indis(root_nodes)
  return fams, indis

def print_tables(fams, indis):
  fam_table = PrettyTable()
  fam_table.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name',
                           'Wife ID', 'Wife Name', 'Children']
  for fam_id in sorted(fams.keys()):
    fam_data = fams[fam_id]
    fam_table.add_row([fam_id, fam_data['MARR'] or 'NA', fam_data['DIV'] or 'NA',
                       fam_data['HUSB'] or 'NA', indis[fam_data['HUSB']]['NAME'] or 'NA' if fam_data['HUSB'] else 'NA',
                       fam_data['WIFE'] or 'NA', indis[fam_data['WIFE']]['NAME'] or 'NA' if fam_data['WIFE'] else 'NA',
                       utils.format_list(fam_data['CHIL']) if len(fam_data['CHIL']) > 0 else 'NA' ])

  indi_table = PrettyTable()
  indi_table.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age',
                            'Alive', 'Death', 'Child', 'Spouse']
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
                        utils.format_list(children) if len(children) > 0 else 'NA', spouse or 'NA'])

  print(indi_table)
  print(fam_table)

def run_validation(valid_f, log, vtype, US, fams, indis):
  for oid, reason in valid_f(fams, indis):
    log('%s: %s: %s: %s', vtype, US, oid, reason)

def main():
  parser = argparse.ArgumentParser(description='Parse a GED file to extract \
                                                individuals and families.')
  parser.add_argument('file', type=str, help='the GED file')

  args = parser.parse_args()

  if not os.path.isfile(args.file):
    logging.critical('missing file %s in cwd', args.file)
    exit(1)

  with open(args.file) as f:
    lines = f.readlines()

  fams, indis = parse_ged_data(lines)
  print_tables(fams, indis)

  run_validation(validation.validate_dates_before_current,        logging.error,   'DATE',       'US01', fams, indis)
  run_validation(validation.validate_birth_before_marriage,       logging.error,   'INDIVIDUAL', 'US02', fams, indis)
  run_validation(validation.validate_birth_before_death,          logging.error,   'INDIVIDUAL', 'US03', fams, indis)
  run_validation(validation.validate_marriage_before_divorce,     logging.error,   'FAMILY',     'US04', fams, indis)
  run_validation(validation.validate_marriage_before_death,       logging.error,   'FAMILY',     'US05', fams, indis)
  run_validation(validation.validate_divorce_before_death,        logging.error,   'FAMILY',     'US06', fams, indis)
  run_validation(validation.validate_reasonable_age,              logging.warning, 'INDIVIDUAL', 'US07', fams, indis)
  run_validation(validation.validate_marriage_before_child,       logging.warning, 'FAMILY',     'US08', fams, indis)
  run_validation(validation.validate_birth_before_parent_death,   logging.error,   'INDIVIDUAL', 'US09', fams, indis)
  run_validation(validation.validate_marriage_after_fourteen,     logging.warning, 'FAMILY',     'US10', fams, indis)
  run_validation(validation.validate_no_bigamy,                   logging.warning, 'FAMILY',     'US11', fams, indis)
  run_validation(validation.validate_parent_age,                  logging.warning, 'INDIVIDUAL', 'US12', fams, indis)
  run_validation(validation.validate_sibling_births,              logging.warning, 'FAMILY',     'US13', fams, indis)
  run_validation(validation.validate_no_sextuples,                logging.warning, 'FAMILY',     'US14', fams, indis)
  run_validation(validation.validate_no_excessive_siblings,       logging.warning, 'FAMILY',     'US15', fams, indis)
  run_validation(validation.validate_all_men_have_same_last_name, logging.warning, 'FAMILY',     'US16', fams, indis)

if __name__ == '__main__':
  main()
