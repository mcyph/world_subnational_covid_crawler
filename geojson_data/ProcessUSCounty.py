import csv

from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


def get_fips_map():
    r = {}
    with open(DATA_DIR / 'us_county' / 'us_state_fips_codes.csv',
              'r', encoding='utf-8') as f:
        for name, postal_code, fips in csv.reader(f):
            r[fips] = postal_code
    return r


fips_map = get_fips_map()


class ProcessNZDHB(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'us_county')

    def get_region_parent(self, fnam, feature):
        return 'us-'+fips_map[feature['STATEFP']]

    def get_region_child(self, fnam, feature):
        return feature['COUNTYFP']  # FIPS county code

    def get_region_printable(self, fnam, feature):
        return feature['NAME']


if __name__ == '__main__':
    ProcessNZDHB().output_json([
        DATA_DIR / 'us_county' / 'us_county.geojson'
    ], OUTPUT_DIR, pretty_print=False)
