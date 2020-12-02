import csv

from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_crawlers._base_classes.GithubRepo import GithubRepo
from _utility.get_package_dir import get_overseas_dir
from covid_crawlers.w_europe.uk_data.uk_place_map import place_map


class UKData(GithubRepo):
    SOURCE_URL = 'https://github.com/tomwhite/covid-19-uk-data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'gb_uk_unofficial'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'uk' / 'covid-19-uk-data' / 'data',
                            github_url='https://github.com/tomwhite/covid-19-uk-data')
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases_uk())
        r.extend(self._get_indicators_uk())
        return r

    def _get_cases_uk(self):
        r = self.sdpf()

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

                if item['Country'] == 'England':
                    # England, Wales and Scotland all use different systems
                    # England is close to standard Admin1, but Wales
                    # and Scotland use their own hospital systems
                    area = place_map[item['Area']]
                else:
                    area = item['Area']

                r.append(
                    region_schema=Schemas.UK_AREA,
                    region_parent='GB', #item['Country'],
                    region_child=area,
                    datatype=DataTypes.TOTAL,
                    value=int(item['TotalCases']),
                    date_updated=date,
                    source_url='https://github.com/tomwhite/covid-19-uk-data'
                )

        return r

    def _get_indicators_uk(self):
        r = self.sdpf()

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
                    'ConfirmedCases': DataTypes.TOTAL,
                    'Tests': DataTypes.TESTS_TOTAL,
                    'Deaths': DataTypes.STATUS_DEATHS
                }
                schema, parent, country = {
                    'UK': (Schemas.ADMIN_0, None, 'GB'),
                    'England': (Schemas.ADMIN_1, 'GB', 'GB-ENG'),
                    'Wales': (Schemas.ADMIN_1, 'GB', 'GB-WLS'),
                    'Scotland': (Schemas.ADMIN_1, 'GB', 'GB-SCT'),
                    'Northern Ireland': (Schemas.ADMIN_1, 'GB', 'GB-NIR'),
                }[item['Country']]

                r.append(
                    region_schema=schema,  # TODO: Should this be a separate schema?
                    region_parent=parent,
                    region_child=country,
                    datatype=datatype_map[item['Indicator'].strip()],
                    value=int(item['Value']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(UKData().get_datapoints())
