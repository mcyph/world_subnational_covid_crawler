from os import listdir
from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)


class ProcessJPCity(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'jp_city')

    def get_region_parent(self, fnam, feature):
        return 'JP-'+feature['admin2_code'][:2]

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['admin2_code'])

    def get_region_printable(self, fnam, feature):
        return {
            'ja': feature['ja'],
            'en': feature['en']
        }


if __name__ == '__main__':
    ProcessJPCity().output_json([
        DATA_DIR / 'jp_city' / fnam
        for fnam in listdir(DATA_DIR / 'jp_city')
        if fnam.endswith('.json')
    ], OUTPUT_DIR, pretty_print=False)
