import csv

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


class IQData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/iraq-coronavirus-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'iq_hdx_humdata'

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
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'iq', 'anbar'): ('admin_1', 'iq', 'IQ-AN'),
                ('admin_1', 'iq', 'babylon'): ('admin_1', 'iq', 'IQ-BB'),
                ('admin_1', 'iq', 'baghdad-karkh'): ('MERGE', 'admin_1', 'iq', 'IQ-BG'),
                ('admin_1', 'iq', 'baghdad-rusafa and medical city'): ('MERGE', 'admin_1', 'iq', 'IQ-BG'),
                ('admin_1', 'iq', 'baghdad-resafa and midical city'): ('MERGE', 'admin_1', 'iq', 'IQ-BG'),
                ('admin_1', 'iq', 'basrah'): ('admin_1', 'iq', 'IQ-BA'),
                ('admin_1', 'iq', 'diwaniya'): ('admin_1', 'iq', 'IQ-QA'),
                ('admin_1', 'iq', 'kerbala'): ('admin_1', 'iq', 'IQ-KA'),
                ('admin_1', 'iq', 'iq-ki'): None, # FIXME!
                ('admin_1', 'iq', 'kirkuk'): None, # FIXME!
                ('admin_1', 'iq', 'missan'): ('admin_1', 'iq', 'IQ-MA'),
                ('admin_1', 'iq', 'muthanna'): ('admin_1', 'iq', 'IQ-MU'),
                ('admin_1', 'iq', 'ninewa'): ('admin_1', 'iq', 'IQ-NI'),
                ('admin_1', 'iq', 'salah al-din'): ('admin_1', 'iq', 'IQ-SD'),
                ('admin_1', 'iq', 'thi-qar'): ('admin_1', 'iq', 'IQ-DQ'),
                ('admin_1', 'iq', 'wassit'): ('admin_1', 'iq', 'IQ-WA'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()

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

            #print(item)
            date = self.convert_date(item['Date'])
            region_child = item['Governorate'].title()

            if item['Cases']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IQ',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(item['Cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Deaths']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IQ',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['Deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Recoveries']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IQ',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(item['Recoveries']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Active Cases']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IQ',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(item['Active Cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(IQData().get_datapoints())
