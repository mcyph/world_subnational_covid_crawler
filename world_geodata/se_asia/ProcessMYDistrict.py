from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from _utility.normalize_locality_name import (
    normalize_locality_name
)


place_map = dict([i.split('\t')[::-1] for i in """
MY-14	Wilayah Persekutuan Kuala Lumpur
MY-14	W.P. Kuala Lumpur
MY-15	Wilayah Persekutuan Labuan
MY-15	W.P. Labuan
MY-16	Wilayah Persekutuan Putrajaya
MY-16	W.P. Putrajaya
MY-01	Johor
MY-02	Kedah
MY-02	Kedeh
MY-03	Kelantan
MY-04	Melaka
MY-05	Negeri Sembilan
MY-05	Negeri
MY-06	Pahang
MY-08	Perak
MY-09	Perlis
MY-07	Pulau Pinang
MY-12	Sabah
MY-13	Sarawak
MY-10	Selangor
MY-11	Terengganu
""".strip().split('\n')])


class ProcessMYDistrict(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'my_district')

    def get_region_parent(self, fnam, feature):
        return 'MY' #place_map[feature['ADM1_EN']]

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['ADM2_EN'])

    def get_region_printable(self, fnam, feature):
        return feature['ADM2_EN']


if __name__ == '__main__':
    ProcessMYDistrict().output_json([
        DATA_DIR / 'my_district' / 'my_districts.json'
    ], OUTPUT_DIR, pretty_print=False)
