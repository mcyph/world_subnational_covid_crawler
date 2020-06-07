from os import listdir
from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)

place_map = dict([i.split('\t')[::-1] for i in """
BR-AC	Acre
BR-AL	Alagoas
BR-AP	Amapá
BR-AM	Amazonas
BR-BA	Bahia
BR-CE	Ceará
BR-DF	Distrito Federal
BR-ES	Espírito Santo
BR-GO	Goiás
BR-MA	Maranhão
BR-MT	Mato Grosso
BR-MS	Mato Grosso do Sul
BR-MG	Minas Gerais
BR-PA	Pará
BR-PB	Paraíba
BR-PR	Paraná
BR-PE	Pernambuco
BR-PI	Piauí
BR-RJ	Rio de Janeiro
BR-RN	Rio Grande do Norte
BR-RS	Rio Grande do Sul
BR-RO	Rondônia
BR-RR	Roraima
BR-SC	Santa Catarina
BR-SP	São Paulo
BR-SE	Sergipe
BR-TO	Tocantins 
""".strip().split('\n')])


class ProcessBGDistrict(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'br_city')

    def get_region_parent(self, fnam, feature):
        iso_code = 'BR-'+feature['UF']
        assert iso_code in place_map.values()
        return iso_code

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(feature['NOME'])

    def get_region_printable(self, fnam, feature):
        return feature['NOME']


if __name__ == '__main__':
    ProcessBGDistrict().output_json([
        DATA_DIR / 'br_city' / fnam
        for fnam in listdir(DATA_DIR / 'br_city')
        if fnam.endswith('.min.json')
    ], OUTPUT_DIR, pretty_print=False)
