import json
from os import listdir

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


DISTRICT_CASE = "https://services6.arcgis.com/MpOjf90wsc96wTq1/arcgis/rest/services/Case/FeatureServer/0/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&&outFields=*"
SUB_DISTRICT_CASE = "https://services6.arcgis.com/MpOjf90wsc96wTq1/arcgis/rest/services/COVID19_Daerah_Mukim_Parlimen_250320/FeatureServer/0/query?f=json&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometry={%22xmin%22%3A0%2C%22ymin%22%3A0%2C%22xmax%22%3A999999999%2C%22ymax%22%3A9999999%2C%22spatialReference%22%3A{%22wkid%22%3A102100}}&outFields=*"


class MYESRIDashData(URLBase):
    # Remember to send e-mail to below link!!! =======================================================================================
    SOURCE_URL = 'https://www.arcgis.com/apps/opsdashboard/index.html#/6520fd7121374686aa35578ffe2d2cb7'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'my_esri_dash'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'my' / 'esri_dash_data',
             urls_dict={
                 'district_case.json': URL(
                     DISTRICT_CASE,
                     static_file=False
                 ),
                 'sub_district_case.json': URL(
                     SUB_DISTRICT_CASE,
                     static_file=False
                 ),
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'my', 'johor'): ('admin_1', 'my', 'my-01'),
                ('admin_1', 'my', 'kedah'): ('admin_1', 'my', 'my-02'),
                ('admin_1', 'my', 'kelantan'): ('admin_1', 'my', 'my-03'),
                ('admin_1', 'my', 'kuala lumpur'): ('admin_1', 'my', 'my-14'),
                ('admin_1', 'my', 'labuan'): ('admin_1', 'my', 'my-15'),
                ('admin_1', 'my', 'melaka'): ('admin_1', 'my', 'my-04'),
                ('admin_1', 'my', 'my-01'): ('admin_1', 'my', 'my-01'),
                ('admin_1', 'my', 'my-02'): ('admin_1', 'my', 'my-02'),
                ('admin_1', 'my', 'my-03'): ('admin_1', 'my', 'my-03'),
                ('admin_1', 'my', 'my-04'): ('admin_1', 'my', 'my-04'),
                ('admin_1', 'my', 'my-05'): ('admin_1', 'my', 'my-05'),
                ('admin_1', 'my', 'my-06'): ('admin_1', 'my', 'my-06'),
                ('admin_1', 'my', 'my-07'): ('admin_1', 'my', 'my-07'),
                ('admin_1', 'my', 'my-08'): ('admin_1', 'my', 'my-08'),
                ('admin_1', 'my', 'my-09'): ('admin_1', 'my', 'my-09'),
                ('admin_1', 'my', 'my-10'): ('admin_1', 'my', 'my-10'),
                ('admin_1', 'my', 'my-11'): ('admin_1', 'my', 'my-11'),
                ('admin_1', 'my', 'my-12'): ('admin_1', 'my', 'my-12'),
                ('admin_1', 'my', 'my-13'): ('admin_1', 'my', 'my-13'),
                ('admin_1', 'my', 'my-14'): ('admin_1', 'my', 'my-14'),
                ('admin_1', 'my', 'my-15'): ('admin_1', 'my', 'my-15'),
                ('admin_1', 'my', 'my-16'): ('admin_1', 'my', 'my-16'),
                ('admin_1', 'my', 'negeri sembilan'): ('admin_1', 'my', 'my-05'),
                ('admin_1', 'my', 'pahang'): ('admin_1', 'my', 'my-06'),
                ('admin_1', 'my', 'perak'): ('admin_1', 'my', 'my-08'),
                ('admin_1', 'my', 'perlis'): ('admin_1', 'my', 'my-09'),
                ('admin_1', 'my', 'pulau pinang'): ('admin_1', 'my', 'my-07'),
                ('admin_1', 'my', 'putrajaya'): ('admin_1', 'my', 'my-16'),
                ('admin_1', 'my', 'sabah'): ('admin_1', 'my', 'my-12'),
                ('admin_1', 'my', 'sarawak'): ('admin_1', 'my', 'my-13'),
                ('admin_1', 'my', 'selangor'): ('admin_1', 'my', 'my-10'),
                ('admin_1', 'my', 'terengganu'): ('admin_1', 'my', 'my-11'),
                ('admin_1', 'my', 'tiada data'): None,
                ('my_district', 'my', 'alor gajah'): ('my_district', 'my', 'alor gajah'),
                ('my_district', 'my', 'asajaya'): ('my_district', 'my', 'asajaya'),
                ('my_district', 'my', 'bachok'): ('my_district', 'my', 'bachok'),
                ('my_district', 'my', 'baling'): ('my_district', 'my', 'baling'),
                ('my_district', 'my', 'bandar baharu'): ('my_district', 'my', 'bandar baharu'),
                ('my_district', 'my', 'bandar bahru'): ('my_district', 'my', 'bandar baharu'),
                ('my_district', 'my', 'bandar tun razak'): None,
                ('my_district', 'my', 'bangsar'): None,
                ('my_district', 'my', 'barat daya'): ('my_district', 'my', 'barat daya'),
                ('my_district', 'my', 'batang padang'): ('my_district', 'my', 'batang padang'),
                ('my_district', 'my', 'batu'): None,
                ('my_district', 'my', 'batu pahat'): ('my_district', 'my', 'batu pahat'),
                ('my_district', 'my', 'bau'): ('my_district', 'my', 'bau'),
                ('my_district', 'my', 'beaufort'): ('my_district', 'my', 'beaufort'),
                ('my_district', 'my', 'bentong'): ('my_district', 'my', 'bentong'),
                ('my_district', 'my', 'bera'): ('my_district', 'my', 'bera'),
                ('my_district', 'my', 'besut'): ('my_district', 'my', 'besut'),
                ('my_district', 'my', 'betong'): ('my_district', 'my', 'betong'),
                ('my_district', 'my', 'bintulu'): ('my_district', 'my', 'bintulu'),
                ('my_district', 'my', 'brickfields'): None,
                ('my_district', 'my', 'bukit damansara'): None,
                ('my_district', 'my', 'bukit jalil'): None,
                ('my_district', 'my', 'bukit bintang'): None,
                ('my_district', 'my', 'cameron highlands'): ('my_district', 'my', 'cameron highlands'),
                ('my_district', 'my', 'cheras'): None,
                ('my_district', 'my', 'dalat'): ('my_district', 'my', 'dalat'),
                ('my_district', 'my', 'daro'): ('my_district', 'my', 'daro'),
                ('my_district', 'my', 'dungun'): ('my_district', 'my', 'dungun'),
                ('my_district', 'my', 'duta'): None,
                ('my_district', 'my', 'gombak'): ('my_district', 'my', 'gombak'),
                ('my_district', 'my', 'gua musang'): ('my_district', 'my', 'gua musang'),
                ('my_district', 'my', 'hilir perak'): ('my_district', 'my', 'hilir perak'),
                ('my_district', 'my', 'hulu langat'): None,
                ('my_district', 'my', 'hulu perak'): None,
                ('my_district', 'my', 'hulu selangor'): None,
                ('my_district', 'my', 'hulu terengganu'): ('my_district', 'my', 'hulu terengganu'),
                ('my_district', 'my', 'ibu kota'): None,
                ('my_district', 'my', 'jasin'): ('my_district', 'my', 'jasin'),
                ('my_district', 'my', 'jelebu'): ('my_district', 'my', 'jelebu'),
                ('my_district', 'my', 'jeli'): ('my_district', 'my', 'jeli'),
                ('my_district', 'my', 'jempol'): ('my_district', 'my', 'jempol'),
                ('my_district', 'my', 'jerantut'): ('my_district', 'my', 'jerantut'),
                ('my_district', 'my', 'johor bahru'): ('my_district', 'my', 'johor bahru'),
                ('my_district', 'my', 'julau'): ('my_district', 'my', 'julau'),
                ('my_district', 'my', 'kampar'): ('my_district', 'my', 'kampar'),
                ('my_district', 'my', 'kampung bharu'): None,
                ('my_district', 'my', 'kangar'): None,
                ('my_district', 'my', 'kanowit'): ('my_district', 'my', 'kanowit'),
                ('my_district', 'my', 'kapit'): ('my_district', 'my', 'kapit'),
                ('my_district', 'my', 'kemaman'): ('my_district', 'my', 'kemaman'),
                ('my_district', 'my', 'keningau'): ('my_district', 'my', 'keningau'),
                ('my_district', 'my', 'kepong'): None,
                ('my_district', 'my', 'kerian'): ('my_district', 'my', 'kerian'),
                ('my_district', 'my', 'kinabatangan'): ('my_district', 'my', 'kinabatangan'),
                ('my_district', 'my', 'kinta'): ('my_district', 'my', 'kinta'),
                ('my_district', 'my', 'klang'): ('my_district', 'my', 'klang'),
                ('my_district', 'my', 'kluang'): ('my_district', 'my', 'kluang'),
                ('my_district', 'my', 'kota belud'): ('my_district', 'my', 'kota belud'),
                ('my_district', 'my', 'kota bharu'): ('my_district', 'my', 'kota bharu'),
                ('my_district', 'my', 'kota kinabalu'): ('my_district', 'my', 'kota kinabalu'),
                ('my_district', 'my', 'kota marudu'): ('my_district', 'my', 'kota marudu'),
                ('my_district', 'my', 'kota samarahan'): None,
                ('my_district', 'my', 'kota setar'): ('my_district', 'my', 'kota setar'),
                ('my_district', 'my', 'kota tinggi'): ('my_district', 'my', 'kota tinggi'),
                ('my_district', 'my', 'kuala kangsar'): ('my_district', 'my', 'kuala kangsar'),
                ('my_district', 'my', 'kuala krai'): ('my_district', 'my', 'kuala krai'),
                ('my_district', 'my', 'kuala langat'): ('my_district', 'my', 'kuala langat'),
                ('my_district', 'my', 'kuala lumpur'): None,  # FIXME!!!!! ===================================================
                ('my_district', 'my', 'setiawangsa'): None,
                ('my_district', 'my', 'kuala muda'): ('my_district', 'my', 'kuala muda'),
                ('my_district', 'my', 'kuala pilah'): ('my_district', 'my', 'kuala pilah'),
                ('my_district', 'my', 'kuala selangor'): ('my_district', 'my', 'kuala selangor'),
                ('my_district', 'my', 'kuala terengganu'): ('my_district', 'my', 'kuala terengganu'),
                ('my_district', 'my', 'kuantan'): ('my_district', 'my', 'kuantan'),
                ('my_district', 'my', 'kubang pasu'): ('my_district', 'my', 'kubang pasu'),
                ('my_district', 'my', 'kuching'): ('my_district', 'my', 'kuching'),
                ('my_district', 'my', 'kudat'): ('my_district', 'my', 'kudat'),
                ('my_district', 'my', 'kulai'): None,
                ('my_district', 'my', 'kulim'): ('my_district', 'my', 'kulim'),
                ('my_district', 'my', 'labuan'): None,
                ('my_district', 'my', 'lahad datu'): ('my_district', 'my', 'lahad datu'),
                ('my_district', 'my', 'langkawi'): ('my_district', 'my', 'langkawi'),
                ('my_district', 'my', 'larut, matang, selama'): None,
                ('my_district', 'my', 'lawas'): ('my_district', 'my', 'lawas'),
                ('my_district', 'my', 'lembah pantai'): None,
                ('my_district', 'my', 'limbang'): ('my_district', 'my', 'limbang'),
                ('my_district', 'my', 'lipis'): ('my_district', 'my', 'lipis'),
                ('my_district', 'my', 'lubok antu'): ('my_district', 'my', 'lubok antu'),
                ('my_district', 'my', 'machang'): ('my_district', 'my', 'machang'),
                ('my_district', 'my', 'manjalara'): None,
                ('my_district', 'my', 'manjung'): None,
                ('my_district', 'my', 'maran'): ('my_district', 'my', 'maran'),
                ('my_district', 'my', 'marang'): ('my_district', 'my', 'marang'),
                ('my_district', 'my', 'matu'): ('my_district', 'my', 'matu'),
                ('my_district', 'my', 'melaka tengah'): ('my_district', 'my', 'melaka tengah'),
                ('my_district', 'my', 'mersing'): ('my_district', 'my', 'mersing'),
                ('my_district', 'my', 'miri'): ('my_district', 'my', 'miri'),
                ('my_district', 'my', 'mont kiara'): None,
                ('my_district', 'my', 'muar'): ('my_district', 'my', 'muar'),
                ('my_district', 'my', 'mukah'): ('my_district', 'my', 'mukah'),
                ('my_district', 'my', 'nabawan'): ('my_district', 'my', 'nabawan'),
                ('my_district', 'my', 'padang terap'): ('my_district', 'my', 'padang terap'),
                ('my_district', 'my', 'pakan'): ('my_district', 'my', 'pakan'),
                ('my_district', 'my', 'pandan'): None,
                ('my_district', 'my', 'pantai barat utara'): None,
                ('my_district', 'my', 'papar'): ('my_district', 'my', 'papar'),
                ('my_district', 'my', 'pasir mas'): ('my_district', 'my', 'pasir mas'),
                ('my_district', 'my', 'pasir puteh'): ('my_district', 'my', 'pasir puteh'),
                ('my_district', 'my', 'pekan'): ('my_district', 'my', 'pekan'),
                ('my_district', 'my', 'penampang'): ('my_district', 'my', 'penampang'),
                ('my_district', 'my', 'pendang'): ('my_district', 'my', 'pendang'),
                ('my_district', 'my', 'perak tengah'): ('my_district', 'my', 'perak tengah'),
                ('my_district', 'my', 'petaling'): ('my_district', 'my', 'petaling'),
                ('my_district', 'my', 'pitas'): ('my_district', 'my', 'pitas'),
                ('my_district', 'my', 'pokok sena'): ('my_district', 'my', 'pokok sena'),
                ('my_district', 'my', 'pontian'): ('my_district', 'my', 'pontian'),
                ('my_district', 'my', 'port dickson'): ('my_district', 'my', 'port dickson'),
                ('my_district', 'my', 'pudu'): None,
                ('my_district', 'my', 'putatan'): ('my_district', 'my', 'putatan'),
                ('my_district', 'my', 'putrajaya'): None,
                ('my_district', 'my', 'ranau'): ('my_district', 'my', 'ranau'),
                ('my_district', 'my', 'raub'): ('my_district', 'my', 'raub'),
                ('my_district', 'my', 'rembau'): ('my_district', 'my', 'rembau'),
                ('my_district', 'my', 'rompin'): ('my_district', 'my', 'rompin'),
                ('my_district', 'my', 'sabak bernam'): ('my_district', 'my', 'sabak bernam'),
                ('my_district', 'my', 'samarahan'): ('my_district', 'my', 'samarahan'),
                ('my_district', 'my', 'sandakan'): ('my_district', 'my', 'sandakan'),
                ('my_district', 'my', 'saratok'): ('my_district', 'my', 'saratok'),
                ('my_district', 'my', 'sarikei'): ('my_district', 'my', 'sarikei'),
                ('my_district', 'my', 'seberang perai selatan'): None,
                ('my_district', 'my', 'seberang perai tengah'): None,
                ('my_district', 'my', 'seberang perai utara'): None,
                ('my_district', 'my', 'segamat'): ('my_district', 'my', 'segamat'),
                ('my_district', 'my', 'semporna'): ('my_district', 'my', 'semporna'),
                ('my_district', 'my', 'sentul'): None,
                ('my_district', 'my', 'sepang'): ('my_district', 'my', 'sepang'),
                ('my_district', 'my', 'seputeh'): None,
                ('my_district', 'my', 'seremban'): ('my_district', 'my', 'seremban'),
                ('my_district', 'my', 'serian'): ('my_district', 'my', 'serian'),
                ('my_district', 'my', 'setiu'): ('my_district', 'my', 'setiu'),
                ('my_district', 'my', 'sibu'): ('my_district', 'my', 'sibu'),
                ('my_district', 'my', 'sik'): ('my_district', 'my', 'sik'),
                ('my_district', 'my', 'simunjan'): ('my_district', 'my', 'simunjan'),
                ('my_district', 'my', 'sipitang'): ('my_district', 'my', 'sipitang'),
                ('my_district', 'my', 'song'): ('my_district', 'my', 'song'),
                ('my_district', 'my', 'sri aman'): ('my_district', 'my', 'sri aman'),
                ('my_district', 'my', 'sri petaling'): None,
                ('my_district', 'my', 'tambunan'): ('my_district', 'my', 'tambunan'),
                ('my_district', 'my', 'tampin'): ('my_district', 'my', 'tampin'),
                ('my_district', 'my', 'tanah merah'): ('my_district', 'my', 'tanah merah'),
                ('my_district', 'my', 'tangkak'): None,
                ('my_district', 'my', 'tatau'): ('my_district', 'my', 'tatau'),
                ('my_district', 'my', 'tawau'): ('my_district', 'my', 'tawau'),
                ('my_district', 'my', 'temerloh'): ('my_district', 'my', 'temerloh'),
                ('my_district', 'my', 'tenom'): ('my_district', 'my', 'tenom'),
                ('my_district', 'my', 'timur laut'): ('my_district', 'my', 'timur laut'),
                ('my_district', 'my', 'titiwangsa'): None,
                ('my_district', 'my', 'tuaran'): ('my_district', 'my', 'tuaran'),
                ('my_district', 'my', 'tumpat'): ('my_district', 'my', 'tumpat'),
                ('my_district', 'my', 'wangsa maju'): None,
                ('my_district', 'my', 'yan'): ('my_district', 'my', 'yan'),
                ('my_district', 'my', 'kuala nerus'): None,
                ('my_district', 'my', 'telupid'): None,

                ('my_district', 'my', 'segambut'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self.get_district_datapoints())
        r.extend(self.get_sub_district_datapoints())
        return r

    def get_district_datapoints(self):
        # {
        #       "attributes": {
        #         "OBJECTID": 1,
        #         "State": 8,
        #         "Last_Update": 1594425600000,
        #         "Latitude": 2.07,
        #         "Logitude": 103.4,
        #         "Confirmed": 750,
        #         "Recovered": 8,
        #         "Deaths": 20,
        #         "GlobalID": "fe673177-c04b-42b3-a93f-b27515f87aa8",
        #         "CreationDate": 1584525341792,
        #         "Creator": "kylo_em",
        #         "EditDate": 1597509951578,
        #         "Editor": "drp_editor",
        #         "Tarikh_Kemaskini": 1585299600000
        #       }
        #     },

        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/district_case.json'

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

            states_map = {
                i['code']: i['name']
                for i in data['fields'][1]['domain']['codedValues']
            }

            for feature in data['features']:
                attributes = feature['attributes']

                #date = datetime.datetime.fromtimestamp(
                #    attributes['EditDate'] / 1000.0
                #).strftime('%Y_%m_%d')
                if attributes['State'] is None:
                    continue  # HACK!

                region_child = states_map[attributes['State']].lower().strip()
                if region_child.startswith('wp '):
                    region_child = region_child[3:]

                confirmed = attributes['Confirmed']
                recovered = attributes['Recovered']
                deaths = attributes['Deaths']

                if confirmed is not None:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if recovered is not None:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if deaths is not None:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if confirmed is not None and recovered is not None:
                    active = confirmed - recovered - (deaths or 0)
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(active),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r

    def get_sub_district_datapoints(self):
        # {
        #         "OBJECTID": 437,
        #         "POLYGON_ID": 703841954,
        #         "AREA_ID": 23288894,
        #         "NM_AREA_ID": 1,
        #         "POLYGON_NM": "Jelebu",
        #         "FEAT_TYPE": "DISTRICT",
        #         "COVID19": 2,
        #         "Zone_Class": "ZON KUNING",
        #         "Shape__Area": 0.110571529552118,
        #         "Shape__Length": 1.88281903151022,
        #         "CreationDate": 1585237810887,
        #         "Creator": "nazmeen_nsesrimy",
        #         "EditDate": 1587551346219,
        #         "Editor": "nazmeen_nsesrimy",
        #         "Negeri": "Negeri Sembilan",
        #         "GlobalID": "4da873b1-fd9f-4dc1-a308-a4353a016ce9",
        #         "Kes_Aktif": 0,
        #         "Kes_Aktif_Zone": "ZON HIJAU"
        #       }

        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/sub_district_case.json'

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

            for feature in data['features']:
                attributes = feature['attributes']

                #date = datetime.datetime.fromtimestamp(
                #    attributes['EditDate']/1000.0
                #).strftime('%Y_%m_%d')
                region_child = attributes['POLYGON_NM']

                total = attributes['COVID19']
                active = attributes['Kes_Aktif']

                if total is not None:
                    r.append(
                        region_schema=Schemas.MY_DISTRICT,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(total),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if active is not None:
                    r.append(
                        region_schema=Schemas.MY_DISTRICT,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(active),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = MYESRIDashData()
    datapoints = inst.get_datapoints()
    #inst.sdpf.print_mappings()
    pprint(datapoints)
