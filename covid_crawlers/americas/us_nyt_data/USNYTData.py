# https://github.com/nytimes/covid-19-data

import csv

from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_crawlers._base_classes.GithubRepo import GithubRepo
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


class USNYTData(GithubRepo):
    SOURCE_URL = 'https://github.com/nytimes/covid-19-data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'us_nytimes'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'us_nytimes' / 'covid-19-data',
                            github_url='https://github.com/nytimes/covid-19-data')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('us_county', 'alaska', 'fairbanks north star borough'): None,
                ('us_county', 'alaska', 'ketchikan gateway borough'): None,
                ('us_county', 'alaska', 'kenai peninsula borough'): None,
                ('us_county', 'missouri', 'kansas city'): None,
                ('us_county', 'alaska', 'juneau city and borough'): None,
                ('us_county', 'alaska', 'matanuska-susitna borough'): None,
                ('us_county', 'alaska', 'yukon-koyukuk census area'): None,
                ('us_county', 'alaska', 'southeast fairbanks census area'): None,
                ('us_county', 'alaska', 'petersburg borough'): None,
                ('us_county', 'alaska', 'bethel census area'): None,
                ('us_county', 'alaska', 'prince of wales-hyder census area'): None,
                ('us_county', 'alaska', 'nome census area'): None,
                ('us_county', 'alaska', 'kodiak island borough'): None,
                ('us_county', 'alaska', 'sitka city and borough'): None,
                ('us_county', 'puerto rico', 'anasco'): None,
                ('us_county', 'puerto rico', 'bayamon'): None,
                ('us_county', 'puerto rico', 'canovanas'): None,
                ('us_county', 'puerto rico', 'catano'): None,
                ('us_county', 'puerto rico', 'comerio'): None,
                ('us_county', 'puerto rico', 'guanica'): None,
                ('us_county', 'puerto rico', 'juana diaz'): None,
                ('us_county', 'puerto rico', 'las marias'): None,
                ('us_county', 'puerto rico', 'loiza'): None,
                ('us_county', 'puerto rico', 'manati'): None,
                ('us_county', 'puerto rico', 'mayaguez'): None,
                ('us_county', 'puerto rico', 'penuelas'): None,
                ('us_county', 'puerto rico', 'rincon'): None,
                ('us_county', 'puerto rico', 'rio grande'): None,
                ('us_county', 'puerto rico', 'san german'): None,
                ('us_county', 'puerto rico', 'san sebastian'): None,
                ('us_county', 'alaska', 'valdez-cordova census area'): None,
                ('us_county', 'alaska', 'northwest arctic borough'): None,
                ('us_county', 'alaska', 'north slope borough'): None,
                ('us_county', 'alaska', 'bristol bay borough'): None,
                ('us_county', 'alaska', 'dillingham census area'): None,
                ('us_county', 'alaska', 'aleutians west census area'): None,
                ('us_county', 'alaska', 'lake and peninsula borough'): None,
                ('us_county', 'alaska', 'wrangell city and borough'): None,
                ('us_county', 'alaska', 'aleutians east borough'): None,
                ('us_county', 'alaska', 'haines borough'): None,
                ('us_county', 'alaska', 'denali borough'): None,
                ('us_county', 'alaska', 'kusilvak census area'): None,
                ('us_county', 'alaska', 'skagway municipality'): None,
                ('us_county', 'missouri', 'joplin'): None,

                ('admin_1', 'us', 'puerto rico'): None,
                ('admin_1', 'us', 'virgin islands'): None,
                ('admin_1', 'us', 'guam'): None,
                ('admin_1', 'us', 'northern mariana islands'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_us_counties())
        r.extend(self._get_us_states())
        return r

    def _get_us_counties(self):
        r = self.sdpf()

        # date,county,state,fips,cases,deaths
        # 2020-01-21,Snohomish,Washington,53061,1,0
        # 2020-01-22,Snohomish,Washington,53061,1,0
        # 2020-01-23,Snohomish,Washington,53061,1,0
        # 2020-01-24,Cook,Illinois,17031,1,0

        with open(self.get_path_in_dir('us-counties.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                #print(item)
                date = self.convert_date(item['date'])

                r.append(
                    region_parent=item['state'],
                    region_schema=Schemas.US_COUNTY,
                    datatype=DataTypes.TOTAL,
                    region_child=item['county'],
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                )
                r.append(
                    region_parent=item['state'],
                    region_schema=Schemas.US_COUNTY,
                    datatype=DataTypes.STATUS_DEATHS,
                    region_child=item['county'],
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                )

        return r

    def _get_us_states(self):
        r = self.sdpf()

        # date,state,fips,cases,deaths
        # 2020-01-21,Washington,53,1,0
        # 2020-01-22,Washington,53,1,0
        # 2020-01-23,Washington,53,1,0
        # 2020-01-24,Illinois,17,1,0

        with open(self.get_path_in_dir('us-states.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                #print(item)
                date = self.convert_date(item['date'])

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='US',
                    region_child=item['state'],
                    datatype=DataTypes.TOTAL,
                    value=int(item['cases']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='US',
                    region_child=item['state'],
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['deaths']),
                    date_updated=date,
                    source_url='https://github.com/nytimes/covid-19-data'
                )
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(USNYTData().get_datapoints())
