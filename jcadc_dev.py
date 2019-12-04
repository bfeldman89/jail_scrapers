# !/usr/bin/env python3
"""This module does blah blah."""
import os
import re
import time
from airtable import Airtable

airtab = Airtable(os.environ['jail_scrapers_db'], 'intakes',
                  os.environ['AIRTABLE_API_KEY'])


def get_all_intake_deets(record):
    charges = []
    bond_ammts = []
    classifications = []
    this_dict = {}
    txt_str = record['fields']['recent_text']
    chunks = txt_str.split('\nRequest Victim Notification\n')
    match_1 = re.search(r"(\w+)\s+(Male|Female)", chunks[0])
    this_dict['race'] = match_1.group(1)[0]
    this_dict['sex'] = match_1.group(2)[0]
    try:
        this_dict['intake_weight'] = re.search(r"(\d+) Pounds", chunks[0]).group(1)
    except AttributeError:
        print('there isnt weight info')
    try:
        this_dict['intake_height'] = re.search(r"(\d Ft. \d+ In.)", chunks[0]).group(1)
    except AttributeError:
        print('idk how tall this person is')
    try:
        this_dict['intake_eye'] = re.search(r"(\w+)\s+Eyes", chunks[0]).group(1)
    except AttributeError:
        print('eye color is a mystery')
    this_dict['intake_age'] = re.search(r"(\d\d) Years Old", chunks[0]).group(1)
    crim_details = chunks[1].splitlines()
    for ln in crim_details:
        results = re.search(r"([MF]\w+) - Bond: (\$.*)", ln)
        if results:
            bond_ammts.append(results.group(2))
            classifications.append(results.group(1))
        elif ', ' in ln:
            charges.append(f"\"{ln}\"")
        else:
            charges.append(ln)
    this_dict['charges'] = ', '.join(charges)
    this_dict['bond_ammounts'] = '\n'.join(bond_ammts)
    this_dict['charge_classifications'] = ', '.join(classifications)
    airtab.update(record['id'], this_dict, typecast=True)
    time.sleep(.7)


def main():
    records = airtab.get_all(view='jcadc', fields='recent_text')
    print(len(records))
    for record in records:
        get_all_intake_deets(record)
        # regex_7 = r"(NJCADC\d+)\n(.*)\nRequest Victim Notification"


if __name__ == '__main__':
    main()
