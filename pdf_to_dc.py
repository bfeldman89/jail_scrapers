# !/usr/bin/env python3
"""This module does blah blah."""
import glob
import datetime
import os
import time
from bs4 import BeautifulSoup
import pdfkit
import requests
from airtable import Airtable
from documentcloud import DocumentCloud
import send2trash


airtab = Airtable(os.environ['jail_scrapers_db'],
                  'intakes', os.environ['AIRTABLE_API_KEY'])

dc = DocumentCloud(os.environ['DOCUMENT_CLOUD_USERNAME'],
                   os.environ['DOCUMENT_CLOUD_PW'])

jails_lst = [['mcdc', 'intake_number'],
             ['prcdf', 'intake_number'],
             ['lcdc', 'intake_number'],
             ['jcadc', 'intake_number'],
             ['tcdc', 'bk'],
             ['kcdc', 'bk'],
             ['ccdc', 'bk'],
             ['acdc', 'bk'],
             ['hcdc', 'bk']]


def pdf_to_dc():
    for jail in jails_lst:
        os.chdir(f"{os.getenv('HOME')}/code/jail_scrapers/output/{jail[0]}")
        for fn in glob.glob('*.pdf'):
            obj = dc.documents.upload(fn, access="public")
            obj = dc.documents.get(obj.id)
            while obj.access != "public":
                time.sleep(7)
                obj = dc.documents.get(obj.id)
            this_dict = {"jail": jail[0]}
            obj.data = this_dict
            obj.put()
            this_dict["dc_id"] = obj.id
            this_dict["dc_title"] = obj.title
            this_dict["dc_access"] = obj.access
            this_dict["dc_pages"] = obj.pages
            full_text = obj.full_text.decode("utf-8")
            this_dict["dc_full_text"] = os.linesep.join(
                [s for s in full_text.splitlines() if s]
            )
            record = airtab.match(
                jail[1], this_dict["dc_title"], view=jail[0])
            airtab.update(record["id"], this_dict)
            send2trash.send2trash(fn)
            time.sleep(7)


def get_dor_if_possible():
    records = airtab.get_all(view="needs DOR")
    for record in records:
        this_dict = {}
        r = requests.get(record["fields"]["link"])
        soup = BeautifulSoup(r.text, "html.parser")
        data = []
        for string in soup.stripped_strings:
            data.append(str(string))
        if "Release Date:" in data:
            os.chdir(
                f"{os.getenv('HOME')}/code/jail_scrapers/output/{record['fields']['jail']}/updated")
            options = {
                "quiet": "",
                "footer-font-size": 10,
                "footer-left": record["fields"]["link"],
                "footer-right": time.strftime('%c'),
            }
            fn = f"{record['fields']['bk']} (final).pdf"
            pdfkit.from_url(record["fields"]["link"], fn, options=options)
            this_dict["DOR"] = datetime.datetime.strptime(
                data[1 + data.index("Release Date:")], "%m-%d-%Y - %I:%M %p"
            ).strftime('%m/%d/%Y %H:%M')
            airtab.update(record["id"], this_dict)


def main():
    pdf_to_dc()
    get_dor_if_possible()


if __name__ == "__main__":
    main()
