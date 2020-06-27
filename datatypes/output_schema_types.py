import json
from os import listdir
from os.path import expanduser
from covid_19_au_grab.get_package_dir import get_package_dir


def __get_boundary(geodata):
    min_lng = 9999999999999999
    min_lat = 9999999999999999
    max_lng = -99999999999999999
    max_lat = -99999999999999999

    for lng1, lat1, lng2, lat2 in geodata:
        if lng1 < min_lng: min_lng = lng1
        if lng2 < min_lng: min_lng = lng2

        if lat1 < min_lat: min_lat = lat1
        if lat2 < min_lat: min_lat = lat2

        if lng1 > max_lng: max_lng = lng1
        if lng2 > max_lng: max_lng = lng2

        if lat1 > max_lat: max_lat = lat1
        if lat2 > max_lat: max_lat = lat2

    return min_lng, min_lat, max_lng, max_lat


def get_boundaries():
    r = {}
    dir_ = get_package_dir() / 'geojson_data' / 'output'

    for fnam in listdir(dir_):
        if not (fnam == 'admin_0.geojson' or fnam.startswith('admin_1')):
            continue

        with open(dir_ / fnam, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        for schema, schema_dict in data.items():
            for region_parent, region_parent_dict in schema_dict.items():
                for region_child, region_child_item in region_parent_dict.items():
                    #print(region_child_item)
                    r[region_child.lower()] = __get_boundary([i[1] for i in region_child_item['geodata']])

    return r


def get_underlay_key():
    return {'absData.json': []}  # HACK!


def get_listings():
    def r(l):
        return [i for i in l if not i.startswith('.') and 'json' in i]

    return {
        'case_data_listing': r(listdir(expanduser('~/dev/pull_req/covid-19-au.github.io/src/data/caseData'))),
        'geo_json_data_listing': r(listdir(expanduser('~/dev/pull_req/covid-19-au.github.io/src/data/geoJSONData'))),
        'underlay_data_listing': r(listdir(expanduser('~/dev/pull_req/covid-19-au.github.io/src/data/underlayData')))
    }


with open('schema_types.json', 'r', encoding='utf-8') as f:
    data = f.read()
    schema_types = json.loads(data)

    schema_types['underlays'] = get_underlay_key()
    schema_types['boundaries'] = get_boundaries()
    schema_types['listings'] = get_listings()

    for schema, schema_dict in schema_types['schemas'].items():
        if schema_dict['iso_3166']:
            schema_dict['iso_3166'] = schema_dict['iso_3166'].lower()


with open('schema_types_out.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(schema_types,
                       ensure_ascii=False,
                       indent=4))
