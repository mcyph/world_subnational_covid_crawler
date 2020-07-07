from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)

cn_map = dict([_line.split() for _line in """
CN-11 CN-BJ
CN-12 CN-TJ
CN-13 CN-HE
CN-14 CN-SX
CN-15 CN-NM
CN-21 CN-LN
CN-22 CN-JL
CN-23 CN-HL
CN-31 CN-SH
CN-32 CN-JS
CN-33 CN-ZJ
CN-34 CN-AH
CN-35 CN-FJ
CN-36 CN-JX
CN-37 CN-SD
CN-41 CN-HA
CN-42 CN-HB
CN-43 CN-HN
CN-44 CN-GD
CN-45 CN-GX
CN-46 CN-HI
CN-50 CN-CQ
CN-51 CN-SC
CN-52 CN-GZ
CN-53 CN-YN
CN-54 CN-XZ
CN-61 CN-SN
CN-62 CN-GS
CN-63 CN-QH
CN-64 CN-NX
CN-65 CN-XJ
CN-71 CN-TW
CN-91 CN-HK
CN-92 CN-MO
""".strip().split('\n')])


class ProcessAdmin0(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')

    def get_region_parent(self, fnam, feature):
        return feature['iso_a2']

    def get_region_child(self, fnam, feature):
        return cn_map.get(feature['iso_3166_2'].upper(), feature['iso_3166_2']).lower()

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
