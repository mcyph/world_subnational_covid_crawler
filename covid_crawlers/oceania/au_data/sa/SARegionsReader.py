import json
import datetime
from os import listdir

from _utility.URLArchiver import URLArchiver
from _utility.cache_by_date import cache_by_date
from _utility.get_package_dir import get_data_dir
from covid_db.datatypes.DataPoint import DataPoint
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DatapointMerger import DataPointMerger


SA_MAP_DIR = get_data_dir() / 'sa' / 'custom_map'


class SARegionsReader:
    SOURCE_ID = 'au_sa_dashmap'
    SOURCE_URL = 'https://www.covid-19.sa.gov.au/home/dashboard'
    SOURCE_DESCRIPTION = ''

    def get_datapoints(self):
        SA_DASH_JSON_URL = 'https://www.covid-19.sa.gov.au/__data/assets/' \
                           'file/0004/145849/covid_19_daily.json'
        ua = URLArchiver(f'sa/dashboard')
        ua.get_url_data(SA_DASH_JSON_URL, cache=False)

        r = []
        dpm = DataPointMerger()
        for sub_dir in sorted(listdir(SA_MAP_DIR)):
            joined_dir = f'{SA_MAP_DIR}/{sub_dir}'
            r.extend(self._get_data(joined_dir, dpm))
        return r

    @cache_by_date(source_id=SOURCE_ID, validate_date=False)  # NOTE ME!!
    def _get_data(self, joined_dir, dpm):
        r = []

        for fnam in listdir(joined_dir):
            with open(f'{joined_dir}/{fnam}', 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for feature_dict in data.get('features', []):
                """
                {
                    {
                      "exceededTransferLimit": false,
                      "features": [
                        {
                          "attributes": {
                            "objectid": 52,
                            "lga_code18": "49399",
                            "lga_name18": "Unincorporated SA",
                            "ste_code16": "4",
                            "ste_name16": "South Australia",
                            "areasqkm18": 622489.4848,
                            "lga": 49399.0,
                            "lga_name": "Unincorporated SA",
                            "lga_code": 49399,
                            "date_time_20200401_1000": "1/4/2020 @ 10:00 am",
                            "positive_20200401_1000": 0,
                            "active_20200401_1000": 0,
                            "date_time_20200402_0000": "2/4/2020",
                            "positive_20200402_0000": 0,
                            "active_20200402_0000": 0,
                            ...
                          },
                          "geometry": {
                            "rings": [
                              [
                                }
                """

                #print(feature_dict)
                attributes = feature_dict['attributes']
                if attributes.get('exceedslimit'):
                    continue

                for k, v in attributes.items():
                    if k.startswith('positive'):
                        du = datetime.datetime.strptime(
                            k.split('_')[1], '%Y%m%d'
                        ).strftime('%Y_%m_%d')
                        if du == '2020_04_12':
                            # HACK: Ignore this unreliable datapoint!
                            continue
                        elif v is None:
                            continue

                        num = DataPoint(
                            region_schema=Schemas.LGA,
                            region_parent='AU-SA',
                            region_child=attributes['lga_name'].split('(')[0].strip(),
                            datatype=DataTypes.TOTAL,
                            value=int(v),
                            date_updated=du,
                            source_url=self.SOURCE_URL,
                            source_id=self.SOURCE_ID
                        )
                        dpm.append(num, r)
                    elif k.startswith('active'):
                        du = datetime.datetime.strptime(
                            k.split('_')[1], '%Y%m%d'
                        ).strftime('%Y_%m_%d')
                        if du == '2020_04_12':
                            # HACK: Ignore this unreliable datapoint!
                            continue
                        elif du <= '2020_04_15' and not int(v):
                            # HACK: early datapoints were of very low quality!
                            continue
                        elif v is None:
                            continue

                        num = DataPoint(
                            region_schema=Schemas.LGA,
                            region_parent='AU-SA',
                            region_child=attributes['lga_name'].split('(')[0].strip(),
                            datatype=DataTypes.STATUS_ACTIVE,
                            value=int(v),
                            date_updated=du,
                            source_url=self.SOURCE_URL,
                            source_id=self.SOURCE_ID
                        )
                        dpm.append(num, r)

        return r


if __name__ == '__main__':
    from pprint import pprint
    dp = SARegionsReader().get_datapoints()
    pprint(dp)
