# https://covid19portal.gov.bw/

# https://services7.arcgis.com/mbEujVpJG0aE29fS/arcgis/rest/services/Covid19_View/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=1222&geometry=%7B%22xmin%22%3A2504688.542842917%2C%22ymin%22%3A-3130860.678554911%2C%22xmax%22%3A3130860.678554911%2C%22ymax%22%3A-2504688.542842917%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile
# https://services7.arcgis.com/mbEujVpJG0aE29fS/arcgis/rest/services/Covid19_View/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=1222&geometry=%7B%22xmin%22%3A2504688.542842917%2C%22ymin%22%3A-2504688.542842917%2C%22xmax%22%3A3130860.678554911%2C%22ymax%22%3A-1878516.4071309231%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile

import json
from os import listdir
from collections import Counter

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from _utility.get_package_dir import get_overseas_dir

region_map = {
    'Gaborone': 'BW-SE',
    'Ramotswa': 'BW-SE',
    'Molepolole': 'BW-KW',
    'Metsimotlhabe': 'BW-KW',
    'Mahalapye': 'BW-CE',
    'Siviya': 'BW-NE',
    'Kazungula': 'BW-SO'
}


class BWData(URLBase):
    SOURCE_URL = 'https://covid19portal.gov.bw/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'bw_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'bw' / 'data',
            urls_dict={
                'data_1.json': URL('https://services7.arcgis.com/mbEujVpJG0aE29fS/arcgis/rest/services/Covid19_View/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=1222&geometry=%7B%22xmin%22%3A2504688.542842917%2C%22ymin%22%3A-3130860.678554911%2C%22xmax%22%3A3130860.678554911%2C%22ymax%22%3A-2504688.542842917%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile',
                                   static_file=False),
                'data_2.json': URL('https://services7.arcgis.com/mbEujVpJG0aE29fS/arcgis/rest/services/Covid19_View/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=1222&geometry=%7B%22xmin%22%3A2504688.542842917%2C%22ymin%22%3A-2504688.542842917%2C%22xmax%22%3A3130860.678554911%2C%22ymax%22%3A-1878516.4071309231%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile',
                                   static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        # {"date":1589220000000,"division":"Rajshahi","district":"Joypurhat","city":"Joypurhat",
        # "population":1017277,"cases":55,"recovered":null,"death":null,"geo_code":5038,
        # "lat":25.102372,"long":89.021208,"adjusted_cases":54.06590339,"labels":"Joypurhat(55)",
        # "ObjectId":1266},"geometry":{"x":78920,"y":143477}},
        # {"attributes":{"date":1589392800000,"division":"Rajshahi","district":"Joypurhat",
        # "city":"Joypurhat","population":1017277,"cases":55,"recovered":null,"death":null,
        # "geo_code":5038,"lat":25.102372,"long":89.021208,"adjusted_cases":54.06590339,
        # "labels":"Joypurhat(55)","ObjectId":1332},"geometry":{"x":78920,"y":143477}}

        for date in self.iter_nonempty_dirs(base_dir):
            added = set()

            confirmed = Counter()
            death = Counter()
            recoveries = Counter()
            active = Counter()
            male = Counter()
            female = Counter()
            tests = Counter()

            age_keys = {
                'Twelve': '0-12',
                'Nineteen': '13-19',
                'thirtyfive': '20-35',
                'fortyfive': '36-45',
                'sixty': '46-60',
                'sixty60': '61+'
            }
            age = {v: Counter() for v in age_keys.values()}

            for path in (
                f'{base_dir}/{date}/data_1.json',
                f'{base_dir}/{date}/data_2.json'
            ):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.loads(f.read())
                except UnicodeDecodeError:
                    import brotli
                    with open(path, 'rb') as f:
                        data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

                for feature in data['features']:
                    #print(feature)
                    attributes = feature['attributes']

                    if attributes['Name'] in added:
                        # Because Botswana is by town, need to convert
                        # to regions+make sure not in both json files
                        continue

                    region_child = region_map[attributes['Name']]

                    if attributes['Confirmed'] is not None:
                        confirmed[region_child] += attributes['Confirmed']

                    if attributes['Death'] is not None:
                        death[region_child] += attributes['Death']

                    if attributes['Recoveries'] is not None:
                        recoveries[region_child] += attributes['Recoveries']

                    if attributes['Active'] is not None:
                        active[region_child] += attributes['Active']

                    if attributes['Male'] is not None:
                        male[region_child] += attributes['Male']

                    if attributes['Female'] is not None:
                        female[region_child] += attributes['Female']

                    if attributes['Tests'] is not None:
                        tests[region_child] += attributes['Tests']

                    #if attributes['Foreign1'] is not None:
                    #    foreign[region_child] += attributes['Foreign1']

                    #if attributes['Local1'] is not None:
                    #    local[region_child] += attributes['Local1']

                    for k in age_keys:
                        if attributes[k] is not None:
                            age[age_keys[k]][region_child] += attributes[k]

            for counter, datatype in (
                (confirmed, DataTypes.TOTAL),
                (death, DataTypes.STATUS_DEATHS),
                (recoveries, DataTypes.STATUS_RECOVERED),
                (active, DataTypes.STATUS_ACTIVE),
                (male, DataTypes.TOTAL_MALE),
                (female, DataTypes.TOTAL_FEMALE),
                (tests, DataTypes.TESTS_TOTAL),
            ):
                for region_child, value in counter.items():
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='BW',
                        region_child=region_child,
                        datatype=datatype,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

            for agerange, counter in age.items():
                for region_child, value in counter.items():
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='BW',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        agerange=agerange,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(BWData().get_datapoints())
