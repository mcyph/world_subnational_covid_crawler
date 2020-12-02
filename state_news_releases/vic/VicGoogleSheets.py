import csv
from os.path import exists
from urllib.request import urlretrieve

from covid_19_au_grab.get_package_dir import get_data_dir
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes


# https://docs.google.com/spreadsheets/d/1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ/edit#gid=0
URL_TEMPLATE = 'https://docs.google.com/spreadsheet/ccc?key=%(long_id)s&gid=%(short_id)s&output=csv'


class VicGoogleSheets:
    SOURCE_ID = 'vic_the_age_google_doc'
    SOURCE_URL = 'https://docs.google.com/spreadsheets/d/1oxJt0BBPzk-w2Gn1ImO4zASBCdqeeLJRwHEA4DASBFQ/edit#gid=0'
    SOURCE_DESCRIPTION = ''

    def get_datapoints(self):
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
        r.extend(self._get_from_path(path_data_page_31_Jul, '2020_07_31'))
        r.extend(self._get_from_path(path_data_page_08_Aug, '2020_08_06'))
        return r

    def _get_from_path(self, path_data_page, date):
        r = []

        with open(path_data_page, 'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                r.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='AU-VIC',
                    region_child=item['Postcode'],
                    datatype=DataTypes.TOTAL,
                    value=int(item['Confirmed cases (ever)'] or 0),
                    date_updated=date,  # FIXME!!!!!
                    source_url=self.URL_SOURCE,
                    source_id=self.SOURCE_ID
                ))
                r.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='AU-VIC',
                    region_child=item['Postcode'],
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(item['Active cases (current)'] or 0),
                    date_updated=date,  # FIXME!!!!!
                    source_url=self.URL_SOURCE,
                    source_id=self.SOURCE_ID
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(VicGoogleSheets().get_datapoints())
