# https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19

# There's also PPE/ICU capacity and other stats at
# https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19

# Total (cumulative) number of tests performed (v2)
TOTAL_TESTS_URL = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/testy.csv'
# Total (cumulative) number of persons with a proven infection by regional hygienic stations, including laboratories (v2)
TOTAL_CONFIRMED = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakaza.csv'
# Total (cumulative) number of persons with a proven infection according to regional hygienic stations, including laboratories, number of cured persons, number of deaths and tests performed (v2)
TOTAL_NATIONAL_STATS = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'

# datum,vek,pohlavi,kraj_nuts_kod,okres_lau_kod,nakaza_v_zahranici,nakaza_zeme_csu_kod
# 2020-07-04,36,M,CZ080,CZ0803,,
# 2020-04-05,32,M,CZ042,CZ0427,,
INDIVIDUAL_CASES = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv'
REGIONAL_TOTALS = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv'
# datum,vek,pohlavi,kraj_nuts_kod,okres_lau_kod
# 2020-03-14,39,Z,CZ020,CZ020A
# 2020-03-15,53,Z,CZ042,CZ0421
RECOVERED = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/vyleceni.csv'
# datum,vek,pohlavi,kraj_nuts_kod,okres_lau_kod
# 2020-03-22,94,M,CZ010,CZ0100
# 2020-03-24,73,Z,CZ010,CZ0100
DEATHS = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv'

import csv
import json
import datetime
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class CZData(URLBase):
    SOURCE_URL = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'cz_mzcr'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'cz' / 'data',
            urls_dict={
                'national_tests.json': URL(TOTAL_TESTS_URL, static_file=False),
                'national_confirmed.json': URL(TOTAL_CONFIRMED, static_file=False),
                'national_stats.json': URL(TOTAL_NATIONAL_STATS, static_file=False),

                'regional_cases.json': URL(INDIVIDUAL_CASES, static_file=False),
                'regional_totals.json': URL(REGIONAL_TOTALS, static_file=False),
                'regional_recovered.json': URL(RECOVERED, static_file=False),
                'regional_deaths.json': URL(DEATHS, static_file=False),
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_data_from_cases_csv())
        return r

    def _get_data_from_cases_csv(self):
        # datum	kraj_nuts_kod	okres_lau_kod	kumulativni_pocet_nakazenych	kumulativni_pocet_vylecenych	kumulativni_pocet_umrti
        # 2020-03-01	CZ010	CZ0100	2	0	0
        # 2020-03-01	CZ020	CZ0201	0	0	0
        # 2020-03-01	CZ020	CZ0202	0	0	0

        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/regional_totals.json'

            with open(path, 'r', encoding='utf-8-sig') as f:
                for item in csv.DictReader(f):
                    date = self.convert_date(item['datum'])
                    confirmed = int(item['kumulativni_pocet_nakazenych'])
                    recovered = int(item['kumulativni_pocet_nakazenych'])
                    death = int(item['kumulativni_pocet_umrti'])
                    active = confirmed - recovered - death
                    region_child = item['okres_lau_kod']

                    for datatype, value in (
                        (DataTypes.TOTAL, confirmed),
                        (DataTypes.STATUS_RECOVERED, recovered),
                        (DataTypes.STATUS_DEATHS, death),
                        (DataTypes.STATUS_ACTIVE, active)
                    ):
                        r.append(DataPoint(
                            region_schema=Schemas.CZ_OKRES,
                            region_parent='CZ',  # FIXME!
                            region_child=region_child,
                            datatype=datatype,
                            value=value,
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(CZData().get_datapoints())
