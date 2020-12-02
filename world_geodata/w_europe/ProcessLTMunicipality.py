from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from _utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessLTMunicipality(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'lt_municipality')

    def get_region_parent(self, fnam, feature):
        return 'LT'  # NOTE ME: Is also possible to map to admin_1

    def get_region_child(self, fnam, feature):
        r = normalize_locality_name(
            feature['name'].replace(' r. sav.', '')
                           .replace(' m. sav.', '')
                           .replace(' sav.', '')
                           .replace(' m.', '')
        )
        assert not '.' in r, r
        return r

    def get_region_printable(self, fnam, feature):
        return feature['longName']


if __name__ == '__main__':
    ProcessLTMunicipality().output_json([
        DATA_DIR / 'lt_municipality' / 'lt_municipality.json'
    ], OUTPUT_DIR, pretty_print=False)
