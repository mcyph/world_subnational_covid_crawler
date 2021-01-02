# https://www.covid19data.com.au/data-notes
# https://github.com/pappubahry/AU_COVID19

import csv
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_crawlers._base_classes.GithubRepo import GithubRepo
from _utility.get_package_dir import get_overseas_dir


class AUCovid19Data(GithubRepo):
    SOURCE_URL = 'https://github.com/pappubahry/AU_COVID19'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'au_covid_19_data'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'au' / 'AU_COVID19',
                            github_url='https://github.com/pappubahry/AU_COVID19')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={},
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_sources())
        r.extend(self._get_deaths())
        r.extend(self._get_recovered())
        r.extend(self._get_cases())
        r.extend(self._get_tests())
        return r

    def _get_sources(self):
        r = self.sdpf()
        sources = {
            'at_sea': DataTypes.SOURCE_CRUISE_SHIP,
            'overseas': DataTypes.SOURCE_OVERSEAS,
            'interstate': DataTypes.SOURCE_INTERSTATE,
            'local_contact': DataTypes.SOURCE_CONFIRMED,
            'local_unknown': DataTypes.SOURCE_COMMUNITY,
            'under_investigation': DataTypes.SOURCE_UNDER_INVESTIGATION
        }

        for fnam, state in (
            ('time_series_act_sources.csv', 'au-act'),
            ('time_series_vic_sources.csv', 'au-vic'),
            ('time_series_nsw_sources.csv', 'au-nsw'),
            ('time_series_wa_sources.csv', 'au-wa'),
        ):
            with open(self.get_path_in_dir(fnam),
                      'r', encoding='utf-8') as f:
                for item in csv.DictReader(f):
                    date = self.convert_date(item['date'])
                    del item['date']

                    for source, value in item.items():
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='AU',
                            region_child=state,
                            datatype=sources[source],
                            value=int(value),
                            date_updated=date
                        )
        return r

    def _get_deaths(self):
        r = self.sdpf()

        with open(self.get_path_in_dir('time_series_deaths.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])
                del item['Date']

                for state, value in item.items():
                    if state == 'Total':
                        r.append(
                            region_schema=Schemas.ADMIN_0,
                            region_parent='',
                            region_child='AU',
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(value),
                            date_updated=date
                        )
                    else:
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='AU',
                            region_child='AU-%s' % state,
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(value),
                            date_updated=date
                        )
        return r

    def _get_recovered(self):
        r = self.sdpf()

        with open(self.get_path_in_dir('time_series_recovered.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])
                del item['Date']

                for state, value in item.items():
                    if not value:
                        continue

                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='AU',
                        region_child='AU-%s' % state,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(value),
                        date_updated=date
                    )
        return r

    def _get_cases(self):
        r = self.sdpf()

        with open(self.get_path_in_dir('time_series_cases.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])
                del item['Date']

                for state, value in item.items():
                    if state == 'Total':
                        r.append(
                            region_schema=Schemas.ADMIN_0,
                            region_parent='',
                            region_child='AU',
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date
                        )
                    else:
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='AU',
                            region_child='AU-%s' % state,
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date
                        )
        return r

    def _get_tests(self):
        r = self.sdpf()

        with open(self.get_path_in_dir('time_series_tests.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])
                del item['Date']

                for state, value in item.items():
                    if 'pending' in state:
                        continue
                    elif not value:
                        continue

                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='AU',
                        region_child='AU-%s' % state,
                        datatype=DataTypes.TESTS_TOTAL,
                        value=int(value),
                        date_updated=date
                    )
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(AUCovid19Data().get_datapoints())
