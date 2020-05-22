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


class SOData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/somalia-coronavirus-covid-19-subnational-cases'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'so' / 'data',
             urls_dict={
                 'so_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/2PACX-1vRTGuZDNylQKqZC7ITpHkLw-7nHvElQNtImJS7kRFXGak664t6jxDjvdVHHWkKPJ7rvwAtj6VGXrQUC/pub?output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        # Date,Region,Confirmed ,Dead,Recovered,Active
        #
        # #date,#adm1+name,#affected+infected+confirmed,#affected+infected+dead,
        # #affected+infected+recovered,#affected+infected+active
        #
        # 5/15/2020,Awdal,1,0,0,1
        # 5/15/2020,Woqooyi Galbeed,60,5,6,49
        # 5/15/2020,Togdheer,4,0,0,4
        # 5/15/2020,Sanaag,3,0,0,3
        # 5/15/2020,Nugaal,111,4,3,104
        # 5/15/2020,Mudug,4,0,0,4
        # 5/15/2020,Hiran,6,1,0,5

        f = self.get_file('so_data.csv',
                          include_revision=True)

        first_item = True
        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue
            print(item)

            date = self.convert_date(item['Date'],
                                     formats=('%m/%d/%Y',))
            region_child = item['State']

            if item['Confirmed ']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Somalia',
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=int(item['Confirmed ']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
            if item['Dead']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Somalia',
                    region_child=region_child,
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Dead']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
            if item['Recovered']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Somalia',
                    region_child=region_child,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['Recovered']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
            if item['Active']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Somalia',
                    region_child=region_child,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['Active']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(SOData().get_datapoints())
