import json
import gzip
import msgpack
import brotli
import zipfile
from os import listdir

from covid_19_au_grab._utility.get_package_dir import get_package_dir
from covid_19_au_grab.covid_db.datatypes.schema_types import schema_types
from covid_19_au_grab.covid_db.SQLiteDataRevision import SQLiteDataRevision
from covid_19_au_grab.covid_db.output_compressor.OutputSchemaTypes import OutputSchemaTypes
from covid_19_au_grab.covid_db.output_compressor.TimeSeriesDataPoints import TimeSeriesDataPoints
from covid_19_au_grab.world_geodata.get_population_map import get_population_map


def output_revision_datapoints_to_zip(zip_buffer, rev_date=None, rev_subid=None):
    return _TimeSeriesDataZipper().output_revision_datapoints_to_zip(
        zip_buffer, rev_date, rev_subid
    )


USE_MSGPACK = False
GEOJSON_DIR = get_package_dir() / 'world_geodata' / 'output'


class _TimeSeriesDataZipper:
    def __init__(self):
        self._population_map = get_population_map()

    def output_revision_datapoints_to_zip(self, zip_buffer, rev_date=None, rev_subid=None):
        r = {}
        r.update(self._get_revision_datapoints(rev_date, rev_subid))
        r.update(self._get_geojson_data())

        # Output the schema types information
        # TODO: Add geojson data (+later underlay data too?)
        r['schema_types'] = OutputSchemaTypes(
            listings={
                'case_data_listing': [
                    i.split('/')[-1]
                    for i in r.keys()
                    if 'case_data/' in i
                ],
                'geo_data_listing': [
                    i.split('/')[-1]
                    for i in r.keys()
                    if 'geo_data/' in i
                ]
            },
            # Add listing so can know which datatypes
            # are supplied in which case data files
            updated_dates_by_datatype={ # case_data_datatypes
                k.split('/')[-1]: v['updated_dates_by_datatype']
                for k, v in r.items()
                if 'case_data/' in k
            },
            time_format=rev_date,
            revision_id=rev_subid
        ).get_schema_types()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, data in r.items():
                if USE_MSGPACK:
                    json_data = msgpack.dumps(
                        data, use_single_float=True
                    )
                else:
                    json_data = json.dumps(
                        data, separators=(',', ':'), ensure_ascii=False
                    ).encode('utf-8')

                # Add uncompressed
                zip_file.writestr(file_name + '.json', json_data)

                # Add gzipped
                zip_file.writestr(
                    file_name + '.json.gz',
                    gzip.compress(json_data, compresslevel=9)
                )

                # Add brotli
                zip_file.writestr(
                    file_name + '.json.br',
                    brotli.compress(json_data, quality=11)
                )

    def _get_geojson_data(self):
        r = {}
        for fnam in listdir(GEOJSON_DIR):
            if fnam.endswith('.json'):
                with open(GEOJSON_DIR / fnam, 'r', encoding='utf-8') as f:
                    geojson = json.loads(f.read())
                    self.__compress_geojson_in_place(geojson)
                    r[f"geo_data/{fnam.replace('.json', '')}"] = geojson
        return r

    def __compress_geojson_in_place(self, geojson):

        for region_schema, region_schema_dict in geojson.items():
            for region_parent, region_parent_dict in region_schema_dict.items():
                for region_child, region_child_dict in region_parent_dict.items():

                    for feature in region_child_dict['geodata']:
                        # Convert e.g. [[144.543, -33.5], ...] to
                        # [144543, ...], [-33500, ...] to reduce bandwidth

                        feature[1] = [round(i * 1000) for i in feature[1]]
                        feature[2] = [round(i * 1000) for i in feature[2]]

                        for poly in feature[3]:
                            out_long = []
                            out_lat = []

                            for long, lat in poly:
                                out_long.append(round(long*1000))
                                out_lat.append(round(lat*1000))

                            poly[:] = [out_long, out_lat]

                    # Remove everything but English to save space (for now)
                    #region_child_dict['label'] = {
                    #    'en': region_child_dict['label'].get('en')
                    #}

                    # Add population info
                    region_child_dict['population'] = \
                        self._population_map.get((region_schema, region_parent, region_child))

    def _get_revision_datapoints(self, rev_date, rev_subid):
        r = {}
        inst = SQLiteDataRevision(rev_date, rev_subid)

        for region_schema in inst.get_region_schemas():
            print("Getting revision datapoints for zip:", region_schema.value)
            region_schema_str = region_schema.value
            region_dict = schema_types['schemas'][region_schema_str]

            if region_dict['split_by_parent_region']:
                # Split into different json files for each region parent
                datatypes = inst.get_datatypes_by_region_schema(region_schema)

                for region_parent in inst.get_region_parents(region_schema):
                    tsdp = TimeSeriesDataPoints(region_schema)

                    for (region_child, agerange), date_updated_dict in inst.get_time_series(
                            datatypes, region_schema, region_parent,
                            region_child=None
                    ).items():
                        for date_updated, datapoints in date_updated_dict.items():
                            for datapoint in datapoints:
                                tsdp.add_datapoint(datapoint)

                    k = f'case_data/{region_schema_str}_{region_parent.lower()}'
                    assert not k in r, k
                    r[k] = tsdp.get_compressed_data(thin_out=True)  # FIXME: Thinning out can have consequences!!!
            else:
                # Put everything for a region schema in one json file
                tsdp = TimeSeriesDataPoints(region_schema)
                datatypes = inst.get_datatypes_by_region_schema(region_schema)

                for region_parent in inst.get_region_parents(region_schema):
                    for (region_child, agerange), date_updated_dict in inst.get_time_series(
                            datatypes, region_schema, region_parent,
                            region_child=None
                    ).items():
                        for date_updated, datapoints in date_updated_dict.items():
                            for datapoint in datapoints:
                                tsdp.add_datapoint(datapoint)

                assert not region_schema_str in r, region_schema_str
                r[f'case_data/{region_schema_str}'] = tsdp.get_compressed_data(
                    thin_out=True)  # FIXME: Thinning out can have consequences!!!

        for k in r:
            assert k.lower() == k, k

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(_TimeSeriesDataZipper()._get_geojson_data())
