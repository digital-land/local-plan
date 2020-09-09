#!/usr/bin/env python3
import csv

import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

from utils import make_index

session = CacheControl(requests.session(), cache=FileCache(".cache"))

development_plans_csv = "https://raw.githubusercontent.com/digital-land/alpha-data/master/local-plans/development-plan.csv"
development_plan_documents_csv = "https://raw.githubusercontent.com/digital-land/alpha-data/master/local-plans/development-plan-document.csv"
development_plan_timetable_csv = "https://raw.githubusercontent.com/digital-land/alpha-data/master/local-plans/development-plan-timetable.csv"

# fetch from a URL
def get(url):
    r = session.get(url)
    r.raise_for_status()
    return r.text


def create_status_obj(data):
    status_objs = {}
    idxed = make_index(data, "development-plan")
    for plan_id in idxed.keys():
        idxed[plan_id].sort(key=lambda stage: stage['end-date'])
        status_objs[plan_id] = {
            "current": {
                "status": idxed[plan_id][-1]['development-plan-status'],
                "date": idxed[plan_id][-1]['end-date']
            },
            "timeline": idxed[plan_id]
        }

    return status_objs


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

    timeline_reader = csv.DictReader(get(development_plan_timetable_csv).splitlines())
    timelines = [row for row in timeline_reader]
    status_objs = create_status_obj(timelines)

    for plan in plans:
        if status_objs.get(plan['development-plan']) is not None:
            plan['status'] = status_objs[plan['development-plan']]

    return plans
