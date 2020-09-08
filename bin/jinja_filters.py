from filter.organisation_mapper import map_organisation_id_filter

def statistical_geography_code(v):
    if v:
        return v.replace("statistical-geography:", "")
    return v
