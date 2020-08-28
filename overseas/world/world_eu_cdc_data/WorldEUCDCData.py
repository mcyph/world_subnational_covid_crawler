import csv
from datetime import datetime
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)
from covid_19_au_grab.datatypes.StrictDataPointsFactory import (
    StrictDataPointsFactory, MODE_STRICT, MODE_DEV
)


class WorldEUCDCData(URLBase):
    SOURCE_URL = 'https://www.ecdc.europa.eu/en/publications-data/' \
                 'download-todays-data-geographic-distribution-covid-19-cases-worldwide'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'world_eu_cdc'

    def __init__(self):
        URLBase.__init__(self,
                         output_dir=get_overseas_dir() / 'world_eu_cdc' / 'data',
                         urls_dict={
                             'world_data.csv': URL(url='https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
                                                   static_file=False)
                         })
        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
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
        path = get_overseas_dir() / 'world_eu_cdc' / 'data' / date / 'world_data.csv'



        with open(path, 'r', encoding='utf-8') as f:
            cur_geoid = None
            prev_date = None

            for item in reversed(list(csv.DictReader(f))):
                print(item)
                date = self.convert_date(item['dateRep'])

                if item['geoId'] in (
                    'BQ', 'JPG11668'
                ):
                    continue
                elif item['geoId'] == 'EL':
                    item['geoId'] = 'gr'
                elif item['geoId'] == 'UK':
                    item['geoId'] = 'gb'

                if item['geoId'] != cur_geoid:
                    cur_geoid = item['geoId']
                    prev_date = None
                    cases_cumulative = Counter()
                    deaths_cumulative = Counter()

                if prev_date and prev_date >= date:
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
    from pprint import pprint
    inst = WorldEUCDCData()
    pprint(inst.get_datapoints())
