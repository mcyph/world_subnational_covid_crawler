import json
from case_locations.update_spreadsheet import get_worksheet_data_as_dicts


def get_case_locations():
    return get_worksheet_data_as_dicts()


if __name__ == '__main__':
    print(json.dumps(get_case_locations(), indent=2))
