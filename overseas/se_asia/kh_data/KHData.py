


import json
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)

# 'Phnom Penh': '',
#      'Sihanouk': '',
#      'Kampong Cham': '',
#      'Battambang': '',
#      'Siem Reap': '',
#      'Banteay Meanchey': '',
#      'Kep': '',
#      'Honey': '',
#      'Kampong Chhnang': '',
#      'Middle': '',
#      'Koh Kong': '',
#      'Kampot': '',
#      'Temple': ''


place_map = {
    'ភ្នំពេញ': 'KH-12',
    'ព្រះសីហនុ': 'KH-18',
    'កំពង់ចាម': 'KH-3',
    'បាត់ដំបង': 'KH-2',
    'សៀមរាប': 'KH-17',
    'បន្ទាយមានជ័យ': 'KH-1',
    'កែប': 'KH-23',
    'ត្បូងឃ្មុំ': 'KH-25',
    'កំពង់ឆ្នាំង': 'KH-4',
    'កណ្ដាល': 'KH-8',
    'កោះកុង': 'KH-9',
    'កំពត': 'KH-7',
    'ព្រះវិហារ': 'KH-13',
    'កំពង់ស្ពឺ': 'KH-5'
}


class KHData(URLBase):
    SOURCE_URL = 'https://covid19-map.cdcmoh.gov.kh/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'kh_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'kh' / 'data',
            urls_dict={
                'index.html': URL('https://covid19-map.cdcmoh.gov.kh/',
                                  static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/index.html'
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()

            data = html.split("data-covid-19='")[1] \
                       .split("' data-summary='")[0] \
                       .replace('&quot;', '"')

            for data in json.loads(data):
                print(data)
                date = self.convert_date(
                    data['created_at'].split('T')[0]
                )
                region_child = place_map[data['location']['name_km']]

                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KH',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(data['total_case']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KH',
                    region_child=region_child,
                    datatype=DataTypes.NEW,
                    value=int(data['new_case']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KH',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(data['recovered_case']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KH',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS_NEW,
                    value=int(data['new_death_case']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KH',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED_NEW,
                    value=int(data['new_recovered_case']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(KHData().get_datapoints())
