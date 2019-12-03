# !/usr/bin/env python3
"""This module does blah blah."""
import os
from datetime import timedelta, date
from airtable import Airtable

airtab_intakes = Airtable(
    os.environ['jail_scrapers_db'], 'intakes', os.environ['AIRTABLE_API_KEY'])
airtab_daily = Airtable(
    os.environ['jail_scrapers_db'], 'daily stats', os.environ['AIRTABLE_API_KEY'])

county_jails = [('Madison', 'mcdc'), ('Pearl River', 'prcdf'), ('Lee', 'lcdc'), ('Hinds', 'hcdc'),
                ('Kemper', 'kcdc'), ('Tunica', 'tcdc'), ('Clay', 'ccdc'), ('Adams', 'acdc'), ('Jasper', 'jcj'), 'Jackson', 'jcadc']


def pop_otd(day, county, jail, quiet=True):
    record = airtab_daily.match('date_str', day)
    day_before = date.fromisoformat(day) - timedelta(1)
    day_after = date.fromisoformat(day) + timedelta(1)
    pop_formula = f"AND(IS_BEFORE(DOI, '{day_after}'), IS_AFTER(last_verified, '{day_before}'), jail='{jail}')"
    records = airtab_intakes.get_all(fields='jail', formula=pop_formula)
    this_dict = {f"{county} pop": len(records)}
    airtab_daily.update(record['id'], this_dict)
    if not quiet:
        print(this_dict)


def admits_otd(day, county, jail, quiet=True):
    record = airtab_daily.match('date_str', day)
    admits_formula = f"AND(DATETIME_FORMAT(DOI, 'YYYY-MM-DD')='{day}', jail='{jail}')"
    records = airtab_intakes.get_all(fields='jail', formula=admits_formula)
    this_dict = {f"{county} admits": len(records)}
    airtab_daily.update(record['id'], this_dict)
    if not quiet:
        print(this_dict)


def main():
    day = (date.today() - timedelta(1)).isoformat()
    for tup in county_jails:
        county, jail = tup
        admits_otd(day, county, jail, quiet=False)
        pop_otd(day, county, jail, quiet=False)


if __name__ == "__main__":
    main()
