import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    DT_TOTAL
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class SNData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/positive-cases-of-covid-19-in-senegal'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'sn' / 'data',
            urls_dict={
                'by_district.csv': URL(
                    'https://docs.google.com/spreadsheets/d/e/'
                    '2PACX-1vRj1sRWYmyZ2AznFdP5Dr98uZrzsMMudPBRIcMW8FdwAEy-'
                    'Hwq3PSPJYI12xTzLbA/pub?gid=1515611831&single=true&output=csv',
                    static_file=False
                ),
                'national_cases.csv': URL(
                    'https://docs.google.com/spreadsheets/d/e/'
                    '2PACX-1vRj1sRWYmyZ2AznFdP5Dr98uZrzsMMudPBRIcMW8FdwAEy-'
                    'Hwq3PSPJYI12xTzLbA/pub?gid=708820609&single=true&output=csv',
                    static_file=False
                )
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self.get_by_district())
        r.extend(self.get_national_cases())
        return r

    def get_by_district(self):
        r = []

        # https://docs.google.com/spreadsheets/d/e/2PACX-1vRj1sRWYmyZ2AznFdP5Dr98uZrzsMMudPBRIcMW8FdwAEy-Hwq3PSPJYI12xTzLbA/pub?gid=1515611831&single=true&output=csv
        # Date,District,Cas,Ordre
        # #date,#loc +name,#affected +infected,
        # 2-Mar,Dakar-Ouest,1,1
        # 3-Mar,Guédiawaye,1,2
        # 4-Mar,Dakar-Ouest,1,3
        # 9-Mar,Non déterminé,1,4
        # 11-Mar,Touba,1,5
        # 12-Mar,Non déterminé,5,6
        # 12-Mar,Touba,11,6

        f = self.get_file('by_district.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date']+'-20')
            
            if item['Cas']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Senegal',
                    region_child=item['District'],
                    datatype=DT_TOTAL,
                    value=int(item['Cas']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def get_national_cases(self):
        r = []

        # https://docs.google.com/spreadsheets/d/e/2PACX-1vRj1sRWYmyZ2AznFdP5Dr98uZrzsMMudPBRIcMW8FdwAEy-Hwq3PSPJYI12xTzLbA/pub?gid=708820609&single=true&output=csv
        # Ordre,Date,Cas
        # ,#date,#affected +infected
        # 1,2-Mar,1
        # 2,3-Mar,1
        # 3,4-Mar,2
        # 4,5-Mar,0
        # 5,6-Mar,0
        # 6,7-Mar,0

        f = self.get_file('national_cases.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date']+'-20')
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='Senegal',
                datatype=DT_TOTAL,
                value=int(item['Cas']),
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(SNData().get_datapoints())
