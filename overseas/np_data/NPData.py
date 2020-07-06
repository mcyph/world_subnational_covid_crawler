import csv
import json
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1, SCHEMA_NP_DISTRICT,
    DT_TESTS_TOTAL, SCHEMA_ADMIN_0,
    DT_TOTAL, DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_DOMESTIC, DT_SOURCE_OVERSEAS,
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)
from covid_19_au_grab.geojson_data.LabelsToRegionChild import (
    LabelsToRegionChild
)

ltrc = LabelsToRegionChild()


def _get_district(province, district):
    province = province.lower()
    district = district.lower()
    district = district.replace('makwanpur', 'makawanpur')
    district = district.replace('dhanusa', 'dhanusha')
    district = district.replace('kavrepalanchok', 'kabhrepalanchok')
    district = district.replace('chitwan', 'chitawan')
    return ltrc.get_by_label(SCHEMA_NP_DISTRICT, province, district)


class NPData(URLBase):
    SOURCE_URL = 'https://bipad.gov.np'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'np_bipad'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'np' / 'data',
            urls_dict={
                'quarantine_district_data.json': URL('https://bipad.gov.np/api/v1/covid19-quarantineinfo/'
                                                     '?distinct=district',
                                                     static_file=False),
                'quarantine_history.json': URL('https://bipad.gov.np/api/v1/covid19-quarantineinfo/'
                                               '?fields=province%2Cdistrict%2Cid%2Cquarantined_count%2Creported_on&limit=-1',
                                               static_file=False),
                'cases.json': URL('https://bipad.gov.np/api/v1/covid19-case/',
                                  static_file=False)
            }
        )
        self.update()

        self._district_map = {}  # {id: (en, np), ...}
        self._province_map = {}

    def get_datapoints(self):
        r = []
        r.extend(self.get_quarantine_district_data())
        r.extend(self.get_district_history())
        r.extend(self.get_cases())
        return r

    def get_cases(self):
        # {
        #     "count": 15784,
        #     "next": "https://bipad.gov.np/api/v1/covid19-case/?limit=1000&offset=1000",
        #     "previous": null,
        #     "latestModifiedOn": "2020-07-05T16:51:37.447770+05:45",
        #     "results": [
        #         {
        #             "id": 22,
        #             "province": 1,
        #             "district": 14,
        #             "municipality": 14007,
        #             "createdOn": "2020-04-17T19:54:32.704295+05:45",
        #             "modifiedOn": "2020-05-06T20:10:59.216325+05:45",
        #             "label": "COV-NPL-22",
        #             "gender": "male",
        #             "age": 28,
        #             "point": {
        #                 "type": "Point",
        #                 "coordinates": [
        #                     86.683718071875,
        #                     26.813987534074418
        #                 ]
        #             },
        #             "occupation": null,
        #             "reportedOn": "2020-04-17",
        #             "recoveredOn": "2020-05-06",
        #             "deathOn": null,
        #             "currentState": "recovered",
        #             "isReinfected": false,
        #             "source": "https://www.mohp.gov.np/eng/",
        #             "comment": "",
        #             "type": "local_transmission",
        #             "nationality": 3,
        #             "ward": 2781,
        #             "relatedTo": []
        #         },
        #
        # https://bipad.gov.np/api/v1/covid19-case/

        r = []
        data = json.loads(self.get_text('cases.json',
                                        include_revision=True))

        by_total = Counter()
        by_gender = Counter()
        by_age = Counter()
        by_infection_source = Counter()
        by_province = Counter()
        by_district = Counter()
        by_deceased = Counter()

        infection_sources = {
            'local_transmission': DT_SOURCE_DOMESTIC,
            'imported': DT_SOURCE_OVERSEAS,
        }
        genders = {
            'male': DT_TOTAL_MALE,
            'female': DT_TOTAL_FEMALE
        }

        def age_to_range(age):
            for x in range(0, 100, 10):
                if x <= age < x+10:
                    return f'{x}-{x+9}'
            raise Exception()

        for result in data['results']:
            print(result)
            date = self.convert_date(result['reportedOn'])
            province = f'NP-P{result["province"]}'
            district = _get_district(province, self._district_map[result['district']][0])

            by_total[date] += 1

            if result['gender']:
                by_gender[date, genders[result['gender'].lower()]] += 1

            if result['type']:
                by_infection_source[date, infection_sources[result['type']]] += 1

            if result['age']:
                agerange = age_to_range(int(result['age']))
                by_age[date, agerange] += 1

            by_province[date, province] += 1
            by_district[date, province, district] += 1

            if result['deathOn']:
                deceased_date = self.convert_date(result['deathOn'])
                by_deceased[deceased_date] += 1

        cumulative = 0
        for date, value in sorted(by_total.items()):
            cumulative += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='NP',
                datatype=DT_TOTAL,
                value=cumulative,
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[gender] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='NP',
                datatype=gender,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, infection_source), value in sorted(by_infection_source.items()):
            cumulative[infection_source] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='NP',
                datatype=infection_source,
                value=cumulative[infection_source],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, agerange), value in sorted(by_age.items()):
            cumulative[agerange] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='NP',
                agerange=agerange,
                datatype=DT_TOTAL,
                value=cumulative[agerange],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, province), value in sorted(by_province.items()):
            cumulative[province] += value
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='NP',
                region_child=province,
                datatype=DT_TOTAL,
                value=cumulative[province],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        cumulative = Counter()
        for (date, province, district), value in sorted(by_district.items()):
            cumulative[province, district] += value
            r.append(DataPoint(
                region_schema=SCHEMA_NP_DISTRICT,
                region_parent=province,
                region_child=district,
                datatype=DT_TOTAL,
                value=cumulative[province, district],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r

    def get_quarantine_district_data(self):
        # {"count":77,"next":null,"previous":null,"latestModifiedOn":"2020-07-04T11:09:14.424805+05:45",
        # "results":[
        #   {"id":4918,"province":1,"districtName":"Panchthar",
        #    "provinceName":"Province 1","districtNameNe":"पाँचथर",
        #    "provinceNameNe":"प्रदेश नं .१",
        #    "createdOn":"2020-07-03T14:43:27.797177+05:45",
        #    "modifiedOn":"2020-07-03T14:47:19.271789+05:45",
        #    "reportedOn":"2020-07-03",
        #    "testedCount":0,
        #    "testedTodayCount":0,
        #    "releasedCount":0,
        #    "ambulanceCount":23,
        #    "quarantineBedCount":721,
        #    "hasQuarantinedSickFoodService":false,
        #    "quarantinedCount":66,
        #    "quarantinedMaleCount":56,
        #    "quarantinedFemaleCount":10,
        #    "quarantinedSickCount":0,
        #    "quarantinedReleaseCount":51,
        #    "isolatedBedCount":36,
        #    "isolatedCount":0,
        #    "isolatedMaleCount":0,
        #    "isolatedFemaleCount":0,
        #    "isolatedSickCount":0,
        #    "isolatedReleaseCount":0,
        #    "swabCollectedCount":52,
        #    "swabTestedCount":74,
        #    "ppeCount":5,
        #    "reliefProvidedCount":6612,
        #    "reliefProvidedTodayCount":0,
        #    "remarks":"",
        #    "isVerified":true,
        #    "district":2},
        # https://bipad.gov.np/api/v1/covid19-quarantineinfo/?distinct=district

        r = []
        data = json.loads(self.get_text('quarantine_district_data.json',
                                        include_revision=True))

        for result in data['results']:
            print(result)
            date = self.convert_date(result['reportedOn'])
            province = f'NP-P{result["province"]}'

            self._district_map[result['district']] = (result['districtName'], result['districtNameNe'])
            self._province_map[result['province']] = (result['provinceName'], result['provinceNameNe'])

            r.append(DataPoint(
                region_schema=SCHEMA_NP_DISTRICT,
                region_parent=province,
                region_child=_get_district(province, result['districtName']),
                datatype=DT_TESTS_TOTAL,
                value=result['testedCount'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r

    def get_district_history(self):
        # {"count":4537,"next":null,"previous":null,"latestModifiedOn":"2020-07-04T11:09:14.424805+05:45",
        # "results":[{"id":1111,"province":5,"reportedOn":"2020-04-14","quarantinedCount":223,"district":65},
        # https://bipad.gov.np/api/v1/covid19-quarantineinfo/?fields=province%2Cdistrict%2Cid%2Cquarantined_count%2Creported_on&limit=-1
        r = []
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(NPData().get_datapoints())
