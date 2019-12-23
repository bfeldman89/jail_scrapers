# !/usr/bin/env python3
"""This module does blah blah."""
import datetime
import glob
import os
from pathlib import Path
import time
from bs4 import BeautifulSoup
import pdfkit
import requests
import send2trash
from jail_scrapers.common import airtab, dc, muh_headers, wrap_from_module

jails_lst = [['mcdc', 'intake_number'],
             ['prcdf', 'intake_number'],
             ['lcdc', 'intake_number'],
             ['jcadc', 'intake_number'],
             ['tcdc', 'bk'],
             ['kcdc', 'bk'],
             ['ccdc', 'bk'],
             ['acdc', 'bk'],
             ['hcdc', 'bk']]




def ensure_dir(dir_path):
    """Create a directory at the given path, including parents.

    Raises exception if path specifies a file, but not if directory exists.
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def damn_it(error_message):
    print('Another fucking "Connection Error."\n', error_message)
    time.sleep(10)


wrap_it_up = wrap_from_module('jail_scrapers/pdf_stuff.py')


def web_to_pdf():
    t0, i = time.time(), 0
    # records = airtab.get_all(view='needs pdf')
    pdf_formula = "AND(dc_id = '', hours_since_verification < 60, jail != 'jcj')"
    records = airtab.get_all(formula=pdf_formula)
    i = len(records)
    for record in records:
        url = record['fields']['link']
        jail = record['fields']['jail']
        if jail in {'mcdc', 'prcdf', 'lcdc', 'jcadc'}:
            fn = f"./output/{jail}/{record['fields']['intake_number']}.pdf"
        else:
            fn = f"./output/{jail}/{record['fields']['bk']}.pdf"
        options = {
            'quiet': '',
            'footer-right': time.strftime('%c'),
            'footer-left': url,
            'javascript-delay': 5000}
        if jail == 'lcdc':
            options['zoom'] = '.75'
            options['viewport-size'] = '1000x1400'
            options['footer-font-size'] = 9
        else:
            options['footer-font-size'] = 10
        if jail in {'mcdc', 'prcdf'}:
            try:
                r = requests.get(url, headers=muh_headers)
            except requests.ConnectionError as err:
                damn_it(err)
                continue
            data = []
            soup = BeautifulSoup(r.text, 'html.parser')
            for string in soup.stripped_strings:
                data.append(str(string))
            if record['fields']['intake_number'] == data[1 + data.index('INTAKE #:')]:
                pdfkit.from_url(url, fn, options)
            else:
                print('the intake number does not match!')
        else:
            pdfkit.from_url(url, fn, options)
    wrap_it_up(t0, new=i, total=i, function='web_to_pdf')


def pdf_to_dc():
    t0, i = time.time(), 0
    for jail in jails_lst:
        print(jail)
        output_path = os.path.join("output", jail[0])
        try:
            ensure_dir(output_path)
        except NotADirectoryError as err:
            damn_it(f"Skipping {jail[0]}: {err}")
            continue
        for fn in glob.glob(os.path.join(output_path, '*.pdf')):
            print(fn)
            obj = dc.documents.upload(fn, access="public")
            while obj.access != "public":
                time.sleep(7)
                obj = dc.documents.get(obj.id)
            this_dict = {"jail": jail[0]}
            obj.data = this_dict
            obj.put()
            this_dict["dc_id"] = obj.id
            print(obj.id)
            this_dict["dc_title"] = obj.title
            this_dict["dc_access"] = obj.access
            this_dict["dc_pages"] = obj.pages
            full_text = obj.full_text.decode("utf-8")
            this_dict["dc_full_text"] = os.linesep.join([s for s in full_text.splitlines() if s])
            # record = airtab.match(jail[1], this_dict["dc_title"], view='needs pdf')
            record = airtab.match('intake_number', '201005828', sort=[('dc_id', 'asc'), ('initial_scrape', 'desc')])
            airtab.update(record["id"], this_dict)
            send2trash.send2trash(fn)
            i += 1
            time.sleep(3)
    wrap_it_up(t0, new=i, total=i, function='pdf_to_dc')


def get_dor_if_possible():
    t0, i = time.time(), 0
    # records = airtab.get_all(view="check for DOR")
    dor_formula = "AND(OR(jail = 'kcdc', jail = 'tcdc', jail = 'ccdc'), DOR = '', hours_since_verification > 3, hours_since_verification < 48)"
    records = airtab.get_all(formula=dor_formula)
    total = len(records)
    for record in records:
        this_dict = {}
        try:
            r = requests.get(record["fields"]["link"])
        except requests.ConnectionError as err:
            damn_it(err)
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        data = []
        for string in soup.stripped_strings:
            data.append(str(string))
        if "Release Date:" in data:
            options = {
                "quiet": "",
                "footer-font-size": 10,
                "footer-left": record["fields"]["link"],
                "footer-right": time.strftime('%c'),
            }
            directory = f"./output/{record['fields']['jail']}/updated"
            try:
                ensure_dir(directory)
                file_name = f"{record['fields']['bk']} (final).pdf"
                fn = os.path.join(directory, file_name)
                pdfkit.from_url(record["fields"]["link"], fn, options=options)
            except NotADirectoryError as err:
                damn_it(f"Can't write PDF: {err}")

            this_dict["DOR"] = datetime.datetime.strptime(
                data[1 + data.index("Release Date:")], "%m-%d-%Y - %I:%M %p"
            ).strftime('%m/%d/%Y %H:%M')
            airtab.update(record["id"], this_dict)
            i += 1
    wrap_it_up(t0, i, total, function='get_dor_if_possible')


def main():
    web_to_pdf()
    pdf_to_dc()
    get_dor_if_possible()


if __name__ == "__main__":
    main()
