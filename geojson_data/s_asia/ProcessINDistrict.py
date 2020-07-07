from os import listdir

from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)
from covid_19_au_grab.overseas.s_asia.in_data.INData import (
    states_map
)


class ProcessINDistrict(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'in_district')

    def get_region_parent(self, fnam, feature):
        return states_map[feature['st_nm']]

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['district'])

    def get_region_printable(self, fnam, feature):
        return feature['district']


if __name__ == '__main__':
    ProcessINDistrict().output_json([
        DATA_DIR / 'in_district' / fnam
        for fnam in listdir(DATA_DIR / 'in_district')
        if fnam.endswith('.json')
    ], OUTPUT_DIR, pretty_print=False)
