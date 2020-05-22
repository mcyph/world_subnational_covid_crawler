import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_UK_AREA, SCHEMA_UK_COUNTRY,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.state_news_releases.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class UKData(GithubRepo):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'uk' / 'covid-19-uk-data' / 'data',
                            github_url='https://github.com/tomwhite/covid-19-uk-data')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases_uk())
        r.extend(self._get_indicators_uk())
        return r

    def _get_cases_uk(self):
        r = []

        # By area

        # Date,Country,AreaCode,Area,TotalCases
        # 2020-01-08,Wales,W11000028,Aneurin Bevan,0
        # 2020-01-08,Wales,W11000023,Betsi Cadwaladr,0
        # 2020-01-08,Wales,W11000029,Cardiff and Vale,0
        # 2020-01-08,Wales,W11000030,Cwm Taf,0
        # 2020-01-08,Wales,W11000025,Hywel Dda,0
        # 2020-01-08,Wales,,Outside Wales,0

        with open(self.get_path_in_dir('covid-19-cases-uk.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])
                if item['TotalCases'] == 'NaN':
                    continue

                r.append(DataPoint(
                    region_parent=item['Country'],
                    region_schema=SCHEMA_UK_AREA,
                    datatype=DT_TOTAL,
                    region_child=item['Area'],
                    value=int(item['TotalCases']),
                    date_updated=date,
                    source_url='https://github.com/tomwhite/covid-19-uk-data'
                ))

        return r

    def _get_indicators_uk(self):
        r = []

        # By country

        # Date,Country,Indicator,Value
        # 2020-01-08,Wales,ConfirmedCases,0
        # 2020-01-08,Wales,Tests,1
        # 2020-01-09,Wales,ConfirmedCases,0
        # 2020-01-09,Wales,Tests,1

        with open(self.get_path_in_dir('covid-19-indicators-uk.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date'])

                datatype_map = {
                    'ConfirmedCases': DT_TOTAL,
                    'Tests': DT_TESTS_TOTAL,
                    'Deaths': DT_STATUS_DEATHS
                }

                r.append(DataPoint(
                    region_schema=SCHEMA_UK_COUNTRY,
                    datatype=datatype_map[item['Indicator'].strip()],
                    region_child=item['Country'],
                    value=int(item['Value']),
                    date_updated=date,
                    source_url='https://github.com/tomwhite/covid-19-uk-data'
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(UKData().get_datapoints())
