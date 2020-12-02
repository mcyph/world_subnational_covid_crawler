import csv

from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_crawlers._base_classes.GithubRepo import GithubRepo
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


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
    SOURCE_DESCRIPTION = 'Creative Commons Attribution 4.0 International'
    SOURCE_ID = 'ch_open_swiss_data'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'ch' / 'covid_19',
                            github_url='https://github.com/openZH/covid_19')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'ch', 'geneva'): None,
                ('admin_1', 'ch', 'graubünden; grisons'): None,
                ('admin_1', 'ch', 'principality of liechtenstein'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()

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
                if item['abbreviation_canton_and_fl'] == 'FL':
                    canton = 'Principality of Liechtenstein'  # CHECK ME!!! =============================================================
                else:
                    canton = canton_to_name[item['abbreviation_canton_and_fl']]
                source = item['source'] or self.SOURCE_URL

                if item['ncumul_conf']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CH',
                        region_child=canton,
                        datatype=DataTypes.TOTAL,
                        value=int(item['ncumul_conf']),
                        source_url=source,
                        date_updated=date
                    )

                if item['ncumul_tested']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CH',
                        region_child=canton,
                        datatype=DataTypes.TESTS_TOTAL,
                        value=int(item['ncumul_tested']),
                        source_url=source,
                        date_updated=date
                    )

                if item['current_hosp']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CH',
                        region_child=canton,
                        datatype=DataTypes.STATUS_HOSPITALIZED,
                        value=int(item['current_hosp']),
                        source_url=source,
                        date_updated=date
                    )

                if item['current_icu']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CH',
                        region_child=canton,
                        datatype=DataTypes.STATUS_ICU,
                        value=int(item['current_icu']),
                        source_url=source,
                        date_updated=date
                    )

                if item['current_vent']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CH',
                        region_child=canton,
                        datatype=DataTypes.STATUS_ICU_VENTILATORS,
                        value=int(item['current_vent']),
                        source_url=source,
                        date_updated=date
                    )

                if item['ncumul_deceased']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CH',
                        region_child=canton,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(item['ncumul_deceased']),
                        source_url=source,
                        date_updated=date
                    )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(CHData().get_datapoints())
