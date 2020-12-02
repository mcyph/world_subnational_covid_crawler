import json
from os import listdir

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.covid_db.datatypes.DatapointMerger import DataPointMerger


DATA_URL = 'https://services7.arcgis.com/g8j6ESLxQjUogx9p/arcgis/rest/services/Latvia_covid_novadi/FeatureServer/0/query?f=json&where=Novadu_radit%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Novadu_radit%20desc&outSR=102100&resultOffset=0&resultRecordCount=4000&resultType=standard&cacheHint=true'
DATA_URL = DATA_URL.replace(' ', '%20')


county_map = {
}


class LVDataArcGIS(URLBase):
    SOURCE_URL = 'https://spkc.maps.arcgis.com/apps/opsdashboard/index.html#/4469c1fb01ed43cea6f20743ee7d5939'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'lv_arcgis_dash'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'lv' / 'arcgisdata',
            urls_dict={
                'regions_data.json': URL(DATA_URL, static_file=False),
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'lv', 'daugavpils novads'): None,
                ('admin_1', 'lv', 'jelgavas novads'): None,
                ('admin_1', 'lv', 'jēkabpils novads'): None,
                ('admin_1', 'lv', 'kocēnu novads'): None,
                ('admin_1', 'lv', 'līgatnes novads'): None,
                ('admin_1', 'lv', 'pārgaujas novads'): None,
                ('admin_1', 'lv', 'pārgaujas novads'): None,
                ('admin_1', 'lv', 'priekuļu novads'): None,
                ('admin_1', 'lv', 'rēzeknes novads'): None,
                ('admin_1', 'lv', 'rūjienas novads'): None,
                ('admin_1', 'lv', 'strenču novads'): None,
                ('admin_1', 'lv', 'varakļānu novads'): None,
                ('admin_1', 'lv', 'ventspils novads'): None,
                ('admin_1', 'lv', 'viļānu novads'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_regions_data())
        return r

    def _get_regions_data(self):
        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()
            path = f'{base_dir}/{date}/regions_data.json'
            with open(path, 'r') as f:
                data = json.loads(f.read())

            for feature in data['features']:
                attributes = feature['attributes']

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='LV',
                    region_child=attributes['Nos_pilns'],
                    datatype=DataTypes.TOTAL,
                    value=int(attributes['Covid_sasl']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            out.extend(r)
        return out


if __name__ == '__main__':
    from pprint import pprint
    pprint(LVDataArcGIS().get_datapoints())

