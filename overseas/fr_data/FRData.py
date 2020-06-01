import csv

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1, SCHEMA_FR_OVERSEAS_COLLECTIVITY,
    SCHEMA_FR_DEPARTMENT,
    DT_TOTAL, DT_STATUS_ACTIVE,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


# date,granularite,maille_code,maille_nom,cas_confirmes,cas_ehpad,
# cas_confirmes_ehpad,cas_possibles_ehpad,deces,deces_ehpad,
# reanimation,hospitalises,gueris,depistes,source_nom,
# source_url,source_archive,source_type
#
# date, granularity, mesh_code, mesh_name, cas_confirmes, cas_ehpad,
# cas_confirmes_ehpad, cas_possibles_ehpad, deaths, death_ehpad,
# resuscitation, hospitalized, gueris, depistes, source_nom,
# source_url, source_archive, source_type
#
# 2020-01-24,departement,DEP-16,Charente,0,,,,,,,,,,ARS Nouvelle-Aquitaine,https://www.nouvelle-aquitaine.ars.sante.fr/communique-de-presse-coronavirus-point-de-situation-en-nouvelle-aquitaine-du-08032020,,agences-regionales-sante
# 2020-01-24,departement,DEP-17,Charente-Maritime,0,,,,,,,,,,ARS Nouvelle-Aquitaine,https://www.nouvelle-aquitaine.ars.sante.fr/communique-de-presse-coronavirus-point-de-situation-en-nouvelle-aquitaine-du-08032020,,agences-regionales-sante
# 2020-01-24,departement,DEP-19,Corrèze,0,,,,,,,,,,ARS Nouvelle-Aquitaine,https://www.nouvelle-aquitaine.ars.sante.fr/communique-de-presse-coronavirus-point-de-situation-en-nouvelle-aquitaine-du-08032020,,agences-regionales-sante
# 2020-01-24,departement,DEP-23,Creuse,0,,,,,,,,,,ARS Nouvelle-Aquitaine,https://www.nouvelle-aquitaine.ars.sante.fr/communique-de-presse-coronavirus-point-de-situation-en-nouvelle-aquitaine-du-08032020,,agences-regionales-sante
# 2020-01-24,departement,DEP-24,Dordogne,0,,,,,,,,,,ARS Nouvelle-Aquitaine,https://www.nouvelle-aquitaine.ars.sante.fr/communique-de-presse-coronavirus-point-de-situation-en-nouvelle-aquitaine-du-08032020,,agences-regionales-sante
# 2020-01-24,departement,DEP-33,Gironde,1,,,,,,,,,,ARS Nouvelle-Aquitaine,https://www.nouvelle-aquitaine.ars.sante.fr/communique-de-presse-coronavirus-point-de-situation-en-nouvelle-aquitaine-du-08032020,,agences-regionales-sante


class FRData(GithubRepo):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'fr' / 'data',
                            github_url='https://github.com/opencovid19-fr/data')
        self.update()

    def get_datapoints(self):
        r = []

        with open(self.get_path_in_dir('dist/chiffres-cles.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                region_child = item['maille_nom']
                date = self.convert_date(item['date'])

                confirmed = item['cas_confirmes']
                cases_confirmed_agedhomes = item['cas_confirmes_ehpad']
                cases_possible_agedhomes = item['cas_possibles_ehpad']
                deaths = item['deces']
                deaths_agedhomes = item['deces_ehpad']
                icu = item['reanimation']
                hospitalized = item['hospitalises']
                recovered = item['gueris']
                unknown = item['depistes']
                source_name = item['source_nom']
                source_url = item['source_url'] or source_name or self.github_url

                if item['granularite'] == 'pays':
                    region_schema = SCHEMA_ADMIN_0
                    region_parent = None
                elif item['granularite'] in 'departement':
                    region_schema = SCHEMA_FR_DEPARTMENT
                    region_parent = None
                elif item['granularite'] == 'region':
                    region_schema = SCHEMA_ADMIN_1
                    region_parent = 'France'
                elif item['granularite'] == 'collectivite-outremer':
                    region_schema = SCHEMA_FR_OVERSEAS_COLLECTIVITY
                    region_parent = None
                    continue  # HACK: Won't support these in this data for now, as most of this info is in the JHU data!! ============================
                elif item['granularite'] == 'monde':
                    # World
                    continue
                else:
                    raise Exception(item['granularite'])

                if confirmed:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=source_url
                    ))

                if deaths:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_DEATHS,
                        value=int(deaths),
                        date_updated=date,
                        source_url=source_url
                    ))

                if icu:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_ICU,
                        value=int(icu),
                        date_updated=date,
                        source_url=source_url
                    ))

                if hospitalized:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(hospitalized),
                        date_updated=date,
                        source_url=source_url
                    ))

                if recovered:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=source_url
                    ))

                    if confirmed:
                        r.append(DataPoint(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DT_STATUS_ACTIVE,
                            value=int(recovered)-int(confirmed),
                            date_updated=date,
                            source_url=source_url
                        ))

                if confirmed:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=source_url
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(FRData().get_datapoints())
