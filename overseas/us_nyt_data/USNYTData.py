# https://github.com/nytimes/covid-19-data

import csv

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1,
    SCHEMA_US_COUNTY,
    DT_TOTAL, DT_STATUS_DEATHS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class USNYTData(GithubRepo):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'us_nytimes' / 'covid-19-data',
                            github_url='https://github.com/nytimes/covid-19-data')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_us_counties())
        r.extend(self._get_us_states())
        return r

    def _get_us_counties(self):
        r = []

        # date,county,state,fips,cases,deaths
        # 2020-01-21,Snohomish,Washington,53061,1,0
        # 2020-01-22,Snohomish,Washington,53061,1,0
        # 2020-01-23,Snohomish,Washington,53061,1,0
        # 2020-01-24,Cook,Illinois,17031,1,0

        with open(self.get_path_in_dir('us-counties.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_parent=item['state'],
                    region_schema=SCHEMA_US_COUNTY,
                    datatype=DT_TOTAL,
                    region_child=item['county'],
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))

                r.append(DataPoint(
                    region_parent=item['state'],
                    region_schema=SCHEMA_US_COUNTY,
                    datatype=DT_STATUS_DEATHS,
                    region_child=item['county'],
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))

        return r

    def _get_us_states(self):
        r = []

        # date,state,fips,cases,deaths
        # 2020-01-21,Washington,53,1,0
        # 2020-01-22,Washington,53,1,0
        # 2020-01-23,Washington,53,1,0
        # 2020-01-24,Illinois,17,1,0

        with open(self.get_path_in_dir('us-states.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='United States of America',
                    region_child=item['state'],
                    datatype=DT_TOTAL,
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='United States of America',
                    region_child=item['state'],
                    datatype=DT_TOTAL,
                    value=int(item['deaths']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(USNYTData().get_datapoints())
