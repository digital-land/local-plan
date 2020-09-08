def make_index(datalist, key):
    """Returns dict indexed on the provided key field."""
    idx = {}
    idx['with_key_missing'] = []
    for row in datalist:
        if key in row:
            idx.setdefault(row[key], [])
            idx[row[key]].append(row)
        else:
            idx['with_key_missing'].append(row)
    return idx
