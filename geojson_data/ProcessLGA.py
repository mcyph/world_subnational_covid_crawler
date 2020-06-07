from covid_19_au_grab.normalize_locality_name import normalize_locality_name
from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class LGABoundaries(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'lga')

    def get_region_parent(self, fnam, feature):
        if 'wa' in fnam: return 'AU-WA'
        elif 'nsw' in fnam: return 'AU-NSW'
        elif 'vic' in fnam: return 'AU-VIC'
        elif 'nt' in fnam: return 'AU-NT'
        elif 'qld' in fnam: return 'AU-QLD'
        elif 'sa' in fnam: return 'AU-SA'
        elif 'tas' in fnam: return 'AU-TAS'
        else: raise Exception(fnam)

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(
            self.get_region_printable(fnam, feature)
        )

    def get_region_printable(self, fnam, feature):
        if 'wa' in fnam:
            return feature['wa_lga_s_3'].title().strip()
        elif 'nsw' in fnam:
            return feature['nsw_lga__3'].title().strip()
        elif 'vic' in fnam:
            city_name = feature['vic_lga__2']
            city = city_name.split(" ")
            city.pop()
            city_name = ' '.join(city)
            return city_name.title().strip()
        elif 'nt' in fnam:
            return feature['nt_lga_s_3'].title().strip()
        elif 'qld' in fnam:
            return feature['qld_lga__3'].title().strip()
        elif 'sa' in fnam:
            return feature['abbname'].title().strip()
        elif 'tas' in fnam:
            return feature['tas_lga__3'].title().strip()
        else:
            raise Exception(fnam)


if __name__ == '__main__':
    LGABoundaries().output_json([
        DATA_DIR / 'au' / 'lga' / 'lga_nsw.geojson',
        DATA_DIR / 'au' / 'lga' / 'lga_nt.geojson',
        DATA_DIR / 'au' / 'lga' / 'lga_qld.geojson',
        DATA_DIR / 'au' / 'lga' / 'lga_sa.geojson',
        DATA_DIR / 'au' / 'lga' / 'lga_tas.geojson',
        DATA_DIR / 'au' / 'lga' / 'lga_vic.geojson',
        DATA_DIR / 'au' / 'lga' / 'lga_wa.geojson',
    ], OUTPUT_DIR, pretty_print=False)
