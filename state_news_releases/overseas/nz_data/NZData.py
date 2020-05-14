import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_NZ_DHB,
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


class NZData(GithubRepo):
    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'nz' / 'nz-covid19-data' / 'data',
                            github_url='https://github.com/nzherald/nz-covid19-data')
        self.update()

    def get_datapoints(self):
        r = []

        r.extend(self._get_cases())
        r.extend(self._get_days())
        r.extend(self._get_dhb_cases())
        return r

    def _get_cases(self):
        r = []

        # Reported	Sex	Age	DHB	Overseas travel	Last country before return	Flight number	Flight departure date	Arrival date	Origin	Status
        # 2020-02-26	Female	60 to 69	Auckland	Yes	Indonesia	EK450	2020-02-25T00:00:00Z	2020-02-26T00:00:00Z	Overseas	Confirmed

        # Whole of NZ non-age-specified counters
        origins = Counter()
        gender_balances = Counter()

        # Regional counters
        dhb = Counter()
        origins_by_dhb = Counter()
        age_groups_by_dhb = Counter()
        gender_balances_by_dhb = Counter()

        # Agerange counters
        age_groups = Counter()
        origins_by_agerange = Counter()
        gender_balances_by_agerange = Counter()

        with open(self.get_path_in_dir('cases.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                if item['Status'] == 'Probable':
                    # HACK: We won't count cases only deemed probable for now! =========================================
                    continue
                assert item['Status'] == 'Confirmed', item['Status']

                date = self.convert_date(item['Reported'])
                agerange = item['Age'].replace(' to ', '-')

                # Gender balances
                if item['Sex'] == 'Male':
                    gender_balances[date, DT_TOTAL_MALE] += 1
                    gender_balances_by_dhb[date, DT_TOTAL_MALE, item['DHB']] += 1
                    gender_balances_by_agerange[date, DT_TOTAL_MALE, agerange] += 1
                elif item['Sex'] == 'Female':
                    gender_balances[date, DT_TOTAL_FEMALE] += 1
                    gender_balances_by_dhb[date, DT_TOTAL_FEMALE, item['DHB']] += 1
                    gender_balances_by_agerange[date, DT_TOTAL_FEMALE, agerange] += 1
                elif item['Sex'] == 'NA':
                    pass  # Register in overall total only for now
                else:
                    raise Exception(item['Sex'])

                # Overall total
                gender_balances[date, DT_TOTAL] += 1
                gender_balances_by_dhb[date, DT_TOTAL, item['DHB']] += 1
                gender_balances_by_agerange[date, DT_TOTAL, agerange] += 1

                # Source of infection
                if item['Origin'] == 'Overseas':
                    origins[date, DT_SOURCE_OVERSEAS] += 1
                    origins_by_dhb[date, DT_SOURCE_OVERSEAS, item['DHB']] += 1
                    origins_by_agerange[date, DT_SOURCE_OVERSEAS, agerange] += 1
                elif item['Origin'] == 'In New Zealand':
                    origins[date, DT_SOURCE_CONFIRMED] += 1
                    origins_by_dhb[date, DT_SOURCE_CONFIRMED, item['DHB']] += 1
                    origins_by_agerange[date, DT_SOURCE_CONFIRMED, agerange] += 1
                elif item['Origin'] == 'Unknown':
                    origins[date, DT_SOURCE_COMMUNITY] += 1
                    origins_by_dhb[date, DT_SOURCE_COMMUNITY, item['DHB']] += 1
                    origins_by_agerange[date, DT_SOURCE_COMMUNITY, agerange] += 1
                else:
                    raise Exception(item['Origin'])

                # Age groups
                age_groups[date, agerange] += 1
                age_groups_by_dhb[date, agerange, item['DHB']] += 1

        # Whole of NZ counters
        for (date, datatype), value in gender_balances.items():
            r.append(DataPoint(
                datatype=datatype,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, agerange), value in age_groups.items():
            r.append(DataPoint(
                datatype=DT_TOTAL,
                agerange=agerange,
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

        for (date, datatype, region), value in dhb.items():
            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=datatype,
                region=region,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        # Regional counters
        for (date, datatype, region), value in origins_by_dhb.items():
            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=datatype,
                region=region,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, agerange, region), value in age_groups_by_dhb.items():
            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=DT_TOTAL,
                agerange=agerange,
                region=region,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, datatype, region), value in gender_balances_by_dhb.items():
            r.append(DataPoint(
                schema=SCHEMA_NZ_DHB,
                datatype=datatype,
                region=region,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        # Agerange counters
        for (date, datatype, agerange), value in origins_by_agerange.items():
            r.append(DataPoint(
                datatype=datatype,
                agerange=agerange,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        for (date, datatype, agerange), value in gender_balances_by_agerange.items():
            r.append(DataPoint(
                datatype=datatype,
                agerange=agerange,
                value=value,
                date_updated=date,
                source_url=self.github_url
            ))

        return r

    def _get_days(self):
        r = []

        # date,confirmed,totalConfirmed,probable,totalProbable,cases,totalCases,
        # recovered,totalRecovered,inHospitalNow,totalBeenInHospital,inIcu,deaths,
        # totalDeaths,overseas,contact,investigating,community,established,tag
        # 2020-02-28T00:00:00Z,1,1,NA,NA,1,1,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,Manual


        with open(self.get_path_in_dir('days.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'].split('T')[0])

                # Won't add probable for now
                r.append(DataPoint(
                    datatype=DT_NEW,
                    value=int(item['confirmed']),
                    date_updated=date,
                    source_url=self.github_url
                ))
                r.append(DataPoint(
                    datatype=DT_TOTAL,
                    value=int(item['totalConfirmed']),
                    date_updated=date,
                    source_url=self.github_url
                ))

                if item['totalRecovered'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_STATUS_RECOVERED,
                        value=int(item['totalRecovered']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['inHospitalNow'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['inHospitalNow']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['inIcu'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['inIcu']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['totalDeaths'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_STATUS_DEATHS,
                        value=int(item['totalDeaths']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['overseas'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_SOURCE_OVERSEAS,
                        value=int(item['overseas']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['contact'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_SOURCE_CONFIRMED,
                        value=int(item['contact']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['investigating'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_SOURCE_UNDER_INVESTIGATION,
                        value=int(item['investigating']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['community'] != 'NA':
                    r.append(DataPoint(
                        datatype=DT_SOURCE_COMMUNITY,
                        value=int(item['community']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

        return r

    def _get_dhb_cases(self):
        # DHB,Case Status,Count,Date
        # Auckland,Confirmed cases,43,2020-03-26
        r = []

        with open(self.get_path_in_dir('dhb-cases.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                if item['Case Status'] in ('Probable cases', 'Total cases'):
                    continue
                assert item['Case Status'] == 'Confirmed cases', \
                    item['Case Status']

                r.append(DataPoint(
                    datatype=DT_TOTAL,
                    schema=SCHEMA_NZ_DHB,
                    region=item['DHB'],
                    value=int(item['Count']),
                    date_updated=self.convert_date(item['Date']),
                    source_url=self.github_url
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(NZData().get_datapoints())
