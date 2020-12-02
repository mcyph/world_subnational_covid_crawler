import csv
from datetime import datetime

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.covid_crawlers.world.world_jhu_data.get_county_to_code_map import get_county_to_code_map
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT

county_to_code_map = get_county_to_code_map()


class WorldWHO(URLBase):
    SOURCE_ID = 'world_who'
    SOURCE_URL = ''
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'world_who' / 'data',
            urls_dict={
                'WHO-COVID-19-global-data.csv': URL(url='https://covid19.who.int/WHO-COVID-19-global-data.csv',
                                                    static_file=False),
            }
        )
        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = self.sdpf()
        date = datetime.today().strftime('%Y_%m_%d')
        path = get_overseas_dir() / 'world_who' / 'data' / date / 'WHO-COVID-19-global-data.csv'

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Date_reported'])

                if item['Country_code'] in ('BQ', 'GF', 'GP', 'MQ', 'YT', 'RE', 'TK', ' '):
                    continue

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child=item['Country_code'],
                    datatype=DataTypes.NEW,
                    value=int(item['New_cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child=item['Country_code'],
                    datatype=DataTypes.TOTAL,
                    value=int(item['Cumulative_cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child=item['Country_code'],
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['New_deaths']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child=item['Country_code'],
                    datatype=DataTypes.STATUS_DEATHS_NEW,
                    value=int(item['Cumulative_deaths']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(WorldWHO().get_datapoints())
