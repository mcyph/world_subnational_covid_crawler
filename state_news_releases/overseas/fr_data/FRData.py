import csv
import json
from collections import Counter

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_STATEWIDE, SCHEMA_FR_OVERSEAS_COLLECTIVITY,
    SCHEMA_FR_REGION, SCHEMA_FR_DEPARTMENT,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW, DT_STATUS_ACTIVE,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
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
                region = item['maille_nom']
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
                    schema = SCHEMA_STATEWIDE
                    region = None
                elif item['granularite'] in 'departement':
                    schema = SCHEMA_FR_DEPARTMENT
                elif item['granularite'] == 'region':
                    schema = SCHEMA_FR_REGION
                elif item['granularite'] == 'collectivite-outremer':
                    schema = SCHEMA_FR_OVERSEAS_COLLECTIVITY
                elif item['granularite'] == 'monde':
                    # World
                    continue
                else:
                    raise Exception(item['granularite'])

                if confirmed:
                    r.append(DataPoint(
                        schema=schema,
                        datatype=DT_TOTAL,
                        region=region,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=source_url
                    ))

                if deaths:
                    r.append(DataPoint(
                        schema=schema,
                        datatype=DT_STATUS_DEATHS,
                        region=region,
                        value=int(deaths),
                        date_updated=date,
                        source_url=source_url
                    ))

                if icu:
                    r.append(DataPoint(
                        schema=schema,
                        datatype=DT_STATUS_ICU,
                        region=region,
                        value=int(icu),
                        date_updated=date,
                        source_url=source_url
                    ))

                if hospitalized:
                    r.append(DataPoint(
                        schema=schema,
                        datatype=DT_STATUS_HOSPITALIZED,
                        region=region,
                        value=int(hospitalized),
                        date_updated=date,
                        source_url=source_url
                    ))

                if recovered:
                    r.append(DataPoint(
                        schema=schema,
                        datatype=DT_STATUS_RECOVERED,
                        region=region,
                        value=int(recovered),
                        date_updated=date,
                        source_url=source_url
                    ))
                    if confirmed:
                        r.append(DataPoint(
                            schema=schema,
                            datatype=DT_STATUS_ACTIVE,
                            region=region,
                            value=int(recovered)-int(confirmed),
                            date_updated=date,
                            source_url=source_url
                        ))

                if confirmed:
                    r.append(DataPoint(
                        schema=schema,
                        datatype=DT_TOTAL,
                        region=region,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=source_url
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(FRData().get_datapoints())
