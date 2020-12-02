from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessNPProvince(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')  # NOTE ME: The intention is to overwrite the admin 1 from Natural Earth data, which has the superceded zones

    def get_region_parent(self, fnam, feature):
        return 'NP'

    def get_region_child(self, fnam, feature):
        return f"NP-P{feature['ADM1_EN']}"

    def get_region_printable(self, fnam, feature):
        return {
            'en': f"Province No. {feature['ADM1_EN']}"
        }


if __name__ == '__main__':
    ProcessNPProvince().output_json([
        DATA_DIR / 'np_admin1_districts' / 'np_admin1.json'
    ], OUTPUT_DIR, pretty_print=False)
