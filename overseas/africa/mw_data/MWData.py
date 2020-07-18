# https://covid19.health.gov.mw:3000/api/v0/aggregates
# https://covid19.health.gov.mw:3000/api/v0/districts/aggregates

import json
import datetime
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    DT_TESTS_TOTAL, DT_PROBABLE, DT_CONFIRMED,
    DT_TOTAL, DT_STATUS_RECOVERED,
    DT_STATUS_DEATHS, DT_STATUS_ACTIVE
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


town_to_iso_3166_2 = {
    'Chitipa': 'MW-CT',
    'Karonga': 'MW-KR',
    'Rumphi': 'MW-RU',
    'Mzuzu': 'MW-MZ',
    'Mzimba': 'MW-MZ',
    'Mzimba-North': 'MW-MZ',
    'Nkhata Bay': 'MW-NB',
    'Mzimba-South': 'MW-MZ',
    'Nkhotakota': 'MW-NK',
    'Kasungu': 'MW-KS',
    'Mchinji': 'MW-MC',
    'Dowa': 'MW-DO',
    'Salima': 'MW-SA',
    'Lilongwe': 'MW-LI',
    'Likoma': 'MW-LK',
    'Dedza': 'MW-DE',
    'Mangochi': 'MW-MG',
    'Ntcheu': 'MW-NU',
    'Balaka': 'MW-BA',
    'Machinga': 'MW-MH',
    'Neno': 'MW-NE',
    'Ntchisi': 'MW-NI',
    'Mwanza Border': 'MW-MW',
    'Mwanza': 'MW-MW',
    'Mwanza PoE': 'MW-MW',
    'Blantyre': 'MW-BL',
    'Chiradzulu': 'MW-CR',
    'Phalombe': 'MW-PH',
    'Chikwawa': 'MW-CK',
    'Thyolo': 'MW-TH',
    'Mulanje': 'MW-MU',
    'Nsanje': 'MW-NS',
    'Zomba': 'MW-ZO',
    'Mchinji Border': 'MW-MC',
    'Biriwiri Border': None,
    'Muloza border': 'MW-MU',
    'Dedza Border': 'MW-DE',
    'Kamuzu International Airport': 'MW-LI',
    'Chileka Airport': 'MW-BL',
    'Songwe Border': 'MW-CT'
}


class MWData(URLBase):
    SOURCE_URL = 'https://covid19.health.gov.mw/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'mw_moh'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'mw' / 'data',
            urls_dict={
                'aggregates.json': URL(
                    'https://covid19.health.gov.mw:3000/api/v0/aggregates',
                    static_file=False
                ),
                'district_aggregates.json': URL(
                    'https://covid19.health.gov.mw:3000/api/v0/districts/aggregates',
                    static_file=False
                )
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_district_aggregates())
        r.extend(self._get_aggregates())
        return r

    def _get_district_aggregates(self):
        # {"lastUpdate":"2020-07-03T02:03:48.352Z","districts":
        #     [{"districtGeolocation":{"lat":-14.9876054,"lng":34.9561748},
        #       "districtName":"Balaka",
        #       "numberOfConfirmedCases":19,
        #       "numberOfConfirmedDeaths":1,
        #       "numberOfRecoveredPatients":0,
        #       "numberOfSuspectedCases":0},
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/district_aggregates.json'

            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            date = self.convert_date(data['lastUpdate'].split('T')[0])
            confirmed = Counter()
            deaths = Counter()
            recovered = Counter()
            suspected = Counter()

            for district in data['districts']:
                if district['districtName'] is None:
                    continue

                region_child = town_to_iso_3166_2[district['districtName']]
                confirmed[region_child] += district['numberOfConfirmedCases']
                deaths[region_child] += district['numberOfConfirmedDeaths']
                recovered[region_child] += district['numberOfRecoveredPatients']
                suspected[region_child] += district['numberOfSuspectedCases']

            for counter, datatype in (
                (confirmed, DT_CONFIRMED),
                (deaths, DT_STATUS_DEATHS),
                (recovered, DT_STATUS_RECOVERED),
                (suspected, DT_PROBABLE)
            ):
                for region_child, value in counter.items():
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='MW',
                        region_child=region_child,
                        datatype=datatype,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

            for region_child, value in confirmed.items():
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='MW',
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=value+suspected[region_child],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_aggregates(self):
        # {"numberOfConfirmedCases":1402,
        # "numberOfConfirmedDeaths":16,
        # "numberOfRecoveredPatients":317,
        # "numberOfSuspectedCases":15544,
        # "numberOfReceivedSamples":15544,
        # "numberOfTestedSamples":15177}

        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/aggregates.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MW',
                datatype=DT_TOTAL,
                value=data['numberOfConfirmedCases']+data['numberOfSuspectedCases'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MW',
                datatype=DT_CONFIRMED,
                value=data['numberOfConfirmedCases'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MW',
                datatype=DT_PROBABLE,
                value=data['numberOfSuspectedCases'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MW',
                datatype=DT_STATUS_DEATHS,
                value=data['numberOfConfirmedDeaths'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MW',
                datatype=DT_STATUS_RECOVERED,
                value=data['numberOfRecoveredPatients'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

            #r.append(DataPoint(
            #    region_schema=SCHEMA_ADMIN_0,
            #    region_parent=None,
            #    region_child='MW',
            #    datatype=DT_TESTS_TOTAL,
            #    value=data['numberOfReceivedSamples'],
            #    date_updated=date,
            #    source_url=self.SOURCE_URL
            #))
            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_parent=None,
                region_child='MW',
                datatype=DT_TESTS_TOTAL,
                value=data['numberOfTestedSamples'],
                date_updated=date,
                source_url=self.SOURCE_URL
            ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MWData().get_datapoints())
