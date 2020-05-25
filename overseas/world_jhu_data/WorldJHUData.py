import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_ADMIN_1,
    SCHEMA_ADMIN_0,
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


class WorldJHUData(GithubRepo):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'world_jhu' / 'COVID-19',
                            github_url='')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_us_counties())
        r.extend(self._get_us_states())
        return r

    def _get_daily_reports_us(self):
        pass

    def _get_daily_reports_global(self):
        pass

    def _get_confirmed_global(self):
        r = []

        # time_series_covid19_confirmed_global.csv

        with open(self.get_path_in_dir('us-counties.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

        return r

    def _get_confirmed_us(self):
        r = []

        # time_series_covid19_confirmed_US.csv

        with open(self.get_path_in_dir('us-states.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

        return r
    
    def _get_deaths_global(self):
        r = []

        # time_series_covid19_deaths_global.csv

        with open(self.get_path_in_dir('us-states.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

        return r
    
    def _get_deaths_us(self):
        r = []

        # time_series_covid19_deaths_US.csv

        with open(self.get_path_in_dir('us-states.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

        return r
    
    def _get_recovered_global(self):
        r = []

        # time_series_covid19_recovered_global.csv

        with open(self.get_path_in_dir('us-states.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(WorldJHUData().get_datapoints())
