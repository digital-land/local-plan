#!/usr/bin/env python3
import csv

import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

session = CacheControl(requests.session(), cache=FileCache(".cache"))

development_plans_csv = "https://raw.githubusercontent.com/digital-land/alpha-data/master/local-plans/development-plan.csv"
development_plan_documents_csv = "https://raw.githubusercontent.com/digital-land/alpha-data/master/local-plans/development-plan-document.csv"


# fetch from a URL
def get(url):
    r = session.get(url)
    r.raise_for_status()
    return r.text


def get_local_plan_data():
    # get plan data
    reader = csv.DictReader(get(development_plans_csv).splitlines())
    plans = [row for row in reader]
    plans.sort(key=lambda x: 'z' if x['name'] is "" else x['name']) # sort by name, putting blanks at the end
    # get document data
    document_reader = csv.DictReader(get(development_plan_documents_csv).splitlines())
    documents = [row for row in document_reader]

    for plan in plans:
        plan['document'] = [doc for doc in documents if doc['development-plan'] == plan['development-plan']]

    return plans
