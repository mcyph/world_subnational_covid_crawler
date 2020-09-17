import json
from os import makedirs, listdir
from os.path import exists
from urllib.request import urlretrieve
from datetime import datetime, timedelta

from covid_19_au_grab.get_package_dir import get_data_dir
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


# https://dhhs.carto.com/datasets
# https://dhhs.carto.com:443/api/v2/sql?q=select * from public.covid19_postcodes
SOURCE_URL = 'https://www.dhhs.vic.gov.au/victorian-coronavirus-covid-19-data'


def get_vic_carto_datapoints():
    # [{"postcode": 3006, "_new": 0, "activedisp": "Five or fewer active cases",
    # "cases": 65, "ratedisp": 13, "population": 18811},
    #
    # {"rows":[{"cartodb_id":287,
    # "the_geom":"0101000020E6100000386744696F226240E10B93A982E942C0",
    # "the_geom_webmercator":"0101000020110F00008D3881B2A4CD6E41295C51BCE25F51C1",
    # "postcode":3126,"affected":0,"band":"None","lat":-37.8243,"lon":145.0761,
    # "suburbs":"Camberwell East, Canterbury","active":0,"rate":0,"total":2},

    date = (datetime.now() - timedelta(hours=20, minutes=30)).strftime('%Y_%m_%d')
    dir_ = get_data_dir() / 'vic' / 'newmap_postcode' / date
    if not exists(dir_):
        makedirs(dir_)

    postcode_json_path = dir_ / 'postcode.json'
    if not exists(postcode_json_path):
        urlretrieve("https://dhhs.carto.com:443/api/v2/sql?q=select%20*%20from%20public.covid19_postcodes", postcode_json_path)

    r = DataPointMerger()
    dates = sorted(listdir(get_data_dir() / 'vic' / 'newmap_postcode'))
    if not date in dates:
        dates.append(date)

    for i_date in dates:
        path = get_data_dir() / 'vic' / 'newmap_postcode' / i_date / 'postcode.json'
        r.extend(_get_datapoints(i_date, path))
    return r


def _get_datapoints(date, path):
    r = []

    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

        if isinstance(data, list):
            for row in data:
                for datatype, value in (
                    (DataTypes.STATUS_ACTIVE, row['activedisp']),
                    (DataTypes.TOTAL, row['cases'])
                ):
                    if value == 'Five or fewer active cases':
                        continue

                    r.append(DataPoint(
                        region_schema=Schemas.POSTCODE,
                        region_parent='AU-VIC',
                        region_child=str(row['postcode']),
                        datatype=datatype,
                        value=int(value),
                        date_updated=date,
                        source_url=SOURCE_URL
                    ))
        else:
            for row in data['rows']:
                for datatype, value in (
                    (DataTypes.STATUS_ACTIVE, row['active']),
                    (DataTypes.TOTAL, row['total'])
                ):
                    r.append(DataPoint(
                        region_schema=Schemas.POSTCODE,
                        region_parent='AU-VIC',
                        region_child=str(row['postcode']),
                        datatype=datatype,
                        value=int(value),
                        date_updated=date,
                        source_url=SOURCE_URL
                    ))

    return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_vic_carto_datapoints())
