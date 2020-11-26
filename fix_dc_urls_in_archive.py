#!/usr/bin/env python
import sys
import time
from common import airtab_archive_intakes as airtab
from common import dc

def update_dc_fields(how_many, nap):
    records = airtab.get_all(view='need dc urls updated', fields='dc_id', max_records=how_many)
    print(len(records), ' archived records need updated documentcloud URLs.')
    for record in records:
        this_dict = {}
        dc_id = record['fields'].get('dc_id')
        obj = dc.documents.get(dc_id)
        this_dict["PDF"] = obj.pdf_url
        this_dict["dc_canonical_url"] = obj.canonical_url
        this_dict["dc_resources_page_image"] = obj.normal_image_url
        airtab.update(record['id'], this_dict)
        time.sleep(nap)

def main():
    how_many = int(sys.argv[1])
    nap = int(sys.argv[2]) / 10
    update_dc_fields(how_many, nap)


if __name__ == "__main__":
    main()
