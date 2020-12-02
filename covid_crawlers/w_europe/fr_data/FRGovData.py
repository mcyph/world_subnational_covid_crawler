# https://www.data.gouv.fr/fr/organizations/sante-publique-france/
# https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/#_

# article:contains(...) footer div a:contains(Télécharger)
# 'sp-pos-quot-dep-2020-07-03-19h15.csv'
# 'sp-pos-quot-reg-2020-07-03-19h15.csv'
# 'sp-pos-quot-fra-2020-07-03-19h15.csv'

# Colonne	Type 	Description_FR	Description_EN	Exemple
# dep	String	Departement	State	01
# reg	String	Region	region	2.0
# fra	String	France	France	FR
# jour	Date	Jour	Day	2020-05-13
# week	Date	Semaine	Week	2020-S21
# pop	integer	Population de reference (du departement, de la région, nationale)	Reference population (department, region, national)	656955.0
# t	integer	Nombre de test réalisés	Number of tests performed	2141.0
# cl_age90	integer	Classe d'age	Age class	09
# p	integer	Nombre de test positifs	Number of positive tests	34.0
# p_h	integer	Nombre de test positif chez les hommes	Number of positive test in men	1688.0
# t_h	integer	Nombre de test effectués chez les hommes	Number of tests performed on men	93639.0
# p_f	integer	Nombre de test positif chez les femmes	Number of positive test in women	2415.0
# t_f	integer	Nombre de test effectués chez les femmes	Number of tests performed on women	122725.0


import csv
from pyquery import PyQuery as pq
from collections import Counter

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir


class FRGovData(URLBase):
    SOURCE_URL = 'https://www.data.gouv.fr/fr/organizations/sante-publique-france/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'fr_sante_publique'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'fr' / 'govdata',
            urls_dict=self.__get_urls_dict()
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                # TODO: What are all these codes?
                ('admin_1', 'fr', 'fr-971'): None,
                ('admin_1', 'fr', 'fr-972'): None,
                ('admin_1', 'fr', 'fr-973'): None,
                ('admin_1', 'fr', 'fr-974'): None,
                ('admin_1', 'fr', 'fr-975'): None,
                ('admin_1', 'fr', 'fr-976'): None,
                ('admin_1', 'fr', 'fr-977'): None,
                ('admin_1', 'fr', 'fr-978'): None,
                ('admin_1', 'fr', 'fr-979'): None,
                ('admin_1', 'fr', 'fr-980'): None,
                ('admin_1', 'fr', 'fr-981'): None,
                ('admin_1', 'fr', 'fr-982'): None,
                ('admin_1', 'fr', 'fr-983'): None,
                ('admin_1', 'fr', 'fr-984'): None,
                ('admin_1', 'fr', 'fr-985'): None,
                ('admin_1', 'fr', 'fr-986'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def __get_urls_dict(self):
        _URL = 'https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/'
        html = pq(_URL)
        r = {}

        for typ, key in (
            (
                'Taux de positivité - quotidien - département',
                'daily_positive_by_department.csv'
            ),
            (
                'Taux de positivité - quotidien - région',
                'daily_positive_by_region.csv'
            ),
            (
                'Taux de positivité - quotidien - france',
                'daily_positive_national.csv'
            ),
        ):
            r[key] = URL(
                html(f'article:contains("{typ}") '
                     f'footer '
                     f'div '
                     f'a:contains("Télécharger")').attr('href'),
                static_file=False
            )

        return r

    def get_datapoints(self):
        r = []
        r.extend(self._get_positive_by_department())
        return r

    def _get_positive_by_department(self):
        # dep	jour	P	T	cl_age90
        # 1	2020-05-13	0	16	9
        # 1	2020-05-13	1	17	19
        r = self.sdpf()
        f = self.get_file('daily_positive_by_department.csv',
                          include_revision=True)

        positive_totals_by_age = Counter()
        tests_totals_by_age = Counter()

        age_groups = {
            '0': None,
            '09': '0-9',
            '19': '10-19',
            '29': '20-29',
            '39': '30-39',
            '49': '40-49',
            '59': '50-59',
            '69': '60-69',
            '79': '70-79',
            '89': '80-89',
            '90': '90+'
        }

        for item in csv.DictReader(f, delimiter=';'):
            date = self.convert_date(item['jour'])
            try:
                region_child = 'FR-%02d' % int(item['dep'])
            except ValueError:
                # e.g. 2A
                region_child = 'FR-%s' % item['dep']

            # https://www.arcorama.fr/2020/05/reutiliser-les-donnees-de-notre-tableau.html
            # cl_age90 of 0 -> total; 09 means 0-9 and so on
            agerange = age_groups[item['cl_age90']]

            positive_totals_by_age[agerange, region_child] += int(item['P'])
            tests_totals_by_age[agerange, region_child] += int(item['T'])

            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='FR',
                region_child=region_child,
                agerange=agerange,
                datatype=DataTypes.TOTAL,
                value=positive_totals_by_age[agerange, region_child],
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='FR',
                region_child=region_child,
                agerange=agerange,
                datatype=DataTypes.TESTS_TOTAL,
                value=tests_totals_by_age[agerange, region_child],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(FRGovData().get_datapoints())
