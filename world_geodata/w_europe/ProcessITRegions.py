from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)

it_regions = dict([i.split('\t')[::-1] for i in """
IT-65	Abruzzo
IT-77	Basilicata
IT-78	Calabria
IT-72	Campania
IT-45	Emilia-Romagna
IT-62	Lazio
IT-42	Liguria
IT-25	Lombardia
IT-57	Marche
IT-67	Molise
IT-21	Piemonte
IT-75	Puglia
IT-52	Toscana
IT-55	Umbria
IT-34	Veneto
IT-36	Friuli Venezia Giulia
IT-36	Friuli-Venezia Giulia
IT-88	Sardegna
IT-82	Sicilia
IT-32	Trentino-Alto Adige
IT-32	Trentino-Alto Adige/Südtirol
IT-23	Valle d'Aosta
IT-23	Valle d'Aosta/Vallée d'Aoste
""".strip().split('\n')])


class ProcessITProvince(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'admin_1')

    def get_region_parent(self, fnam, feature):
        return 'IT'

    def get_region_child(self, fnam, feature):
        return it_regions[feature['reg_name']]

    def get_region_printable(self, fnam, feature):
        return feature['reg_name']


if __name__ == '__main__':
    ProcessITProvince().output_json([
        DATA_DIR / 'it_province' / 'it_province.geojson'
    ], OUTPUT_DIR, pretty_print=False)
