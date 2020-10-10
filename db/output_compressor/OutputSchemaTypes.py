import json

from os import listdir
from os.path import expanduser
from covid_19_au_grab.get_package_dir import get_package_dir


class OutputSchemaTypes:
    def __init__(self, listings=None, time_format=None, revision_id=None,
                 updated_dates_by_datatype=None):

        self.listings = listings
        self.time_format = time_format
        self.revision_id = revision_id
        self.updated_dates_by_datatype = updated_dates_by_datatype

    def get_schema_types(self):
        """

        """
        with open(get_package_dir() / 'datatypes' / 'schema_types.json',
                  'r', encoding='utf-8') as f:

            data = f.read()
            schema_types = json.loads(data)

            schema_types['underlays'] = self.__get_underlay_key()
            schema_types['boundaries'] = self.__get_boundaries()
            schema_types['listings'] = self.__get_listings()
            schema_types['updated_dates_by_datatype'] = self.updated_dates_by_datatype

            for schema, schema_dict in schema_types['schemas'].items():
                if schema_dict['iso_3166']:
                    schema_dict['iso_3166'] = schema_dict['iso_3166'].lower()

            schema_types['output_path'] = f'{self.time_format}-{self.revision_id}'

        return schema_types

    #=======================================================================#
    #                     Get GeoJSON boundary coordinates                  #
    #=======================================================================#

    def __get_boundaries(self):
        """

        """
        r = {}
        dir_ = get_package_dir() / 'geojson_data' / 'output'

        for fnam in listdir(dir_):
            if not (fnam == 'admin_0.json' or fnam.startswith('admin_1')):
                continue

            with open(dir_ / fnam, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for schema, schema_dict in data.items():
                for region_parent, region_parent_dict in schema_dict.items():
                    for region_child, region_child_item in region_parent_dict.items():
                        #print(region_child_item)
                        r[region_child.lower()] = self.__get_boundary([i[1] for i in region_child_item['geodata']])

        return r

    def __get_boundary(self, geodata):
        """

        """
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

        return round(min_lng*10), round(min_lat*10), round(max_lng*10), round(max_lat*10)

    #=======================================================================#
    #                      Get underlay <select> options                    #
    #=======================================================================#

    def __get_underlay_key(self):
        """

        """
        return {
            'absData.json': []
        }  # HACK!

    #=======================================================================#
    #                         Get JSON file listings                        #
    #=======================================================================#

    def __get_listings(self):
        """

        """
        listings = self.listings or {}

        def do_listdir(dir_):
            return [
                i.replace('.json', '')
                for i in listdir(expanduser(dir_))
                if (not i.startswith('.') and 'json' in i)
            ]

        for k, v in {
            #'case_data_listing': do_listdir(
            #    '~/dev/pull_req/covid-19-au.github.io/src/data/caseData'
            #),
            #'geo_json_data_listing': do_listdir(
            #    '~/dev/pull_req/covid-19-au.github.io/src/data/geoJSONData'
            #),
            'underlay_data_listing': do_listdir(
                '~/dev/pull_req/covid-19-au.github.io/src/data/underlayData'
            )
        }.items():
            # Allow for combining
            if not k in listings:
                listings[k] = v

        return listings

    #=======================================================================#
    #                    Get case data listing details                      #
    #=======================================================================#

    def __get_case_listing(self):
        """
        TODO: Return -> {
            "":
            "filename": [
                bit flag 1 (no age or region),
                bit flag 2 (age but no region parent),
                bit flag 3 (no age but region parent),
                bit flag 4 (age and region parent)
            ],
            "datatype_bitflags": {
                1: ...,
                2: ...,
                ...
            }
        }

        There will be a single bit for each datatype for
        different combinations.

        A region parent equal to the parent in the schema is
        treated as no parent.
        """
        pass


if __name__ == '__main__':
    with open('../../datatypes/schema_types_out.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(
            OutputSchemaTypes().get_schema_types(),
            ensure_ascii=False,
            indent=4
        ))
