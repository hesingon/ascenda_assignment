import json
from mergedeep import merge
import collections.abc


def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def is_valid_latitude_and_longitude(lat, lng):
    try:
        assert(isinstance(lat, float))
        assert(isinstance(lng, float))
        assert(lat <= 90 or lat >= -90)
        assert(lng <= 180 or lng >= 180)
    except AssertionError:
        return False
    return True


def pretty_print_dict(content):
    # parsed = json.loads(content)
    print(json.dumps(content, indent=4, sort_keys=True))


def merge_info(infos):
    merged = {}
    for item in infos:
        merged = merge(merged, item)
    return merged


def merge_dict(dict1, dict2):
    for key, val in dict1.items():
        if type(val) == dict:
            if key in dict2 and type(dict2[key] == dict):
                merge_dict(dict1[key], dict2[key])
        else:
            if key in dict2:
                dict1[key] = dict2[key]

    for key, val in dict2.items():
        if not key in dict1:
            dict1[key] = val

    return dict1

