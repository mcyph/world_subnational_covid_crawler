# https://twitter.com/YSNECCOVID19
# http://yemen-corona.com/

"""
Hadhramaut
Aden
Taiz
Lahij
Shabwah
Dhale
Ma'rib
Al Mahrah
Abyan
Sana'a *
Total

الإجمالي
حضرموت
عدن
تعز
لحج
شبوة
الضالع
مأرب
المهرة
أبين
صنعاء *
"""


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


place_map = {
    'hadhramaut': 'YE-HD',
    'taiz': 'YE-TA',
    'dhale': 'YE-DA',
    "sana'a": 'ye-sn',
    'abyan': 'ye-ab',
    'al mahrah': 'ye-mr',
    "ma'rib": 'ye-ma',
    'shabwah': 'ye-sh',
    'lahij': 'ye-la',
    'aden': 'ye-ad'
}


class YEData(URLBase):
    SOURCE_URL = 'http://yemen-corona.com/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ye_yemen_corona'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'ye' / 'data',
            urls_dict={
                'totalGovDataForTable.json': URL('http://yemen-corona.com/index.php?route=report/statistics/totalGovDataForTable',
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
            path = f'{base_dir}/{date}/totalGovDataForTable.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for data in data:
                # {"gov_id":"11","name":"Hadhramaut","confirmed":"361","new_confirmed":"0",
                # "death":"135","new_death":"0","recovered":"77","new_recovered":"0"}
                governorate = place_map[data['name'].lower()]
                confirmed = int(data['confirmed'])
                deaths = int(data['death'])
                recovered = int(data['recovered'])
                new_confirmed = int(data['new_confirmed'])
                new_death = int(data['new_death'])
                new_recovered = int(data['new_recovered'])
                active = confirmed - recovered - deaths

                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.TOTAL,
                    value=confirmed,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=deaths,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=recovered,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=active,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.NEW,
                    value=new_confirmed,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_DEATHS_NEW,
                    value=new_death,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='YE',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_RECOVERED_NEW,
                    value=new_recovered,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(YEData().get_datapoints())
