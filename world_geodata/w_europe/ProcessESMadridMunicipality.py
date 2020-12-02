from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from _utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessESMadridMunicipality(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'es_madrid_municipality')

    def get_region_parent(self, fnam, feature):
        return 'ES-M'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['NMUN'])

    def get_region_printable(self, fnam, feature):
        return feature['NMUN']


if __name__ == '__main__':
    ProcessESMadridMunicipality().output_json([
        DATA_DIR / 'es_madrid_municipality' / 'madrid.json'
    ], OUTPUT_DIR, pretty_print=False)
