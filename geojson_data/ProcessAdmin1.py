from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessAdmin0(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')

    def get_region_parent(self, fnam, feature):
        return feature['iso_a2']

    def get_region_child(self, fnam, feature):
        return feature['iso_3166_2']

    def get_region_printable(self, fnam, feature):
        r = {}
        for k, v in feature.items():
            if k.startswith('name_'):
                r[k[5:].lower()] = v
        assert r, feature
        return r


if __name__ == '__main__':
    ProcessAdmin0().output_json([
        DATA_DIR / 'admin1' / 'admin_1.json'
    ], OUTPUT_DIR, pretty_print=False)
