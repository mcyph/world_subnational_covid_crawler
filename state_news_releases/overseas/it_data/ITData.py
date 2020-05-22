import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_IT_PROVINCE, SCHEMA_IT_REGION,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_STATUS_ACTIVE,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.state_news_releases.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class ITData(GithubRepo):
    SOURCE_URL = 'https://github.com/pcm-dpc/COVID-19'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'it' / 'COVID-19',
                            github_url='https://github.com/pcm-dpc/COVID-19')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_national_data())
        r.extend(self._get_province_data())
        r.extend(self._get_regions_data())
        return r

    def _get_national_data(self):
        r = []

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

                r.append(DataPoint(
                    datatype=DT_STATUS_HOSPITALIZED,
                    value=int(hospitalized),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_ACTIVE,
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_NEW,
                    value=int(new),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_RECOVERED,
                    value=recovered,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_DEATHS,
                    value=deaths,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_TOTAL,
                    value=total,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_TESTS_TOTAL,
                    value=tests_total,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_ICU,
                    value=icu,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_province_data(self):
        r = []

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

        with open(self.get_path_in_dir('dati-json/dpc-covid19-ita-province.json'),
                  'r', encoding='utf-8') as f:
            for item in json.loads(f.read()):
                date = self.convert_date(item['data'].split('T')[0])

                r.append(DataPoint(
                    region_parent=item['denominazione_regione'],
                    region_schema=SCHEMA_IT_PROVINCE,
                    datatype=DT_TOTAL,
                    region_child=item['denominazione_provincia'],
                    value=int(item['totale_casi']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_regions_data(self):
        r = []

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

                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_STATUS_HOSPITALIZED,
                    region_child=item['denominazione_regione'],
                    value=int(hospitalized),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_STATUS_ACTIVE,
                    region_child=item['denominazione_regione'],
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_NEW,
                    region_child=item['denominazione_regione'],
                    value=int(new),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_STATUS_RECOVERED,
                    region_child=item['denominazione_regione'],
                    value=int(recovered),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_STATUS_DEATHS,
                    region_child=item['denominazione_regione'],
                    value=int(deaths),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_TOTAL,
                    region_child=item['denominazione_regione'],
                    value=int(total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_TESTS_TOTAL,
                    region_child=item['denominazione_regione'],
                    value=int(tests_total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_IT_REGION,
                    datatype=DT_STATUS_ICU,
                    region_child=item['denominazione_regione'],
                    value=int(icu),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ITData().get_datapoints())
