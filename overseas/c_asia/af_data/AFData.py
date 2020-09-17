
# This is in a very easy-to-parse format
# https://docs.google.com/spreadsheets/d/1F-AMEDtqK78EA6LYME2oOsWQsgJi4CT3V_G4Uo-47Rg/edit#gid=1539509351

import csv

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir


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
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'af_humdata'

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
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'af', 'dykundi'): None, #('admin_1', 'af', 'AF-DAY'),
                ('admin_1', 'af', 'hirat'): ('admin_1', 'af', 'AF-HER'),
                ('admin_1', 'af', 'jawzjan'): ('admin_1', 'af', 'AF-JOW'),
                ('admin_1', 'af', 'paktya'): ('admin_1', 'af', 'AF-PIA'),
                ('admin_1', 'af', 'panjsher'): None, #('admin_1', 'af', 'AF-PAN'),
                ('admin_1', 'af', 'sar-e-pul'): ('admin_1', 'af', 'AF-SAR'),
                ('admin_1', 'af', 'daykundi'): None, #('admin_1', 'af', 'AF-DAY'),
                ('admin_1', 'af', 'panjshir'): None, #('admin_1', 'af', 'AF-PAN'),
                ('admin_1', 'af', 'panjshir\xa0province'): None, #('admin_1', 'af', 'AF-PAN'),
                ('admin_1', 'af', 'sar-e\xa0pol\xa0province'): ('admin_1', 'af', 'AF-SAR'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()
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
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AF',
                    region_child=province,
                    datatype=DataTypes.TOTAL,
                    value=int(item['Cases'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            if item['Deaths'].replace('–', ''):
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AF',
                    region_child=province,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['Deaths'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            if item['Recoveries'].replace('–', ''):
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AF',
                    region_child=province,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(item['Recoveries'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            if item['Active Cases'].replace('–', ''):
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AF',
                    region_child=province,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(item['Active Cases'].replace(',', '')),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(AFData().get_datapoints())
