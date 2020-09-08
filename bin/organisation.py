import json
import pandas as pd

from utils import make_index


def get_organisation_data(path_to_csv="https://raw.githubusercontent.com/digital-land/organisation-dataset/master/collection/organisation.csv"):
    csv_pd = pd.read_csv(path_to_csv, sep=",")
    datalist = json.loads(csv_pd.to_json(orient="records"))
    return make_index(datalist, "organisation")


def get_organisation_boundary(organisations, _id):
    if organisations.get(_id) and not organisations.get(_id)[0]['boundary'] == "":
        return organisations[_id][0]['boundary']
    return None
    #return [org for org in organisations if org['organisation'] == _id and org['boundary'] is not None]


def get_boundaries(organisations, ids):
    boundaries = []
    for _id in ids:
        if get_organisation_boundary(organisations, _id) is not None:
            boundaries.append(get_organisation_boundary(organisations, _id))
    return boundaries
