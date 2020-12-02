from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab._utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessPTMunicipality(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'pt_municipality')

    def get_region_parent(self, fnam, feature):
        return 'PT' # CHECK ME!

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['NAME_2'])

    def get_region_printable(self, fnam, feature):
        return feature['NAME_2']


if __name__ == '__main__':
    ProcessPTMunicipality().output_json([
        DATA_DIR / 'pt_municipality' / 'pt_municipality.json'
    ], OUTPUT_DIR, pretty_print=False)
