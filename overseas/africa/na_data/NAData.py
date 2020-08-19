# https://gisserver.nsa.org.na/portal/apps/opsdashboard/index.html#/e8d79f18bd424670b7db99d56866573f
import json
import datetime
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1, DT_TESTS_TOTAL,
    DT_TOTAL, DT_STATUS_RECOVERED,
    DT_STATUS_DEATHS, DT_STATUS_ACTIVE
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class NAData(URLBase):
    SOURCE_URL = 'https://gisserver.nsa.org.na/portal/apps/opsdashboard/index.html#/e8d79f18bd424670b7db99d56866573f'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'na_dash'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'na' / 'data',
            urls_dict={
                'regions.json': URL('https://gisserver.nsa.org.na/server/rest/services/Hosted/covid_19_namibia/FeatureServer/0/query?f=json&where=positive%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultOffset=0&resultRecordCount=500',
                                    static_file=False),
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_regions())
        return r

    def _get_regions(self):
        # {"exceededTransferLimit":false,
        # "features":[{"attributes":
        # {"objectid":1,
        # "region_name":"Zambezi",
        # "region_code":"01",
        # "positive":2,
        # "negative":256,
        # "pending_results":0,
        # "outcome_alive":2,
        # "outcome_dead":0,
        # "recovered":0,
        # "active":2,
        # "mild":2,
        # "severe":0,
        # "globalid":"{7D0B5B96-7091-4163-944B-7A1EB9730543}",
        # "contacts2":39,
        # "critical":0,
        # "total_tested":258,
        # "quarantined":412,
        # "facilities":7}},

        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/regions.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for feature in data['features']:
                attributes = feature['attributes']
                #print(attributes)

                region = {
                    'kavango west': 'NA-KW',
                    '!karas': 'NA-KA',
                }.get(
                    attributes['region_name'].lower(),
                    attributes['region_name']
                )
                positive = attributes['positive']
                num_tests = positive+attributes['negative']
                recovered = attributes['recovered']
                active = attributes['active']
                outcome_dead = attributes['outcome_dead']

                if positive is not None:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='NA',
                        region_child=region,
                        datatype=DT_TOTAL,
                        value=int(positive),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if num_tests is not None:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='NA',
                        region_child=region,
                        datatype=DT_TESTS_TOTAL,
                        value=int(num_tests),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if recovered is not None:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='NA',
                        region_child=region,
                        datatype=DT_STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if active is not None:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='NA',
                        region_child=region,
                        datatype=DT_STATUS_ACTIVE,
                        value=int(active),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if outcome_dead is not None:
                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='NA',
                        region_child=region,
                        datatype=DT_STATUS_DEATHS,
                        value=int(outcome_dead),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(NAData().get_datapoints())