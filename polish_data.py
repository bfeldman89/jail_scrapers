#!/usr/bin/env python
"""This module accesses several airtable 'views' that contain records that need some additional processing."""
import re
import time

import requests

from bs4 import BeautifulSoup
from cloudinary import uploader

from common import airtab_intakes as airtab
from common import cloudinary, dc, wrap_from_module

wrap_it_up = wrap_from_module('jail_scrapers/polish_data.py')


def polish_data():
    """This function does runs each of the module's functions."""
    get_pixelated_mug()
    update_summary()
    get_charges_from_recent_text()
    retry_getting_mugshot()
    remove_weird_character()
    parse_charge_1()
    fix_charges_to_by_lines()
    get_full_text()
    get_all_intake_deets()
    update_dc_fields()


def get_pixelated_mug():
    """This function uploads the raw image to cloudinary and
    then uploads the pixelated version to the airtable record."""
    t0, i = time.time(), 0
    needs_pix_img_formula = "AND(PHOTO != '', PIXELATED_IMG = '', hours_since_verification < 24, jail != 'jcdc')"
    records = airtab.get_all(formula=needs_pix_img_formula)
    for record in records:
        this_dict = {}
        url = record["fields"]["PHOTO"][0]["url"]
        r = requests.get(url)
        content_type = r.headers['Content-Type']
        # print(content_type)
        if content_type == 'image/jpeg':
            try:
                upload_response = uploader.upload(url, opacity=40, effect="blur:400")
                time.sleep(1)
                this_dict["PIXELATED_IMG"] = [{"url": upload_response['secure_url']}]
                airtab.update(record['id'], this_dict)
            except cloudinary.exceptions.Error as err1:
                print("cloudinary can't accept that shit: ", err1)
            except AttributeError as err2:
                print('Attribute Error for cloudinary upload: ', err2)
        else:
            print('this shit was some really weird content type:', content_type)
    wrap_it_up(t0, new=i, total=len(records), function='get_pixelated_mug')


def update_summary(this_many=150):
    """This function updates the record summary. The reason we have this field,
    rather than just use the 'blurb' field, is bc the gallery view works better
    with a text field than it does with a formula field. Because this view will
    regularly be packed full of records, the default max records is 100."""
    t0, i = time.time(), 0
    # outdated_summary_formula = "AND(blurb != '#ERROR!', blurb != summary)"
    # records = airtab.get_all(formula=outdated_summary_formula, fields="blurb", max_records=this_many)
    records = airtab.get_all(view='needs updated summary', fields="blurb", max_records=this_many)
    for record in records:
        this_dict = {}
        this_dict["summary"] = record["fields"]["blurb"]
        airtab.update(record["id"], this_dict)
    wrap_it_up(t0, new=i, total=len(records), function='update_summary')


def get_charges_from_recent_text():
    """This function parces the recent text field and extracts the listed charges."""
    t0, i = time.time(), 0
    # this formula is the same as one used for `needs charges` view
    needs_charges_formula = "AND(charges_updated = '', html != '', recent_text != '', hours_since_verification < 72, DONT_DELETE != 'no charges')"
    records = airtab.get_all(formula=needs_charges_formula)
    for record in records:
        this_dict = {}
        if record["fields"]["jail"] == "lcdc":
            charges = []
            bond_ammounts = []
            fine_ammounts = []
            soup = BeautifulSoup(record["fields"]["html"], "html.parser").tbody
            rows = soup.find_all("tr")
            if soup.tfoot:
                goods = rows[: len(rows) - 1]
                this_dict["intake_bond_cash"] = soup.tfoot.find_all("td")[2].b.string.strip()
                this_dict["intake_fine_ammount"] = soup.tfoot.find_all("td")[3].b.string.strip()
            else:
                goods = rows
            for row in goods:
                cells = row.find_all("td")
                if cells[0].string.strip():
                    if "," in cells[0].string.strip():
                        charges.append('"' + cells[0].string.strip() + '"')
                    else:
                        charges.append(cells[0].string.strip())
                if cells[2].string.strip():
                    bond_ammounts.append(
                        cells[2].string.strip().replace(",", ""))
                if cells[3].string.strip():
                    fine_ammounts.append(
                        cells[3].string.strip().replace(",", ""))
            if charges:
                this_dict["charges"] = ", ".join(charges)
            if bond_ammounts:
                this_dict["bond_ammounts"] = "\n".join(bond_ammounts)
            if fine_ammounts:
                this_dict["fine_ammounts"] = "\n".join(fine_ammounts)
            airtab.update(record["id"], this_dict, typecast=True)
            i += 1
        elif record["fields"]["jail"] == "kcdc":
            charges = []
            text = record["fields"]["recent_text"]
            goods = text[text.find("Charges:"): text.find("Note:")].splitlines()
            if len(goods) > 1:
                for good in goods:
                    if "," in good:
                        charges.append('"' + good.strip() + '"')
                    else:
                        charges.append(good)
                this_dict["charges"] = ", ".join(goods[1:])
                airtab.update(record["id"], this_dict)
                i += 1
        elif record["fields"]["jail"] in {"ccdc", "tcdc", "jcdc"}:
            charges = []
            text = record["fields"]["recent_text"]
            x = text.find("\nCharges:") + 9
            y = text.find("\nBond:")
            goods = text[x:y].strip().splitlines()
            for line in goods:
                if "," in line:
                    charges.append('"' + line + '"')
                else:
                    charges.append(line)
            this_dict["charges"] = ", ".join(charges)
            airtab.update(record["id"], this_dict)
            i += 1
        elif record["fields"]["jail"] == "hcdc":
            messy = []
            goods = []
            data = record["fields"]["recent_text"].splitlines()
            messy.append(data[data.index("Charge 1") + 1].strip())
            messy.append(data[data.index("Charge 2") + 1].strip())
            messy.append(data[data.index("Charge 3") + 1].strip())
            messy.append(data[data.index("Charge 4") + 1].strip())
            for x in messy:
                if not x.startswith("Felony / Misd"):
                    if "," in x:
                        goods.append('"' + x + '"')
                    else:
                        goods.append(x)
            this_dict["charges"] = ", ".join(goods)
            airtab.update(record["id"], this_dict)
            i += 1
    wrap_it_up(t0, new=i, total=len(records), function='get_charges_from_recent_text')


def retry_getting_mugshot():
    t0, i = time.time(), 0
    needs_pic_formula = "AND(PHOTO = '', hours_since_verification < 12, jail != 'lcdc')"
    records = airtab.get_all(formula=needs_pic_formula)
    print("we're gonna retry getting mugs for", len(records), "records...")
    for record in records:
        this_dict = {}
        r = requests.get(record['fields']['link'])
        if record['fields']['jail'] == 'jcdc':
            soup = BeautifulSoup(r.text, 'html.parser').find(id='cms-content')
            img_tag = soup.find('div', class_='inmate_profile_image').img
            if img_tag['alt'] != 'Image Not Availble':
                this_dict['img_src'] = f"https://www.jonesso.com/{img_tag['src']}"
                this_dict['PHOTO'] = [{'url': this_dict['img_src']}]
            # else:
            #     print('image not currently available')
        elif record['fields']['jail'] == 'hcdc':
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                img_src = 'http://www.co.hinds.ms.us' + soup.find('img', {'align': 'middle'})['src']
                if requests.get(img_src).headers['Content-Type'] == 'image/jpeg':
                    this_dict['img_src'] = img_src
                    this_dict['PHOTO'] = [{'url': img_src}]
                else:
                    print('image source isn\'t actually an image')
            except TypeError:
                print('no img tag in intake html')
        elif record['fields']['jail'] == 'kcdc':
            soup = BeautifulSoup(r.text, 'html.parser').find(id='cms-content')
            try:
                img_tag = soup.find('img')
            except AttributeError:
                # print('no img tag in intake html')
                continue
            if soup.img:
                img_src_raw = soup.img['src']
                if img_src_raw.startswith('templates/kempercountysheriff.com/images/inmates'):
                    this_dict['img_src'] = f"https://www.kempercountysheriff.com/{img_src_raw}"
                    this_dict['PHOTO'] = [{'url': this_dict['img_src']}]
        elif record['fields']['jail'] == 'acdc':
            soup = BeautifulSoup(r.text, 'html.parser').find('div', class_='blog-content-container')
            try:
                img_tag = soup.find('img')
                this_dict['img_src'] = img_tag.get('src')
                this_dict['PHOTO'] = [{'url': this_dict['img_src']}]
            except AttributeError:
                # print('no img tag in intake html')
                continue
        else:
            print(f"awww hell... this one is from the {record['fields']['jail']} docket/scraper...")
        airtab.update(record['id'], this_dict)
    wrap_it_up(t0, new=i, total=len(records), function='retry_getting_mugshot')


def parse_charge_1():
    t0, i = time.time(), 0
    needs_charge_1_parsed_formula = "AND(OR(jail = 'mcdc', jail = 'prcdf'), charge_1_statute = '', hours_since_initial_scrape < 48, charge_1 != '', charge_1 != 'HOLDHOLD', charge_1 != 'DRUGDRUG COURT', charge_1 != 'HLD Other AgencyHold for other Agency')"
    records = airtab.get_all(formula=needs_charge_1_parsed_formula)
    for record in records:
        this_dict = {}
        x = None
        if re.search("[)][A-Z]", record["fields"]["charge_1"]):
            x = re.search("[)][A-Z]", record["fields"]["charge_1"])
        elif re.search("[0-9][A-Z]", record["fields"]["charge_1"]):
            x = re.search("[0-9][A-Z]", record["fields"]["charge_1"])
        if x:
            this_dict["charge_1_statute"] = record["fields"]["charge_1"][: x.start() + 1]
            this_dict["charge_1_title"] = record["fields"]["charge_1"][x.end() - 1:]
            try:
                airtab.update(record["id"], this_dict)
                i += 1
            except requests.exceptions.HTTPError as err:
                print(err)
                continue
    wrap_it_up(t0, new=i, total=len(records), function='parse_charge_1')


def fix_charges_to_by_lines():
    t0, i = time.time(), 0
    records = airtab.get_all(formula="AND(TEST_FORMULA != '', TEST_RESULT = '')", fields='charges')
    for record in records:
        this_dict = {}
        cleaner = []
        mess = record['fields']['charges'].replace('", ', '"\n').replace(', "', '\n"').splitlines()
        for c in mess:
            if c.startswith('"'):
                cleaner.append(c.replace('"', ''))
            else:
                for d in c.split(', '):
                    cleaner.append(d)
        this_dict['TEST_RESULT'] = '\n'.join(cleaner)
        airtab.update(record['id'], this_dict)
        i += 1
    wrap_it_up(t0, new=i, total=len(records), function='fix_charges_to_by_lines')


def remove_weird_character():
    t0, i = time.time(), 0
    remove_wierd_character_formula = "AND(hours_since_verification > 12, FIND('ã', recent_text) > 1)"
    records = airtab.get_all(formula=remove_wierd_character_formula, fields='recent_text')
    for record in records:
        this_dict = {}
        x = record['fields']['recent_text'].find('ã')
        y = record['fields']['recent_text'].find('\n', x)
        this_dict['recent_text'] = record['fields']['recent_text'].replace(
            record['fields']['recent_text'][x:y], '')
        airtab.update(record['id'], this_dict)
        i += 1
    wrap_it_up(t0, new=i, total=len(records), function='remove_weird_character')


def get_full_text(this_many=150):
    t0, i = time.time(), 0
    # records = airtab.get_all(formula="AND(dc_id != '', dc_full_text = '')", fields=['dc_id'], max_records=this_many)
    records = airtab.get_all(view="needs full text", fields=['dc_id'], max_records=this_many)
    for record in records:
        this_dict = {}
        obj = dc.documents.get(record['fields']['dc_id'])
        this_dict["dc_title"] = obj.title
        this_dict["dc_access"] = obj.access
        this_dict["dc_pages"] = obj.pages
        # this_dict["dc_full_text"] = obj.full_text.decode("utf-8")
        this_dict["dc_full_text"] = obj.full_text
        airtab.update(record["id"], this_dict)
        i += 1
    wrap_it_up(t0, new=i, total=len(records), function='get_full_text')


def get_all_intake_deets():
    t0, i = time.time(), 0
    jcadc_deets_formula = "AND(jail = 'jcadc', charges = '', recent_text != '')"
    records = airtab.get_all(formula=jcadc_deets_formula, fields='recent_text')
    for record in records:
        charges = []
        bond_ammts = []
        classifications = []
        this_dict = {}
        txt_str = record['fields']['recent_text']
        chunks = txt_str.split('\nRequest Victim Notification\n')
        match_1 = re.search(r"(\w+)\s+(Male|Female)", chunks[0])
        try:
            raw_race = match_1.group(1)
            if raw_race == 'AVAILABLE':
                this_dict['race'] = 'U'
            else:
                this_dict['race'] = raw_race[0]
            this_dict['sex'] = match_1.group(2)[0]
        except AttributeError:
            print('there isnt race/sex info')
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
        try:
            this_dict['intake_age'] = re.search(r"(\d\d) Years Old", chunks[0]).group(1)
        except AttributeError:
            print('intake age is a mystery')
        try:
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
        except IndexError:
            print('no crim details')
        airtab.update(record['id'], this_dict, typecast=True)
        i += 1
    wrap_it_up(t0, new=i, total=len(records), function='get_all_intake_deets')


def update_dc_fields():
    records = airtab.get_all(view='need dc urls updated', fields='dc_id', max_records=100)
    print(len(records), ' records need updated documentcloud URLs.')
    for record in records:
        this_dict = {}
        dc_id = record['fields'].get('dc_id')
        obj = dc.documents.get(dc_id)
        this_dict["PDF"] = obj.pdf_url
        this_dict["dc_canonical_url"] = obj.canonical_url
        this_dict["dc_resources_page_image"] = obj.normal_image_url
        airtab.update(record['id'], this_dict)
        time.sleep(.3)


def main():
    polish_data()


if __name__ == "__main__":
    main()
