import csv
from os import listdir

from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_crawlers._base_classes.GithubRepo import GithubRepo
from _utility.get_package_dir import get_overseas_dir

place_map = {
    'sembilan': 'Negeri Sembilan',
    'pinang': 'Pulau Pinang',
    'lumpur': 'Wilayah Persekutuan Kuala Lumpur'
}


class MYData(GithubRepo):
    SOURCE_URL = 'https://github.com/ynshung/covid-19-malaysia'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'my_unofficial_github'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'my' / 'covid-19-malaysia',
                            github_url='https://github.com/ynshung/covid-19-malaysia')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={('admin_0', '', 'malaysia'): ('admin_0', '', 'my'),
                ('admin_0', '', 'my'): ('admin_0', '', 'my'),
                ('admin_1', 'malaysia', 'johor'): ('admin_1', 'my', 'my-01'),
                ('admin_1', 'malaysia', 'kedah'): ('admin_1', 'my', 'my-02'),
                ('admin_1', 'malaysia', 'kelantan'): ('admin_1', 'my', 'my-03'),
                ('admin_1', 'malaysia', 'melaka'): ('admin_1', 'my', 'my-04'),
                ('admin_1', 'malaysia', 'negeri-sembilan'): None,
                ('admin_1', 'malaysia', 'pahang'): ('admin_1', 'my', 'my-06'),
                ('admin_1', 'malaysia', 'perak'): ('admin_1', 'my', 'my-08'),
                ('admin_1', 'malaysia', 'perlis'): ('admin_1', 'my', 'my-09'),
                ('admin_1', 'malaysia', 'pulau-pinang'): None,
                ('admin_1', 'malaysia', 'sabah'): ('admin_1', 'my', 'my-12'),
                ('admin_1', 'malaysia', 'sarawak'): ('admin_1', 'my', 'my-13'),
                ('admin_1', 'malaysia', 'selangor'): ('admin_1', 'my', 'my-10'),
                ('admin_1', 'malaysia', 'terengganu'): ('admin_1', 'my', 'my-11'),
                ('admin_1', 'malaysia', 'wp-kuala-lumpur'): None,
                ('admin_1', 'malaysia', 'wp-labuan'): None,
                ('admin_1', 'malaysia', 'wp-putrajaya'): None,
                ('admin_1', 'my', 'my-01'): ('admin_1', 'my', 'my-01'),
                ('admin_1', 'my', 'my-02'): ('admin_1', 'my', 'my-02'),
                ('admin_1', 'my', 'my-03'): ('admin_1', 'my', 'my-03'),
                ('admin_1', 'my', 'my-04'): ('admin_1', 'my', 'my-04'),
                ('admin_1', 'my', 'my-06'): ('admin_1', 'my', 'my-06'),
                ('admin_1', 'my', 'my-08'): ('admin_1', 'my', 'my-08'),
                ('admin_1', 'my', 'my-09'): ('admin_1', 'my', 'my-09'),
                ('admin_1', 'my', 'my-10'): ('admin_1', 'my', 'my-10'),
                ('admin_1', 'my', 'my-11'): ('admin_1', 'my', 'my-11'),
                ('admin_1', 'my', 'my-12'): ('admin_1', 'my', 'my-12'),
                ('admin_1', 'my', 'my-13'): ('admin_1', 'my', 'my-13'),
                ('my_district', 'my', 'alor-gajah'): None,
                ('my_district', 'my', 'asajaya'): ('my_district', 'my', 'asajaya'),
                ('my_district', 'my', 'bachok'): ('my_district', 'my', 'bachok'),
                ('my_district', 'my', 'baling'): ('my_district', 'my', 'baling'),
                ('my_district', 'my', 'bandar-bahru'): None,
                ('my_district', 'my', 'barat-daya'): None,
                ('my_district', 'my', 'batang-padang'): None,
                ('my_district', 'my', 'batu-pahat'): None,
                ('my_district', 'my', 'bau'): ('my_district', 'my', 'bau'),
                ('my_district', 'my', 'beaufort'): ('my_district', 'my', 'beaufort'),
                ('my_district', 'my', 'belaga'): ('my_district', 'my', 'belaga'),
                ('my_district', 'my', 'beluran'): ('my_district', 'my', 'beluran'),
                ('my_district', 'my', 'beluru'): None,
                ('my_district', 'my', 'bentong'): ('my_district', 'my', 'bentong'),
                ('my_district', 'my', 'bera'): ('my_district', 'my', 'bera'),
                ('my_district', 'my', 'besut'): ('my_district', 'my', 'besut'),
                ('my_district', 'my', 'betong'): ('my_district', 'my', 'betong'),
                ('my_district', 'my', 'bintulu'): ('my_district', 'my', 'bintulu'),
                ('my_district', 'my', 'bukit-mabong'): None,
                ('my_district', 'my', 'cameron'): None,
                ('my_district', 'my', 'cheras'): None,
                ('my_district', 'my', 'dalat'): ('my_district', 'my', 'dalat'),
                ('my_district', 'my', 'daro'): ('my_district', 'my', 'daro'),
                ('my_district', 'my', 'dungun'): ('my_district', 'my', 'dungun'),
                ('my_district', 'my', 'gombak'): ('my_district', 'my', 'gombak'),
                ('my_district', 'my', 'gua-musang'): None,
                ('my_district', 'my', 'hillir-perak'): None,
                ('my_district', 'my', 'hulu-langat'): None,
                ('my_district', 'my', 'hulu-perak'): None,
                ('my_district', 'my', 'hulu-selangor'): None,
                ('my_district', 'my', 'hulu-terengganu'): None,
                ('my_district', 'my', 'jasin'): ('my_district', 'my', 'jasin'),
                ('my_district', 'my', 'jelebu'): ('my_district', 'my', 'jelebu'),
                ('my_district', 'my', 'jeli'): ('my_district', 'my', 'jeli'),
                ('my_district', 'my', 'jempol'): ('my_district', 'my', 'jempol'),
                ('my_district', 'my', 'jerantut'): ('my_district', 'my', 'jerantut'),
                ('my_district', 'my', 'johor-bahru'): None,
                ('my_district', 'my', 'julau'): ('my_district', 'my', 'julau'),
                ('my_district', 'my', 'kabong'): None,
                ('my_district', 'my', 'kampar'): ('my_district', 'my', 'kampar'),
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
                ('my_district', 'my', 'kota-belud'): None,
                ('my_district', 'my', 'kota-bharu'): None,
                ('my_district', 'my', 'kota-kinabalu'): None,
                ('my_district', 'my', 'kota-marudu'): None,
                ('my_district', 'my', 'kota-samarahan'): None,
                ('my_district', 'my', 'kota-setar'): None,
                ('my_district', 'my', 'kota-tinggi'): None,
                ('my_district', 'my', 'kuala-kangsar'): None,
                ('my_district', 'my', 'kuala-krai'): None,
                ('my_district', 'my', 'kuala-langat'): None,
                ('my_district', 'my', 'kuala-muda'): None,
                ('my_district', 'my', 'kuala-nerus'): None,
                ('my_district', 'my', 'kuala-penyu'): None,
                ('my_district', 'my', 'kuala-pilah'): None,
                ('my_district', 'my', 'kuala-selangor'): None,
                ('my_district', 'my', 'kuala-terengganu'): None,
                ('my_district', 'my', 'kuantan'): ('my_district', 'my', 'kuantan'),
                ('my_district', 'my', 'kubang-pasu'): None,
                ('my_district', 'my', 'kuching'): ('my_district', 'my', 'kuching'),
                ('my_district', 'my', 'kudat'): ('my_district', 'my', 'kudat'),
                ('my_district', 'my', 'kulai'): None,
                ('my_district', 'my', 'kulim'): ('my_district', 'my', 'kulim'),
                ('my_district', 'my', 'kunak'): ('my_district', 'my', 'kunak'),
                ('my_district', 'my', 'lahad-datu'): None,
                ('my_district', 'my', 'langkawi'): ('my_district', 'my', 'langkawi'),
                ('my_district', 'my', 'larut-matang-selama'): None,
                ('my_district', 'my', 'lawas'): ('my_district', 'my', 'lawas'),
                ('my_district', 'my', 'lembah-pantai'): None,
                ('my_district', 'my', 'limbang'): ('my_district', 'my', 'limbang'),
                ('my_district', 'my', 'lipis'): ('my_district', 'my', 'lipis'),
                ('my_district', 'my', 'lubok-antu'): None,
                ('my_district', 'my', 'lundu'): ('my_district', 'my', 'lundu'),
                ('my_district', 'my', 'machang'): ('my_district', 'my', 'machang'),
                ('my_district', 'my', 'manjung'): None,
                ('my_district', 'my', 'maran'): ('my_district', 'my', 'maran'),
                ('my_district', 'my', 'marang'): ('my_district', 'my', 'marang'),
                ('my_district', 'my', 'marudi'): ('my_district', 'my', 'marudi'),
                ('my_district', 'my', 'matu'): ('my_district', 'my', 'matu'),
                ('my_district', 'my', 'melaka-tengah'): None,
                ('my_district', 'my', 'meradong'): ('my_district', 'my', 'meradong'),
                ('my_district', 'my', 'mersing'): ('my_district', 'my', 'mersing'),
                ('my_district', 'my', 'miri'): ('my_district', 'my', 'miri'),
                ('my_district', 'my', 'muallim'): None,
                ('my_district', 'my', 'muar'): ('my_district', 'my', 'muar'),
                ('my_district', 'my', 'mukah'): ('my_district', 'my', 'mukah'),
                ('my_district', 'my', 'nabawan'): ('my_district', 'my', 'nabawan'),
                ('my_district', 'my', 'padang-terap'): None,
                ('my_district', 'my', 'pakan'): ('my_district', 'my', 'pakan'),
                ('my_district', 'my', 'papar'): ('my_district', 'my', 'papar'),
                ('my_district', 'my', 'pasir-mas'): None,
                ('my_district', 'my', 'pasir-putih'): None,
                ('my_district', 'my', 'pekan'): ('my_district', 'my', 'pekan'),
                ('my_district', 'my', 'penampang'): ('my_district', 'my', 'penampang'),
                ('my_district', 'my', 'pendang'): ('my_district', 'my', 'pendang'),
                ('my_district', 'my', 'perak-tengah'): None,
                ('my_district', 'my', 'petaling'): ('my_district', 'my', 'petaling'),
                ('my_district', 'my', 'pitas'): ('my_district', 'my', 'pitas'),
                ('my_district', 'my', 'pontian'): ('my_district', 'my', 'pontian'),
                ('my_district', 'my', 'port-dickson'): None,
                ('my_district', 'my', 'pusa'): None,
                ('my_district', 'my', 'putatan'): ('my_district', 'my', 'putatan'),
                ('my_district', 'my', 'ranau'): ('my_district', 'my', 'ranau'),
                ('my_district', 'my', 'raub'): ('my_district', 'my', 'raub'),
                ('my_district', 'my', 'rembau'): ('my_district', 'my', 'rembau'),
                ('my_district', 'my', 'rompin'): ('my_district', 'my', 'rompin'),
                ('my_district', 'my', 'sabak-bernam'): None,
                ('my_district', 'my', 'sandakan'): ('my_district', 'my', 'sandakan'),
                ('my_district', 'my', 'saratok'): ('my_district', 'my', 'saratok'),
                ('my_district', 'my', 'sarikei'): ('my_district', 'my', 'sarikei'),
                ('my_district', 'my', 'sebauh'): None,
                ('my_district', 'my', 'seberang-perai-selatan'): None,
                ('my_district', 'my', 'seberang-perai-tengah'): None,
                ('my_district', 'my', 'seberang-perai-utara'): None,
                ('my_district', 'my', 'segamat'): ('my_district', 'my', 'segamat'),
                ('my_district', 'my', 'selangau'): ('my_district', 'my', 'selangau'),
                ('my_district', 'my', 'semporna'): ('my_district', 'my', 'semporna'),
                ('my_district', 'my', 'sepang'): ('my_district', 'my', 'sepang'),
                ('my_district', 'my', 'seremban'): ('my_district', 'my', 'seremban'),
                ('my_district', 'my', 'serian'): ('my_district', 'my', 'serian'),
                ('my_district', 'my', 'setiu'): ('my_district', 'my', 'setiu'),
                ('my_district', 'my', 'sibu'): ('my_district', 'my', 'sibu'),
                ('my_district', 'my', 'sik'): ('my_district', 'my', 'sik'),
                ('my_district', 'my', 'simunjan'): ('my_district', 'my', 'simunjan'),
                ('my_district', 'my', 'sipitang'): ('my_district', 'my', 'sipitang'),
                ('my_district', 'my', 'song'): ('my_district', 'my', 'song'),
                ('my_district', 'my', 'sri-aman'): None,
                ('my_district', 'my', 'subis'): None,
                ('my_district', 'my', 'tambunan'): ('my_district', 'my', 'tambunan'),
                ('my_district', 'my', 'tampin'): ('my_district', 'my', 'tampin'),
                ('my_district', 'my', 'tanah-merah'): None,
                ('my_district', 'my', 'tangkak'): None,
                ('my_district', 'my', 'tanjung-manis'): None,
                ('my_district', 'my', 'tatau'): ('my_district', 'my', 'tatau'),
                ('my_district', 'my', 'tawau'): ('my_district', 'my', 'tawau'),
                ('my_district', 'my', 'tebedu'): None,
                ('my_district', 'my', 'telung-usan'): None,
                ('my_district', 'my', 'temerloh'): ('my_district', 'my', 'temerloh'),
                ('my_district', 'my', 'tenom'): ('my_district', 'my', 'tenom'),
                ('my_district', 'my', 'timur-laut'): None,
                ('my_district', 'my', 'titiwangsa'): None,
                ('my_district', 'my', 'tongod'): ('my_district', 'my', 'tongod'),
                ('my_district', 'my', 'tuaran'): ('my_district', 'my', 'tuaran'),
                ('my_district', 'my', 'tumpat'): ('my_district', 'my', 'tumpat'),
                ('my_district', 'my', 'yan'): ('my_district', 'my', 'yan')
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_districts())
        r.extend(self._get_states_cases())
        r.extend(self._get_cases_types())
        r.extend(self._get_malaysia())
        return r

    def _get_districts(self):
        r = self.sdpf()

        # date,batu-pahat,johor-bahru,kluang,kulai,mersing,muar,
        # pontian,segamat,kota-tinggi,tangkak,under-investigation
        # 24/3/2020,28,59,31,10,2,15,7,3,4,3,3
        # 25/3/2020,29,68,54,10,2,15,7,3,5,3,0
        # 26/3/2020,30,73,83,14,3,15,8,3,7,3,0
        # 27/3/2020,30,80,83,18,3,15,11,4,7,3,5

        # NOTE: The states that do not have any
        # districts are Perlis, Putrajaya and WP Labuan.
        # You may refer to their cases in
        # states/covid-19-my-states-cases.csv

        for fnam in listdir(self.get_path_in_dir('districts')):
            if not fnam.endswith('.csv'):
                continue
            path = f"{self.get_path_in_dir('districts')}/{fnam}"

            with open(path, 'r', encoding='utf-8') as f:
                for item in csv.DictReader(f):
                    date = self.convert_date(item['date'])
                    del item['date']

                    for district, value in item.items():
                        if value.strip('-'):
                            parent = fnam.split('-')[-1].split('.')[0]
                            r.append(
                                region_schema=Schemas.MY_DISTRICT,
                                region_parent='MY', #place_map.get(parent, parent),
                                region_child=district.replace('under-investigation', 'Unknown'),
                                datatype=DataTypes.TOTAL,
                                value=int(value),
                                date_updated=date,
                                source_url=self.SOURCE_URL
                            )

        return r

    def _get_states_cases(self):
        r = self.sdpf()

        # date,perlis,kedah,pulau-pinang,perak,selangor,negeri-sembilan,
        # melaka,johor,pahang,terengganu,kelantan,sabah,sarawak,
        # wp-kuala-lumpur,wp-putrajaya,wp-labuan
        #
        # 13/3/2020,1,5,7,2,87,11,1,20,2,0,3,15,0,40,1,2
        # 14/3/2020,2,5,7,2,92,19,6,22,2,0,3,26,6,43,1,2
        # 15/3/2020,,,,,,,,,,,,,,,,
        # 16/3/2020,8,31,15,18,144,42,14,52,19,4,18,57,21,106,-,4

        with open(self.get_path_in_dir('covid-19-my-states-cases.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])
                del item['date']

                for state, value in item.items():
                    if value.strip('-'):
                        child = state.replace('under-investigation', 'Unknown')
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='Malaysia',
                            region_child=place_map.get(child, child),
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

        return r

    def _get_cases_types(self):
        r = self.sdpf()

        # date,pui,close-contact,tabligh,surveillance,hadr,import
        # 15/2/2020,12,8,-,0,2,-
        # 16/2/2020,12,8,-,0,2,-
        # 17/2/2020,12,8,-,0,2,-
        # 18/2/2020,12,8,-,0,2,-

        with open(self.get_path_in_dir('covid-19-my-cases-types.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                if item['pui'].replace('-', ''):
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Malaysia',
                        datatype=DataTypes.SOURCE_UNDER_INVESTIGATION,
                        value=int(item['pui']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if item['tabligh'].replace('-', '') or item['close-contact'].replace('-', ''):
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Malaysia',
                        datatype=DataTypes.SOURCE_CONFIRMED,
                        value=int(item['tabligh'].replace('-', '0') or 0) +
                              int(item['close-contact'].replace('-', '0') or 0),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if item['surveillance'].replace('-', '') or item['hadr'].replace('-', ''):
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Malaysia',
                        datatype=DataTypes.SOURCE_COMMUNITY,
                        value=int(item['surveillance'].replace('-', '0') or 0) +
                              int(item['hadr'].replace('-', '0') or 0),  # CHECK ME!!!! ==============================================
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if item['import'] and item['import'].replace('-', ''):
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Malaysia',
                        datatype=DataTypes.SOURCE_OVERSEAS,
                        value=int(item['import']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r

    def _get_malaysia(self):
        r = self.sdpf()

        # date,cases,discharged,death,icu
        # 24/1/2020,0,0,0,0
        # 25/1/2020,3,0,0,0
        # 26/1/2020,4,0,0,0
        # 27/1/2020,4,0,0,0

        with open(self.get_path_in_dir('covid-19-malaysia.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='Malaysia',
                    datatype=DataTypes.TOTAL,
                    value=int(item['cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                #r.append(
                #    region_schema=Schemas.ADMIN_0,
                #    region_child='Malaysia',
                #    datatype=DataTypes.STATUS_DISCHARGED,
                #    value=int(item['discharged']),
                #    date_updated=date,
                #    source_url=self.SOURCE_URL
                #)
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='Malaysia',
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['death']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='Malaysia',
                    datatype=DataTypes.STATUS_ICU,
                    value=int(item['icu']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = MYData()
    datapoints = inst.get_datapoints()
    #inst.sdpf.print_mappings()
    pprint(datapoints)
