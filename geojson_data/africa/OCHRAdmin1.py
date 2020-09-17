from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class OCHAAdmin1(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'ocha_admin_1')

    def get_region_parent(self, fnam, feature):
        return feature['admin0Pcod']

    def get_region_child(self, fnam, feature):
        return feature['admin1Pcod']

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['admin1Name'],
        }


if __name__ == '__main__':
    OCHAAdmin1().output_json([
        DATA_DIR / 'ocha_admin_1' / 'ocha_admin_1.json'
    ], OUTPUT_DIR, pretty_print=False)
