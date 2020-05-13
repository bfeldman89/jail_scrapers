#!/usr/bin/env python
"""This module does blah blah."""
from datetime import date, datetime, timedelta

from common import airtab_daily, airtab_intakes, county_jails


def pop_otd(day, county, jail, quiet=True):
    record = airtab_daily.match('date_str', day)
    day_before = datetime.strptime(day, '%Y-%m-%d') - timedelta(1)
    day_after = datetime.strptime(day, '%Y-%m-%d') + timedelta(1)
    pop_formula = f"AND(IS_BEFORE(DOI, '{day_after.date()}'), IS_AFTER(last_verified, '{day_before.date()}'), jail='{jail}')"
    records = airtab_intakes.get_all(fields='jail', formula=pop_formula)
    # other_records = airtab_archive_intakes.get_all(fields='jail', formula=pop_formula)
    # this_dict = {f"{county} pop": len(records) + len(other_records)}
    this_dict = {f"{county} pop": len(records)}
    airtab_daily.update(record['id'], this_dict)
    if not quiet:
        # print(this_dict, f"active, {len(records)}; archive, {len(other_records)}")
        print(this_dict)


def admits_otd(day, county, jail, quiet=True):
    record = airtab_daily.match('date_str', day)
    admits_formula = f"AND(DATETIME_FORMAT(DOI, 'YYYY-MM-DD')='{day}', jail='{jail}')"
    records = airtab_intakes.get_all(fields='jail', formula=admits_formula)
    # other_records = airtab_archive_intakes.get_all(fields='jail', formula=admits_formula)
    # this_dict = {f"{county} admits": len(records) + len(other_records)}
    this_dict = {f"{county} admits": len(records)}
    airtab_daily.update(record['id'], this_dict)
    if not quiet:
        # print(this_dict, f"active, {len(records)}; archive, {len(other_records)}")
        print(this_dict)


def main():
    day = (date.today() - timedelta(1)).isoformat()
    for tup in county_jails:
        county, jail = tup
        admits_otd(day, county, jail, quiet=False)
        pop_otd(day, county, jail, quiet=False)


if __name__ == "__main__":
    main()
