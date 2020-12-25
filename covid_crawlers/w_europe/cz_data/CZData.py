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
from os import listdir

from _utility.cache_by_date import cache_by_date
from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.DatapointMerger import DataPointMerger


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
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('cz_okres', 'cz', 'cz010'): None,
                ('cz_okres', 'cz', 'cz020'): None,
                ('cz_okres', 'cz', 'cz031'): None,
                ('cz_okres', 'cz', 'cz032'): None,
                ('cz_okres', 'cz', 'cz041'): None,
                ('cz_okres', 'cz', 'cz042'): None,
                ('cz_okres', 'cz', 'cz051'): None,
                ('cz_okres', 'cz', 'cz052'): None,
                ('cz_okres', 'cz', 'cz053'): None,

                ('cz_okres', 'cz', 'cz064'): None,
                ('cz_okres', 'cz', 'cz071'): None,
                ('cz_okres', 'cz', 'cz063'): None,
                ('cz_okres', 'cz', 'cz072'): None,
                ('cz_okres', 'cz', 'cz080'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        dpm = DataPointMerger()
        base_dir = self.get_path_in_dir('')
        for date in self.iter_nonempty_dirs(base_dir):
            r.extend(self._get_data_from_cases_csv(date, dpm))
        return r

    @cache_by_date(source_id=SOURCE_ID)
    def _get_data_from_cases_csv(self, date, dpm):
        # datum	kraj_nuts_kod	okres_lau_kod	kumulativni_pocet_nakazenych	kumulativni_pocet_vylecenych	kumulativni_pocet_umrti
        # 2020-03-01	CZ010	CZ0100	2	0	0
        # 2020-03-01	CZ020	CZ0201	0	0	0
        # 2020-03-01	CZ020	CZ0202	0	0	0

        r = self.sdpf()

        base_dir = self.get_path_in_dir('')
        path = f'{base_dir}/{date}/regional_totals.json'

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                #print(item)

                date = self.convert_date(item['datum'])
                confirmed = int(item['kumulativni_pocet_nakazenych'])
                recovered = int(item['kumulativni_pocet_nakazenych'])
                death = int(item['kumulativni_pocet_umrti'])
                active = confirmed - recovered - death
                region_child = item['okres_lau_kod'] or 'unknown'

                for datatype, value in (
                    (DataTypes.TOTAL, confirmed),
                    (DataTypes.STATUS_RECOVERED, recovered),
                    (DataTypes.STATUS_DEATHS, death),
                    (DataTypes.STATUS_ACTIVE, active)
                ):
                    r.append(
                        region_schema=Schemas.CZ_OKRES,
                        region_parent='CZ',  # FIXME!
                        region_child=region_child,
                        datatype=datatype,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return dpm.extend(r)


if __name__ == '__main__':
    from pprint import pprint
    datapoints = CZData().get_datapoints()
    pprint(datapoints)
