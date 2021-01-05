import csv

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from _utility.get_package_dir import get_overseas_dir


class SNData(URLBase):
    # Pretty sure this isn't being updated any more...
    SOURCE_URL = 'https://data.humdata.org/dataset/positive-cases-of-covid-19-in-senegal'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'sn_ocha_rowca_humdata'

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
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'sn', 'dakar-ouest'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'dakar'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'dakar-centre'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'dakar-nord'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'dakar-sud'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'mbao'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'guédiawaye'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'yeumbeul'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'rufisque'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'diamniadio'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'pikine'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'sangalkam'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'keur massar'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),
                ('admin_1', 'sn', 'guediawaye'): ('MERGE', 'admin_1', 'sn', 'sn-dk'),

                ('admin_1', 'sn', 'touba'): ('MERGE', 'admin_1', 'sn', 'sn-db'),

                ('admin_1', 'sn', 'mbour'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'popenguine'): ('MERGE', 'admin_1', 'sn', 'sn-th'),

                ('admin_1', 'sn', 'oussouye'): ('MERGE', 'admin_1', 'sn', 'sn-zg'),

                ('admin_1', 'sn', 'saint louis'): ('MERGE', 'admin_1', 'sn', 'sn-sl'),
                ('admin_1', 'sn', 'richard toll'): ('MERGE', 'admin_1', 'sn', 'sn-sl'),

                ('admin_1', 'sn', 'non déterminé'): ('MERGE', 'admin_1', 'sn', 'unknown'),
                ('admin_1', 'sn', ''): ('MERGE', 'admin_1', 'sn', 'unknown'),

                ('admin_1', 'sn', 'velingara'): ('MERGE', 'admin_1', 'sn', 'sn-kd'),
                ('admin_1', 'sn', 'goudiry'): ('MERGE', 'admin_1', 'sn', 'sn-tc'),
                ('admin_1', 'sn', 'keur massar'): ('MERGE', 'admin_1', 'sn', 'sn-tc'),
                ('admin_1', 'sn', 'sakal'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'mbacke'): ('MERGE', 'admin_1', 'sn', 'sn-db'),
                ('admin_1', 'sn', 'tivaouane'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'pout'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'nioro du rip'): ('MERGE', 'admin_1', 'sn', 'sn-kl'),
                ('admin_1', 'sn', 'sedhiou'): ('MERGE', 'admin_1', 'sn', 'sn-se'),
                ('admin_1', 'sn', 'diouloulou'): ('MERGE', 'admin_1', 'sn', 'sn-zg'),
                ('admin_1', 'sn', 'linguere'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'kedougou'): ('MERGE', 'admin_1', 'sn', 'sn-ke'),
                ('admin_1', 'sn', 'thiadiaye'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'mekhe'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'koungheul'): ('MERGE', 'admin_1', 'sn', 'sn-ka'),
                ('admin_1', 'sn', 'coki'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'poponguine'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'tivaoune'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'joal fadiouth'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'joal-fadiouth'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'bignona'): ('MERGE', 'admin_1', 'sn', 'sn-zg'),
                ('admin_1', 'sn', 'bikilane'): ('MERGE', 'admin_1', 'sn', 'sn-dk'), # Pikine??
                ('admin_1', 'sn', 'dioffior'): ('MERGE', 'admin_1', 'sn', 'sn-fk'),
                ('admin_1', 'sn', 'darou mousty'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'thilogne'): ('MERGE', 'admin_1', 'sn', 'sn-mt'),
                ('admin_1', 'sn', 'bounkiling'): ('MERGE', 'admin_1', 'sn', 'sn-se'),
                ('admin_1', 'sn', 'khombole'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'richard-toll'): ('MERGE', 'admin_1', 'sn', 'sn-sl'),
                ('admin_1', 'sn', 'birkilane'): ('MERGE', 'admin_1', 'sn', 'sn-ka'),
                ('admin_1', 'sn', 'kebemer'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'ranerou'): ('MERGE', 'admin_1', 'sn', 'sn-mt'),
                ('admin_1', 'sn', 'gossas'): ('MERGE', 'admin_1', 'sn', 'sn-fk'),
                ('admin_1', 'sn', 'bambey'): ('MERGE', 'admin_1', 'sn', 'sn-db'),
                ('admin_1', 'sn', 'sokone'): ('MERGE', 'admin_1', 'sn', 'sn-fk'),
                ('admin_1', 'sn', 'mékhé'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'joal'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'mbacké'): ('MERGE', 'admin_1', 'sn', 'sn-db'),
                ('admin_1', 'sn', 'vélingara'): ('MERGE', 'admin_1', 'sn', 'sn-kd'),
                ('admin_1', 'sn', 'bounkilig'): ('MERGE', 'admin_1', 'sn', 'sn-se'),
                ('admin_1', 'sn', 'diakhao'): ('MERGE', 'admin_1', 'sn', 'sn-fk'),
                ('admin_1', 'sn', 'linguère'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'cocki'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'kébémer'): ('MERGE', 'admin_1', 'sn', 'sn-lg'),
                ('admin_1', 'sn', 'nioro'): ('MERGE', 'admin_1', 'sn', 'sn-kl'),
                ('admin_1', 'sn', 'ranérou'): ('MERGE', 'admin_1', 'sn', 'sn-mt'),
                ('admin_1', 'sn', 'kanel'): ('MERGE', 'admin_1', 'sn', 'sn-mt'),
                ('admin_1', 'sn', 'joal  fadiouth'): ('MERGE', 'admin_1', 'sn', 'sn-th'),
                ('admin_1', 'sn', 'passy'): ('MERGE', 'admin_1', 'sn', 'sn-fk'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self.get_by_district())
        r.extend(self.get_national_cases())
        return r

    def get_by_district(self):
        r = self.sdpf()

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

            #print(item)
            date = self.convert_date(item['Date']+'-20')
            
            if item['Cas']:
                try:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='SN',
                        region_child=item['District'].strip(),
                        datatype=DataTypes.TOTAL,
                        value=int(item['Cas']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )
                except AssertionError:
                    if item['District'].strip().lower() == 'dakar-ouest':
                        continue

        return r

    def get_national_cases(self):
        r = self.sdpf()

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
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='SN',
                datatype=DataTypes.TOTAL,
                value=int(item['Cas']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(SNData().get_datapoints())
