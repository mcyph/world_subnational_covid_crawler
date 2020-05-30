
# This is in a very easy-to-parse format
# https://docs.google.com/spreadsheets/d/1F-AMEDtqK78EA6LYME2oOsWQsgJi4CT3V_G4Uo-47Rg/edit#gid=1539509351

import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_ADMIN_1,
    DT_TOTAL,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


# Province	Cases	Deaths	Recoveries	Active Cases	Date
# #adm1+name	#affected+infected+cases	#affected+infected+deaths
# #affected+infected+recoveries	#affected+infected+active	#date
#
# Badakhshan Province	13	0	1		2020-05-13
# Badghis Province	80	0	2		2020-05-13
# Baghlan Province	88	3	4		2020-05-13
# Balkh Province	437	17	10		2020-05-13
# Bamyan Province	36	1	7		2020-05-13


class AFData(URLBase):
    SOURCE_URL = 'https://docs.google.com/spreadsheets/d/' \
                 '1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw/edit'
    SOURCE_LICENSE = ''

    GEO_DIR = 'af'
    GEO_URL = 'https://data.humdata.org/dataset/afg-admin-boundaries'
    GEO_LICENSE = 'Humanitarian use only'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'af' / 'data',
             urls_dict={
                 'provinces_1.csv': URL(
                     'https://docs.google.com/spreadsheet/ccc?'
                     'key=1F-AMEDtqK78EA6LYME2oOsWQsgJi4CT3V_G4Uo-47Rg&'
                     'gid=1539509351&output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []
        first_line = True

        f = self.get_file('provinces_1.csv',
                          include_revision=True)

        for item in csv.DictReader(f):
            if first_line:
                first_line = False
                continue

            date = self.convert_date(item['Date'])
            province = item['Province'].strip().replace(' Province', '')
            if not province:
                break

            if item['Cases'].replace('–', ''):
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Afghanistan',
                    region_child=province,
                    datatype=DT_TOTAL,
                    value=int(item['Cases'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            if item['Deaths'].replace('–', ''):
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Afghanistan',
                    region_child=province,
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Deaths'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            if item['Recoveries'].replace('–', ''):
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Afghanistan',
                    region_child=province,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['Recoveries'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            if item['Active Cases'].replace('–', ''):
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Afghanistan',
                    region_child=province,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['Active Cases'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(AFData().get_datapoints())
