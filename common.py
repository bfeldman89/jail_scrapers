#!/usr/bin/env /python
"""This module provides a function for shipping logs to Airtable."""

import os

from airtable import Airtable

airtab = Airtable(os.environ['jail_scrapers_db'], 'intakes', os.environ['AIRTABLE_API_KEY'])
airtab_log = Airtable(os.environ['log_db'], 'log', os.environ['AIRTABLE_API_KEY'])

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
