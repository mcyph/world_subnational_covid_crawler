from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)


class ProcessCNCity(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'cn_city')

    def get_region_parent(self, fnam, feature):
        return 'CN'

    def get_region_child(self, fnam, feature):
        return str(feature['adcode'])

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['name'], # TODO!
            'zh': feature['name']
        }


if __name__ == '__main__':
    ProcessCNCity().output_json([
        DATA_DIR / 'cn_city' / 'cn_city.json'
    ], OUTPUT_DIR, pretty_print=False)
