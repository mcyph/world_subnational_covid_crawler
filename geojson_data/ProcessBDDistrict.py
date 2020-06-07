from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.overseas.bd_data.BDData import (
    division_map, place_map
)


class ProcessBDDistrict(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'bd_district')

    def get_region_parent(self, fnam, feature):
        return division_map[feature['ADM1_EN']]

    def get_region_child(self, fnam, feature):
        return place_map[feature['ADM2_EN']]

    def get_region_printable(self, fnam, feature):
        return feature['ADM2_EN']


if __name__ == '__main__':
    ProcessBDDistrict().output_json([
        DATA_DIR / 'bd_district' / 'bd_admin2.json'
    ], OUTPUT_DIR, pretty_print=False)
