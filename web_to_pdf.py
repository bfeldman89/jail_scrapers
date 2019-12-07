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

output_path = f"{os.getenv('HOME')}/code/jail_scrapers/output"


def web_to_pdf(this_record):
    url = this_record['fields']['link']
    jail = this_record['fields']['jail']
    os.chdir(f"{output_path}/{jail}")
    if jail in {'mcdc', 'prcdf', 'lcdc', 'jcadc'}:
        fn = f"{this_record['fields']['intake_number']}.pdf"
    else:
        fn = f"{this_record['fields']['bk']}.pdf"
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
        r = requests.get(url, headers=muh_headers)
        data = []
        soup = BeautifulSoup(r.text, 'html.parser')
        for string in soup.stripped_strings:
            data.append(str(string))
        if this_record['fields']['intake_number'] == data[1 + data.index('INTAKE #:')]:
            pdfkit.from_url(url, fn, options)
        else:
            print('the intake number does not match!')
    else:
        pdfkit.from_url(url, fn, options)


def main():
    records = airtab.get_all(view='needs pdf')
    for record in records:
        web_to_pdf(record)


if __name__ == "__main__":
    main()
