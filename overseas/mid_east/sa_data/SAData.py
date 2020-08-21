import csv
import json
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class SAData(URLBase):
    SOURCE_URL = 'https://covid19.moh.gov.sa/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'sa_gov'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'sa' / 'data',
             urls_dict={
                 'recovered_sum.json': URL('https://services6.arcgis.com/bKYAIlQgwHslVRaK/arcgis/rest/services/VWPlacesUniqueWithStatistics/FeatureServer/1/query?f=json&where=Recovered_SUM%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Recovered_SUM%20desc&outSR=102100&resultOffset=0&resultRecordCount=1000&resultType=standard&cacheHint=true',
                                   static_file=False),
                 'tested_sum.json': URL('https://services6.arcgis.com/bKYAIlQgwHslVRaK/arcgis/rest/services/VWPlacesUniqueWithStatistics01/FeatureServer/1/query?f=json&where=Tested_SUM%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Tested_SUM%20desc&outSR=102100&resultOffset=0&resultRecordCount=1000&resultType=standard&cacheHint=true',
                                      static_file=False),
                 'confirmed_sum.json': URL('https://services6.arcgis.com/bKYAIlQgwHslVRaK/arcgis/rest/services/VWPlacesUniqueWithStatistics/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed_SUM%20desc&outSR=102100&resultOffset=0&resultRecordCount=1000&resultType=standard&cacheHint=true',
                                 static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        r.extend(self._get_tested_sum())
        #r.extend(self._get_confirmed_sum())
        return r

    def _get_recovered_sum(self):
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/recovered_sum.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            confirmed = Counter()
            deaths = Counter()
            recovered = Counter()

            for feature in data['features']:
                # "features":[{"attributes":{"PlaceName_AR":"الرياض","PlaceName_EN":"AR RIYAD",
                # "GovernorateName_AR":"الرياض (مقر الامارة)","GovernorateName_EN":"Ar Riyad",
                # "RegionName_AR":"الرياض","RegionName_EN":"Ar Riyad","PLC_CODE":"C531G10R01",
                # "REG_CODE":"R01","GOV_CODE":"G10R01","Place_Category":"City",
                # "DataSource":"GCS","GlobalID":"296ee29a-b190-4064-a3c5-cdd778046ab2",
                # "Place_Code":"C531G10R01","Join_Count":80,"Confirmed_SUM":20039,
                # "Deaths_SUM":30,"Recovered_SUM":13468,"ObjectId":46}}

                attributes = feature['attributes']
                confirmed[attributes['RegionName_EN']] += int(attributes['Confirmed_SUM'])
                deaths[attributes['RegionName_EN']] += int(attributes['Deaths_SUM'])
                recovered[attributes['RegionName_EN']] += int(attributes['Recovered_SUM'])

            for region_child, value in confirmed.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            for region_child, value in deaths.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            for region_child, value in recovered.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_tested_sum(self):
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/tested_sum.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            tested = Counter()

            for feature in data['features']:
                # {"attributes":{"PlaceName_AR":"الرياض","PlaceName_EN":"AR RIYAD",
                # "GovernorateName_AR":"الرياض (مقر الامارة)","GovernorateName_EN":"Ar Riyad",
                # "RegionName_AR":"الرياض","RegionName_EN":"Ar Riyad","PLC_CODE":"C531G10R01",
                # "REG_CODE":"R01","GOV_CODE":"G10R01","Place_Category":"City",
                # "DataSource":"GCS","GlobalID":"296ee29a-b190-4064-a3c5-cdd778046ab2",
                # "Place_Code":"C531G10R01","Join_Count":80,"Confirmed_SUM":20039,
                # "Deaths_SUM":30,"Recovered_SUM":13468,"Tested_SUM":6541,"ObjectId":46}}
                print(feature)

                attributes = feature['attributes']
                tested[attributes['RegionName_EN']] += int(attributes['Tested_SUM'])

            for region_child, value in tested.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.TESTS_TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_confirmed_sum(self):
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/confirmed_sum.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            confirmed = Counter()
            deaths = Counter()
            recovered = Counter()

            for feature in data['features']:
                # "features":[{"attributes":{"PlaceName_AR":"الرياض","PlaceName_EN":"AR RIYAD",
                # "GovernorateName_AR":"الرياض (مقر الامارة)","GovernorateName_EN":"Ar Riyad",
                # "RegionName_AR":"الرياض","RegionName_EN":"Ar Riyad","PLC_CODE":"C531G10R01",
                # "REG_CODE":"R01","GOV_CODE":"G10R01","Place_Category":"City",
                # "DataSource":"GCS","GlobalID":"296ee29a-b190-4064-a3c5-cdd778046ab2",
                # "Place_Code":"C531G10R01","Join_Count":80,"Confirmed_SUM":20039,
                # "Deaths_SUM":30,"Recovered_SUM":13468,"ObjectId":46}}

                attributes = feature['attributes']
                confirmed[attributes['RegionName_EN']] += int(attributes['Confirmed_SUM'])
                deaths[attributes['RegionName_EN']] += int(attributes['Deaths_SUM'])
                recovered[attributes['RegionName_EN']] += int(attributes['Recovered_SUM'])

            for region_child, value in confirmed.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            for region_child, value in deaths.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            for region_child, value in recovered.items():
                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Saudi Arabia',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(SAData().get_datapoints())
