# https://www.covid19data.com.au/data-notes
# https://github.com/M3IT/COVID-19_Data

import csv
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_crawlers._base_classes.GithubRepo import GithubRepo
from _utility.get_package_dir import get_overseas_dir


class Covid19DataComAUData(GithubRepo):
    SOURCE_URL = 'https://github.com/M3IT/COVID-19_Data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'au_covid_19_data_com_au'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'au' / 'COVID-19_Data',
                            github_url='https://github.com/M3IT/COVID-19_Data')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={},
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cumulative())
        return r

    def _get_cumulative(self):
        # "date","confirmed","deaths","tests","positives","recovered","hosp","icu",
        # "vent","population","administrative_area_level","administrative_area_level_1",
        # "administrative_area_level_2","administrative_area_level_3","id","state_abbrev"
        # 2020-01-25,4,0,0,0,0,0,0,0,25459470,1,"Australia",NA,NA,"99999999",NA
        # 2020-01-26,4,0,0,0,0,0,0,0,25459470,1,"Australia",NA,NA,"99999999",NA
        # 2020-01-27,5,0,0,0,0,0,0,0,25459470,1,"Australia",NA,NA,"99999999",NA

        r = self.sdpf()

        with open(self.get_path_in_dir('Data/COVID_AU_cumulative.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                assert item['administrative_area_level_1'] == 'Australia', \
                    item['administrative_area_level_1']
                admin1 = item['administrative_area_level_2']
                if admin1 == 'NA':
                    admin1 = None
                assert item['administrative_area_level_3'] == 'NA'

                d = {}
                d[DataTypes.TOTAL] = int(item['confirmed'])
                d[DataTypes.STATUS_DEATHS] = int(item['deaths'])
                d[DataTypes.TESTS_TOTAL] = int(item['tests'])
                d[DataTypes.CONFIRMED] = int(item['positives'])
                d[DataTypes.STATUS_RECOVERED] = int(item['recovered'])
                d[DataTypes.STATUS_HOSPITALIZED] = int(float(item['hosp']))
                d[DataTypes.STATUS_ICU] = int(item['icu'])
                d[DataTypes.STATUS_ICU_VENTILATORS] = int(item['vent'])

                if d[DataTypes.STATUS_RECOVERED] and \
                   d[DataTypes.STATUS_DEATHS] and False:
                    d[DataTypes.STATUS_ACTIVE] = d[DataTypes.TOTAL] - \
                                                 d[DataTypes.STATUS_RECOVERED] - \
                                                 d[DataTypes.STATUS_DEATHS]

                for datatype, value in d.items():
                    if admin1:
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='AU',
                            region_child=admin1,
                            datatype=datatype,
                            value=value,
                            date_updated=date
                        )
                    else:
                        r.append(
                            region_schema=Schemas.ADMIN_0,
                            region_parent='',
                            region_child='AU',
                            datatype=datatype,
                            value=value,
                            date_updated=date
                        )
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(Covid19DataComAUData().get_datapoints())
