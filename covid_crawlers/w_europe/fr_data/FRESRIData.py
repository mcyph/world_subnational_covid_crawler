# https://mapthenews.maps.arcgis.com/home/item.html?id=45b99aa511cf444695bd1574daf33ea2&sublayer=0
# https://www.arcorama.fr/2020/05/reutiliser-les-donnees-de-notre-tableau.html

import json
from os import listdir
from datetime import timedelta, date
from collections import Counter, defaultdict

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DatapointMerger import DataPointMerger
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT


class FRESRIData(URLBase):
    SOURCE_URL = 'https://www.arcgis.com/apps/opsdashboard/index.html#/80d409fa3b6e4c52b095cb8f56074c41'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'fr_esri_france'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'fr' / 'esridata',
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
        r = {}

        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        start_date = date.today() - timedelta(days=14)
        #start_date = date(2020, 3, 18)
        end_date = date.today()

        for single_date in daterange(start_date, end_date):
            url = (
                'https://services1.arcgis.com/5PzxEwuu4GtMhqQ6/arcgis/rest/services/Synthese_Covid19_France/FeatureServer/0/query?'
                'f=json&'
                f'where=(OBJECTID%20%3E%200)%20AND%20(Jour=%27{single_date.strftime("%d/%m/%Y")}%27)&'
                'returnGeometry=false&'
                'spatialRel=esriSpatialRelIntersects&'
                'maxAllowableOffset=2445&'
                'geometryType=esriGeometryEnvelope&inSR=102100&'
                'outFields=*&outSR=102100&'
                'resultType=tile'
            )
            r[f'data_{single_date.strftime("%Y_%m_%d")}.json'] = URL(url, False)

        return r

    def get_datapoints(self):
        r = DataPointMerger()
        totals = Counter()
        added_totals = defaultdict(set)
        tests = Counter()
        added_tests = defaultdict(set)

        for date in sorted(listdir(get_overseas_dir() / 'fr' / 'esridata')):
            r.extend(self._get_positive_by_department(date, totals, added_totals, tests, added_tests))
        return r

    def _get_positive_by_department(self, date,
                                    totals, added_totals,
                                    tests, added_tests):
        out = DataPointMerger()
        base_path = get_overseas_dir() / 'fr' / 'esridata' / date

        for fnam in sorted(listdir(base_path)):
            r = self.sdpf()
            with open(base_path / fnam, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                print(base_path, fnam, data)

            for property in data['features']:
                attributes = property['attributes']
                print(property)

                date = self.convert_date(attributes['Jour'])
                try:
                    region_child = 'FR-%02d' % int(attributes['CODE_DEPT'])
                except ValueError:
                    # e.g. 2A
                    region_child = 'FR-%s' % attributes['CODE_DEPT']

                for datatype, value in (
                    (DataTypes.STATUS_HOSPITALIZED, attributes['Hospitalisation_T']),
                    #(DataTypes.FIXME, attributes['Hospitalisation_H']),
                    #(DataTypes.FIXME, attributes['Hospitalisation_F']),
                    (DataTypes.STATUS_ICU, attributes['Reanimation_T']),
                    #(DataTypes.FIXME, attributes['Reanimation_H']),
                    #(DataTypes.FIXME, attributes['Reanimation_F']),
                    (DataTypes.STATUS_DEATHS, attributes['Deces_T']),
                    #(DataTypes.FIXME, attributes['Deces_H']),
                    #(DataTypes.FIXME, attributes['Deces_F']),
                    (DataTypes.NEW, attributes['Tests_Viro_P']),
                    #(DataTypes.TESTS_TOTAL, attributes['Tests_Viro_T'])  # FIXME: This is new tests!
                ):
                    if value is None:
                        continue

                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='FR',
                        region_child=region_child,
                        datatype=datatype,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                # I don't think Nbre_Cas_Confirmes is ever not None
                assert attributes['Nbre_Cas_Confirmes'] is None, attributes

                if attributes['Tests_Viro_P'] and not date in added_totals[region_child]:
                    added_totals[region_child].add(date)
                    totals[region_child] += attributes['Tests_Viro_P']# or attributes['Nbre_Cas_Confirmes'])

                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='FR',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=totals[region_child],
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if attributes['Tests_Viro_T'] and not date in added_tests[region_child]:
                    added_tests[region_child].add(date)
                    tests[region_child] += attributes['Tests_Viro_T']

                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='FR',
                        region_child=region_child,
                        datatype=DataTypes.TESTS_TOTAL,
                        value=tests[region_child],
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

            out.extend(r)
        return out


if __name__ == '__main__':
    from pprint import pprint
    pprint(FRESRIData().get_datapoints())
