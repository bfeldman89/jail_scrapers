#!/usr/bin/env python
"""This module does blah blah."""
import os
import time

from airtable import Airtable

from common import airtab_intakes, airtab_archive_intakes, county_jails


airtab_weekly = Airtable(os.environ['jail_scrapers_db'],
                         table_name='weekly_stats',
                         api_key=os.environ['AIRTABLE_API_KEY'])


def get_weeks():
    this_list = []
    records = airtab_weekly.get_all(view='to-do', fields=['WOI', 'week_of'])
    for record in records:
        this_list.append(record['fields']['WOI'])
    return this_list


def admits_otw(week, county, jail):
    record = airtab_weekly.match('WOI', week)
    admits_formula = f"AND(WOI='{week}', jail='{jail}')"
    records = airtab_intakes.get_all(fields='jail', formula=admits_formula)
    other_records = airtab_archive_intakes.get_all(fields='jail', formula=admits_formula)
    this_dict = {f"{county} total admits": len(records) + len(other_records)}
    airtab_weekly.update(record['id'], this_dict)
    # print(this_dict, f"active, {len(records)}; archive, {len(other_records)}")
    print(week, ' --> ', this_dict, f"active, {len(records)}; archive, {len(other_records)}")


def weekly(this_week):
    for tup in county_jails:
        county, jail = tup
        admits_otw(this_week, county, jail,)


def main():
    WOIs = get_weeks()
    for this_week in WOIs:
        print(f'getting avg. admits for {this_week} ... ')
        weekly(this_week)
        time.sleep(.3)


if __name__ == "__main__":
    main()
