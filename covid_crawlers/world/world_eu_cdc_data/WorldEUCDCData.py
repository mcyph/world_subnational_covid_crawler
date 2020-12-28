import csv
import requests
import pandas as pd
from datetime import datetime
from collections import Counter

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT


class WorldEUCDCData(URLBase):
    SOURCE_URL = 'https://www.ecdc.europa.eu/en/publications-data/' \
                 'download-todays-data-geographic-distribution-covid-19-cases-worldwide'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'world_eu_cdc'

    def __init__(self):
        # https://www.ecdc.europa.eu/en/publications-data/covid-19-testing
        # https://www.ecdc.europa.eu/en/publications-data/download-data-hospital-and-icu-admission-rates-and-current-occupancy-covid-19

        URLBase.__init__(
            self,
            output_dir=get_overseas_dir() / 'world_eu_cdc' / 'data',
            urls_dict=self.__get_urls_dict()
        )

        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)

    def __get_urls_dict(self):
        r = {}
        r['world_data.xlsx'] = URL(url='https://opendata.ecdc.europa.eu/covid19/casedistribution/xlsx',
                                  static_file=False)
        for url, key in (
            ('https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/xlsx', 'hosp_icu.xlsx'),
            ('https://opendata.ecdc.europa.eu/covid19/testing/xlsx', 'tests.xlsx'),
        ):
            r[key] = URL(url, static_file=False)
        return r

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        date = datetime.today().strftime('%Y_%m_%d')
        r.extend(self._get_tests_datapoints(date))
        r.extend(self._get_hosp_icu_datapoints(date))
        return r

    def _get_tests_datapoints(self, date):
        r = self.sdpf()
        df = pd.read_excel(get_overseas_dir() / 'world_eu_cdc' / 'data' / date / 'tests.xlsx', engine='openpyxl')
        tests_done = Counter()

        for idx, row in df.iterrows():
            #print(row)
            date = datetime.strptime(row['year_week'] + '-1', "%Y-W%W-%w").strftime('%Y_%m_%d')
            tests_done[row['country']] += int(row['tests_done'])

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent='',
                region_child=row['country'],
                datatype=DataTypes.TESTS_TOTAL,
                value=tests_done[row['country']],
                date_updated=date,
                source_url='#'
            )
        return r

    def _get_hosp_icu_datapoints(self, date):
        r = self.sdpf()
        df = pd.read_excel(get_overseas_dir() / 'world_eu_cdc' / 'data' / date / 'hosp_icu.xlsx', engine='openpyxl')

        for idx, row in df.iterrows():
            #print(row)
            try:
                date = self.convert_date(row['date'])
            except:
                date = datetime.strptime(row['year_week'] + '-1', "%Y-W%W-%w").strftime('%Y_%m_%d')

            if row['indicator'] == 'Daily hospital occupancy':
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child=row['country'],
                    datatype=DataTypes.STATUS_HOSPITALIZED,
                    value=int(row['value']),  # WARNING WARNING!!!
                    date_updated=date,
                    source_url='#'
                )
            elif row['indicator'] == 'Daily ICU occupancy':
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child=row['country'],
                    datatype=DataTypes.STATUS_ICU,
                    value=int(row['value']),  # WARNING WARNING!!!
                    date_updated=date,
                    source_url='#'
                )
            elif row['indicator'] == 'Weekly new hospital admissions per 100k':
                pass
            elif row['indicator'] == 'Weekly new ICU admissions per 100k':
                pass
            else:
                raise Exception(row)

        return r

    def _get_datapoints(self):
        # dateRep	day	month	year	cases	deaths	countriesAndTerritories	geoId	countryterritoryCode
        # popData2019	continentExp	Cumulative_number_for_14_days_of_COVID-19_cases_per_100000
        #s
        # 25/08/2020	25	8	2020	71	10	Afghanistan	AF	AFG	38041757	Asia	2.67074941
        # 24/08/2020	24	8	2020	0	0	Afghanistan	AF	AFG	38041757	Asia	2.48411239
        # 23/08/2020	23	8	2020	105	2	Afghanistan	AF	AFG	38041757	Asia	2.48411239
        # 22/08/2020	22	8	2020	38	0	Afghanistan	AF	AFG	38041757	Asia	2.31061883
        # 21/08/2020	21	8	2020	97	2	Afghanistan	AF	AFG	38041757	Asia	2.41576644
        # 20/08/2020	20	8	2020	160	8	Afghanistan	AF	AFG	38041757	Asia	2.26855978
        r = self.sdpf()

        date = datetime.today().strftime('%Y_%m_%d')
        df = pd.read_excel(get_overseas_dir() / 'world_eu_cdc' / 'data' / date / 'world_data.xlsx', engine="openpyxl")
        df = df.sort_values('dateRep', axis=0)

        prev_date = None

        cases_cumulative = Counter()
        deaths_cumulative = Counter()

        for idx, item in df.iterrows():
            #print(item)
            date = self.convert_date(str(item['dateRep']).split()[0])

            if item['geoId'] in ('BQ', 'JPG11668'):
                continue
            elif item['geoId'] == 'EL':
                item['geoId'] = 'gr'
            elif item['geoId'] == 'UK':
                item['geoId'] = 'gb'
            elif not isinstance(item['geoId'], str):
                continue

            if prev_date and prev_date > date:
                raise Exception(prev_date, date)
            prev_date = date

            cases_cumulative[item['geoId']] += int(item['cases'])
            deaths_cumulative[item['geoId']] += int(item['deaths'])

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent='',
                region_child=item['geoId'],
                datatype=DataTypes.TOTAL,
                value=cases_cumulative[item['geoId']],
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent='',
                region_child=item['geoId'],
                datatype=DataTypes.STATUS_DEATHS,
                value=deaths_cumulative[item['geoId']],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return r


if __name__ == "__main__":
    inst = WorldEUCDCData()
    datapoints = inst.get_datapoints()
    #pprint(datapoints)
