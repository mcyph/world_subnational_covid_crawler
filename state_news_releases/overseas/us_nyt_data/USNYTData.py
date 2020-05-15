# https://github.com/nytimes/covid-19-data

import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_US_COUNTY, SCHEMA_US_STATE,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.state_news_releases.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class USNYTData(GithubRepo):
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
                    statename=item['state'],
                    schema=SCHEMA_US_COUNTY,
                    datatype=DT_TOTAL,
                    region=item['county'],
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))

                r.append(DataPoint(
                    statename=item['state'],
                    schema=SCHEMA_US_COUNTY,
                    datatype=DT_STATUS_DEATHS,
                    region=item['county'],
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
                    schema=SCHEMA_US_STATE,
                    datatype=DT_TOTAL,
                    region=item['state'],
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))

                r.append(DataPoint(
                    schema=SCHEMA_US_STATE,
                    datatype=DT_TOTAL,
                    region=item['state'],
                    value=int(item['deaths']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                ))
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(USNYTData().get_datapoints())
