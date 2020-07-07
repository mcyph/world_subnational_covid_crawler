# https://data.humdata.org/dataset/haiti-covid-19-subnational-cases
# https://docs.google.com/spreadsheets/u/1/d/10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ/export?format=csv&id=10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ
import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1,
    DT_TOTAL, DT_NEW,
    DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class HTData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/haiti-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ht_hdx_humdata'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / '' / 'data',
             urls_dict={
                 'ht_data.csv': URL(
                     'https://docs.google.com/spreadsheets/u/1/d/10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ/export?format=csv&id=10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        # Date,Département,Cumulative cases,New cases (24h),Cumulative Deaths,New deaths (24h) Rate Of,Case fatality rate,Source
        # #date,#adm1+name,#affected+infected+confirmed+total,#affected+infected+confirmed+new,#affected+infected+dead+total,#affected+infected+dead+new,,
        # 12-05-2020,Ouest,166,15,9,0,5.4%,https://mspp.gouv.ht/site/downloads/Sitrep%20COVID-19_12-05-2020.pdf
        # 12-05-2020,Artibonite,27,0,5,0,18.5%,https://mspp.gouv.ht/site/downloads/Sitrep%20COVID-19_12-05-2020.pdf
        # 12-05-2020,Nord-Est,12,0,2,0,16.7%,https://mspp.gouv.ht/site/downloads/Sitrep%20COVID-19_12-05-2020.pdf
        # 12-05-2020,Nord,8,0,1,0,12.5%,https://mspp.gouv.ht/site/downloads/Sitrep%20COVID-19_12-05-2020.pdf
        # 12-05-2020,Sud-Est,7,0,1,0,14.3%,https://mspp.gouv.ht/site/downloads/Sitrep%20COVID-19_12-05-2020.pdf

        f = self.get_file('ht_data.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date'])
            region_child = item['Département']

            if item['Cumulative cases']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Haiti',
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=int(item['Cumulative cases']),
                    source_url=item['Source'],
                    date_updated=date
                ))

            if item['New cases (24h)']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Haiti',
                    region_child=region_child,
                    datatype=DT_NEW,
                    value=int(item['New cases (24h)']),
                    source_url=item['Source'],
                    date_updated=date
                ))

            if item['Cumulative Deaths']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Haiti',
                    region_child=region_child,
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Cumulative Deaths']),
                    source_url=item['Source'],
                    date_updated=date
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(HTData().get_datapoints())
