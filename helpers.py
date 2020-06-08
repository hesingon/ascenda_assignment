import json
from datetime import datetime, timedelta


def has_time_elapsed_for(then, minutes):
    # then = datetime(then_time)
    now = datetime.now()
    diff = timedelta(minutes=minutes)
    if now - then >= diff:
        print("Confirmed elapsed for more than {} minutes".format(minutes))
        return True
    else:
        return False


def time_now():
    return datetime.now()


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
    print(json.dumps(content, indent=4, sort_keys=True))
