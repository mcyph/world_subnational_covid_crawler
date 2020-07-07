# https://covid-19-greece.herokuapp.com/regions-history

import csv
import json
from os import listdir

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1, DT_TESTS_TOTAL,
    DT_TOTAL, DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class GRCovid19Greece(URLBase):
    SOURCE_URL = 'https://covid-19-greece.herokuapp.com'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'gr_covid_19_greece'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'gr' / 'data',
            urls_dict={
                'regions.json': URL('https://covid-19-greece.herokuapp.com/regions-history',
                                    static_file=False),
            }
        )
        self.update()

    def get_datapoints(self):
        # {
        #   "regions-history": [
        #     {
        #       "date": "2020-04-20",
        #       "regions": [
        #         {
        #           "cases_per_100000_people": 11.88,
        #           "population": 606170,
        #           "region_cases": 72,
        #           "region_en_name": "East Macedonia and Thrace",
        #           "region_gr_name": "Ανατολική Μακεδονία και Θράκη"
        #         },

        r = []
        base_dir = self.get_path_in_dir('')

        region_map = {
            'west greece': 'GR-G',
            'central greece': 'GR-H',
            'north aegean': 'GR-K',
            'west macedonia': 'GR-C',
            'without permanent residency in greece': 'Other',
            'under investigation': 'Unknown',
        }

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/regions.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for day_dict in data['regions-history']:
                date = self.convert_date(day_dict['date'])

                for region_dict in day_dict['regions']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='GR',
                        region_child=region_map.get(
                            region_dict['region_en_name'].lower(),
                            region_dict['region_en_name']
                        ),
                        datatype=DT_TOTAL,
                        value=int(region_dict['region_cases']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(GRCovid19Greece().get_datapoints())
