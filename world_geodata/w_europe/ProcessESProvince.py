from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessESProvince(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'es_province')

    def get_region_parent(self, fnam, feature):
        return feature['iso_a2']

    def get_region_child(self, fnam, feature):
        return feature['iso_3166_2'].lower()

    def get_region_printable(self, fnam, feature):
        r = {}
        for k, v in feature.items():
            if k.startswith('name_'):
                r[k[5:].lower()] = v
        assert r, feature
        return r


if __name__ == '__main__':
    ProcessESProvince().output_json([
        DATA_DIR / 'es_province' / 'es_province.json'
    ], OUTPUT_DIR, pretty_print=False)
