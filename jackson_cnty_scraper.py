# !/usr/bin/env python3
"""This module does blah blah."""
import glob
import os
import time
from datetime import datetime, timezone
import cloudinary
import pdfkit
import requests
import send2trash
from airtable import Airtable
from bs4 import BeautifulSoup
from cloudinary import uploader
from documentcloud import DocumentCloud
from nameparser import HumanName

airtab = Airtable(os.environ['jail_scrapers_db'], 'jcadc',
                  os.environ['AIRTABLE_API_KEY'])

cloudinary.config(cloud_name='bfeldman89',
                  api_key=os.environ['CLOUDINARY_API_KEY'],
                  api_secret=os.environ['CLOUDINARY_API_SECRET'])

dc = DocumentCloud(os.environ['DOCUMENT_CLOUD_USERNAME'],
                   os.environ['DOCUMENT_CLOUD_PW'])


muh_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

options = {'quiet': '',
           'footer-font-size': 10,
           'footer-right': time.strftime('%c')}

root = 'https://services.co.jackson.ms.us/jaildocket'

os.chdir(f"{os.getenv('HOME')}/code/jail_scrapers/output/jcadc")


def get_name(raw_name, this_dict):
    name = HumanName(raw_name)
    name.capitalize()
    this_dict['first_name'] = name.first
    this_dict['last_name'] = name.last
    this_dict['middle_name'] = name.middle
    this_dict['suffix'] = name.suffix


def get_pages():
    r = requests.post(
        f"{root}/_inmateList.php?Function=count", headers=muh_headers)
    count = r.json()
    last_page = int(count / 15)
    return range(1, last_page + 1)


def jcadc_scraper():
    pages = get_pages()
    for pg in pages:
        r = requests.post(
            f"{root}/_inmateList.php?Function=list&Page={pg}&Order=BookDesc&Search=0",
            headers=muh_headers)
        intakes = r.json()
        for intake in intakes:
            this_dict = {'bk': intake["Book_Number"]}
            this_dict['last_verified'] = (datetime.utcnow().replace(
                tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M'))
            m = airtab.match('bk', this_dict['bk'])
            if m:
                airtab.update(m['id'], this_dict, typecast=True)
            else:
                raw_name = f"{intake['Name_First_MI']} {intake['Name_Middle']} {intake['Name_Last']} {intake['Name_Suffix']}"
                get_name(raw_name, this_dict)
                this_dict['DOI'] = intake["BookDate"]
                this_dict['DOA'] = intake["ArrestDate"]
                this_dict['LEA'] = intake["Arrest_Agency"]
                this_dict['id'] = intake["ID_Number"].strip()
                this_dict[
                    'link'] = f"{root}/inmate/_inmatedetails.php?id={this_dict['id']}"
                r = requests.get(this_dict['link'], headers=muh_headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                articles = soup.find_all('articles')
                this_dict['html'] = f"<html>\n<body>\n{articles[0].prettify()}\n{articles[1].prettify()}\n</body>\n</html>"
                this_dict[
                    'img_url'] = f"{root}/inmate/{this_dict['id']}.jpg"
                this_dict['mug'] = [{'url': this_dict['img_url']}]
                airtab.insert(this_dict, typecast=True)
                time.sleep(1)


def get_pixelated_mug():
    records = airtab.get_all(formula="AND(mug != '', pixelated_mug = '')")
    print(len(records))
    for record in records:
        url = record["fields"]["img_url"]
        fn = record["fields"]["bk"]
        uploader.upload(url, public_id=fn)
        time.sleep(2)
        this_dict = {}
        this_dict['pixelated_mug'] = [
            {'url': record['fields']['pixelated_mug']}]
        airtab.update(record['id'], this_dict)


def web_to_pdf():
    records = airtab.get_all(formula="dc_id = ''")
    for record in records:
        url = record['fields']['link']
        fn = f"{record['fields']['id']}.pdf"
        options['footer-left'] = url
        pdfkit.from_url(url, fn, options)


def pdf_to_dc():
    for fn in glob.glob('*.pdf'):
        obj = dc.documents.upload(fn, access="public")
        obj = dc.documents.get(obj.id)
        while obj.access != "public":
            time.sleep(7)
            obj = dc.documents.get(obj.id)
        this_dict = {"jail": 'jcadc'}
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
        record = airtab.match('id', fn.replace('.pdf', ''))
        airtab.update(record["id"], this_dict)
        send2trash.send2trash(fn)


def parse_html(record):
    this_dict = {}
    data = []
    r = requests.get(record['fields']['link'], headers=muh_headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    for string in soup.stripped_strings:
        data.append(string)
    this_dict['recent_text'] = '\n'.join(data[1:])
    articles = soup.find_all('article')
    this_dict['html'] = f"<html>\n<body>\n{articles[0].prettify()}\n{articles[1].prettify()}</body>\n</html>"
    airtab.update(record['id'], this_dict)


def main():
    jcadc_scraper()
    web_to_pdf()
    get_pixelated_mug()
    pdf_to_dc()


if __name__ == '__main__':
    main()
