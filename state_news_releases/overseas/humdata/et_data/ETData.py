import csv
import json

from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_ET_ADMIN_1,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class ETData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/' \
                 'ethiopia-coronavirus-covid-19-subnational-cases'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'et' / 'data',
             urls_dict={
                 'et_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/'
                     '1wpMiswWu5En3Ljoqv-N9gK_VQWU6xYA9NBAYzJ3aE2g/'
                     'export?format=csv&'
                     'id=1wpMiswWu5En3Ljoqv-N9gK_VQWU6xYA9NBAYzJ3aE2g',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        # Date	admin1Name_en	admin1Pcode	Number of confirmed COVID-19	Number of reported deaths	Number of reported recoveries
        # #date	#adm1+name	#adm1+code	#affected+infected+confirmed	#affected+infected+dead	#affected+infected+recovered
        # 2020-05-13	Addis Ababa	ET14	172	3	47
        # 2020-05-13	Afar	ET02	20
        # 2020-05-13	Amhara	ET03	9		2
        # 2020-05-13	Dire Dawa	ET15	8		1
        # 2020-05-13	Oromia	ET04	17

        f = self.get_file('et_data.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue
            date = self.convert_date(item['Date'])
            region = item['admin1Name_en'].strip()

            if item['Number of confirmed COVID-19']:
                r.append(DataPoint(
                    schema=SCHEMA_ET_ADMIN_1,
                    region=region,
                    datatype=DT_TOTAL,
                    value=int(item['Number of confirmed COVID-19']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
                
            if item['Number of reported deaths']:
                r.append(DataPoint(
                    schema=SCHEMA_ET_ADMIN_1,
                    region=region,
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Number of reported deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Number of reported recoveries']:
                r.append(DataPoint(
                    schema=SCHEMA_ET_ADMIN_1,
                    region=region,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['Number of reported recoveries']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
                r.append(DataPoint(
                    schema=SCHEMA_ET_ADMIN_1,
                    region=region,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['Number of confirmed COVID-19'])-int(item['Number of reported recoveries']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ETData().get_datapoints())