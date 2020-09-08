#!/usr/bin/env python3

import os
import jinja2

from local_plans_data import get_local_plan_data
from organisation import get_organisation_data, get_boundaries
from jinja_filters import map_organisation_id_filter, statistical_geography_code

docs = "docs/"
static_path = "https://digital-land.github.io" # use frontend assets we have published

def render(path, template, **kwargs):
    path = os.path.join(docs, path)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(template.render(staticPath=static_path, **kwargs))


# register templates
multi_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(searchpath="./templates"),
    jinja2.PrefixLoader({
        'govuk-jinja-components': jinja2.PackageLoader('govuk_jinja_components')
    })
])
env = jinja2.Environment(loader=multi_loader)

# register jinja filters
env.filters['map_organisation_by_id'] = map_organisation_id_filter
env.filters['statistical_geography_code'] = statistical_geography_code

# get page template
list_template = env.get_template("list.html")
plan_template = env.get_template("plan.html")

# get the data
plan_data = get_local_plan_data()
organisations = get_organisation_data()

# generate the pages
render("local-plan/index.html", list_template, data=plan_data)

for plan in plan_data:
    plan_organisations = plan['organisations'].split(';')
    boundaries = get_boundaries(organisations, plan_organisations)

    # need to replace this with real data
    status = {
        "current": {
            "status": "adopted",
            "date": "14 Dec 2017"
        },
        "timeline": [
            {"status": "published", "date": "31 Mar 2016"},
            {"status": "submitted", "date": "20 Oct 2016"},
            {"status": "sound", "date": "29 Sep 2017"},
            {"status": "adopted", "date": "14 Dec 2017"}
        ]
    }
    plan['status'] = status

    render(
        f"local-plan/{plan['development-plan']}/index.html",
        plan_template,
        plan=plan,
        boundaries=boundaries)