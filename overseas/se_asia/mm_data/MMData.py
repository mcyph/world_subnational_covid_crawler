# https://docs.google.com/spreadsheets/d/1-Csmn_rXTQvnkJR8tnFkQEyKBnhq8fz-YxyHidhONiI/edit#gid=0
# https://mohs.gov.mm/Main/content/publication/2019-ncov
# humdata also supports Myanmar, but last check it was updated 14 May (on 1st June)

import csv
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    DT_TOTAL, DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class MMData(URLBase):
    # Remember to send e-mail to below link!!! =======================================================================================
    SOURCE_URL = 'https://data.covidmyanmar.com'
    SOURCE_DESCRIPTION = 'Dataset created by Dr.Nyein Chan Ko Ko (covidmyanmar.com) dr.nyeinchankoko@gmail.com'
    SOURCE_ID = 'mm_covidmyanmar'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'mm' / 'data',
             urls_dict={
                 'case_reports.csv': URL(
                     'https://docs.google.com/spreadsheet/ccc?key=1-Csmn_rXTQvnkJR8tnFkQEyKBnhq8fz-YxyHidhONiI&output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        f = self.get_file('case_reports.csv',
                          include_revision=True)

        by_total = Counter()
        by_gender = Counter()
        by_deceased = Counter()
        by_age = Counter()
        by_province = Counter()

        def age_to_range(age):
            for x in range(0, 100, 10):
                if x <= age < x+10:
                    return f'{x}-{x+9}'
            raise Exception()

        for item in csv.DictReader(f):
            print(item)

            if item['lab tested date'].count('/') == 1:
                item['lab tested date'] += '/2020'
            if item['announced date'].count('/') == 1:
                item['announced date'] += '/2020'

            date = self.convert_date(
                item['lab tested date'].strip() or
                item['announced date'].strip()
            )
            iso_3166_2 = item['region_code'].strip()

            by_total[date] += 1

            if item['sex'] != 'n/a':
                gender = {
                    'm': DT_TOTAL_MALE,
                    'f': DT_TOTAL_FEMALE
                }[item['sex'].strip()]
                by_gender[date, gender] += 1

            if item['age'] != 'n/a':
                by_age[date, age_to_range(int(float(item['age'])))] += 1

            by_province[date, iso_3166_2] += 1

            if item['discharged/deceased date'].strip():
                is_deceased = bool(item['cause of death'].strip())
                if is_deceased:
                    if item['discharged/deceased date'].count('/') == 1:
                        item['discharged/deceased date'] += '/2020'

                    dd_date = self.convert_date(item['discharged/deceased date'])
                    by_deceased[dd_date] += 1

        r = []

        cumulative = 0
        for date, value in sorted(by_total.items()):
            cumulative += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MM',
                datatype=DT_TOTAL,
                value=cumulative,
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[gender] += 1
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MM',
                datatype=DT_TOTAL,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, agerange), value in sorted(by_age.items()):
            cumulative[agerange] += 1
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MM',
                agerange=agerange,
                datatype=DT_TOTAL,
                value=cumulative[agerange],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, region_child), value in sorted(by_province.items()):
            cumulative[region_child] += 1
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='MM',
                region_child=region_child,
                datatype=DT_TOTAL,
                value=cumulative[region_child],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MMData().get_datapoints())