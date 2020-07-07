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


class FRGovData:
    pass

