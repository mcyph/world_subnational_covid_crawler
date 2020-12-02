# http://sam.lrv.lt/lt/naujienos/koronavirusas
# https://registrucentras.maps.arcgis.com/apps/opsdashboard/index.html#/becd01f2fade4149ba7a9e5baaddcd8d

import json
import datetime
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.DatapointMerger import DataPointMerger


DATA_URL = 'https://maps.registrucentras.lt/arcgis/rest/services/covid/savivaldybes/FeatureServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A2504688.542843003%2C%22ymin%22%3A5009377.085700966%2C%22xmax%22%3A5009377.08569099%2C%22ymax%22%3A7514065.628548957%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4891.96981024998%2C%22extent%22%3A%7B%22xmin%22%3A306507.4031%2C%22ymin%22%3A5973291.0439%2C%22xmax%22%3A680103.2769%2C%22ymax%22%3A6257813.452%2C%22spatialReference%22%3A%7B%22wkid%22%3A2600%2C%22latestWkid%22%3A3346%7D%7D%7D&callback=dojo_request_script_callbacks.dojo_request_script57'


county_map = {
    'Tauragės apskr.': 'LT-TA',
    'Vilniaus apskr.': 'LT-VL',
    'Kauno apskr.': 'LT-KU',
    'Alytaus apskr.': 'LT-AL',
    'Telšių apskr.': 'LT-TE',
    'Utenos apskr.': 'LT-UT',
    'Marijampolės apskr.': 'LT-MR',
    'Panevėžio apskr.': 'LT-PN',
    'Šiaulių apskr.': 'LT-SA',
}


class LTData(URLBase):
    SOURCE_URL = 'https://registrucentras.maps.arcgis.com/apps/opsdashboard/index.html#/becd01f2fade4149ba7a9e5baaddcd8d'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'lt_dash'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'lt' / 'data',
            urls_dict={
                'regions_data.json': URL(DATA_URL, static_file=False),
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_regions_data())
        return r

    def _get_regions_data(self):
        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()
            path = f'{base_dir}/{date}/regions_data.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read().replace('dojo_request_script_callbacks.dojo_request_script57(', '').rstrip().rstrip(');')
                data = json.loads(data)

            for feature in data['features']:
                attributes = feature['attributes']
                #print(attributes)

                # Only confirmed and deaths are shown in the dashboard
                date = datetime.datetime.fromtimestamp(
                    attributes['ATNUJINTA'] / 1000
                ).strftime('%Y_%m_%d')
                region_parent = 'LT'  #county_map[attributes['APSKRITIS']]  #  NOTE ME: Not sure it's worth splitting for now, but can map to admin_1
                region_child = attributes['SAV_PAV'].replace(' r.', '').replace(' m.', '')
                confirmed = attributes['ATVEJAI']
                deaths = attributes['MIRTYS_KITA']
                positive = attributes['VYRAI']
                recovered = attributes['PASVEIKO']
                women = attributes['MOTERYS']
                men = attributes['VYRAI']
                treated = attributes['GYDOMA']
                unknown = attributes['MIRE']

                if confirmed is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if positive is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.CONFIRMED,
                        value=int(positive),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if women is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.TOTAL_FEMALE,
                        value=int(women),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if men is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.TOTAL_MALE,
                        value=int(men),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if deaths is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if recovered is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if recovered is not None and confirmed is not None and deaths is not None:
                    r.append(
                        region_schema=Schemas.LT_MUNICIPALITY,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(confirmed)-int(recovered)-int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

            out.extend(r)
        return out


if __name__ == '__main__':
    from pprint import pprint
    pprint(LTData().get_datapoints())
