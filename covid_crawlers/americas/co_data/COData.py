import csv
from collections import Counter

from covid_crawlers._base_classes.URLBase import URL, URLBase
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT


class COData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/positive-cases-of-covid-19-in-colombia'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'co_ocha_humdata'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'co' / 'data',
             urls_dict={
                 'co_data.csv': URL(
                     'https://proxy.hxlstandard.org/data.csv?dest=data_edit&tagger-match-all=on&tagger-01-header=id+de+caso&tagger-01-tag=%23meta+%2Bid&tagger-02-header=fecha+de+notificacion&tagger-02-tag=%23date+%2Bnotification&tagger-03-header=codigo+divipola&tagger-03-tag=%23code&tagger-04-header=ciudad+de+ubicacion&tagger-04-tag=%23adm3+%2Bname&tagger-05-header=departamento+o+distrito&tagger-05-tag=%23adm2+%2Bname&tagger-06-header=atencion&tagger-06-tag=%23indicator+%2Binfected+%2Btype&tagger-07-header=edad&tagger-07-tag=%23indicator+%2Binfected+%2Bage&tagger-08-header=sexo&tagger-08-tag=%23indicator+%2Binfected+%2Bsex&tagger-10-header=estado&tagger-10-tag=%23indicator+%2Binfected+%2Bstatus&tagger-11-header=pais+de+procedencia&tagger-11-tag=%23indicator+%2Binfected+%2Borigin&tagger-13-header=fecha+de+muerte&tagger-13-tag=%23date+%2Breported+%2Bdeath&tagger-14-header=fecha+diagnostico&tagger-14-tag=%23date+%2Breported+%2Bnotification&tagger-15-header=fecha+recuperado&tagger-15-tag=%23date+%2Breported+%2Brecovered&tagger-16-header=fecha+reporte+web&tagger-16-tag=%23date+%2Breported&header-row=1&url=https%3A%2F%2Fwww.datos.gov.co%2Fapi%2Fviews%2Fgt2j-8ykr%2Frows.csv%3FaccessType%3DDOWNLOAD',
                     static_file=False
                 ),
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'co', 'co-dc'): ('MERGE', 'admin_1', 'co', 'co-cun'),
                ('admin_1', 'co', 'co-cun'): ('MERGE', 'admin_1', 'co', 'co-cun'),
                ('admin_1', 'co', 'cartagena d.t. y c.'): ('MERGE', 'admin_1', 'co', 'co-bol'),
                ('admin_1', 'co', 'cartagena'): ('MERGE', 'admin_1', 'co', 'co-bol'),
                ('admin_1', 'co', 'barranquilla d.e.'): ('MERGE', 'admin_1', 'co', 'co-atl'),
                ('admin_1', 'co', 'barranquilla'): ('MERGE', 'admin_1', 'co', 'co-atl'),
                ('admin_1', 'co', 'santa marta d.t. y c.'): ('MERGE', 'admin_1', 'co', 'co-atl'),
                ('admin_1', 'co', 'santa marta'): ('MERGE', 'admin_1', 'co', 'co-atl'),
                ('admin_1', 'co', 'archipiélago de san andrés providencia y santa catalina'): ('MERGE', 'admin_1', 'co', 'co-atl'),
                ('admin_1', 'co', 'buenaventura d.e.'): ('MERGE', 'admin_1', 'co', 'co-vac'),
                ('admin_1', 'co', 'buenaventura'): ('MERGE', 'admin_1', 'co', 'co-vac'),
                ('admin_1', 'co', 'norte santander'): ('MERGE', 'admin_1', 'co', 'co-vac'),

                ('co_municipality', 'cartagena d.t. y c.', 'cartagena de indias'): ('co_municipality', 'co-bol', 'cartagena de indias'),
                ('co_municipality', 'norte de santander', 'cúcuta'): None,
                ('co_municipality', 'barranquilla d.e.', 'barranquilla'): ('co_municipality', 'co-atl', 'barranquilla'),
                ('co_municipality', 'santa marta d.t. y c.', 'santa marta'): None,
                ('co_municipality', 'archipiélago de san andrés providencia y santa catalina', 'san andrés'): None,
                ('co_municipality', 'archipiélago de san andrés providencia y santa catalina', 'providencia'): None,
                ('co_municipality', 'buenaventura d.e.', 'buenaventura'): ('co_municipality', 'co-vac', 'buenaventura'),
                ('co_municipality', 'co-dc', 'bogotá d.c.'): None, # FIXME!!!!
                ('co_municipality', 'cundinamarca', 'villa de de ubaté'): None,
                ('co_municipality', 'nariño', 'cuaspúd'): None,
                ('co_municipality', 'nariño', 'ancuyá'): None,
                ('co_municipality', 'cauca', 'piendamó'): None,
                ('co_municipality', 'cauca', 'guapí'): None,
                ('co_municipality', 'cauca', 'sotara'): None,
                ('co_municipality', 'vaupés', 'mitú'): None,
                ('co_municipality', 'vaupés', 'yavaraté'): None,
                ('co_municipality', 'vaupés', 'taraira'): None,
                ('co_municipality', 'chocó', 'el cantón san pablo'): None,
                ('co_municipality', 'chocó', 'el litoral san juan'): None,
                ('co_municipality', 'sucre', 'tolú viejo'): None,
                ('co_municipality', 'sucre', 'coloso'): None,
                ('co_municipality', 'antioquia', 'san pedro los milagros'): None,
                ('co_municipality', 'antioquia', 'san josé la montaña'): None,
                ('co_municipality', 'meta', 'san luis de cubarral'): None,
                ('co_municipality', 'santander', 'el carmen de chucurí'): None,
                ('co_municipality', 'vaupés', 'carurú'): None,
                ('co_municipality', 'guainía', 'barranco minas'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_co_data())
        return r

    def _get_co_data(self):
        r = self.sdpf()
        
        # # https://proxy.hxlstandard.org/data.csv?dest=data_edit&tagger-match-all=on&tagger-01-header=id+de+caso&tagger-01-tag=%23meta+%2Bid&tagger-02-header=fecha+de+notificacion&tagger-02-tag=%23date+%2Bnotification&tagger-03-header=codigo+divipola&tagger-03-tag=%23code&tagger-04-header=ciudad+de+ubicacion&tagger-04-tag=%23adm3+%2Bname&tagger-05-header=departamento+o+distrito&tagger-05-tag=%23adm2+%2Bname&tagger-06-header=atencion&tagger-06-tag=%23indicator+%2Binfected+%2Btype&tagger-07-header=edad&tagger-07-tag=%23indicator+%2Binfected+%2Bage&tagger-08-header=sexo&tagger-08-tag=%23indicator+%2Binfected+%2Bsex&tagger-10-header=estado&tagger-10-tag=%23indicator+%2Binfected+%2Bstatus&tagger-11-header=pais+de+procedencia&tagger-11-tag=%23indicator+%2Binfected+%2Borigin&tagger-13-header=fecha+de+muerte&tagger-13-tag=%23date+%2Breported+%2Bdeath&tagger-14-header=fecha+diagnostico&tagger-14-tag=%23date+%2Breported+%2Bnotification&tagger-15-header=fecha+recuperado&tagger-15-tag=%23date+%2Breported+%2Brecovered&tagger-16-header=fecha+reporte+web&tagger-16-tag=%23date+%2Breported&header-row=1&url=https%3A%2F%2Fwww.datos.gov.co%2Fapi%2Fviews%2Fgt2j-8ykr%2Frows.csv%3FaccessType%3DDOWNLOAD
        # #
        # # ID de caso,Fecha de notificación,Codigo DIVIPOLA,Ciudad de ubicación,
        # # Departamento o Distrito ,atención,Edad,Sexo,Tipo,Estado,País de procedencia,
        # # FIS,Fecha de muerte,Fecha diagnostico,Fecha recuperado,fecha reporte web
        # #
        # # #meta+id,#date+notification,#code,#adm3+name,#adm2+name,#indicator+infected+type,
        # # #indicator+infected+age,#indicator+infected+sex,,#indicator+infected+status,
        # # #indicator+infected+origin,,#date+reported+death,#date+reported+notification,
        # # #date+reported+recovered,#date+reported
        # #
        # # 1,2020-03-02T00:00:00.000,11001,Bogotá D.C.,Bogotá D.C.,Recuperado,19,F,Importado,Recuperado,Italia,2020-02-27T00:00:00.000,-   -,2020-03-06T00:00:00.000,2020-03-13T00:00:00.000,2020-03-06T00:00:00.000
        # # 2,2020-03-06T00:00:00.000,76111,Guadalajara de Buga,Valle del Cauca,Recuperado,34,M,Importado,Recuperado,España,2020-03-04T00:00:00.000,-   -,2020-03-09T00:00:00.000,2020-03-19T00:00:00.000,2020-03-09T00:00:00.000
        # # 3,2020-03-07T00:00:00.000,5001,Medellín,Antioquia,Recuperado,50,F,Importado,Recuperado,España,2020-02-29T00:00:00.000,-   -,2020-03-09T00:00:00.000,2020-03-15T00:00:00.000,2020-03-09T00:00:00.000
        # # 4,2020-03-09T00:00:00.000,5001,Medellín,Antioquia,Recuperado,55,M,Relacionado,Recuperado,Colombia,2020-03-06T00:00:00.000,-   -,2020-03-11T00:00:00.000,2020-03-26T00:00:00.000,2020-03-11T00:00:00.000

        by_age = Counter()
        by_status = Counter()  # And source of infection

        by_admin1_age = Counter()
        by_admin1_status = Counter()

        by_municipality_age = Counter()
        by_municipality_status = Counter()

        first_item = True
        f = self.get_file('co_data.csv', include_revision=True)

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue
            elif '<html>' in item:
                continue

            print(item)
            case_id = item['ID de caso']
            notification_date = self.convert_date(item['Fecha de notificación'].split('T')[0].split()[0])
            #divipola = item['Codigo DIVIPOLA']
            municipality = item['Nombre municipio']
            admin1 = {
                'bogotá d.c.': 'co-dc', #'Distrito Capital de Bogota',
            }.get(item['Nombre departamento'].lower(), item['Nombre departamento'])
            #attention = item['atención']
            age = self._age_to_range(item['Edad'])
            gender = {
                'M': DataTypes.TOTAL_MALE,
                'F': DataTypes.TOTAL_FEMALE
            }[item['Sexo'].upper()]
            source_of_infection = {
                'importado': DataTypes.SOURCE_OVERSEAS,
                'relacionado': DataTypes.SOURCE_CONFIRMED,
                'en estudio': DataTypes.SOURCE_UNDER_INVESTIGATION,
                'desconocido': DataTypes.SOURCE_COMMUNITY,
                '': DataTypes.SOURCE_COMMUNITY,  # HACK!
            }[item['Tipo de contagio'].lower()]
            state = item['Estado']
            country_of_origin = item['Nombre del país']  # TODO: Add support for this!! ============================

            #date_reported = self.convert_date(item['FIS'])
            #date_diagnosed = self.convert_date(item['Fecha diagnostico'])
            #date_web_report = self.convert_date(item['fecha reporte web'])

            if item['Fecha de muerte'].strip('-/NA').strip():
                date_death = self.convert_date(item['Fecha de muerte'].split('T')[0].split()[0])
                by_status[date_death, DataTypes.STATUS_DEATHS] += 1
                by_admin1_status[date_death, admin1, DataTypes.STATUS_DEATHS] += 1
                by_municipality_status[date_death, admin1, municipality, DataTypes.STATUS_DEATHS] += 1

            if item['Fecha de recuperación'].strip('-/NA').strip():
                date_recovered = self.convert_date(item['Fecha de recuperación'].split('T')[0].split()[0])
                by_status[date_recovered, DataTypes.STATUS_RECOVERED] += 1
                by_admin1_status[date_recovered, admin1, DataTypes.STATUS_RECOVERED] += 1
                by_municipality_status[date_recovered, admin1, municipality, DataTypes.STATUS_RECOVERED] += 1

            by_status[notification_date, source_of_infection] += 1
            by_admin1_status[notification_date, admin1, source_of_infection] += 1
            by_municipality_status[notification_date, admin1, municipality, source_of_infection] += 1

            by_status[notification_date, gender] += 1
            by_admin1_status[notification_date, admin1, gender] += 1
            by_municipality_status[notification_date, admin1, municipality, gender] += 1

            by_status[notification_date, DataTypes.TOTAL] += 1
            by_admin1_status[notification_date, admin1, DataTypes.TOTAL] += 1
            by_municipality_status[notification_date, admin1, municipality, DataTypes.TOTAL] += 1

            by_age[notification_date, age] += 1
            by_admin1_age[notification_date, admin1, age] += 1
            by_municipality_age[notification_date, admin1, municipality, age] += 1

        cumulative = Counter()
        for (notification_date, age), value in sorted(by_age.items()):
            cumulative[age] += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='co',
                datatype=DataTypes.TOTAL,
                agerange=age,
                value=cumulative[age],
                date_updated=notification_date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (notification_date, status), value in sorted(by_status.items()):
            cumulative[status] += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='co',
                datatype=status,
                value=cumulative[status],
                date_updated=notification_date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (notification_date, admin1, age), value in sorted(by_admin1_age.items()):
            cumulative[admin1, age] += value
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='co',
                region_child=admin1,
                agerange=age,
                datatype=DataTypes.TOTAL,
                value=cumulative[admin1, age],
                date_updated=notification_date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (notification_date, admin1, status), value in sorted(by_admin1_status.items()):
            cumulative[admin1, status] += value
            #print(admin1, status)
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='co',
                region_child=admin1,
                datatype=status,
                value=cumulative[admin1, status],
                date_updated=notification_date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (notification_date, admin1, municipality, age), value in sorted(by_municipality_age.items()):
            cumulative[admin1, municipality, age] += value
            r.append(
                region_schema=Schemas.CO_MUNICIPALITY,
                region_parent=admin1,
                region_child=municipality,
                agerange=age,
                datatype=DataTypes.TOTAL,
                value=cumulative[admin1, municipality, age],
                date_updated=notification_date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (notification_date, admin1, municipality, status), value in sorted(by_municipality_status.items()):
            cumulative[admin1, municipality, status] += value
            r.append(
                region_schema=Schemas.CO_MUNICIPALITY,
                region_parent=admin1,
                region_child=municipality,
                datatype=status,
                value=cumulative[admin1, municipality, status],
                date_updated=notification_date,
                source_url=self.SOURCE_URL
            )

        return r

    def _age_to_range(self, age):
        age = int(age)
        for x in range(0, 150, 10):
            if x <= age <= x+9:
                return f'{x}-{x+9}'
        raise Exception(age)


if __name__ == '__main__':
    from pprint import pprint
    pprint(COData().get_datapoints())
