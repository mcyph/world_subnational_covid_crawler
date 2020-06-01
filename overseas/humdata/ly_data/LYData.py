import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1,
    DT_TOTAL,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class LYData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/' \
                 'libya-coronavirus-covid-19-subnational-cases'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'ly' / 'data',
             urls_dict={
                 'ly_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/'
                     '2PACX-1vQQWJZmGZJfUm22CPWoeW6rSS7Xh4K54r4A8RlN214ZCIPBUBOug3UbxFPrbiT3FQic6HS8wGdUhv3f/'
                     'pub?output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        # Governorate,Confirmed Cases,Recoveries,Deaths,Active,Date
        #
        # #adm2+name,#affected+infected+confirmed,#affected+infected+recovered,
        # #affected+infected+dead,#affected+infected+active,#date
        #
        # Benghazi,4,4,,,2020-05-12
        # Misurata,10,10,,,2020-05-12
        # Sorman,1,1,,,2020-05-12
        # Tripoli,49,13,3,33,2020-05-12

        first_item = True
        f = self.get_file('ly_data.csv',
                          include_revision=True)

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue
            date = self.convert_date(item['Date'])
            region_child = item['Governorate'].title()

            if item['Confirmed Cases']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Libya',
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=int(item['Confirmed Cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Deaths']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Libya',
                    region_child=region_child,
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Recoveries']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Libya',
                    region_child=region_child,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['Recoveries']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

            if item['Active']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Libya',
                    region_child=region_child,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['Active']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(LYData().get_datapoints())
