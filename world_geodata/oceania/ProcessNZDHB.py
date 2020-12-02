from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from _utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessNZDHB(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'nz_dhb')

    def get_region_parent(self, fnam, feature):
        return 'NZ'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['DHB2015_Na'])

    def get_region_printable(self, fnam, feature):
        return feature['DHB2015_Na']


if __name__ == '__main__':
    ProcessNZDHB().output_json([
        DATA_DIR / 'nz_dhb' / 'nz_dhb.geojson'
    ], OUTPUT_DIR, pretty_print=False)
