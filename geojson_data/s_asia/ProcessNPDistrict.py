from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessNPDistricts(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'np_district')

    def get_region_parent(self, fnam, feature):
        return f"NP-P{feature['ADM1_EN']}"

    def get_region_child(self, fnam, feature):
        return feature['DIST_PCODE']

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['DIST_EN']
        }


if __name__ == '__main__':
    ProcessNPDistricts().output_json([
        DATA_DIR / 'np_admin1_districts' / 'np_districts.json'
    ], OUTPUT_DIR, pretty_print=False)
