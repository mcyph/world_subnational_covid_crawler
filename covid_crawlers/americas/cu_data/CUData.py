# https://github.com/covid19cubadata/covid19cubadata.github.io/tree/master/data
import csv
from collections import Counter

from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_crawlers._base_classes.GithubRepo import GithubRepo
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.world_geodata.LabelsToRegionChild import LabelsToRegionChild


region_map = dict([i.split('\t')[::-1] for i in '''
CU-15	Artemisa
CU-09	Camagüey
CU-08	Ciego de Ávila
CU-06	Cienfuegos
CU-12	Granma
CU-14	Guantánamo
CU-11	Holguín
CU-03	La Habana
CU-10	Las Tunas
CU-04	Matanzas
CU-16	Mayabeque
CU-01	Pinar del Río
CU-07	Sancti Spíritus
CU-13	Santiago de Cuba
CU-05	Villa Clara
CU-99	Isla de la Juventud
'''.strip().split('\n')])


class CUData(GithubRepo):
    SOURCE_URL = 'https://github.com/covid19cubadata/covid19cubadata.github.io/tree/master/data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'cu_covid19cubadata'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'cu' / 'covid19cubadata.github.io',
                            github_url='https://github.com/covid19cubadata/covid19cubadata.github.io/tree/master/data')
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'cu', 'trinidad'): ('MERGE', 'admin_1', 'cu', 'cu-07'),
                ('cu_municipality', 'cu', 'trinidad'): ('MERGE', 'cu_municipality', 'cu-07', 'trinidad'),
            },
            mode=MODE_STRICT
        )
        self.ltrc = LabelsToRegionChild()
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases())
        return r

    def _get_cases(self):
        # caso,sexo,edad,pais,municipio,provincia,fecha_confirmacion,fecha_ingreso,tipo_contagio
        # case, sex, age, country, municipality, province, confirmation_date, entry_date, contact_type
        # ,hombre,61,it,Trinidad,Sancti Spíritus,2020/03/11,2020/03/10,primario
        # ,mujer,57,it,Trinidad,Sancti Spíritus,2020/03/11,2020/03/10,primario

        r = self.sdpf()

        genders = {
            'hombre': DataTypes.TOTAL_MALE,
            'mujer': DataTypes.TOTAL_FEMALE
        }

        #infection_sources = {
        #    'primario': FIXME,
        #    'secundario': FIXME,
        #    'desconocido': FIXME
        #}

        def age_to_range(age):
            for x in range(0, 110, 10):
                if x <= age < x+10:
                    return f'{x}-{x+9}'
            raise Exception()

        with open(self.get_path_in_dir('data/covid19-casos.csv'),
                  'r', encoding='utf-8') as f:

            by_totals = Counter()
            by_gender = Counter()
            by_age = Counter()
            by_municipality = Counter()
            by_province = Counter()
            by_source_of_infection = Counter()

            for item in csv.DictReader(f):
                #print(item)
                date = self.convert_date(item['fecha_confirmacion'])

                by_totals[date] += 1
                by_gender[date, genders[item['sexo']]] += 1
                by_age[date, age_to_range(int(item['edad']))] += 1

                if item['provincia'] and item['municipio']:
                    by_municipality[date, region_map[item['provincia']], item['municipio']] += 1

                if item['provincia']:
                    by_province[date, region_map[item['provincia']]] += 1

                #by_source_of_infection[date, item['tipo_contagio']] += 1

            cumulative = 0
            for date, value in sorted(by_totals.items()):
                cumulative += value

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent=None,
                    region_child='CU',
                    datatype=DataTypes.TOTAL,
                    date_updated=date,
                    value=cumulative,
                    source_url=self.SOURCE_URL
                )

            cumulative = Counter()
            for (date, gender), value in sorted(by_gender.items()):
                cumulative[gender] += value

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent=None,
                    region_child='CU',
                    datatype=gender,
                    date_updated=date,
                    value=cumulative[gender],
                    source_url=self.SOURCE_URL
                )

            cumulative = Counter()
            for (date, age), value in sorted(by_age.items()):
                cumulative[age] += value

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent=None,
                    region_child='CU',
                    datatype=DataTypes.TOTAL,
                    agerange=age,
                    date_updated=date,
                    value=cumulative[age],
                    source_url=self.SOURCE_URL
                )

            cumulative = Counter()
            for (date, province, municipality), value in sorted(by_municipality.items()):
                cumulative[province, municipality] += value

                r.append(
                    region_schema=Schemas.CU_MUNICIPALITY,
                    region_parent=province,
                    region_child=municipality,
                    datatype=DataTypes.TOTAL,
                    date_updated=date,
                    value=cumulative[municipality, province],
                    source_url=self.SOURCE_URL
                )

            cumulative = Counter()
            for (date, province), value in sorted(by_province.items()):
                cumulative[province] += value

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='CU',
                    region_child=province,
                    datatype=DataTypes.TOTAL,
                    date_updated=date,
                    value=cumulative[province],
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(CUData().get_datapoints())
