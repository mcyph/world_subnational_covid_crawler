# https://github.com/datadista/datasets/

# https://www.ciencia.gob.es/stfls/MICINN/Ministerio/FICHEROS/ENECOVID_Informe_preliminar_cierre_primera_ronda_13Mayo2020.pdf
#

import csv

from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


# This PDF has a lot of info that might not be in other places
# https://www.ciencia.gob.es/stfls/MICINN/Ministerio/FICHEROS/ENECOVID_Informe_preliminar_cierre_primera_ronda_13Mayo2020.pdf
# https://www.mscbs.gob.es/gabinetePrensa/notaPrensa/pdf/13.05130520204528614.pdf


class ESData(GithubRepo):
    SOURCE_URL = 'https://github.com/datadista/datasets/'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'es' / 'datasets',
                            github_url='https://github.com/datadista/datasets/')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_by_datos_isciii())
        r.extend(self._get_by_distritos_madrid())
        r.extend(self._get_by_age_national())
        r.extend(self._get_national_data())
        return r

    def _get_by_datos_isciii(self):
        r = []

        # Fecha,cod_ine,CCAA,Casos,PCR+,TestAc+,Hospitalizados,UCI,Fallecidos,Recuperados
        # 2020-02-20,01,Andalucía,0,0,,,,,
        # 2020-02-20,02,Aragón,,0,,,,,
        # 2020-02-20,03,Asturias,,0,,,,,
        # 2020-02-20,04,Baleares,,1,,,,,
        # 2020-02-20,05,Canarias,,1,,,,,
        # 2020-02-20,06,Cantabria,,0,,,,,
        # 2020-02-20,08,Castilla La Mancha,,0,,,,,
        # 2020-02-20,07,Castilla y León,,0,,,,,

        with open(self.get_path_in_dir('COVID 19/ccaa_covid19_datos_isciii.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['Fecha'])

                if item['Casos']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='Spain',
                        region_child=item['CCAA'],
                        datatype=DT_TOTAL,
                        value=int(item['Casos']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['PCR+'] or item['TestAc+']:   # NOTE ME: I'm combining PCR and other tests!!
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='Spain',
                        region_child=item['CCAA'],
                        datatype=DT_TESTS_TOTAL,
                        value=int(item['PCR+'] or 0) +
                              int(item['TestAc+'] or 0),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['Hospitalizados']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='Spain',
                        region_child=item['CCAA'],
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['Hospitalizados']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['Fallecidos']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='Spain',
                        region_child=item['CCAA'],
                        datatype=DT_STATUS_DEATHS,
                        value=int(item['Fallecidos']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item.get('Recuperados'):
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='Spain',
                        region_child=item['CCAA'],
                        datatype=DT_STATUS_RECOVERED,
                        value=int(item['Recuperados']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r

    def _get_by_distritos_madrid(self):
        r = []

        # fecha,cod_ine,municipio_distrito,casos_confirmados_ultimos_14dias,tasa_incidencia_acumulada_ultimos_14dias,casos_confirmados_totales,tasa_incidencia_acumulada_total
        # 2020-05-13,07903,Madrid-Retiro,77,"64,53",1447,"1212,74"
        # 2020-05-13,07904,Madrid-Salamanca,57,"39,01",1609,"1101,27"
        # 2020-05-13,07901,Madrid-Centro,37,"27,44",1139,"844,65"
        # 2020-05-13,07902,Madrid-Arganzuela,54,"35,11",1556,"1011,68"
        # 2020-05-13,07905,Madrid-Chamartín,47,"32,23",1590,"1090,17"
        # 2020-05-13,07906,Madrid-Tetuán,51,"32,27",2087,"1320,69"
        # 2020-05-13,07907,Madrid-Chamberí,56,"40,18",1511,"1084,09"

        with open(self.get_path_in_dir('COVID 19/municipios_distritos_madrid_casos.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['fecha'])

                if item['casos_confirmados_totales']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='Spain',
                        region_child=item['municipio_distrito'],
                        datatype=DT_TOTAL,
                        value=int(item['casos_confirmados_totales']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r
    
    def _get_by_age_national(self):
        r = []

        # fecha,rango_edad,sexo,casos_confirmados,hospitalizados,ingresos_uci,fallecidos
        # 2020-03-23,0-9,ambos,129,34,1,0
        # 2020-03-23,10-19,ambos,221,15,0,1
        # 2020-03-23,20-29,ambos,1285,183,8,4
        # 2020-03-23,30-39,ambos,2208,365,15,3
        # 2020-03-23,40-49,ambos,2919,663,40,9
        # 2020-03-23,50-59,ambos,3129,936,89,20
        # 2020-03-23,60-69,ambos,2916,1230,132,63
        # 2020-03-23,70-79,ambos,3132,1678,165,164

        with open(self.get_path_in_dir('COVID 19/nacional_covid19_rango_edad.csv'),
                  'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['fecha'])
                item['rango_edad'] = item['rango_edad'].replace('90 y +', '90+')

                if item['rango_edad'] == 'Total':
                    datatype = {
                        'ambos': DT_TOTAL,
                        'mujeres': DT_TOTAL_FEMALE,
                        'hombres': DT_TOTAL_MALE
                    }[item['sexo']]

                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=datatype,
                        value=int(item['casos_confirmados']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    continue

                if item['casos_confirmados']:
                    datatype = {
                        'ambos': DT_TOTAL,
                        'mujeres': DT_TOTAL_FEMALE,
                        'hombres': DT_TOTAL_MALE
                    }[item['sexo']]

                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=datatype,
                        agerange=item['rango_edad'],
                        value=int(item['casos_confirmados']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                
                if item['sexo'] == 'ambos':
                    if item['hospitalizados']:   # NOTE ME: I'm combining PCR and other tests!!
                        r.append(DataPoint(
                            region_schema=SCHEMA_ADMIN_0,
                            region_child='Spain',
                            datatype=DT_STATUS_HOSPITALIZED,
                            agerange=item['rango_edad'],
                            value=int(item['hospitalizados']),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))
    
                    if item['ingresos_uci']:   # WARNING: This is **accumulated** cases!!! ========================================================
                        r.append(DataPoint(
                            region_schema=SCHEMA_ADMIN_0,
                            region_child='Spain',
                            datatype=DT_STATUS_ICU,
                            agerange=item['rango_edad'],
                            value=int(item['ingresos_uci']),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))
    
                    if item['fallecidos']:
                        r.append(DataPoint(
                            region_schema=SCHEMA_ADMIN_0,
                            region_child='Spain',
                            datatype=DT_STATUS_DEATHS,
                            agerange=item['rango_edad'],
                            value=int(item['fallecidos']),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))
        return r
    
    def _get_national_data(self):
        r = []

        # fecha,casos_total,casos_pcr,casos_test_ac,altas,fallecimientos,ingresos_uci,hospitalizados
        # 2020-02-21,3,3,,,,,
        # 2020-02-22,3,3,,,,,
        # 2020-02-23,3,3,,,,,
        # 2020-02-24,3,3,,,,,
        # 2020-02-25,4,4,,,,,
        # 2020-02-26,10,10,,,,,
        # 2020-02-27,18,18,,,,,

        with open(self.get_path_in_dir('COVID 19/nacional_covid19.csv'),
                  'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['fecha'])

                if item['casos_total']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=DT_TOTAL,
                        value=int(item['casos_total']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['casos_pcr'] or item['casos_test_ac']:   # NOTE ME: I'm combining PCR and other tests!!
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=DT_TESTS_TOTAL,
                        value=int(item['casos_pcr'] or 0) +
                              int(item['casos_test_ac'] or 0),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['hospitalizados']:   # WARNING: This is **accumulated** cases!!! ========================================================
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(item['hospitalizados']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['ingresos_uci']:   # WARNING: This is **accumulated** cases!!! ========================================================
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=DT_STATUS_ICU,
                        value=int(item['ingresos_uci']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['fallecimientos']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=DT_STATUS_DEATHS,
                        value=int(item['fallecimientos']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['altas']:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_0,
                        region_child='Spain',
                        datatype=DT_STATUS_RECOVERED,
                        value=int(item['altas']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ESData().get_datapoints())
