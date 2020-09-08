#!/usr/bin/env python3

import os
import jinja2

from local_plans_data import get_local_plan_data
from jinja_filters import map_organisation_id_filter

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

# get page template
list_template = env.get_template("list.html")
plan_template = env.get_template("plan.html")

# get the data
plan_data = get_local_plan_data()

# generate the pages
render("local-plan/index.html", list_template, data=plan_data)

for plan in plan_data:
    render(f"local-plan/{plan['development-plan']}/index.html", plan_template, plan=plan)