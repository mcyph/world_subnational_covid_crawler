# NOTE: LTLA = lower tier-level authority, in finer granularity than UTLA
from covid_19_au_grab.world_geodata.ProcessGeoJSONBase import ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
from covid_19_au_grab._utility.normalize_locality_name import normalize_locality_name
from covid_19_au_grab.covid_crawlers.w_europe.uk_data.uk_place_map import place_map


class ProcessUKArea(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'uk_area')

    def get_region_parent(self, fnam, feature):
        return 'GB'

    def get_region_child(self, fnam, feature):
        if 'LGDNAME' in feature:
            # North Ireland
            return place_map[feature['LGDNAME']]
        elif 'LAD13NM' in feature:
            return normalize_locality_name(feature['LAD13NM'])
        else:
            raise Exception(feature)

    def get_region_printable(self, fnam, feature):
        if 'LGDNAME' in feature:
            return feature['LGDNAME']
        elif 'LAD13NM' in feature:
            return feature['LAD13NM']
        else:
            raise Exception(feature)


if __name__ == '__main__':
    ProcessUKArea().output_json([
        DATA_DIR / 'gb_ltla' / 'lad_gb.json',
        DATA_DIR / 'gb_ltla' / 'gb_north_ireland_admin1.json'
    ], OUTPUT_DIR, pretty_print=False)
