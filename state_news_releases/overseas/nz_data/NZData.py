import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_NZ_DHB,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP
)
from covid_19_au_grab.state_news_releases.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class NZData(GithubRepo):
    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'nz' / 'nz-covid19-data' / 'data',
                            github_url='https://github.com/nzherald/nz-covid19-data')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_days())
        r.extend(self._get_cases())
        r.extend(self._get_dhb_cases())
        return r

    def _get_cases(self):
        r = []

        # Reported	Sex	Age	DHB	Overseas travel	Last country before return	Flight number	Flight departure date	Arrival date	Origin	Status
        # 2020-02-26	Female	60 to 69	Auckland	Yes	Indonesia	EK450	2020-02-25T00:00:00Z	2020-02-26T00:00:00Z	Overseas	Confirmed

        dhb = Counter()
        origins = Counter()
        age_groups = Counter()
        gender_balances = Counter()

        with open(self.get_path_in_dir('cases.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                if item['Status'] == 'Probable':
                    # HACK: We won't count cases only deemed probable for now! =========================================
                    continue
                assert item['Status'] == 'Probable'

                date = self.convert_date(item['Reported'])

                if item['Sex'] == 'Male':
                    gender_balances[date, DT_TOTAL_MALE] += 1
                elif item['Sex'] == 'Female':
                    gender_balances[date, DT_TOTAL_FEMALE] += 1
                else:
                    raise Exception

                if item['Origin'] == 'Overseas':
                    origins[date, DT_SOURCE_OVERSEAS] += 1
                else:
                    raise Exception(item['Origin'])

        for (date, datatype), value in gender_balances.items():
            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                region=item['DHB'],
                agerange=item['Age'].replace(' to ', '-'),
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, datatype, agerange), value in age_groups.items():
            r.append(DataPoint(
                datatype=datatype,
                agerange=agerange.replace(' to ', '-'),
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=datatype,
                region=item['DHB'],
                agerange=agerange.replace(' to ', '-'),
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, datatype), value in origins.items():
            r.append(DataPoint(
                datatype=datatype,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=datatype,
                region=item['DHB'],
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, datatype, region), value in dhb.items():
            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=datatype,
                region=region,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        return r

    def _get_days(self):
        with open(self.get_path_in_dir('days.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                pass

    def _get_dhb_cases(self):
        with open(self.get_path_in_dir('dhb-cases.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                pass
