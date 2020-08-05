from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)


class ProcessHKDistrict(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'hk_district')

    def get_region_parent(self, fnam, feature):
        return 'HK'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['District'])

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['District'],
            'zh': feature['地區']
        }


if __name__ == '__main__':
    ProcessHKDistrict().output_json([
        DATA_DIR / 'hk_district' / 'hksar_18_district_boundary.json'
    ], OUTPUT_DIR, pretty_print=False)
