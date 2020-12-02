from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessAdmin0(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_0')

    def get_region_parent(self, fnam, feature):
        return ''

    def get_region_child(self, fnam, feature):
        r = feature['ISO_A2'] if not '-' in feature['ISO_A2'] else feature['WB_A2'] # France -99 hack!
        if r == '-99' and feature['SOV_A3'] == 'NOR':
            return 'NO'
        elif r == '-99':
            print(feature)
        return r

    def get_region_printable(self, fnam, feature):
        r = {}
        for k, v in feature.items():
            if k.startswith('NAME_'):
                r[k[5:].lower()] = v
        assert r, feature
        return r


if __name__ == '__main__':
    ProcessAdmin0().output_json([
        DATA_DIR / 'admin0' / 'admin_0_heavycompressed.json'
    ], OUTPUT_DIR, pretty_print=False)
