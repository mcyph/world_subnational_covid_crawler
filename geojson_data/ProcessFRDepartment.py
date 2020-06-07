from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)
from covid_19_au_grab.overseas.fr_data.FRData import (
    place_map, department_to_region_map
)


class ProcessFRDepartment(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'fr_department')

    def get_region_parent(self, fnam, feature):
        return place_map[department_to_region_map[feature['nom']]]

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['nom'])

    def get_region_printable(self, fnam, feature):
        return feature['nom']


if __name__ == '__main__':
    ProcessFRDepartment().output_json([
        DATA_DIR / 'fr_department' / 'departements.geojson'
    ], OUTPUT_DIR, pretty_print=False)
