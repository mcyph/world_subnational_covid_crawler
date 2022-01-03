# https://data.humdata.org/dataset/haiti-covid-19-subnational-cases
# https://docs.google.com/spreadsheets/u/1/d/10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ/export?format=csv&id=10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ
import csv

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT


class HTData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/haiti-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ht_hdx_humdata'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / '' / 'data',
             urls_dict={
                 'ht_data.csv': URL(
                     'https://docs.google.com/spreadsheets/u/1/d/10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ/export?format=csv&id=10YxLT870MwYJ3Tm_a3WvvU2r1zQbT5F20TSXzw03BxQ',
                     static_file=False
                 )
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'ht', 'grand anse'): ('admin_1', 'ht', 'ht-ga'),
                ('admin_1', 'ht', 'grandanse'): ('admin_1', 'ht', 'ht-ga'),
                ('admin_1', 'ht', 'grand total'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()

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
            #print(item)
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date'])
            region_child = item['Département']
            if region_child == 'Quest':
                region_child = 'Ouest'

            if item['Cumulative cases']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ht',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(item['Cumulative cases'].replace(',', '')),
                    source_url=item['Source'],
                    date_updated=date
                )

            if item['New cases (24h)']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ht',
                    region_child=region_child,
                    datatype=DataTypes.NEW,
                    value=int(item['New cases (24h)'].replace(',', '')),
                    source_url=item['Source'],
                    date_updated=date
                )

            if item['Cumulative Deaths']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ht',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['Cumulative Deaths'].replace(',', '')),
                    source_url=item['Source'],
                    date_updated=date
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(HTData().get_datapoints())
