import csv
import json

from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_ID_PROVINCE,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


# https://proxy.hxlstandard.org/data.csv?dest=data_edit&tagger-match-all=on&tagger-01-header=id+de+caso&tagger-01-tag=%23meta+%2Bid&tagger-02-header=fecha+de+notificacion&tagger-02-tag=%23date+%2Bnotification&tagger-03-header=codigo+divipola&tagger-03-tag=%23code&tagger-04-header=ciudad+de+ubicacion&tagger-04-tag=%23adm3+%2Bname&tagger-05-header=departamento+o+distrito&tagger-05-tag=%23adm2+%2Bname&tagger-06-header=atencion&tagger-06-tag=%23indicator+%2Binfected+%2Btype&tagger-07-header=edad&tagger-07-tag=%23indicator+%2Binfected+%2Bage&tagger-08-header=sexo&tagger-08-tag=%23indicator+%2Binfected+%2Bsex&tagger-10-header=estado&tagger-10-tag=%23indicator+%2Binfected+%2Bstatus&tagger-11-header=pais+de+procedencia&tagger-11-tag=%23indicator+%2Binfected+%2Borigin&tagger-13-header=fecha+de+muerte&tagger-13-tag=%23date+%2Breported+%2Bdeath&tagger-14-header=fecha+diagnostico&tagger-14-tag=%23date+%2Breported+%2Bnotification&tagger-15-header=fecha+recuperado&tagger-15-tag=%23date+%2Breported+%2Brecovered&tagger-16-header=fecha+reporte+web&tagger-16-tag=%23date+%2Breported&header-row=1&url=https%3A%2F%2Fwww.datos.gov.co%2Fapi%2Fviews%2Fgt2j-8ykr%2Frows.csv%3FaccessType%3DDOWNLOAD
#
# ID de caso,Fecha de notificación,Codigo DIVIPOLA,Ciudad de ubicación,
# Departamento o Distrito ,atención,Edad,Sexo,Tipo,Estado,País de procedencia,
# FIS,Fecha de muerte,Fecha diagnostico,Fecha recuperado,fecha reporte web
#
# #meta+id,#date+notification,#code,#adm3+name,#adm2+name,#indicator+infected+type,
# #indicator+infected+age,#indicator+infected+sex,,#indicator+infected+status,
# #indicator+infected+origin,,#date+reported+death,#date+reported+notification,
# #date+reported+recovered,#date+reported
#
# 1,2020-03-02T00:00:00.000,11001,Bogotá D.C.,Bogotá D.C.,Recuperado,19,F,Importado,Recuperado,Italia,2020-02-27T00:00:00.000,-   -,2020-03-06T00:00:00.000,2020-03-13T00:00:00.000,2020-03-06T00:00:00.000
# 2,2020-03-06T00:00:00.000,76111,Guadalajara de Buga,Valle del Cauca,Recuperado,34,M,Importado,Recuperado,España,2020-03-04T00:00:00.000,-   -,2020-03-09T00:00:00.000,2020-03-19T00:00:00.000,2020-03-09T00:00:00.000
# 3,2020-03-07T00:00:00.000,5001,Medellín,Antioquia,Recuperado,50,F,Importado,Recuperado,España,2020-02-29T00:00:00.000,-   -,2020-03-09T00:00:00.000,2020-03-15T00:00:00.000,2020-03-09T00:00:00.000
# 4,2020-03-09T00:00:00.000,5001,Medellín,Antioquia,Recuperado,55,M,Relacionado,Recuperado,Colombia,2020-03-06T00:00:00.000,-   -,2020-03-11T00:00:00.000,2020-03-26T00:00:00.000,2020-03-11T00:00:00.000


class COData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/positive-cases-of-covid-19-in-colombia'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'co' / 'data',
             urls_dict={
                 'co_data.csv': URL(
                     'https://proxy.hxlstandard.org/data.csv?'
                     'dest=data_edit&tagger-match-all=on&tagger-01-header=id+de+caso&'
                     'tagger-01-tag=%23meta+%2Bid&tagger-02-header=fecha+de+notificacion&'
                     'tagger-02-tag=%23date+%2Bnotification&tagger-03-header=codigo+divipola&'
                     'tagger-03-tag=%23code&tagger-04-header=ciudad+de+ubicacion&tagger-04-tag=%23adm3+%2Bname&'
                     'tagger-05-header=departamento+o+distrito&tagger-05-tag=%23adm2+%2Bname&'
                     'tagger-06-header=atencion&tagger-06-tag=%23indicator+%2Binfected+%2Btype&'
                     'tagger-07-header=edad&tagger-07-tag=%23indicator+%2Binfected+%2Bage&'
                     'tagger-08-header=sexo&tagger-08-tag=%23indicator+%2Binfected+%2Bsex&'
                     'tagger-10-header=estado&tagger-10-tag=%23indicator+%2Binfected+%2Bstatus&'
                     'tagger-11-header=pais+de+procedencia&tagger-11-tag=%23indicator+%2Binfected+%2Borigin&'
                     'tagger-13-header=fecha+de+muerte&tagger-13-tag=%23date+%2Breported+%2Bdeath&'
                     'tagger-14-header=fecha+diagnostico&tagger-14-tag=%23date+%2Breported+%2Bnotification&'
                     'tagger-15-header=fecha+recuperado&tagger-15-tag=%23date+%2Breported+%2Brecovered&'
                     'tagger-16-header=fecha+reporte+web&tagger-16-tag=%23date+%2Breported&header-row=1&'
                     'url=https%3A%2F%2Fwww.datos.gov.co%2Fapi%2Fviews%2Fgt2j-8ykr%2Frows.csv%3FaccessType%3DDOWNLOAD',
                     static_file=False
                 ),
             }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_provinces_1())
        #r.extend(self._get_provinces_2())
        return r

    def _get_provinces_1(self):
        r = []

        f = self.get_file('co_data.csv', include_revision=True)
        for item in csv.DictReader(f):
            case_id = item['ID de caso']
            notification_date = item['Fecha de notificación']
            divipola = item['Codigo DIVIPOLA']
            city = item['Ciudad de ubicación']
            department_district = item['Departamento o Distrito']
            attention = item['atención']
            age = item['Edad']
            gender = item['Sexo']
            status = item['Tipo']  # Source of infection??
            state = item['Estado']
            country_of_origin = item['País de procedencia']

            date_reported = item['FIS']
            date_death = item['Fecha de muerte']
            date_diagnosed = item['Fecha diagnostico']
            date_recovered = item['Fecha recuperado']
            date_web_report = item['fecha reporte web']

        return r

    def _get_provinces_2(self):
        r = []

        return r

if __name__ == '__main__':
    from pprint import pprint
    pprint(COData().get_datapoints())
