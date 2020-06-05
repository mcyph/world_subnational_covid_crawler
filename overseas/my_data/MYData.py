import csv
from os import listdir

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    SCHEMA_MY_DISTRICT,
    DT_TOTAL, DT_STATUS_ICU,
    DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)

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
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_districts())
        r.extend(self._get_states_cases())
        r.extend(self._get_cases_types())
        r.extend(self._get_malaysia())
        return r

    def _get_districts(self):
        r = []

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
                            r.append(DataPoint(
                                region_schema=SCHEMA_MY_DISTRICT,
                                region_parent=place_map.get(parent, parent),
                                region_child=district.replace('under-investigation', 'Unknown'),
                                datatype=DT_TOTAL,
                                value=int(value),
                                date_updated=date,
                                source_url=self.SOURCE_URL
                            ))

        return r

    def _get_states_cases(self):
        r = []

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
                        r.append(DataPoint(
                            region_schema=SCHEMA_ADMIN_1,
                            region_parent='Malaysia',
                            region_child=place_map.get(child, child),
                            datatype=DT_TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))

        return r

    def _get_cases_types(self):
        r = []

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
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Malaysia',
                        datatype=DT_SOURCE_UNDER_INVESTIGATION,
                        value=int(item['pui']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['tabligh'].replace('-', '') or item['close-contact'].replace('-', ''):
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Malaysia',
                        datatype=DT_SOURCE_CONFIRMED,
                        value=int(item['tabligh'].replace('-', '0') or 0) +
                              int(item['close-contact'].replace('-', '0') or 0),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['surveillance'].replace('-', '') or item['hadr'].replace('-', ''):
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Malaysia',
                        datatype=DT_SOURCE_COMMUNITY,
                        value=int(item['surveillance'].replace('-', '0') or 0) +
                              int(item['hadr'].replace('-', '0') or 0),  # CHECK ME!!!! ==============================================
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['import'] and item['import'].replace('-', ''):
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Malaysia',
                        datatype=DT_SOURCE_OVERSEAS,
                        value=int(item['import']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r

    def _get_malaysia(self):
        r = []

        # date,cases,discharged,death,icu
        # 24/1/2020,0,0,0,0
        # 25/1/2020,3,0,0,0
        # 26/1/2020,4,0,0,0
        # 27/1/2020,4,0,0,0

        with open(self.get_path_in_dir('covid-19-malaysia.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Malaysia',
                    datatype=DT_TOTAL,
                    value=int(item['cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                #r.append(DataPoint(
                #    region_schema=SCHEMA_ADMIN_0,
                #    region_child='Malaysia',
                #    datatype=DT_STATUS_DISCHARGED,
                #    value=int(item['discharged']),
                #    date_updated=date,
                #    source_url=self.SOURCE_URL
                #))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Malaysia',
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['death']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Malaysia',
                    datatype=DT_STATUS_ICU,
                    value=int(item['icu']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MYData().get_datapoints())
