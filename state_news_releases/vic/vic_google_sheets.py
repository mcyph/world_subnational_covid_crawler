import csv
from os.path import exists
from urllib.request import urlretrieve

from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_POSTCODE,
    DT_STATUS_ACTIVE, DT_TOTAL
)


# https://docs.google.com/spreadsheets/d/1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ/edit#gid=0
URL_TEMPLATE = 'https://docs.google.com/spreadsheet/ccc?key=%(long_id)s&gid=%(short_id)s&output=csv'
URL_SOURCE = 'https://docs.google.com/spreadsheets/d/1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ/edit#gid=0'


def get_from_google_sheets():
    dir_ = get_data_dir() / 'vic' / 'google_sheets'
    path_data_page_31_Jul = dir_ / 'data_page_2020_07_31.csv'
    path_data_page_08_Aug = dir_ / 'data_page_2020_08_06.csv'
    path_source_page = dir_ / 'source_page.csv'

    if not exists(path_data_page_31_Jul):
        urlretrieve(
            URL_TEMPLATE % {
                'long_id': '1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ',
                'short_id': '0'
            },
            path_data_page_31_Jul
        )
        urlretrieve(
            URL_TEMPLATE % {
                'long_id': '1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ',
                'short_id': '1919344323'
            },
            path_data_page_08_Aug
        )
        urlretrieve(
            URL_TEMPLATE % {
                'long_id': '1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ',
                'short_id': '1195577978'
            },
            path_source_page
        )

    r = []
    r.extend(_get_from_path(path_data_page_31_Jul, '2020_07_31'))
    r.extend(_get_from_path(path_data_page_08_Aug, '2020_08_06'))
    return r


def _get_from_path(path_data_page, date):
    r = []

    with open(path_data_page, 'r', encoding='utf-8') as f:
        for item in csv.DictReader(f):
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