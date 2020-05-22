import csv

from covid_19_au_grab.state_news_releases.overseas.URLBase import (
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


class IQData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/iraq-coronavirus-covid-19-subnational-cases'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / '' / 'data',
             urls_dict={
                 'ml_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/2PACX-1vQh_BwL222rdcpIH2rLPIbvdKLJu3fevAy2L82FHUcl-84w6byWRITQicetYzpqX707EUc3qgAJm7Hr/pub?gid=0&single=true&output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        # Governorate,Cases,Deaths,Recoveries,Active Cases,Date
        #
        # #adm1+name,#affected+infected+confirmed,#affected+infected+dead,
        # #affected+infected+recovered,#affected+infected+active,#date
        #
        # ANBAR,5,2,0,3,2020-05-13
        # BABYLON,47,26,5,16,2020-05-13

        f = self.get_file('ml_data.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue
            date = self.convert_date(item['Date'])
            region_child = item['Governorate'].title()

            if item['Cases']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Iraq',
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=int(item['Cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Deaths']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Iraq',
                    region_child=region_child,
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Recoveries']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Iraq',
                    region_child=region_child,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['Recoveries']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Active Cases']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Iraq',
                    region_child=region_child,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['Active Cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(IQData().get_datapoints())
