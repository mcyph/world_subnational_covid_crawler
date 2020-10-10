from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)
from covid_19_au_grab.overseas.w_europe.uk_data.uk_place_map import place_map


# NOTE: Admin1 seems equvalent to UTLA (upper tier-level authority)
class ProcessUKAdmin1(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')

    def get_region_parent(self, fnam, feature):
        return 'GB'

    def get_region_child(self, fnam, feature):
        if 'ctyua16nm' in feature:
            # England/Wales
            return place_map[feature['ctyua16nm']]
        elif 'LGDNAME' in feature:
            # North Ireland
            return place_map[feature['LGDNAME']]
        elif 'local_authority' in feature:
            # Scotland
            return place_map[feature['local_authority']]
        else:
            raise Exception(feature)

    def get_region_printable(self, fnam, feature):
        if 'ctyua16nm' in feature:
            return feature['ctyua16nm']
        elif 'LGDNAME' in feature:
            return feature['LGDNAME']
        elif 'local_authority' in feature:
            return feature['local_authority']
        else:
            raise Exception(feature)


if __name__ == '__main__':
    ProcessUKAdmin1().output_json([
        DATA_DIR / 'gb_admin1' / 'Counties_and_Unitary_Authorities__December_2016__Boundaries.json',
        DATA_DIR / 'gb_admin1' / 'gb_north_ireland_admin1.json',
        DATA_DIR / 'gb_admin1' / 'scotland_electoral_admin_1.json',
    ], OUTPUT_DIR, pretty_print=False)
