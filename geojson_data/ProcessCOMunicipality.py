from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)

place_map = dict([i.split('\t')[::-1] for i in """
CO-DC	Distrito Capital de Bogotá
CO-DC	Bogotá, D.C.
CO-AMA	Amazonas
CO-ANT	Antioquia
CO-ARA	Arauca
CO-ATL	Atlántico
CO-BOL	Bolívar
CO-BOY	Boyacá
CO-CAL	Caldas
CO-CAQ	Caquetá
CO-CAS	Casanare
CO-CAU	Cauca
CO-CES	Cesar
CO-COR	Córdoba
CO-CUN	Cundinamarca
CO-CHO	Chocó
CO-GUA	Guainía
CO-GUV	Guaviare
CO-HUI	Huila
CO-LAG	La Guajira
CO-MAG	Magdalena
CO-MET	Meta
CO-NAR	Nariño
CO-NSA	Norte de Santander
CO-PUT	Putumayo
CO-QUI	Quindío
CO-QUI	Quindio
CO-RIS	Risaralda
CO-SAP	San Andrés, Providencia y Santa Catalina
CO-SAN	Santander
CO-SUC	Sucre
CO-TOL	Tolima
CO-VAC	Valle del Cauca
CO-VAU	Vaupés
CO-VID	Vichada 
""".strip().split('\n')])


class ProcessCOMunicipality(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'co_municipality')

    def get_region_parent(self, fnam, feature):
        return place_map[feature['admin1Name_es']]

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['admin2Name_es'])

    def get_region_printable(self, fnam, feature):
        return feature['admin2Name_es']


if __name__ == '__main__':
    ProcessCOMunicipality().output_json([
        DATA_DIR / 'co_municipality' / 'co_municipality.geojson'
    ], OUTPUT_DIR, pretty_print=False)
