"""This module does blah blah."""
import os
import time
import pdfkit
import requests
from airtable import Airtable
from bs4 import BeautifulSoup

airtab = Airtable(os.environ['jail_scrapers_db'], 'intakes',
                  os.environ['AIRTABLE_API_KEY'])

muh_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

records = airtab.get_all(view='needs pdf')
for record in records:
    os.chdir(
        f"{os.getenv('HOME')}/code/jail_scrapers/output/{record['fields']['jail']}")
    if record['fields']['jail'] == 'lcdc':
        options = {'zoom': '.75', 'viewport-size': '1000x1400', 'quiet': '',
                   'footer-left': record['fields']['link'], 'footer-font-size': 9, 'footer-right': time.strftime('%c')}
        pdfkit.from_url(record['fields']['link'],
                        f"{record['fields']['intake_number']}.pdf", options)
    elif record['fields']['jail'] in {'mcdc', 'prcdf'}:
        r = requests.get(record['fields']['link'], headers=muh_headers)
        data = []
        soup = BeautifulSoup(r.text, 'html.parser')
        for string in soup.stripped_strings:
            data.append(str(string))
        if record['fields']['intake_number'] == data[1 + data.index('INTAKE #:')]:
            options = {'quiet': '', 'footer-font-size': 10,
                       'footer-left': record['fields']['link'], 'footer-right': time.strftime('%c')}
            pdfkit.from_url(
                record['fields']['link'], f"{record['fields']['intake_number']}.pdf", options)
        else:
            print('intake numbers didn\'t match')
    else:
        options = {'quiet': '', 'footer-font-size': 10,
                   'footer-left': record['fields']['link'], 'footer-right': time.strftime('%c')}
        pdfkit.from_url(record['fields']['link'],
                        f"{record['fields']['bk']}.pdf", options)
