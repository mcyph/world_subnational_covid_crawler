import csv

from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_crawlers.w_europe.de_data.DEData import (
    state_to_name
)


name_to_state = {
    state: name for name, state in state_to_name.items()
}


class ProcessDEKreis(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'de_kreis')

    def get_region_parent(self, fnam, feature):
        return name_to_state[feature['NAME_1']]

    def get_region_child(self, fnam, feature):
        return feature['NAME_3'] #.replace(' Städte', '')

    def get_region_printable(self, fnam, feature):
        return feature['NAME_3']


if __name__ == '__main__':
    ProcessDEKreis().output_json([
        DATA_DIR / 'de_kreis' / '4_niedrig.geo.json'
    ], OUTPUT_DIR, pretty_print=False)
