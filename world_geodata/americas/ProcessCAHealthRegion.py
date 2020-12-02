from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessCAHealthRegion(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'ca_health_region')

    def get_region_parent(self, fnam, feature):
        return f"CA-{feature['Province']}"

    def get_region_child(self, fnam, feature):
        return feature['HR_UID']

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['ENGNAME'],
            'fr': feature['FRENAME']
        }


if __name__ == '__main__':
    ProcessCAHealthRegion().output_json([
        DATA_DIR / 'ca_health' / 'ca_health.geojson'
    ], OUTPUT_DIR, pretty_print=False)
