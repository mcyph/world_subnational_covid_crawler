from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessTRNUTS1(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'tr_nuts1')

    def get_region_parent(self, fnam, feature):
        return 'TR'

    def get_region_child(self, fnam, feature):
        return feature['NUTS_ID']

    def get_region_printable(self, fnam, feature):
        return {
            'tr': feature['NUTS_NAME'],
            'en': feature['NAME_LATN']
        }


if __name__ == '__main__':
    ProcessTRNUTS1().output_json([
        DATA_DIR / 'tr_nuts1' / 'tr_nuts_1.geojson'
    ], OUTPUT_DIR, pretty_print=False)
