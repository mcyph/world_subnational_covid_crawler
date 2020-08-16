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


class ProcessINState(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')

    def get_region_parent(self, fnam, feature):
        return 'in'

    def get_region_child(self, fnam, feature):
        return states_map[feature['ST_NM']]

    def get_region_printable(self, fnam, feature):
        return feature['ST_NM']


if __name__ == '__main__':
    ProcessINState().output_json([
        DATA_DIR / 'in_states' / 'in_states.json'
    ], OUTPUT_DIR, pretty_print=False)
