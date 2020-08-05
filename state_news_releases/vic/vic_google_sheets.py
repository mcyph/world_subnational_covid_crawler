import csv
from os import makedirs, listdir
from os.path import exists
from urllib.request import urlretrieve
from datetime import datetime, timedelta

from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_LGA, SCHEMA_POSTCODE, SCHEMA_LHD,
    DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_INTERSTATE,
    DT_SOURCE_CONFIRMED, DT_SOURCE_COMMUNITY,
    DT_SOURCE_OVERSEAS,

    DT_TESTS_TOTAL,
    DT_STATUS_ACTIVE, DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_TOTAL, DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TESTS_POSITIVE, DT_TESTS_NEGATIVE
)


# https://docs.google.com/spreadsheets/d/1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ/edit#gid=0
URL_TEMPLATE = 'https://docs.google.com/spreadsheet/ccc?key=%(long_id)s&gid=%(short_id)s&output=csv'
URL_SOURCE = 'https://docs.google.com/spreadsheets/d/1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ/edit#gid=0'


def get_from_google_sheets():
    date = (datetime.now() - timedelta(hours=20, minutes=30)).strftime('%Y_%m_%d')
    i_dir = get_data_dir() / 'vic' / 'google_sheets' / date
    if not exists(i_dir):
        makedirs(i_dir)

    r = []
    for date in listdir(get_data_dir() / 'vic' / 'google_sheets'):
        i_dir = get_data_dir() / 'vic' / 'google_sheets' / date
        r.extend(_get_from_google_sheets(i_dir, date))
    return r


def _get_from_google_sheets(dir_, date):
    path_data_page = dir_ / 'data_page.csv'
    path_source_page = dir_ / 'source_page.csv'

    if not exists(path_data_page) or not exists(path_source_page):
        urlretrieve(
            URL_TEMPLATE % {
                'long_id': '1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ',
                'short_id': '0'
            },
            path_data_page
        )
        urlretrieve(
            URL_TEMPLATE % {
                'long_id': '1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ',
                'short_id': '1195577978'
            },
            path_source_page
        )

    r = []

    with open(path_data_page, 'r', encoding='utf-8') as f:
        for item in csv.DictReader(f):
            #print(item)

            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_parent='AU-VIC',
                region_child=item['Postcode'],
                datatype=DT_TOTAL,
                value=int(item['Confirmed cases (ever)'] or 0),
                date_updated=date,  # FIXME!!!!!
                source_url=URL_SOURCE
            ))

            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_parent='AU-VIC',
                region_child=item['Postcode'],
                datatype=DT_STATUS_ACTIVE,
                value=int(item['Active cases (current)'] or 0),
                date_updated=date,  # FIXME!!!!!
                source_url=URL_SOURCE
            ))

    return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_from_google_sheets())
