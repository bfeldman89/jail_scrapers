# !/usr/bin/env python3
"""This module accesses several airtable 'views' that contain records that need some additional processing."""
import os
import re
import time
import cloudinary
from cloudinary import uploader
from airtable import Airtable
from bs4 import BeautifulSoup
from documentcloud import DocumentCloud


airtab = Airtable(os.environ['jail_scrapers_db'], 'intakes', os.environ['AIRTABLE_API_KEY'])
airtab_log = Airtable(os.environ['log_db'], 'log', os.environ['AIRTABLE_API_KEY'])
dc = DocumentCloud(os.environ['DOCUMENT_CLOUD_USERNAME'], os.environ['DOCUMENT_CLOUD_PW'])

cloudinary.config(cloud_name='bfeldman89', api_key=os.environ['CLOUDINARY_API_KEY'], api_secret=os.environ['CLOUDINARY_API_SECRET'])


def wrap_it_up(t0, new=None, total=None, function=None):
    this_dict = {'module': 'jail_scrapers/polish_data.py'}
    this_dict['function'] = function
    this_dict['duration'] = round(time.time() - t0, 2)
    this_dict['total'] = total
    this_dict['new'] = new
    airtab_log.insert(this_dict, typecast=True)


def polish_data():
    """This function does runs each of the module's functions."""
    get_pixelated_mug()
    update_summary()
    get_charges_from_recent_text()
    retry_getting_mugshot()
    remove_weird_character()
    parse_charge_1()
    fix_charges_to_by_lines()
    get_all_intake_deets()


def get_pixelated_mug():
    """This function uploads the raw image to cloudinary and then uploads the pixelated version to the airtable record."""
    records = airtab.get_all(view="needs pixelated mug")
    for record in records:
        url = record["fields"]["PHOTO"][0]["url"]
        fn = record["fields"]["UID"]
        try:
            uploader.upload(url, public_id=fn)
        except cloudinary.api.Error as err:
            print("cloudinary can't accept that shit: ", err)
        time.sleep(1.5)
        this_dict = {}
        this_dict["PIXELATED_IMG"] = [{"url": record["fields"]["pixelated_url"]}]
        airtab.update(record["id"], this_dict)


def update_summary(this_many=100):
    """This function updates the record summary. The reason we have this field,
    rather than just use the 'blurb' field, is bc the gallery view works better
    with a text field than it does with a formula field. Because this view will
    regularly be packed full of records, the default max records is 100."""
    records = airtab.get_all(view="needs updated summary", fields="blurb", max_records=this_many)
    for record in records:
        this_dict = {}
        this_dict["summary"] = record["fields"]["blurb"]
        airtab.update(record["id"], this_dict)


def get_charges_from_recent_text():
    """This function parces the recent text field and extracts the listed charges."""
    records = airtab.get_all(view="needs charges")
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
                this_dict["intake_bond_cash"] = soup.tfoot.find_all("td")[
                    2
                ].b.string.strip()
                this_dict["intake_fine_ammount"] = soup.tfoot.find_all("td")[
                    3
                ].b.string.strip()
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
        elif record["fields"]["jail"] == "kcdc":
            charges = []
            text = record["fields"]["recent_text"]
            goods = text[text.find("Charges:"): text.find(
                "Note:")].splitlines()
            if len(goods) > 1:
                for good in goods:
                    if "," in good:
                        charges.append('"' + good.strip() + '"')
                    else:
                        charges.append(good)
                this_dict["charges"] = ", ".join(goods[1:])
                airtab.update(record["id"], this_dict)
        elif record["fields"]["jail"] in {"ccdc", "tcdc"}:
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


def retry_getting_mugshot():
    """This function does blah blah."""
    records = airtab.get_all(view="needs pic")
    for record in records:
        this_dict = {}
        this_dict["PHOTO"] = [{"url": record["fields"]["img_src"]}]
        airtab.update(record["id"], this_dict)


def parse_charge_1():
    """This function does blah blah."""
    records = airtab.get_all(view="needs charge_1 parsed")
    for record in records:
        this_dict = {}
        x = None
        if re.search("[)][A-Z]", record["fields"]["charge_1"]):
            x = re.search("[)][A-Z]", record["fields"]["charge_1"])
        elif re.search("[0-9][A-Z]", record["fields"]["charge_1"]):
            x = re.search("[0-9][A-Z]", record["fields"]["charge_1"])
        if x:
            this_dict["charge_1_statute"] = record["fields"]["charge_1"][
                : x.start() + 1
            ]
            this_dict["charge_1_title"] = record["fields"]["charge_1"][x.end() - 1:]
            airtab.update(record["id"], this_dict)


def fix_charges_to_by_lines():
    """This function does blah blah."""
    records = airtab.get_all(view='test', fields='charges')
    for record in records:
        this_dict = {}
        cleaner = []
        mess = record['fields']['charges'].replace(
            '", ', '"\n').replace(', "', '\n"').splitlines()
        for c in mess:
            if c.startswith('"'):
                cleaner.append(c.replace('"', ''))
            else:
                for d in c.split(', '):
                    cleaner.append(d)
        this_dict['TEST RESULT'] = '\n'.join(cleaner)
        airtab.update(record['id'], this_dict)


def remove_weird_character():
    """This function does blah blah."""
    records = airtab.get_all(
        view='needs weird character removed', fields='recent_text')
    for record in records:
        this_dict = {}
        x = record['fields']['recent_text'].find('ã')
        y = record['fields']['recent_text'].find('\n', x)
        this_dict['recent_text'] = record['fields']['recent_text'].replace(
            record['fields']['recent_text'][x:y], '')
        airtab.update(record['id'], this_dict)


def get_full_text():
    """This function does blah blah."""
    records = airtab.get_all(
        view='needs full text', fields=['dc_id'])
    for record in records:
        this_dict = {}
        obj = dc.documents.get(record['fields']['dc_id'])
        this_dict["dc_title"] = obj.title
        this_dict["dc_access"] = obj.access
        this_dict["dc_pages"] = obj.pages
        this_dict["dc_full_text"] = obj.full_text.decode("utf-8")
        airtab.update(record["id"], this_dict)


def get_all_intake_deets():
    records = airtab.get_all(view='needs_jcadc_deets', fields='recent_text')
    for record in records:
        charges = []
        bond_ammts = []
        classifications = []
        this_dict = {}
        txt_str = record['fields']['recent_text']
        chunks = txt_str.split('\nRequest Victim Notification\n')
        match_1 = re.search(r"(\w+)\s+(Male|Female)", chunks[0])
        raw_race = match_1.group(1)
        if raw_race == 'AVAILABLE':
            this_dict['race'] = 'U'
        else:
            this_dict['race'] = raw_race[0]
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


def main():
    """This function does blah blah."""
    t0 = time.time()
    polish_data()
    funcs = ['get_pixelated_mug', 'update_summary', 'get_charges_from_recent_text',
             'retry_getting_mugshot', 'remove_weird_character', 'parse_charge_1',
             'fix_charges_to_by_lines', 'get_all_intake_deets']
    wrap_it_up(t0, function=funcs)


if __name__ == "__main__":
    main()
