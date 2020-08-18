import json
from collections import Counter

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_NZ_DHB,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class NZData(GithubRepo):
    SOURCE_URL = 'https://github.com/philiprenich/nz-covid19-data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'nz_moh'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'nz' / 'nz-covid19-data',
                            github_url='https://github.com/philiprenich/nz-covid19-data')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases())
        #r.extend(self._get_days())
        #r.extend(self._get_dhb_cases())
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

        with open(self.get_path_in_dir('nz-covid-cases.json'),
                  'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        for status, items in (
            ('Confirmed', data['confirmed']),
            ('Probable', data['probable'])
        ):
            for item in items:
                if status == 'Probable':
                    # HACK: We won't count cases only deemed probable for now! =========================================
                    continue
                assert status == 'Confirmed', item['Status']

                print(item)

                date = self.convert_date(item['Date notified of potential case'].split('T')[0])
                agerange = item['Age group'].strip().replace(' to ', '-') or 'Unknown'

                # Gender balances
                if 'Sex' in item:
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
                if 'Overseas travel' in item and item['Overseas travel'].strip():
                    if item['Overseas travel'] == 'Yes':
                        origins[date, DT_SOURCE_OVERSEAS] += 1
                        origins_by_dhb[date, DT_SOURCE_OVERSEAS, item['DHB']] += 1
                        origins_by_agerange[date, DT_SOURCE_OVERSEAS, agerange] += 1
                    elif item['Overseas travel'] == 'No':
                        origins[date, DT_SOURCE_CONFIRMED] += 1
                        origins_by_dhb[date, DT_SOURCE_CONFIRMED, item['DHB']] += 1
                        origins_by_agerange[date, DT_SOURCE_CONFIRMED, agerange] += 1
                    else:
                        raise Exception(item['Overseas travel'])
                else:
                    origins[date, DT_SOURCE_COMMUNITY] += 1
                    origins_by_dhb[date, DT_SOURCE_COMMUNITY, item['DHB']] += 1
                    origins_by_agerange[date, DT_SOURCE_COMMUNITY, agerange] += 1

                # Age groups
                age_groups[date, agerange] += 1
                age_groups_by_dhb[date, agerange, item['DHB']] += 1

        # Whole of NZ counters
        cumulative = Counter()
        for (date, datatype), value in sorted(gender_balances.items()):
            cumulative[datatype] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='New Zealand',
                datatype=datatype,
                value=cumulative[datatype],
                date_updated=date,
                source_url=self.github_url
            ))

        cumulative = Counter()
        for (date, agerange), value in sorted(age_groups.items()):
            cumulative[agerange] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='New Zealand',
                datatype=DT_TOTAL,
                agerange=agerange,
                value=cumulative[agerange],
                date_updated=date,
                source_url=self.github_url
            ))

        cumulative = Counter()
        for (date, datatype), value in sorted(origins.items()):
            cumulative[datatype] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='New Zealand',
                datatype=datatype,
                value=cumulative[datatype],
                date_updated=date,
                source_url=self.github_url
            ))

        cumulative = Counter()
        for (date, datatype, region_child), value in sorted(dhb.items()):
            cumulative[datatype, region_child] += value
            r.append(DataPoint(
                region_schema=SCHEMA_NZ_DHB,
                region_parent='NZ',
                region_child=region_child,
                datatype=datatype,
                value=cumulative[datatype, region_child],
                date_updated=date,
                source_url=self.github_url
            ))

        # Regional counters
        cumulative = Counter()
        for (date, datatype, region_child), value in sorted(origins_by_dhb.items()):
            cumulative[datatype, region_child] += value
            r.append(DataPoint(
                region_schema=SCHEMA_NZ_DHB,
                region_parent='NZ',
                region_child=region_child,
                datatype=datatype,
                value=cumulative[datatype, region_child],
                date_updated=date,
                source_url=self.github_url
            ))

        cumulative = Counter()
        for (date, agerange, region_child), value in sorted(age_groups_by_dhb.items()):
            cumulative[agerange, region_child] += value
            r.append(DataPoint(
                region_schema=SCHEMA_NZ_DHB,
                region_parent='NZ',
                region_child=region_child,
                datatype=DT_TOTAL,
                agerange=agerange,
                value=cumulative[agerange, region_child],
                date_updated=date,
                source_url=self.github_url
            ))

        cumulative = Counter()
        for (date, datatype, region_child), value in sorted(gender_balances_by_dhb.items()):
            cumulative[datatype, region_child] += value
            r.append(DataPoint(
                region_schema=SCHEMA_NZ_DHB,
                region_parent='NZ',
                region_child=region_child,
                datatype=datatype,
                value=cumulative[datatype, region_child],
                date_updated=date,
                source_url=self.github_url
            ))

        # Agerange counters
        cumulative = Counter()
        for (date, datatype, agerange), value in sorted(origins_by_agerange.items()):
            cumulative[datatype, agerange] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='New Zealand',
                datatype=datatype,
                agerange=agerange,
                value=cumulative[datatype, agerange],
                date_updated=date,
                source_url=self.github_url
            ))

        cumulative = Counter()
        for (date, datatype, agerange), value in sorted(gender_balances_by_agerange.items()):
            cumulative[datatype, agerange] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='New Zealand',
                datatype=datatype,
                agerange=agerange,
                value=cumulative[datatype, agerange],
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
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='New Zealand',
                    datatype=DT_NEW,
                    value=int(item['confirmed']),
                    date_updated=date,
                    source_url=self.github_url
                ))
                
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='New Zealand',
                    datatype=DT_TOTAL,
                    value=int(item['totalConfirmed']),
                    date_updated=date,
                    source_url=self.github_url
                ))

                if item['totalRecovered'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_STATUS_RECOVERED,
                        value=int(item['totalRecovered']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['inHospitalNow'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['inHospitalNow']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['inIcu'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['inIcu']),
                        date_updated=date,
                        source_url=self.github_url
                    ))
                if item['totalDeaths'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_STATUS_DEATHS,
                        value=int(item['totalDeaths']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['overseas'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_SOURCE_OVERSEAS,
                        value=int(item['overseas']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['contact'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_SOURCE_CONFIRMED,
                        value=int(item['contact']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['investigating'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
                        datatype=DT_SOURCE_UNDER_INVESTIGATION,
                        value=int(item['investigating']),
                        date_updated=date,
                        source_url=self.github_url
                    ))

                if item['community'] != 'NA':
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='New Zealand',
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
                    region_schema=SCHEMA_NZ_DHB,
                    region_parent='NZ',
                    region_child=item['DHB'],
                    datatype=DT_TOTAL,
                    value=int(item['Count']),
                    date_updated=self.convert_date(item['Date']),
                    source_url=self.github_url
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(NZData().get_datapoints())
