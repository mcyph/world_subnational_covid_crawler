from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
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

it_provinces = """
IT-23	Valle d'Aosta/Vallée d'Aoste	23
IT-AL	Alessandria	21
IT-AN	Ancona	57
IT-AR	Arezzo	52
IT-AP	Ascoli Piceno	57
IT-AT	Asti	21
IT-AV	Avellino	72
IT-BT	Barletta-Andria-Trani	75
IT-BL	Belluno	34
IT-BN	Benevento	72
IT-BG	Bergamo	25
IT-BI	Biella	21
IT-BS	Brescia	25
IT-BR	Brindisi	75
IT-CB	Campobasso	67
IT-CE	Caserta	72
IT-CZ	Catanzaro	78
IT-CH	Chieti	65
IT-CO	Como	25
IT-CS	Cosenza	78
IT-CR	Cremona	25
IT-KR	Crotone	78
IT-CN	Cuneo	21
IT-FM	Fermo	57
IT-FE	Ferrara	45
IT-FG	Foggia	75
IT-FC	Forlì-Cesena	45
IT-FR	Frosinone	62
IT-GR	Grosseto	52
IT-IM	Imperia	42
IT-IS	Isernia	67
IT-SP	La Spezia	42
IT-AQ	L'Aquila	65
IT-LT	Latina	62
IT-LE	Lecce	75
IT-LC	Lecco	25
IT-LI	Livorno	52
IT-LO	Lodi	25
IT-LU	Lucca	52
IT-MC	Macerata	57
IT-MN	Mantova	25
IT-MS	Massa-Carrara	52
IT-MT	Matera	77
IT-MO	Modena	45
IT-MB	Monza e Brianza	25
IT-MB	Monza e della Brianza	25
IT-NO	Novara	21
IT-NU	Nuoro	88
IT-OR	Oristano	88
IT-PD	Padova	34
IT-PR	Parma	45
IT-PV	Pavia	25
IT-PG	Perugia	55
IT-PU	Pesaro e Urbino	57
IT-PE	Pescara	65
IT-PC	Piacenza	45
IT-PI	Pisa	52
IT-PT	Pistoia	52
IT-PZ	Potenza	77
IT-PO	Prato	52
IT-RA	Ravenna	45
IT-RE	Reggio Emilia	45
IT-RE	Reggio nell'Emilia	45
IT-RI	Rieti	62
IT-RN	Rimini	45
IT-RO	Rovigo	34
IT-SA	Salerno	72
IT-SS	Sassari	88
IT-SV	Savona	42
IT-SI	Siena	52
IT-SO	Sondrio	25
IT-SD	Sud Sardegna	88
IT-TA	Taranto	75
IT-TE	Teramo	65
IT-TR	Terni	55
IT-TV	Treviso	34
IT-VA	Varese	25
IT-VB	Verbano-Cusio-Ossola	21
IT-VC	Vercelli	21
IT-VR	Verona	34
IT-VV	Vibo Valentia	78
IT-VI	Vicenza	34
IT-VT	Viterbo	62 
IT-BZ	Bolzano	32
IT-BZ	Bolzano/Bozen	32
IT-TN	Trento	32 
IT-AG	Agrigento	82
IT-CL	Caltanissetta	82
IT-EN	Enna	82
IT-RG	Ragusa	82
IT-SR	Siracusa	82
IT-TP	Trapani	82 
IT-BA	Bari	75
IT-BO	Bologna	45
IT-CA	Cagliari	88
IT-CT	Catania	82
IT-FI	Firenze	52
IT-GE	Genova	42
IT-ME	Messina	82
IT-MI	Milano	25
IT-NA	Napoli	72
IT-PA	Palermo	82
IT-RC	Reggio Calabria	78
IT-RC	Reggio di Calabria	78
IT-RM	Roma	62
IT-TO	Torino	21
IT-VE	Venezia	34
IT-UD	Udine	IT-36
IT-CI	Carbonia-Iglesias	88
IT-GO	Gorizia	36
IT-VS	Medio Campidano	88
IT-OG	Ogliastra	88
IT-OT	Olbia-Tempio	88
IT-PN	Pordenone	36
IT-TS	Trieste	36
IT-UD	Udine	36
""".strip()


def get_province_to_iso_code():
    r = {}
    for iso_code, province, id in [
        i.split('\t') for i in it_provinces.split('\n')
    ]:
        r[province] = iso_code
    return r


province_to_iso_code = get_province_to_iso_code()


class ProcessITProvince(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'it_province')

    def get_region_parent(self, fnam, feature):
        return it_regions[feature['reg_name']]

    def get_region_child(self, fnam, feature):
        print(feature)
        return province_to_iso_code[feature['prov_name']]

    def get_region_printable(self, fnam, feature):
        return feature['prov_name']


if __name__ == '__main__':
    ProcessITProvince().output_json([
        DATA_DIR / 'it_province' / 'it_province.geojson'
    ], OUTPUT_DIR, pretty_print=False)
