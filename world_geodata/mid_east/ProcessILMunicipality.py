from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab._utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessILProvince(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'il_municipality')

    def get_region_parent(self, fnam, feature):
        return 'IL'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['MUN_ENG'])

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['MUN_ENG'],
            'he': feature['MUN_HEB']
        }


if __name__ == '__main__':
    ProcessILProvince().output_json([
        DATA_DIR / 'il_municipality' / 'il_municipalities.json'
    ], OUTPUT_DIR, pretty_print=False)
