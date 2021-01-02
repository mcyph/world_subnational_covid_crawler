import json
from case_locations.nsw.get_nsw_case_locations import get_nsw_case_locations
from case_locations.vic.get_vic_case_locations import get_vic_case_locations


def get_case_locations():
    out = []
    out.extend(get_nsw_case_locations())
    out.extend(get_vic_case_locations())
    return out


if __name__ == '__main__':
    print(json.dumps(get_case_locations(), indent=2))
