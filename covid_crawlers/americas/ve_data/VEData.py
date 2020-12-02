# https://covid19.patria.org.ve/estadisticas-venezuela/
# https://covid19.patria.org.ve/api/v1/summary

import json
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT


class VEData(URLBase):
    SOURCE_URL = 'https://covid19.patria.org.ve/estadisticas-venezuela/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 've_patria'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 've' / 'data2',
             urls_dict={
                 'regions.json': URL('https://covid19.patria.org.ve/api/v1/summary',
                                     static_file=False)
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 've', 'la guaira'): ('MERGE', 'admin_1', 've', 've-x'),
                ('admin_1', 've', 'los roques'): ('MERGE', 'admin_1', 've', 've-w'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases())
        return r

    def _get_cases(self):
        r = self.sdpf()

        # {"Confirmed":
        # {"Count":6273,
        #  "ByAgeRange": {"0-9":492,"10-19":625,"20-29":1486,"30-39":1212,"40-49":835,"50-59":546,"60-69":295,"70-79":115,"80-89":32,"90-99":2},
        #  "ByGender":{"male":3557,"female":2716},
        #  "ByState":{"Amazonas":17,"Anzo\u00e1tegui":27,"Apure":1207,"Aragua":241,"Barinas":110,"Bol\u00edvar":710,
        #             "Carabobo":67,"Cojedes":11,"Delta Amacuro":10,"Distrito Capital":435,"Falc\u00f3n":54,"Gu\u00e1rico":7,
        #             "La Guaira":125,"Lara":146,"Los Roques":4,"M\u00e9rida":81,"Miranda":557,"Monagas":42,"Nueva Esparta":174,
        #             "Portuguesa":24,"Sucre":141,"T\u00e1chira":729,"Trujillo":73,"Yaracuy":30,"Zulia":1251}
        # },
        # "Recovered":{"Count":2100},
        # "Deaths":{"Count":57},
        # "Active":{"Count":4116}
        # }

        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/regions.json'
            with open(path, 'rb') as f:
                case_dict = json.loads(f.read())

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='VE',
                datatype=DataTypes.TOTAL,
                value=int(case_dict['Confirmed']['Count']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='VE',
                datatype=DataTypes.STATUS_DEATHS,
                value=int(case_dict['Deaths']['Count']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='VE',
                datatype=DataTypes.STATUS_ACTIVE,
                value=int(case_dict['Active']['Count']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='VE',
                datatype=DataTypes.STATUS_RECOVERED,
                value=int(case_dict['Recovered']['Count']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='VE',
                datatype=DataTypes.TOTAL_MALE,
                value=int(case_dict['Confirmed']['ByGender']['male']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='VE',
                datatype=DataTypes.TOTAL_FEMALE,
                value=int(case_dict['Confirmed']['ByGender']['female']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )

            for state_name, value in case_dict['Confirmed']['ByState'].items():
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='VE',
                    region_child=state_name,
                    datatype=DataTypes.TOTAL,
                    value=int(value),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            for agerange, value in case_dict['Confirmed']['ByAgeRange'].items():
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent=None,
                    region_child='VE',
                    agerange=agerange,
                    datatype=DataTypes.TOTAL,
                    value=int(value),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r

if __name__ == '__main__':
    from pprint import pprint
    pprint(VEData().get_datapoints())
