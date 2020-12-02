from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_db.datatypes.enums import Schemas, DataTypes

iso639_map = {
    'sme': 'se',
    'nor': 'no',
    'sma': 'sma',
    'fkv': 'fkv',
}


class ProcessNOCounty(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')  # NOTE ME: The intention is to overwrite the admin 1 from Natural Earth data

    def get_region_parent(self, fnam, feature):
        return 'NO'

    def get_region_child(self, fnam, feature):
        return 'NO-%s' % feature['fylkesnummer']

    def get_region_printable(self, fnam, feature):
        r = {}
        for navn_dict in feature['navn']:
            r[iso639_map[navn_dict['sprak']]] = navn_dict['navn']
        if not 'en' in r:
            r['en'] = r['no']
        return r


if __name__ == '__main__':
    ProcessNOCounty().output_json([
        DATA_DIR / 'no_counties' / 'no_counties.json'
    ], OUTPUT_DIR, pretty_print=False)
