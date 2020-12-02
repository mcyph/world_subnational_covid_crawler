# https://github.com/jlacko/RCzechia
# {"KOD_OKRES":"40185","KOD_LAU1":"CZ0203","NAZ_LAU1":"Kladno","KOD_KRAJ":"3026","KOD_CZNUTS3":"CZ020","NAZ_CZNUTS3":"Stďż˝edoďż˝eskďż˝ kraj"}

from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab._utility.normalize_locality_name import (
    normalize_locality_name
)


class ProcessCZOkres(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'cz_okres')

    def get_region_parent(self, fnam, feature):
        return 'CZ'  # CHECK ME!

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['KOD_LAU1'])

    def get_region_printable(self, fnam, feature):
        return feature['NAZ_LAU1']  # okres_lau_kod


if __name__ == '__main__':
    ProcessCZOkres().output_json([
        DATA_DIR / 'cz_okres' / 'okresy_utf8.json'
    ], OUTPUT_DIR, pretty_print=False)
