import json
import datetime
from os import listdir

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


DISTRICT_CASE = "https://services6.arcgis.com/MpOjf90wsc96wTq1/arcgis/rest/services/Case/FeatureServer/0/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&&outFields=*"
SUB_DISTRICT_CASE = "https://services6.arcgis.com/MpOjf90wsc96wTq1/arcgis/rest/services/COVID19_Daerah_Mukim_Parlimen_250320/FeatureServer/0/query?f=json&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometry={%22xmin%22%3A0%2C%22ymin%22%3A0%2C%22xmax%22%3A999999999%2C%22ymax%22%3A9999999%2C%22spatialReference%22%3A{%22wkid%22%3A102100}}&outFields=*"


class MYESRIDashData(URLBase):
    # Remember to send e-mail to below link!!! =======================================================================================
    SOURCE_URL = 'https://www.arcgis.com/apps/opsdashboard/index.html#/6520fd7121374686aa35578ffe2d2cb7'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'my_esri_dash'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'my' / 'esri_dash_data',
             urls_dict={
                 'district_case.json': URL(
                     DISTRICT_CASE,
                     static_file=False
                 ),
                 'sub_district_case.json': URL(
                     SUB_DISTRICT_CASE,
                     static_file=False
                 ),
             }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self.get_district_datapoints())
        r.extend(self.get_sub_district_datapoints())
        return r

    def get_district_datapoints(self):
        # {
        #       "attributes": {
        #         "OBJECTID": 1,
        #         "State": 8,
        #         "Last_Update": 1594425600000,
        #         "Latitude": 2.07,
        #         "Logitude": 103.4,
        #         "Confirmed": 750,
        #         "Recovered": 8,
        #         "Deaths": 20,
        #         "GlobalID": "fe673177-c04b-42b3-a93f-b27515f87aa8",
        #         "CreationDate": 1584525341792,
        #         "Creator": "kylo_em",
        #         "EditDate": 1597509951578,
        #         "Editor": "drp_editor",
        #         "Tarikh_Kemaskini": 1585299600000
        #       }
        #     },

        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/district_case.json'

            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            states_map = {
                i['code']: i['name']
                for i in data['fields'][1]['domain']['codedValues']
            }

            for feature in data['features']:
                attributes = feature['attributes']

                #date = datetime.datetime.fromtimestamp(
                #    attributes['EditDate'] / 1000.0
                #).strftime('%Y_%m_%d')
                if attributes['State'] is None:
                    continue  # HACK!

                region_child = states_map[attributes['State']].lower().strip()
                if region_child.startswith('wp '):
                    region_child = region_child[3:]

                confirmed = attributes['Confirmed']
                recovered = attributes['Recovered']
                deaths = attributes['Deaths']

                if confirmed is not None:
                    r.append(DataPoint(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if recovered is not None:
                    r.append(DataPoint(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if deaths is not None:
                    r.append(DataPoint(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if confirmed is not None and recovered is not None:
                    active = confirmed - recovered - (deaths or 0)
                    r.append(DataPoint(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(active),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r

    def get_sub_district_datapoints(self):
        # {
        #         "OBJECTID": 437,
        #         "POLYGON_ID": 703841954,
        #         "AREA_ID": 23288894,
        #         "NM_AREA_ID": 1,
        #         "POLYGON_NM": "Jelebu",
        #         "FEAT_TYPE": "DISTRICT",
        #         "COVID19": 2,
        #         "Zone_Class": "ZON KUNING",
        #         "Shape__Area": 0.110571529552118,
        #         "Shape__Length": 1.88281903151022,
        #         "CreationDate": 1585237810887,
        #         "Creator": "nazmeen_nsesrimy",
        #         "EditDate": 1587551346219,
        #         "Editor": "nazmeen_nsesrimy",
        #         "Negeri": "Negeri Sembilan",
        #         "GlobalID": "4da873b1-fd9f-4dc1-a308-a4353a016ce9",
        #         "Kes_Aktif": 0,
        #         "Kes_Aktif_Zone": "ZON HIJAU"
        #       }

        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/sub_district_case.json'

            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for feature in data['features']:
                attributes = feature['attributes']

                #date = datetime.datetime.fromtimestamp(
                #    attributes['EditDate']/1000.0
                #).strftime('%Y_%m_%d')
                region_child = attributes['POLYGON_NM']

                total = attributes['COVID19']
                active = attributes['Kes_Aktif']

                if total is not None:
                    r.append(DataPoint(
                        region_schema=Schemas.MY_DISTRICT,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(total),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if active is not None:
                    r.append(DataPoint(
                        region_schema=Schemas.MY_DISTRICT,
                        region_parent='MY',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(active),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MYESRIDashData().get_datapoints())
