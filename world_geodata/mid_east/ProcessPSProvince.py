from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab._utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessPSProvince(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'ps_province')

    def get_region_parent(self, fnam, feature):
        return 'PS'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['iso_3166_2'])

    def get_region_printable(self, fnam, feature):
        return feature['admin2Name']


if __name__ == '__main__':
    ProcessPSProvince().output_json([
        DATA_DIR / 'ps_province' / 'ps_province.geojson'
    ], OUTPUT_DIR, pretty_print=False)
