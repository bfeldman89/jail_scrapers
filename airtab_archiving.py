#!/usr/bin/env python
import os
import time

from airtable import Airtable

airtab_active = Airtable(os.environ['jail_scrapers_db'], 'intakes', os.environ['AIRTABLE_API_KEY'])
airtab_archive = Airtable(os.environ['jails_archive_db'], 'intakes', os.environ['AIRTABLE_API_KEY'])


def archive_intakes():
    # the airtable view, 'to be archived', filters intakes to only include those
    # where the `days_since_verification` field > 60. I have no idea why I'm too
    # paranoid to add a function to delete the record from the active base once the
    # record has been successfully added to the archive base, but I am. So I do that
    # manually after manually verifying that the archived record is actual and complete.
    records = airtab_active.get_all(view='to be archived')
    len(records)
    for record in records:
        this_dict = {}
        this_dict['old_record_id'] = record['id']
        # this_dict['_charge_1_statute'] = record['fields'].get('_charge_1_statute')
        # this_dict['_courts'] = record['fields'].get('_courts')
        # this_dict['_jail'] = record['fields'].get('_jail')
        # this_dict['_charges'] = record['fields'].get('_charges')
        # this_dict['_LEA'] = record['fields'].get('_LEA')
        this_dict['issue(s)'] = record['fields'].get('issue(s)')
        this_dict['what_changed'] = record['fields'].get('what_changed')
        this_dict['updated'] = record['fields'].get('updated')
        this_dict['intake_bond_written'] = record['fields'].get('intake_bond_written')
        this_dict['intake_bond_cash'] = record['fields'].get('intake_bond_cash')
        this_dict['intake_fine_ammount'] = record['fields'].get('intake_fine_ammount')
        this_dict['html'] = record['fields'].get('html')
        this_dict['recent_text'] = record['fields'].get('recent_text')
        this_dict['dc_full_text'] = record['fields'].get('dc_full_text')
        this_dict['charge_classifications'] = record['fields'].get('charge_classifications')
        this_dict['summary'] = record['fields'].get('summary')
        this_dict['bond_ammounts'] = record['fields'].get('bond_ammounts')
        this_dict['fine_ammounts'] = record['fields'].get('fine_ammounts')
        this_dict['NOTES'] = record['fields'].get('NOTES')
        this_dict['diff'] = record['fields'].get('diff')
        this_dict['TEST_RESULT'] = record['fields'].get('TEST_RESULT')
        this_dict['jail'] = record['fields'].get('jail')
        this_dict['dc_access'] = record['fields'].get('dc_access')
        this_dict['sex'] = record['fields'].get('sex')
        this_dict['race'] = record['fields'].get('race')
        this_dict['glasses'] = record['fields'].get('glasses')
        this_dict['charge_1_statute'] = record['fields'].get('charge_1_statute')
        this_dict['intake_number'] = record['fields'].get('intake_number')
        this_dict['bk'] = record['fields'].get('bk')
        this_dict['intake_case_number'] = record['fields'].get('intake_case_number')
        this_dict['dc_id'] = record['fields'].get('dc_id')
        this_dict['dc_title'] = record['fields'].get('dc_title')
        this_dict['first_name'] = record['fields'].get('first_name')
        this_dict['last_name'] = record['fields'].get('last_name')
        this_dict['middle_name'] = record['fields'].get('middle_name')
        this_dict['suffix'] = record['fields'].get('suffix')
        this_dict['nickname'] = record['fields'].get('nickname')
        this_dict['intake_hair'] = record['fields'].get('intake_hair')
        this_dict['intake_eye'] = record['fields'].get('intake_eye')
        this_dict['intake_compl'] = record['fields'].get('intake_compl')
        this_dict['intake_height'] = record['fields'].get('intake_height')
        this_dict['intake_weight'] = record['fields'].get('intake_weight')
        this_dict['intake_address_line_1'] = record['fields'].get('intake_address_line_1')
        this_dict['intake_address_line_2'] = record['fields'].get('intake_address_line_2')
        this_dict['intake_pin'] = record['fields'].get('intake_pin')
        this_dict['intake_cell'] = record['fields'].get('intake_cell')
        this_dict['intake_section'] = record['fields'].get('intake_section')
        this_dict['intake_location'] = record['fields'].get('intake_location')
        this_dict['intake_pod'] = record['fields'].get('intake_pod')
        this_dict['charge_1'] = record['fields'].get('charge_1')
        this_dict['charge_1_title'] = record['fields'].get('charge_1_title')
        this_dict['charges'] = record['fields'].get('charges')
        this_dict['LEA'] = record['fields'].get('LEA')
        this_dict['courts'] = record['fields'].get('courts')
        this_dict['dc_pages'] = record['fields'].get('dc_pages')
        this_dict['intake_age'] = record['fields'].get('intake_age')
        this_dict['initial_scrape'] = record['fields'].get('initial_scrape')
        this_dict['DOI'] = record['fields'].get('DOI')
        this_dict['DOA'] = record['fields'].get('DOA')
        this_dict['DOO'] = record['fields'].get('DOO')
        this_dict['DOR'] = record['fields'].get('DOR')
        this_dict['SDOR'] = record['fields'].get('SDOR')
        this_dict['last_verified'] = record['fields'].get('last_verified')
        this_dict['DOB'] = record['fields'].get('DOB')
        try:
            this_dict['PIXELATED_IMG'] = [{"url": record['fields']['PIXELATED_IMG'][0]['url']}]
        except KeyError:
            print('no pixelated image')
        try:
            this_dict['PHOTO'] = [{"url": record['fields']['PHOTO'][0]['url']}]
        except KeyError:
            print('no image')
        try:
            this_dict['updated_pdf'] = [{"url": record['fields']['updated_pdf'][0]['url']}]
        except KeyError:
            print('no updated pdf')
        match = airtab_archive.match('old_record_id', record['id'])
        if match:
            print(f"this record, {record['id']}, was already archived... hmmmm...")
            airtab_archive.update(match['id'], this_dict)
        else:
            print('just archived record ', record['id'])
            airtab_archive.insert(this_dict)
        time.sleep(.3)


def main():
    archive_intakes()


if __name__ == "__main__":
    main()
