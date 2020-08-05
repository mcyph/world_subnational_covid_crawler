import json
import zipfile

from covid_19_au_grab.db.SQLiteDataRevision import \
    SQLiteDataRevision
from covid_19_au_grab.datatypes.TimeSeriesDataPoints import \
    TimeSeriesDataPoints
from covid_19_au_grab.datatypes.constants import (
    schema_to_name,
)
from covid_19_au_grab.datatypes.schema_types import schema_types
from covid_19_au_grab.datatypes.OutputSchemaTypes import OutputSchemaTypes


def output_revision_datapoints_to_zip(zip_buffer, rev_date=None, rev_subid=None):
    return _TimeSeriesDataZipper().output_revision_datapoints_to_zip(
        zip_buffer, rev_date, rev_subid
    )


class _TimeSeriesDataZipper:
    def output_revision_datapoints_to_zip(self, zip_buffer, rev_date=None, rev_subid=None):
        r = {}
        inst = SQLiteDataRevision(rev_date, rev_subid)

        for region_schema in inst.get_region_schemas():
            region_schema_str = schema_to_name(region_schema)
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

                    k = f'{region_schema_str}_{region_parent.lower()}'
                    assert not k in r, k
                    r[k] = tsdp.get_compressed_data(thin_out=False)  # FIXME: Thinning out can have consequences!!!
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
                    thin_out=False)  # FIXME: Thinning out can have consequences!!!

        for k in r:
            assert k.lower() == k, k

        # Output the schema types information
        # TODO: Add geojson data (+later underlay data too?)
        r['schema_types'] = OutputSchemaTypes(
            listings={
                'case_data_listing': list(r.keys()),
            },
            time_format=rev_date,
            revision_id=rev_subid
        ).get_schema_types()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, data in r.items():
                zip_file.writestr(
                    file_name + '.json',
                    json.dumps(
                        data,
                        separators=(',', ':'),
                        ensure_ascii=False
                    ).encode('utf-8')
                )
