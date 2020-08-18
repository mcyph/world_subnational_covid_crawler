from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)


class ProcessUKArea(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'uk_area')

    def get_region_parent(self, fnam, feature):
        return 'GB'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['LAD13NM'])

    def get_region_printable(self, fnam, feature):
        return feature['LAD13NM']


if __name__ == '__main__':
    ProcessUKArea().output_json([
        DATA_DIR / 'uk_area' / 'lad_gb.json',
        #DATA_DIR / 'uk_area' / 'lad_ni.json'
    ], OUTPUT_DIR, pretty_print=False)
