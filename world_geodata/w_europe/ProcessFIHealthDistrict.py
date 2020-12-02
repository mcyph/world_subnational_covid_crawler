from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from _utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessPTMunicipality(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'fi_health_district')

    def get_region_parent(self, fnam, feature):
        return 'FI'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['healthCareDistrict'])

    def get_region_printable(self, fnam, feature):
        return feature['healthCareDistrict']


if __name__ == '__main__':
    pass
ProcessPTMunicipality().output_json([
    DATA_DIR / 'fi_health_district' / 'healthDistrictsEPSG4326.json'
], OUTPUT_DIR, pretty_print=False)
