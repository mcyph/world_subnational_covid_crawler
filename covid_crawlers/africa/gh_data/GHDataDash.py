# https://www.ghanahealthservice.org/covid19/

regions_url = 'https://services9.arcgis.com/XPDxEtZ1oS0ENZZq/arcgis/rest/services/COVID_19_Ghana/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Number_of_Cases%20desc&outSR=102100&resultOffset=0&resultRecordCount=25&resultType=standard&cacheHint=true'
recoveries_url = 'https://services9.arcgis.com/XPDxEtZ1oS0ENZZq/arcgis/rest/services/COVID_19_Ghana/FeatureServer/4/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true'
deaths_url = 'https://services9.arcgis.com/XPDxEtZ1oS0ENZZq/arcgis/rest/services/COVID_19_Ghana/FeatureServer/3/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true'
confirmed_url = 'https://services9.arcgis.com/XPDxEtZ1oS0ENZZq/arcgis/rest/services/COVID_19_Ghana/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true'

import json
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT


place_map = dict([i.split('\t')[::-1] for i in '''
GH-AF	Ahafo
GH-AH	Ashanti
GH-BO	Bono
GH-BE	Bono East
GH-CP	Central
GH-EP	Eastern
GH-AA	Greater Accra
GH-NE	North East
GH-NP	Northern
GH-OT	Oti
GH-SV	Savannah
GH-UE	Upper East
GH-UW	Upper West
GH-TV	Volta
GH-WP	Western
GH-WN	Western North
'''.strip().split('\n')])


class GHDataDash(URLBase):
    SOURCE_URL = 'https://www.ghanahealthservice.org/covid19/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'gh_ghs'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'gh' / 'data2',
            urls_dict={
                'regions.json': URL(regions_url, static_file=False),
                'recoveries.json': URL(recoveries_url, static_file=False),
                'deaths.json': URL(deaths_url, static_file=False),
                'confirmed.json': URL(confirmed_url, static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/regions.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for feature in data['features']:
                attributes = feature['attributes']
                #print(attributes)

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='GH',
                    region_child=place_map[attributes['REGION'].replace(' Region', '')],
                    datatype=DataTypes.TOTAL,
                    value=int(attributes['Number_of_Cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(GHDataDash().get_datapoints())
