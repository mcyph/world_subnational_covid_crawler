from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)
from covid_19_au_grab.geojson_data.LabelsToRegionChild import (
    LabelsToRegionChild
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes

ltrc = LabelsToRegionChild()


_province_map = {
    'Western Province': 'LK-1',
    'Central Province': 'LK-2',
    'Southern Province': 'LK-3',
    'Northern Province': 'LK-4',
    'Eastern Province': 'LK-5',
    'North Western Province': 'LK-6',
    'North Central Province': 'LK-7',
    'Uva Province': 'LK-8',
    'Sabaragamuwa Province': 'LK-9',
}


class ProcessCRCanton(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'lk_district')

    def get_region_parent(self, fnam, feature):
        return _province_map[feature['ADM1_EN']+' Province']

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['ADM2_PCODE'])

    def get_region_printable(self, fnam, feature):
        return {
            'ta': feature['ADM2_TA'],
            'en': feature['ADM2_EN'],
            'si': feature['ADM2_SI'],
        }


if __name__ == '__main__':
    ProcessCRCanton().output_json([
        DATA_DIR / 'lk_district' / 'lk_districts.json'
    ], OUTPUT_DIR, pretty_print=False)
