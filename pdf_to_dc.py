# !/usr/bin/env python3
"""This module does blah blah."""
import datetime
import os
import time
from bs4 import BeautifulSoup
import pdfkit
import requests
from airtable import Airtable
from documentcloud import DocumentCloud
import send2trash
from tabulate import tabulate

airtab_log = Airtable(os.environ['jail_scrapers_db'],
                      "log", os.environ['AIRTABLE_API_KEY'])
log_dict = {}

airtab = Airtable(os.environ['jail_scrapers_db'],
                  'intakes', os.environ['AIRTABLE_API_KEY'])

dc = DocumentCloud(os.environ['DOCUMENT_CLOUD_USERNAME'],
                   os.environ['DOCUMENT_CLOUD_PW'])


def pdf_to_dc(log_id, print_table=True):
    table = [["jail", "minutes", "uploads"]]
    t0 = time.time()
    jails_lst = [
        ["mcdc", "intake_number"],
        ["prcdf", "intake_number"],
        ["lcdc", "intake_number"],
        ["jcdc", "bk"],
        ["tcdc", "bk"],
        ["kcdc", "bk"],
        ["ccdc", "bk"],
        ["acdc", "bk"],
        ["hcdc", "bk"],
    ]
    for jail in jails_lst:
        i = 0
        mins = 0
        os.chdir(f"{os.getenv('HOME')}/code/jail_scrapers/output/{jail[0]}")
        for fn in os.listdir("."):
            if fn.endswith(".pdf"):
                start_time = time.time()
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
                duration = time.time() - start_time
                this_dict["pdf_processing_time"] = round(duration / 60, 2)
                record = airtab.match(
                    jail[1], this_dict["dc_title"], view=jail[0])
                airtab.update(record["id"], this_dict)
                send2trash.send2trash(fn)
                time.sleep(7)
                i += 1
                mins += this_dict["pdf_processing_time"]
        log_dict[str(jail[0] + " uploads")] = i
        if i > 0:
            table.append([jail[0], mins, i])
    log_dict["pdf-uploading duration"] = round((time.time() - t0) / 60, 2)
    airtab_log.update(log_id, log_dict)
    # print(f"`pdf_to_dc` took {round((time.time() - t0), 2)} seconds")
    if print_table:
        if len(table) > 1:
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))


def get_dor_if_possible(quiet=True):
    t0 = time.time()
    records = airtab.get_all(view="needs DOR")
    start = len(records)
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
                "footer-right": time.strftime("%x %X"),
            }
            fn = f"{record['fields']['bk']} (final).pdf"
            pdfkit.from_url(record["fields"]["link"], fn, options=options)
            this_dict["DOR"] = datetime.datetime.strptime(
                data[1 + data.index("Release Date:")], "%m-%d-%Y - %I:%M %p"
            ).strftime("%Y-%m-%d %H:%M")
            this_dict["updated"] = True
            airtab.update(record["id"], this_dict)
    if not quiet:
        print(
            f"`get_dor_if_possible` took {round((time.time() - t0), 2)} seconds")
    time.sleep(2)
    records = airtab.get_all(view="needs DOR")
    log_dict["needs DOR"] = len(records)
    log_dict["got DOR"] = start - len(records)


def main():
    log_entry = airtab_log.insert({"code": "jail_scraper.py"})
    log_id = log_entry["id"]
    pdf_to_dc(log_id, print_table=True)
    get_dor_if_possible(quiet=False)


if __name__ == "__main__":
    main()
