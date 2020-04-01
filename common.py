#!/usr/bin/env python
"""This module provides a function for shipping logs to Airtable."""
import os
import time
from airtable import Airtable
import cloudinary
from documentcloud import DocumentCloud

airtab_intakes = Airtable(base_key=os.environ['jail_scrapers_db'],
                          table_name='intakes',
                          api_key=os.environ['AIRTABLE_API_KEY'])

airtab_log = Airtable(base_key=os.environ['log_db'],
                      table_name='log',
                      api_key=os.environ['AIRTABLE_API_KEY'])

airtab_daily = Airtable(base_key=os.environ['jail_scrapers_db'],
                        table_name='daily stats',
                        api_key=os.environ['AIRTABLE_API_KEY'])

airtab_archive_intakes = Airtable(base_key=os.environ['jails_archive_db'],
                                  table_name='intakes',
                                  api_key=os.environ['AIRTABLE_API_KEY'])

airtab_tweets = Airtable(base_key=os.environ['botfeldman89_db'],
                         table_name='scheduled_tweets',
                         api_key=os.environ['AIRTABLE_API_KEY'])


cloudinary.config(cloud_name='bfeldman89',
                  api_key=os.environ['CLOUDINARY_API_KEY'],
                  api_secret=os.environ['CLOUDINARY_API_SECRET'])

dc = DocumentCloud(username=os.environ['DOCUMENT_CLOUD_USERNAME'],
                   password=os.environ['DOCUMENT_CLOUD_PW'])


muh_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


my_funcs = {'acdc_scraper': 'recZdPJHytCXB3v7C',
            'ccdc_scraper': 'recDAFRGM4gkPhHEO',
            'hcdc_scraper': 'rec3CEVirsVhbogFp',
            'jcadc_scraper': 'recVgj1nGL6H79bNZ',
            'jcj_scraper': 'recQIKW9Ky2K5s9sS',
            'jcdc_scraper': 'recsDwt7wzD03PcKE',
            'kcdc_scraper': 'recVkA9ZjjDC7WHMl',
            'lcdc_scraper': 'recqvYm2sWOVXVFwE',
            'mcdc_scraper': 'rec2kqwh9Nj8jyeqW',
            'prcdf_scraper': 'recsbEUfUO9WjXi8I',
            'tcdc_scraper': 'rec19KIgPSPYX8dyG',
            'fix_charges_to_by_lines': 'rechl6T1MRB4EK9NF',
            'get_all_intake_deets': 'recz3G21RAFoebeqe',
            'get_charges_from_recent_text': 'rec1QQGOdKrliYy52',
            'get_full_text': 'recszZqgqyMZbrZWA',
            'get_pixelated_mug': 'rece3aWHAWx2dAv09',
            'parse_charge_1': 'recndlqiBduVHEekv',
            'remove_weird_character': 'recDlfvTxn2YQyJ7V',
            'retry_getting_mugshot': 'rechPDYn5Koib8fjq',
            'update_summary': 'reczRWJZM7KIz1LRd',
            'get_dor_if_possible': 'recFMBytEdFfWEghZ',
            'pdf_to_dc': 'recqUaIfPApOsw6SB',
            'web_to_pdf': 'recFWboNnGFfVBnnS'}


def wrap_from_module(module):
    def wrap_it_up(t0, new=None, total=None, function=None):
        this_dict = {
            'module': module,
            'function': function,
            '_function': my_funcs[function],
            'duration': round(time.time() - t0, 2),
            'total': total,
            'new': new
        }
        airtab_log.insert(this_dict, typecast=True)

    return wrap_it_up
