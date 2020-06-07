from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessUKArea(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'uk_area')

    def get_region_parent(self, fnam, feature):
        return 'GB'

    def get_region_child(self, fnam, feature):
        if 'HBName' in feature:
            return feature['HBName']
        elif 'iso_3166_2' in feature:
            return feature['iso_3166_2']
        else:
            return feature['lhb19nm'].replace(' University Health Board', '')

    def get_region_printable(self, fnam, feature):
        'name_*'
        if 'HBName' in feature:
            # Scotland health board
            return feature['HBName']
        elif 'iso_3166_2' in feature:
            # Standard admin1 - have translations
            r = {}
            for k, v in feature.items():
                if k.startswith('name_'):
                    r[k[5:]] = v
            return r
        else:
            # Wales local health board
            return feature['lhb19nm'].replace(' University Health Board', '')


if __name__ == '__main__':
    ProcessUKArea().output_json([
        DATA_DIR / 'uk_area' / 'gb_england.geojson',
        DATA_DIR / 'uk_area' / 'gb_scotland.geojson',
        DATA_DIR / 'uk_area' / 'gb_wales.geojson'
    ], OUTPUT_DIR, pretty_print=False)
