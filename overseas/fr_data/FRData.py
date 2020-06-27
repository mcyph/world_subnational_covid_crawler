import csv

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1, SCHEMA_FR_OVERSEAS_COLLECTIVITY,
    #SCHEMA_FR_DEPARTMENT,
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

place_map = dict([i.split('\t')[::-1] for i in """
FR-ARA	Auvergne-Rhône-Alpes
FR-BFC	Bourgogne-Franche-Comté
FR-BRE	Bretagne
FR-BRE	Brittany
FR-CVL	Centre-Val de Loire
FR-COR	Corse
FR-COR	Corsica
FR-GES	Grand-Est
FR-GES	Grand Est
FR-GUA	Guadeloupe
FR-HDF	Hauts-de-France
FR-IDF	Île-de-France
FR-MAY	Mayotte
FR-NOR	Normandie
FR-NOR	Normandy
FR-NAQ	Nouvelle-Aquitaine
FR-OCC	Occitanie
FR-PDL	Pays-de-la-Loire
FR-PDL	Pays de la Loire
FR-PAC	Provence-Alpes-Côte-d’Azur
FR-PAC	Provence-Alpes-Côte d'Azur
FR-LRE	La Réunion
FR-GF	French Guiana
FR-GF	Guyane
FR-MQ	Martinique
FR-LRE	Réunion
""".strip().split('\n')])

fr_departments = dict([i.split('\t')[::-1] for i in """
FR-01	Ain
FR-02	Aisne
FR-03	Allier
FR-04	Alpes-de-Haute-Provence
FR-06	Alpes-Maritimes
FR-07	Ardèche
FR-08	Ardennes
FR-09	Ariège
FR-10	Aube
FR-11	Aude
FR-12	Aveyron
FR-67	Bas-Rhin
FR-13	Bouches-du-Rhône
FR-14	Calvados
FR-15	Cantal
FR-16	Charente
FR-17	Charente-Maritime
FR-18	Cher
FR-19	Corrèze
FR-2A	Corse-du-Sud
FR-21	Côte-d'Or
FR-22	Côtes-d'Armor
FR-23	Creuse
FR-79	Deux-Sèvres
FR-24	Dordogne
FR-25	Doubs
FR-26	Drôme
FR-91	Essonne
FR-27	Eure
FR-28	Eure-et-Loir
FR-29	Finistère
FR-30	Gard
FR-32	Gers
FR-33	Gironde
FR-GP	Guadeloupe
FR-2B	Haute-Corse
FR-31	Haute-Garonne
FR-43	Haute-Loire
FR-52	Haute-Marne
FR-05	Hautes-Alpes
FR-70	Haute-Saône
FR-74	Haute-Savoie
FR-65	Hautes-Pyrénées
FR-87	Haute-Vienne
FR-68	Haut-Rhin
FR-92	Hauts-de-Seine
FR-34	Hérault
FR-35	Ille-et-Vilaine
FR-36	Indre
FR-37	Indre-et-Loire
FR-38	Isère
FR-39	Jura
FR-40	Landes
FR-42	Loire
FR-44	Loire-Atlantique
FR-45	Loiret
FR-41	Loir-et-Cher
FR-46	Lot
FR-47	Lot-et-Garonne
FR-48	Lozère
FR-49	Maine-et-Loire
FR-50	Manche
FR-51	Marne
FR-53	Mayenne
FR-YT	Mayotte
FR-54	Meurthe-et-Moselle
FR-55	Meuse
FR-56	Morbihan
FR-57	Moselle
FR-58	Nièvre
FR-59	Nord
FR-60	Oise
FR-61	Orne
FR-75	Paris
FR-62	Pas-de-Calais
FR-63	Puy-de-Dôme
FR-64	Pyrénées-Atlantiques
FR-66	Pyrénées-Orientales
FR-RE	La Réunion
FR-69	Rhône
FR-71	Saône-et-Loire
FR-72	Sarthe
FR-73	Savoie
FR-77	Seine-et-Marne
FR-76	Seine-Maritime
FR-93	Seine-Saint-Denis
FR-80	Somme
FR-81	Tarn
FR-82	Tarn-et-Garonne
FR-90	Territoire de Belfort
FR-94	Val-de-Marne
FR-95	Val-d'Oise
FR-83	Var
FR-84	Vaucluse
FR-85	Vendée
FR-86	Vienne
FR-88	Vosges
FR-89	Yonne
FR-78	Yvelines 
""".strip().split('\n')])

fr_divisions = """
1	Ain	Bourg-en-Bresse	Auvergne-Rhône-Alpes
2	Aisne	Laon	Hauts-de-France
3	Allier	Moulins	Auvergne-Rhône-Alpes
4	Alpes-de-Haute-Provence	Digne-les-Bains	Provence-Alpes-Côte d'Azur
5	Hautes-Alpes	Gap	Provence-Alpes-Côte d'Azur
6	Alpes-Maritimes	Nice	Provence-Alpes-Côte d'Azur
7	Ardèche	Privas	Auvergne-Rhône-Alpes
8	Ardennes	Charleville-Mézières	Grand Est
9	Ariège	Foix	Occitanie
10	Aube	Troyes	Grand Est
11	Aude	Carcassonne	Occitanie
12	Aveyron	Rodez	Occitanie
13	Bouches-du-Rhône	Marseille	Provence-Alpes-Côte d'Azur
14	Calvados	Caen	Normandy
15	Cantal	Aurillac	Auvergne-Rhône-Alpes
16	Charente	Angoulême	Nouvelle-Aquitaine
17	Charente-Maritime	La Rochelle	Nouvelle-Aquitaine
18	Cher	Bourges	Centre-Val de Loire
19	Corrèze	Tulle	Nouvelle-Aquitaine
2A	Corse-du-Sud	Ajaccio	Corsica
2B	Haute-Corse	Bastia	Corsica
21	Côte-d'Or	Dijon	Bourgogne-Franche-Comté
22	Côtes-d'Armor	Saint-Brieuc	Brittany
23	Creuse	Guéret	Nouvelle-Aquitaine
24	Dordogne	Périgueux	Nouvelle-Aquitaine
25	Doubs	Besançon	Bourgogne-Franche-Comté
26	Drôme	Valence	Auvergne-Rhône-Alpes
27	Eure	Évreux	Normandy
28	Eure-et-Loir	Chartres	Centre-Val de Loire
29	Finistère	Quimper	Brittany
30	Gard	Nîmes	Occitanie
31	Haute-Garonne	Toulouse	Occitanie
32	Gers	Auch	Occitanie
33	Gironde	Bordeaux	Nouvelle-Aquitaine
34	Hérault	Montpellier	Occitanie
35	Ille-et-Vilaine	Rennes	Brittany
36	Indre	Châteauroux	Centre-Val de Loire
37	Indre-et-Loire	Tours	Centre-Val de Loire
38	Isère	Grenoble	Auvergne-Rhône-Alpes
39	Jura	Lons-le-Saunier	Bourgogne-Franche-Comté
40	Landes	Mont-de-Marsan	Nouvelle-Aquitaine
41	Loir-et-Cher	Blois	Centre-Val de Loire
42	Loire	Saint-Étienne	Auvergne-Rhône-Alpes
43	Haute-Loire	Le Puy-en-Velay	Auvergne-Rhône-Alpes
44	Loire-Atlantique	Nantes	Pays de la Loire
45	Loiret	Orléans	Centre-Val de Loire
46	Lot	Cahors	Occitanie
47	Lot-et-Garonne	Agen	Nouvelle-Aquitaine
48	Lozère	Mende	Occitanie
49	Maine-et-Loire	Angers	Pays de la Loire
50	Manche	Saint-Lô	Normandy
51	Marne	Châlons-en-Champagne	Grand Est
52	Haute-Marne	Chaumont	Grand Est
53	Mayenne	Laval	Pays de la Loire
54	Meurthe-et-Moselle	Nancy	Grand Est
55	Meuse	Bar-le-Duc	Grand Est
56	Morbihan	Vannes	Brittany
57	Moselle	Metz	Grand Est
58	Nièvre	Nevers	Bourgogne-Franche-Comté
59	Nord	Lille	Hauts-de-France
60	Oise	Beauvais	Hauts-de-France
61	Orne	Alençon	Normandy
62	Pas-de-Calais	Arras	Hauts-de-France
63	Puy-de-Dôme	Clermont-Ferrand	Auvergne-Rhône-Alpes
64	Pyrénées-Atlantique	Pau	Nouvelle-Aquitaine
64	Pyrénées-Atlantiques	Pau	Nouvelle-Aquitaine
65	Hautes-Pyrénées	Tarbes	Occitanie
66	Pyrénées-Orientales	Perpignan	Occitanie
67	Bas-Rhin	Strasbourg	Grand Est
68	Haut-Rhin	Colmar	Grand Est
69	Rhône	Lyon (provisional)	Auvergne-Rhône-Alpes
69M	Lyon Metropolis	Lyon	Auvergne-Rhône-Alpes
70	Haute-Saône	Vesoul	Bourgogne-Franche-Comté
71	Saône-et-Loire	Mâcon	Bourgogne-Franche-Comté
72	Sarthe	Le Mans	Pays de la Loire
73	Savoie	Chambéry	Auvergne-Rhône-Alpes
74	Haute-Savoie	Annecy	Auvergne-Rhône-Alpes
75	Pari	Paris	Île-de-France
75	Paris	Paris	Île-de-France
76	Seine-Maritime	Rouen	Normandy
77	Seine-et-Marne	Melun	Île-de-France
78	Yvelines	Versailles	Île-de-France
79	Deux-Sèvres	Niort	Nouvelle-Aquitaine
80	Somme	Amiens	Hauts-de-France
81	Tarn	Albi	Occitanie
82	Tarn-et-Garonne	Montauban	Occitanie
83	Var	Toulon	Provence-Alpes-Côte d'Azur
84	Vaucluse	Avignon	Provence-Alpes-Côte d'Azur
85	Vendée	La Roche-sur-Yon	Pays de la Loire
86	Vienne	Poitiers	Nouvelle-Aquitaine
87	Haute-Vienne	Limoges	Nouvelle-Aquitaine
88	Vosges	Épinal	Grand Est
89	Yonne	Auxerre	Bourgogne-Franche-Comté
90	Territoire de Belfort	Belfort	Bourgogne-Franche-Comté
91	Essonne	Évry	Île-de-France
92	Hauts-de-Seine	Nanterre	Île-de-France
93	Seine-Saint-Denis	Bobigny	Île-de-France
94	Val-de-Marne	Créteil	Île-de-France
95	Val-d'Oise	Pontoise	Île-de-France
971	Guadeloupe	Basse-Terre	Guadeloupe
972	Martinique	Fort-de-France	Martinique
973	Guyane	Cayenne	French Guiana
974	La Réunion	Saint-Denis	Réunion
976	Mayotte	Mamoudzou	Mayotte 
""".strip()


def get_department_to_region_map():
    r = {}
    for id, department, _, region in [
        i.split('\t') for i in fr_divisions.split('\n')
    ]:
        r[department] = region
    return r


department_to_region_map = get_department_to_region_map()


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
    SOURCE_URL = 'https://github.com/opencovid19-fr/data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'fr_opencovid_fr'

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
                    region_schema = SCHEMA_ADMIN_1 #SCHEMA_FR_DEPARTMENT
                    region_parent = 'FR'  # CHECK ME for overseas territories!!!! ==================================================
                    try:
                        region_child = fr_departments[region_child]
                    except KeyError:
                        region_child = place_map[region_child]
                elif item['granularite'] == 'region':
                    region_schema = SCHEMA_ADMIN_1
                    region_parent = 'France'
                    continue  # HACK: It seems the natural earth geojson files use departments rather than regions!!!
                elif item['granularite'] == 'collectivite-outremer':
                    region_schema = SCHEMA_FR_OVERSEAS_COLLECTIVITY
                    region_parent = None
                    continue  # HACK: Won't support these in this data for now, as most of this info is in the JHU data!! ============================
                elif item['granularite'] == 'monde':
                    # World
                    continue
                else:
                    raise Exception(item['granularite'])

                if confirmed.strip('NaN'):
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=source_url
                    ))

                if deaths.strip('NaN'):
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_DEATHS,
                        value=int(deaths),
                        date_updated=date,
                        source_url=source_url
                    ))

                if icu.strip('NaN'):
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_ICU,
                        value=int(icu),
                        date_updated=date,
                        source_url=source_url
                    ))

                if hospitalized.strip('NaN'):
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_HOSPITALIZED,
                        value=int(hospitalized),
                        date_updated=date,
                        source_url=source_url
                    ))

                if recovered.strip('NaN'):
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=source_url
                    ))

                    if confirmed.strip('NaN'):
                        r.append(DataPoint(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DT_STATUS_ACTIVE,
                            value=int(recovered)-int(confirmed),
                            date_updated=date,
                            source_url=source_url
                        ))

                if confirmed.strip('NaN'):
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
