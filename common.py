#!/usr/bin/env /python
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

airtab_courts = Airtable(base_key=os.environ['other_scrapers_db'],
                         table_name='courts',
                         api_key=os.environ['AIRTABLE_API_KEY'])

airtab_mdoc = Airtable(base_key=os.environ['other_scrapers_db'],
                       table_name='mdoc',
                       api_key=os.environ['AIRTABLE_API_KEY'])

airtab_sos = Airtable(base_key=os.environ['other_scrapers_db'],
                      table_name='exec_orders',
                      api_key=os.environ['AIRTABLE_API_KEY'])

airtab_tweets = Airtable(base_key=os.environ['botfeldman89_db'],
                         table_name='scheduled_tweets',
                         api_key=os.environ['AIRTABLE_API_KEY'])


dc = DocumentCloud(username=os.environ['DOCUMENT_CLOUD_USERNAME'],
                   password=os.environ['DOCUMENT_CLOUD_PW'])

cloudinary.config(cloud_name='bfeldman89',
                  api_key=os.environ['CLOUDINARY_API_KEY'],
                  api_secret=os.environ['CLOUDINARY_API_SECRET'])

muh_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


def wrap_from_module(module):
    def wrap_it_up(t0, new=None, total=None, function=None):
        this_dict = {
            'module': module,
            'function': function,
            'duration': round(time.time() - t0, 2),
            'total': total,
            'new': new
        }
        airtab_log.insert(this_dict, typecast=True)

    return wrap_it_up
