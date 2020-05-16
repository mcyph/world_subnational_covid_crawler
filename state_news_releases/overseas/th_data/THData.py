# https://data.go.th/en/dataset/covid-19-daily
import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_TH_PROVINCE, SCHEMA_TH_DISTRICT,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


def get_districts_map():
    r = {}

    with open(get_package_dir() / 'state_news_releases' /
              'overseas' / 'th_data' / 'th_districts.csv',
              'r', encoding='utf-8') as f:

        for item in csv.DictReader(f):
            if item['Status'].strip() != 'District':
                continue

            assert not item['Native'] in r
            r[item['Native'].strip()] = item['Name'].strip()

    return r


class THData(URLBase):
    SOURCE_URL = 'https://covid19.th-stat.com/th/api'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'th' / 'data',
             urls_dict={
                 'cases.json': URL('https://covid19.th-stat.com/api/open/cases',
                                   static_file=False),
                 'timeline.json': URL('https://covid19.th-stat.com/api/open/timeline',
                                      static_file=False),
                 'sum.json': URL('https://covid19.th-stat.com/api/open/cases/sum',
                                 static_file=False)
            }
        )
        self.districts_map = get_districts_map()
        self.update()

    def get_datapoints(self):
        r = []

        return r

    def _get_cases(self):
        # {"Data":[{
        #   "ConfirmDate":"2020-05-10 00:00:00",
        #   "No":"3009",
        #   "Age":80,
        #   "Gender":"\u0e0a\u0e32\u0e22",
        #   "GenderEn":"Male",
        #   "Nation":"\u0e44\u0e17\u0e22",
        #   "NationEn":"Thai",
        #   "Province":"\u0e19\u0e23\u0e32\u0e18\u0e34\u0e27\u0e32\u0e2a",
        #   "ProvinceId":25,
        #   "District":"\u0e41\u0e27\u0e49\u0e07",
        #   "ProvinceEn":"Narathiwat",
        #   "Detail":null}, ...
        r = []

        by_total = Counter()

        by_district = Counter()
        by_province = Counter()
        by_age = Counter()
        by_gender = Counter()

        by_age_gender = Counter()

        by_district_age = Counter()
        by_district_gender = Counter()

        by_province_age = Counter()
        by_province_gender = Counter()

        def age_to_range(age):
            for x in range(0, 100, 10):
                if x <= age < x+10:
                    return f'{x}-{x+9}'
            raise Exception()

        for case_dict in data['Data']:
            date = self.convert_date(case_dict['ConfirmDate'].split()[0])
            agerange = age_to_range(case_dict['Age'])
            district = self.districts_map[case_dict['District']]
            gender = {'Male': DT_TOTAL_MALE,
                      'Female': DT_TOTAL_FEMALE}[case_dict['GenderEn']]

            by_total[date] += 1
            by_age[date, agerange] += 1
            by_gender[date, gender] += 1
            by_district[date, district] += 1
            by_province[date, case_dict['ProvinceEn']] += 1

            by_age_gender[date, agerange, gender] += 1
            by_age_gender[date, agerange, gender] += 1

            r.append(DataPoint(
                schema=SCHEMA_TH_PROVINCE,
                datatype=DT_TOTAL
            ))
            r.append(DataPoint(
                schema=SCHEMA_TH_PROVINCE,
                datatype=DT_TOTAL_MALE
            ))
            r.append(DataPoint(
                schema=SCHEMA_TH_PROVINCE,
                datatype=DT_FEMALE
            ))


    def _get_timeline(self):
        # {"UpdateDate":"14\/05\/2020 11:35",
        #  "Source":"https:\/\/covid19.th-stat.com\/",
        #  "DevBy":"https:\/\/www.kidkarnmai.com\/",
        #  "SeverBy":"https:\/\/smilehost.asia\/",
        #  "Data":[{
        #      "Date":"01\/01\/2020",
        #      "NewConfirmed":0,
        #      "NewRecovered":0,
        #      "NewHospitalized":0,
        #      "NewDeaths":0,
        #      "Confirmed":0,
        #      "Recovered":0,
        #      "Hospitalized":0,
        #      "Deaths":0
        #  }, ...
        r = []


    def _get_sum(self):
        # {"Province":{"Bangkok":1547,"Phuket":220,...},
        #  "Nation":{"Thai":2674,"Burmese":56,"Unknown":36,"Chinese":34, ...},
        #  "Gender":{"Male":1635,"Female":1375},
        #  "LastData":"2020-05-10 00:00:00",
        #  "UpdateDate":"10\/05\/2020",
        #  "Source":"https:\/\/data.go.th\/dataset\/covid-19-daily",
        #  "DevBy":"https:\/\/www.kidkarnmai.com\/",
        #  "SeverBy":"https:\/\/smilehost.asia\/"}
        r = []


if __name__ == '__main__':
    THData()
