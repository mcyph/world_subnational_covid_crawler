import csv

from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.overseas.de_data.DEData import (
    state_to_name
)

name_to_state = {
    state: name for name, state in state_to_name.items()
}


def get_ags_maps():
    r1 = {}
    r2 = {}
    with open(DATA_DIR / 'de_ags' / 'ags_map.csv',
              'r', encoding='utf-8') as f:
        for _, _, ags_id, ags_name in csv.reader(f, delimiter=';'):
            r1[ags_id] = ags_name
            r2[ags_name] = ags_id
    return r1, r2


ags_id_to_name, name_to_ags_id = get_ags_maps()

found = set()


class ProcessDEAGS(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'de_ags')

    def get_region_parent(self, fnam, feature):
        return name_to_state[feature['NAME_1']]

    def get_region_child(self, fnam, feature):
        # There are some 50 regions which aren't mapped!
        # Will need to find real AGS shapefile/geojson data if possible! ==============================================
        try:
            r = name_to_ags_id[feature['NAME_3'].replace(' Städte', '')]
            print("FOUND:", feature['NAME_3'])
            found.add(r)
            return r
        except KeyError:
            print("KEYERROR:", feature['NAME_3'])
            return feature['NAME_3'].replace(' Städte', '')

    def get_region_printable(self, fnam, feature):
        return feature['NAME_3']


if __name__ == '__main__':
    ProcessDEAGS().output_json([
        DATA_DIR / 'de_ags' / '4_niedrig.geo.json'
    ], OUTPUT_DIR, pretty_print=False)
    print(len(found))
