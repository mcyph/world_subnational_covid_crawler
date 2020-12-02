# https://data.go.th/en/dataset/covid-19-daily
import csv
import json
from collections import Counter

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.covid_db.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import (
    get_overseas_dir, get_package_dir
)
from covid_19_au_grab.world_geodata.LabelsToRegionChild import (
    LabelsToRegionChild
)

ltrc = LabelsToRegionChild()


def get_districts_map():
    r = {}

    with open(get_package_dir() /
              'covid_crawlers' / 'se_asia' / 'th_data' / 'th_districts.csv',
              'r', encoding='utf-8') as f:

        for item in csv.DictReader(f, delimiter='\t'):
            #print(item)
            if item['Status'].strip() not in ('District', 'City District'):
                continue

            assert r.get(item['Native'], item['Name'].strip()) == item['Name'].strip(), \
                (item, r[item['Native']])
            r[item['Native'].strip()] = item['Name'].strip()
            r[item['Native'].strip().replace('เขต', '')] = item['Name'].strip()
            r[item['Native'].strip().replace('อำเภอ', '')] = item['Name'].strip()

    return r


class THData(URLBase):
    SOURCE_URL = 'https://covid19.th-stat.com/th/api'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'th_open_data'

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
        r.extend(self._get_cases())
        r.extend(self._get_sum())
        r.extend(self._get_timeline())
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

        def age_to_range(age):
            for x in range(0, 100, 10):
                if x <= age < x+10:
                    return f'{x}-{x+9}'
            raise Exception()

        text = self.get_text('cases.json',
                             include_revision=True)
        data = json.loads(text)
        not_found = Counter()

        for case_dict in data['Data']:
            #print(case_dict)
            date = self.convert_date(case_dict['ConfirmDate'].split()[0])
            agerange = age_to_range(case_dict['Age'])
            gender = {
                'Male': DataTypes.TOTAL_MALE,
                'Female': DataTypes.TOTAL_FEMALE
            }[case_dict['GenderEn']]

            if case_dict['ProvinceEn'].lower() == 'unknown':
                province = 'unknown'
            else:
                province = ltrc.get_by_label(
                    Schemas.ADMIN_1, 'TH', case_dict['ProvinceEn']
                )

            by_total[date] += 1
            by_age[date, agerange] += 1
            by_gender[date, gender] += 1
            by_province[date, province] += 1

            if case_dict['District'].strip() and case_dict['District'] not in (
                'เมือง', 'กระทู้', 'คลองจั่น', 'พัฒนาการ', 'รามอินทรา',
                'จตุุจักร', 'บางลำพู', 'ไม่ระบุ', 'สะเตง', 'รังสิต', 'ท่าอิฐ',
                'ศาลาธรรมสพน์',
            ):
                try:
                    district = ltrc.get_by_label(
                        Schemas.TH_DISTRICT, province, case_dict['District']
                    )
                    by_district[date, province, district] += 1
                    #print('FOUND:', district)
                except KeyError:
                    #print(province)
                    try:
                        district = self.districts_map[case_dict['District']]
                        by_district[date, province, district] += 1
                    except KeyError:
                        print("KEYERROR:", case_dict['District'])
                        not_found[case_dict['District']] += 1

        from pprint import pprint
        pprint(not_found)

        cumulative = 0
        for date, value in sorted(by_total.items()):
            cumulative += value
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                datatype=DataTypes.TOTAL,
                value=cumulative,
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, age), value in sorted(by_age.items()):
            cumulative[age] += value
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                agerange=age,
                datatype=DataTypes.TOTAL,
                value=cumulative[age],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[gender] += value
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                datatype=gender,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, province), value in sorted(by_province.items()):
            cumulative[province] += value
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='TH',
                region_child=province,
                datatype=DataTypes.TOTAL,
                value=cumulative[province],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, province, district), value in sorted(by_district.items()):
            cumulative[province, district] += value
            r.append(DataPoint(
                region_schema=Schemas.TH_DISTRICT,
                region_parent=province,
                region_child=district,
                datatype=DataTypes.TOTAL,
                value=cumulative[province, district],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r

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

        text = self.get_text('timeline.json',
                             include_revision=True)
        data = json.loads(text)

        for item in data['Data']:
            if not item['Date']:
                continue
            date = self.convert_date(item['Date'], formats=('%m/%d/%Y',))

            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                datatype=DataTypes.TOTAL,
                value=int(item['Confirmed']),
                date_updated=date,
                source_url=self.SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                datatype=DataTypes.STATUS_RECOVERED,
                value=int(item['Recovered']),
                date_updated=date,
                source_url=self.SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                datatype=DataTypes.STATUS_HOSPITALIZED,
                value=int(item['Hospitalized']),
                date_updated=date,
                source_url=self.SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='TH',
                datatype=DataTypes.STATUS_DEATHS,
                value=int(item['Deaths']),
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r

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

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(THData().get_datapoints())
