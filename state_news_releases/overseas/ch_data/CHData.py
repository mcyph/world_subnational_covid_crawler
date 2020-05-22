import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_CH_CANTON,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_STATUS_ACTIVE, DT_STATUS_ICU_VENTILATORS,
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


canton_to_name = dict([i.split('\t') for i in """
AG	Aargau
AI	Appenzell Innerrhoden
AR	Appenzell Ausserrhoden
BE	Bern
BL	Basel-Landschaft
BS	Basel-Stadt
FR	Fribourg
GE	Geneva
GL	Glarus
GR	Graubünden; Grisons
JU	Jura
LU	Luzern
NE	Neuchâtel
NW	Nidwalden
OW	Obwalden
SG	St. Gallen
SH	Schaffhausen
SO	Solothurn
SZ	Schwyz
TG	Thurgau
TI	Ticino
UR	Uri
VD	Vaud
VS	Valais
ZG	Zug
ZH	Zürich
CH	Switzerland
""".strip().split('\n')])


class CHData(GithubRepo):
    SOURCE_URL = 'https://github.com/openZH/covid_19'
    SOURCE_LICENSE = 'Creative Commons Attribution 4.0 International'

    GEO_DIR = 'ch'
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'ch' / 'covid_19',
                            github_url='https://github.com/pcm-dpc/COVID-19')
        self.update()

    def get_datapoints(self):
        r = []

        # Switzerland

        # date,time,abbreviation_canton_and_fl,ncumul_tested,ncumul_conf,new_hosp,current_hosp,current_icu,current_vent,ncumul_released,ncumul_deceased,source
        # 2020-02-25,,GE,73,0,,0,0,0,,0,https://www.ge.ch/document/20094/telecharger
        # 2020-02-25,,TI,,0,,0,0,0,0,0,https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/dati/COVID19_Dati_TI_per_github.xlsx
        # 2020-02-26,,GE,178,1,,1,0,0,,0,https://www.ge.ch/document/20094/telecharger
        # 2020-02-26,,TI,,1,,0,0,0,0,0,https://www4.ti.ch/fileadmin/DSS/DSP/UMC/malattie_infettive/Coronavirus/dati/COVID19_Dati_TI_per_github.xlsx

        with open(self.get_path_in_dir('COVID19_Fallzahlen_CH_total_v2.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])
                canton = canton_to_name[item['abbreviation_canton_and_fl']]
                source = item['source'] or self.SOURCE_URL

                if item['ncumul_conf']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_CH_CANTON,
                        region_child=canton,
                        datatype=DT_TOTAL,
                        value=int(item['ncumul_conf']),
                        source_url=source,
                        date_updated=date
                    ))

                if item['ncumul_tested']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_CH_CANTON,
                        region_child=canton,
                        datatype=DT_TESTS_TOTAL,
                        value=int(item['ncumul_tested']),
                        source_url=source,
                        date_updated=date
                    ))

                if item['current_hosp']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_CH_CANTON,
                        region_child=canton,
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['current_hosp']),
                        source_url=canton,
                        date_updated=date
                    ))

                if item['current_icu']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_CH_CANTON,
                        region_child=canton,
                        datatype=DT_STATUS_ICU,
                        value=int(item['current_icu']),
                        source_url=canton,
                        date_updated=date
                    ))

                if item['current_vent']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_CH_CANTON,
                        region_child=canton,
                        datatype=DT_STATUS_ICU_VENTILATORS,
                        value=int(item['current_vent']),
                        source_url=canton,
                        date_updated=date
                    ))

                if item['ncumul_deceased']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_CH_CANTON,
                        region_child=canton,
                        datatype=DT_STATUS_DEATHS,
                        value=int(item['ncumul_deceased']),
                        source_url=canton,
                        date_updated=date
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(CHData().get_datapoints())
