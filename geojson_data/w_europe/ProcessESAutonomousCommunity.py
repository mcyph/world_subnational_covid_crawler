from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1
)

region_map = {
    'Ciudad Autónoma de Melilla': 'ES-ML',
    'Ciudad Autónoma de Ceuta': 'ES-CE',
    'La Rioja': 'ES-RI',
    'País Vasco/Euskadi': 'ES-PV',
    'Comunidad Foral de Navarra': 'ES-NC',
    'Región de Murcia': 'ES-MC',
    'Comunidad de Madrid': 'ES-MD',
    'Galicia': 'ES-GA',
    'Extremadura': 'ES-EX',
    'Comunitat Valenciana': 'ES-VC',
    'Cataluña/Catalunya': 'ES-CT',
    'Castilla-La Mancha': 'ES-CM',
    'Castilla y León': 'ES-CL',
    'Cantabria': 'ES-CB',
    'Illes Balears': 'ES-IB',
    'Principado de Asturias': 'ES-AS',
    'Aragón': 'ES-AR',
    'Andalucía': 'ES-AN',
}


class ProcessESAutonomousCommunity(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')  # NOTE ME: The intention is to overwrite the admin 1 from Natural Earth data, which has provinces (which I think should be admin 2?)

    def get_region_parent(self, fnam, feature):
        return 'ES'

    def get_region_child(self, fnam, feature):
        return region_map[feature['NAMEUNIT']]

    def get_region_printable(self, fnam, feature):
        return {
            'en': feature['NAMEUNIT']
        }


if __name__ == '__main__':
    ProcessESAutonomousCommunity().output_json([
        DATA_DIR / 'es_autonomous_community' / 'es_autonomous_community.json'
    ], OUTPUT_DIR, pretty_print=False)
