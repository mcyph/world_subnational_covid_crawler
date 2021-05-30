# https://coronavirus.data.gov.uk/developers-guide

import datetime
from requests import get
from os import makedirs, listdir
from os.path import exists
from http import HTTPStatus
from json import loads, dumps

from _utility.cache_by_date import cache_by_date
from covid_crawlers._base_classes.URLBase import URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_crawlers.w_europe.uk_data.uk_place_map import place_map, ni_mappings
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from _utility.normalize_locality_name import normalize_locality_name
from covid_db.datatypes.DatapointMerger import DataPointMerger

"""
TODO: Assign some of these codes, of which some have been recently allocated:

Exception: Region child not found in GeoJSON: DataPoint(region_schema=1, region_parent='gb', region_child='bournemouth, christchurch and poole', date_updated='2020_08_15', datatype=3, agerange='', value=855, source_url='https://coronavirus.data.gov.uk/', text_match='') admin_1 gb bournemouth, christchurch and poole
Exception: Region child not found in GeoJSON: DataPoint(region_schema=1, region_parent='gb', region_child='gb-edh', date_updated='2020_08_16', datatype=3, agerange='', value=1848, source_url='https://coronavirus.data.gov.uk/', text_match='') admin_1 gb edinburgh
Exception: Region child not found in GeoJSON: DataPoint(region_schema=1, region_parent='gb', region_child='gb-rct', date_updated='2020_08_14', datatype=3, agerange='', value=1887, source_url='https://coronavirus.data.gov.uk/', text_match='') admin_1 gb rhondda cynon taf
Exception: Region child not found in GeoJSON: DataPoint(region_schema=1, region_parent='gb', region_child='gb-scb', date_updated='2020_08_16', datatype=3, agerange='', value=350, source_url='https://coronavirus.data.gov.uk/', text_match='') admin_1 gb scottish borders
Exception: Region child not found in GeoJSON: DataPoint(region_schema=1, region_parent='gb', region_child='gb-shn', date_updated='2020_08_15', datatype=3, agerange='', value=1252, source_url='https://coronavirus.data.gov.uk/', text_match='') admin_1 gb gb-shn
Exception: Region child not found in GeoJSON: DataPoint(region_schema=1, region_parent='gb', region_child='gb-wrl', date_updated='2020_08_15', datatype=3, agerange='', value=2102, source_url='https://coronavirus.data.gov.uk/', text_match='') admin_1 gb gb-wrl

Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='bournemouth, christchurch and poole', date_updated='2020_08_15', datatype=3, agerange='', value=855, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb bournemouth, christchurch and poole
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='cornwall and isles of scilly', date_updated='2020_08_15', datatype=3, agerange='', value=957, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb cornwall and isles of scilly
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='dorset', date_updated='2020_08_15', datatype=3, agerange='', value=638, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb dorset
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='folkestone and hythe', date_updated='2020_08_15', datatype=3, agerange='', value=787, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb folkestone and hythe
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='hackney and of london', date_updated='2020_08_15', datatype=3, agerange='', value=1050, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb hackney and of london
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='na h-eileanan siar', date_updated='2020_08_16', datatype=3, agerange='', value=7, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb na h-eileanan siar
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='somerset west and taunton', date_updated='2020_08_15', datatype=3, agerange='', value=456, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb somerset west and taunton
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='east suffolk', date_updated='2020_08_15', datatype=3, agerange='', value=896, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb east suffolk
Exception: Region child not found in GeoJSON: DataPoint(region_schema=21, region_parent='gb', region_child='west suffolk', date_updated='2020_08_15', datatype=3, agerange='', value=512, source_url='https://coronavirus.data.gov.uk/', text_match='') uk_area gb west suffolk
"""


class UKGovData(URLBase):
    SOURCE_URL = 'https://coronavirus.data.gov.uk/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'gb_gov_api'

    def __init__(self):
        URLBase.__init__(self,
                         output_dir=get_overseas_dir() / 'uk' / 'covid-19-uk-data' / 'data',
                         urls_dict={})

        self.update()

        self.__download_dataset('utla')
        self.__download_dataset('ltla')
        self.__download_dataset('region')
        self.__download_dataset('nhsRegion')
        self.__download_dataset('nation')
        self.__download_dataset('overview')

        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)

    def get_datapoints(self):
        r = []
        dpm = DataPointMerger()
        for date in sorted(listdir(get_overseas_dir() / 'uk' / 'gov-api')):
            r.extend(self._get_datapoints(date, dpm))
        return r

    @cache_by_date(source_id=SOURCE_ID)
    def _get_datapoints(self, date, dpm):
        r = []
        try:
            r.extend(dpm.extend(self._get_utla_datapoints(date)))
        except FileNotFoundError:
            pass

        try:
            r.extend(dpm.extend(self._get_ltla_datapoints(date)))
        except FileNotFoundError:
            pass
        return r

    def _get_utla_datapoints(self, date):
        r = self.sdpf()
        path = get_overseas_dir() / 'uk' / 'gov-api' / date / 'utla.json'
        exc_printed = set()

        with open(path, 'r', encoding='utf-8') as f:
            data = loads(f.read())

            for item in data:
                date = self.convert_date(item['date'])

                try:
                    # England, Wales and Scotland all use different systems
                    # England is close to standard Admin1, but Wales
                    # and Scotland use their own hospital systems
                    area = place_map[item['name']]
                except KeyError:
                    area = normalize_locality_name(item['name'])

                for datatype, value in (
                    (DataTypes.TOTAL, item['cumulative']),
                    (DataTypes.NEW, item['daily']),
                    (DataTypes.STATUS_DEATHS, item['deathsCumulative']),
                    (DataTypes.STATUS_DEATHS_NEW, item['deathsDaily']),
                    (DataTypes.TESTS_TOTAL, item['cumTestsByPublishDate']),
                    (DataTypes.TESTS_NEW, item['newTestsByPublishDate']),
                    (DataTypes.STATUS_HOSPITALIZED_RUNNINGTOTAL, item['cumAdmissions']),
                    (DataTypes.STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW, item['newAdmissions']),
                    (DataTypes.STATUS_HOSPITALIZED, item['hospitalCases']),
                    (DataTypes.STATUS_ICU_VENTILATORS, item['covidOccupiedMVBeds']),

                    # TODO: Support these separately!!!
                    # (item['cumAdmissionsByAge']),
                    #(item['maleCases']),
                    #(item['femaleCases']),
                ):
                    if value is None:
                        continue

                    try:
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='GB',
                            region_child=area,
                            datatype=datatype,
                            value=int(value),
                            date_updated=date,
                            source_url='https://coronavirus.data.gov.uk/'
                        )
                    except:
                        if not area in exc_printed:
                            import traceback
                            traceback.print_exc()
                            exc_printed.add(area)

        return r

    def _get_ltla_datapoints(self, date):
        r = self.sdpf()
        path = get_overseas_dir() / 'uk' / 'gov-api' / date / 'ltla.json'
        exc_printed = set()

        with open(path, 'r', encoding='utf-8') as f:
            data = loads(f.read())

            for item in data:
                print(item)

                date = self.convert_date(item['date'])
                if item['name'] in ni_mappings:
                    area = ni_mappings[item['name']]
                else:
                    area = item['name']
                area = normalize_locality_name(area)

                for datatype, value in (
                    (DataTypes.TOTAL, item['cumulative']),
                    (DataTypes.NEW, item['daily']),
                    (DataTypes.STATUS_DEATHS, item['deathsCumulative']),
                    (DataTypes.STATUS_DEATHS_NEW, item['deathsDaily']),
                    (DataTypes.TESTS_TOTAL, item['cumTestsByPublishDate']),
                    (DataTypes.TESTS_NEW, item['newTestsByPublishDate']),
                    (DataTypes.STATUS_HOSPITALIZED_RUNNINGTOTAL, item['cumAdmissions']),
                    (DataTypes.STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW, item['newAdmissions']),
                    (DataTypes.STATUS_HOSPITALIZED, item['hospitalCases']),
                    (DataTypes.STATUS_ICU_VENTILATORS, item['covidOccupiedMVBeds']),

                    # TODO: Support these separately!!!
                    # (item['cumAdmissionsByAge']),
                    # (item['maleCases']),
                    # (item['femaleCases']),
                ):
                    if value is None:
                        continue

                    try:
                        r.append(
                            region_schema=Schemas.UK_AREA,
                            region_parent='GB',
                            region_child=area,
                            datatype=datatype,
                            value=int(value),
                            date_updated=date,
                            source_url='https://coronavirus.data.gov.uk/'
                        )
                    except:
                        if not area in exc_printed:
                            import traceback
                            traceback.print_exc()
                            exc_printed.add(area)

        return r

    def __download_dataset(self, area_type):
        """
        Extracts paginated data by requesting all of the pages
        and combining the results.
        """
        date = datetime.datetime.now().strftime('%Y_%m_%d')
        dir_ = get_overseas_dir() / 'uk' / 'gov-api' / date
        if not exists(dir_):
            makedirs(dir_)

        path = dir_ / f'{area_type}.json'
        if exists(path):
            # Don't download if already downloaded!
            return

        endpoint = "https://api.coronavirus.data.gov.uk/v1/data"
        structure = {
            "date": "date",
            "name": "areaName",
            "code": "areaCode",
            "daily": "newCasesBySpecimenDate",
            "cumulative": "cumCasesBySpecimenDate",
            "deathsDaily": "newDeaths28DaysByPublishDate",
            "deathsCumulative": "cumDeaths28DaysByPublishDate",

            "cumTestsByPublishDate": "cumTestsByPublishDate",
            "newTestsByPublishDate": "newTestsByPublishDate",
            "newAdmissions": "newAdmissions",
            "cumAdmissions": "cumAdmissions",
            "cumAdmissionsByAge": "cumAdmissionsByAge",
            "hospitalCases": "hospitalCases",
            "covidOccupiedMVBeds": "covidOccupiedMVBeds",
            "maleCases": "maleCases",
            "femaleCases": "femaleCases"
        }
        api_params = {
            "filters": f"areaType={area_type}",
            "structure": dumps(structure, separators=(",", ":")),
            "format": "json"
        }

        data = []
        page_number = 1

        while True:
            # Adding page number to query params
            api_params["page"] = page_number
            print("getting:", endpoint, api_params)
            response = get(endpoint, params=api_params, timeout=30)

            if response.status_code >= HTTPStatus.BAD_REQUEST:
                raise RuntimeError(f'Request failed: {response.text}')
            elif response.status_code == HTTPStatus.NO_CONTENT:
                break

            current_data = response.json()
            page_data = current_data['data']
            data.extend(page_data)
            #print(page_data)

            # The "next" attribute in "pagination" will be `None`
            # when we reach the end.
            if current_data["pagination"]["next"] is None:
                break
            elif page_number > 100:
                break
            page_number += 1

        with open(path, 'w', encoding='utf-8') as f:
            f.write(dumps(data))


if __name__ == "__main__":
    from pprint import pprint
    inst = UKGovData()
    dp = inst.get_datapoints()
    #pprint(dp)
