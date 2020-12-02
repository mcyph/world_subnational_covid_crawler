import json

from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_crawlers._base_classes.GithubRepo import GithubRepo
from _utility.get_package_dir import get_overseas_dir
from world_geodata.LabelsToRegionChild import LabelsToRegionChild


ltrc = LabelsToRegionChild()


province_map = dict([i.split('\t')[::-1] for i in """
IT-AL	Alessandria
IT-AN	Ancona
IT-AR	Arezzo
IT-AP	Ascoli Piceno
IT-AT	Asti
IT-AV	Avellino
IT-BT	Barletta-Andria-Trani
IT-BL	Belluno
IT-BN	Benevento
IT-BG	Bergamo
IT-BI	Biella
IT-BS	Brescia
IT-BR	Brindisi
IT-CB	Campobasso
IT-CE	Caserta
IT-CZ	Catanzaro
IT-CH	Chieti
IT-CO	Como
IT-CS	Cosenza
IT-CR	Cremona
IT-KR	Crotone
IT-CN	Cuneo
IT-FM	Fermo
IT-FE	Ferrara
IT-FG	Foggia
IT-FC	Forlì-Cesena
IT-FR	Frosinone
IT-GR	Grosseto
IT-IM	Imperia
IT-IS	Isernia
IT-SP	La Spezia
IT-AQ	L'Aquila
IT-LT	Latina
IT-LE	Lecce
IT-LC	Lecco
IT-LI	Livorno
IT-LO	Lodi
IT-LU	Lucca
IT-MC	Macerata
IT-MN	Mantova
IT-MS	Massa-Carrara
IT-MS	Massa Carrara
IT-MT	Matera
IT-MO	Modena
IT-MB	Monza e Brianza
IT-MB	Monza e della Brianza
IT-NO	Novara
IT-NU	Nuoro
IT-OR	Oristano
IT-PD	Padova
IT-PR	Parma
IT-PV	Pavia
IT-PG	Perugia
IT-PU	Pesaro e Urbino
IT-PE	Pescara
IT-PC	Piacenza
IT-PI	Pisa
IT-PT	Pistoia
IT-PZ	Potenza
IT-PO	Prato
IT-RA	Ravenna
IT-RE	Reggio Emilia
IT-RE	Reggio nell'Emilia
IT-RI	Rieti
IT-RN	Rimini
IT-RO	Rovigo
IT-SA	Salerno
IT-SS	Sassari
IT-SV	Savona
IT-SI	Siena
IT-SO	Sondrio
IT-SD	Sud Sardegna
IT-TA	Taranto
IT-TE	Teramo
IT-TR	Terni
IT-TV	Treviso
IT-VA	Varese
IT-VB	Verbano-Cusio-Ossola
IT-VC	Vercelli
IT-VR	Verona
IT-VV	Vibo Valentia
IT-VI	Vicenza
IT-VT	Viterbo
IT-BZ	Bolzano
IT-TN	Trento
IT-BA	Bari
IT-BO	Bologna
IT-CA	Cagliari
IT-CT	Catania
IT-FI	Firenze
IT-GE	Genova
IT-ME	Messina
IT-MI	Milano
IT-NA	Napoli
IT-PA	Palermo
IT-RC	Reggio di Calabria
IT-RC	Reggio Calabria
IT-RM	Roma
IT-TO	Torino
IT-VE	Venezia
IT-CI	Carbonia-Iglesias
IT-GO	Gorizia
IT-VS	Medio Campidano
IT-OG	Ogliastra
IT-OT	Olbia-Tempio
IT-PN	Pordenone
IT-TS	Trieste
IT-UD	Udine
IT-AG	Agrigento
IT-CL	Caltanissetta
IT-EN	Enna
IT-RG	Ragusa
IT-SR	Siracusa
IT-TP	Trapani
IT-AO	Aosta
""".strip().split('\n')])


class ITData(GithubRepo):
    SOURCE_URL = 'https://github.com/pcm-dpc/COVID-19'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'it_protezionecivile_covid19'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'it' / 'COVID-19',
                            github_url='https://github.com/pcm-dpc/COVID-19')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('it_province', 'friuli venezia giulia', 'it-ud')
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_national_data())
        r.extend(self._get_province_data())
        r.extend(self._get_regions_data())
        return r

    def _get_national_data(self):
        r = self.sdpf()

        # dpc-covid19-ita-andamento-nazionale.json
        # [
        #     {
        #         "data": "2020-02-24T18:00:00",
        #         "stato": "ITA",
        #         "ricoverati_con_sintomi": 101,
        #         "terapia_intensiva": 26,
        #         "totale_ospedalizzati": 127,
        #         "isolamento_domiciliare": 94,
        #         "totale_positivi": 221,
        #         "variazione_totale_positivi": 0,
        #         "nuovi_positivi": 221,
        #         "dimessi_guariti": 1,
        #         "deceduti": 7,
        #         "totale_casi": 229,
        #         "tamponi": 4324,
        #         "casi_testati": null,
        #         "note_it": "",
        #         "note_en": ""
        #     },

        with open(self.get_path_in_dir('dati-json/dpc-covid19-ita-andamento-nazionale.json'),
                  'r', encoding='utf-8') as f:
            for item in json.loads(f.read()):
                date = self.convert_date(item['data'].split('T')[0])
                state = item['stato']
                assert state == 'ITA'

                #hospitalized_with_symptoms = item['ricoverati_con_sintomi']
                icu = item['terapia_intensiva']
                hospitalized = item['totale_ospedalizzati']
                #isolation = item['isolamento_domiciliare']
                active = item['totale_positivi']
                new = item['variazione_totale_positivi']
                recovered = item['dimessi_guariti']
                deaths = item['deceduti']
                total = item['totale_casi']
                tests_total = item['tamponi']
                #tests_total_people = item['casi_testati']

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.STATUS_HOSPITALIZED,
                    value=int(hospitalized),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.NEW,
                    value=int(new),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=recovered,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.STATUS_DEATHS,
                    value=deaths,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.TOTAL,
                    value=total,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.TESTS_TOTAL,
                    value=tests_total,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='IT',
                    datatype=DataTypes.STATUS_ICU,
                    value=icu,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r

    def _get_province_data(self):
        r = self.sdpf()

        # dpc-covid19-ita-province.json
        # [
        #     {
        #         "data": "2020-02-24T18:00:00",
        #         "stato": "ITA",
        #         "codice_regione": 13,
        #         "denominazione_regione": "Abruzzo",
        #         "codice_provincia": 69,
        #         "denominazione_provincia": "Chieti",
        #         "sigla_provincia": "CH",
        #         "lat": 42.35103167,
        #         "long": 14.16754574,
        #         "totale_casi": 0,
        #         "note_it": "",
        #         "note_en": ""
        #     },

        # NOTE: Provinces/regions are reversed from most other countries.
        # TODO: Change the admin_1 to be regions and have provinces as a separate schema!!! ======================

        with open(self.get_path_in_dir('dati-json/dpc-covid19-ita-province.json'),
                  'r', encoding='utf-8') as f:
            for item in json.loads(f.read()):
                date = self.convert_date(item['data'].split('T')[0])

                if item['denominazione_provincia'] == 'In fase di definizione/aggiornamento':
                    continue
                elif item['denominazione_provincia'] == 'In fase di definizione':
                    continue
                elif item['denominazione_provincia'] == 'fuori Regione/P.A.':
                    continue
                elif item['denominazione_provincia'] == 'Fuori Regione / Provincia Autonoma':
                    continue

                region_child = province_map[item['denominazione_provincia']]
                region_parent = item['denominazione_regione'].lower()

                if region_parent == 'friuli venezia giulia':
                    region_parent = 'it-36'
                elif region_parent == 'p.a. bolzano':
                    region_parent = 'it-32'
                elif region_parent == 'p.a. trento':
                    region_parent = 'it-32'
                elif region_parent == 'valle d\'aosta':
                    region_parent = 'it-23'
                    region_child = 'it-23'
                else:
                    region_parent = ltrc.get_by_label('admin_1', 'it', region_parent)

                r.append(
                    region_schema=Schemas.IT_PROVINCE,
                    region_parent=region_parent,
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(item['totale_casi']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r

    def _get_regions_data(self):
        r = self.sdpf()

        # dpc-covid19-ita-regioni.json
        # [
        #     {
        #         "data": "2020-02-24T18:00:00",
        #         "stato": "ITA",
        #         "codice_regione": 13,
        #         "denominazione_regione": "Abruzzo",
        #         "lat": 42.35122196,
        #         "long": 13.39843823,
        #         "ricoverati_con_sintomi": 0,
        #         "terapia_intensiva": 0,
        #         "totale_ospedalizzati": 0,
        #         "isolamento_domiciliare": 0,
        #         "totale_positivi": 0,
        #         "variazione_totale_positivi": 0,
        #         "nuovi_positivi": 0,
        #         "dimessi_guariti": 0,
        #         "deceduti": 0,
        #         "totale_casi": 0,
        #         "tamponi": 5,
        #         "casi_testati": null,
        #         "note_it": "",
        #         "note_en": ""
        #     },

        with open(self.get_path_in_dir('dati-json/dpc-covid19-ita-regioni.json'),
                  'r', encoding='utf-8') as f:
            for item in json.loads(f.read()):
                date = self.convert_date(item['data'].split('T')[0])

                # hospitalized_with_symptoms = item['ricoverati_con_sintomi']
                icu = item['terapia_intensiva']
                hospitalized = item['totale_ospedalizzati']
                # isolation = item['isolamento_domiciliare']
                active = item['totale_positivi']
                new = item['variazione_totale_positivi']
                recovered = item['dimessi_guariti']
                deaths = item['deceduti']
                total = item['totale_casi']
                tests_total = item['tamponi']
                # tests_total_people = item['casi_testati']

                region_child = item['denominazione_regione'].lower()
                if region_child == 'friuli venezia giulia':
                    region_child = 'it-36'
                elif region_child == 'p.a. bolzano':
                    region_child = 'it-32'
                elif region_child == 'p.a. trento':
                    region_child = 'it-32'
                elif region_child == 'valle d\'aosta':
                    region_child = 'it-23'

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_HOSPITALIZED,
                    value=int(hospitalized),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.NEW,
                    value=int(new),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(recovered),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(deaths),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.TESTS_TOTAL,
                    value=int(tests_total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IT',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ICU,
                    value=int(icu),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ITData().get_datapoints())
