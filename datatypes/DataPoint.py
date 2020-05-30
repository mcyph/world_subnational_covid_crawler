import csv
import unidecode
from collections import namedtuple

from covid_19_au_grab.datatypes.constants import SCHEMA_ADMIN_0, SCHEMA_ADMIN_1, name_to_schema, schema_to_name
from covid_19_au_grab.other_data.iso_3166_1 import iso_3166_data
from covid_19_au_grab.other_data.iso_3166_2 import iso_3166_2_data
from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.datatypes.SchemaTypeInfo import get_schema_type_info


def _get_mappings_to_iso_3166():
    r = {}

    with open(get_package_dir() / 'datatypes' / 'schema_mappings.csv',
              'r', encoding='utf-8') as f:
        for item in csv.DictReader(f, delimiter='\t'):
            r[name_to_schema(item['original_schema']), item['original_parent'], item['original_child']] = (
                name_to_schema(item['schema']), item['parent'], item['child']
            )

    return r


_mappings_to_iso_3166 = _get_mappings_to_iso_3166()


def DataPoint(region_parent=None,
              region_schema=SCHEMA_ADMIN_1,
              datatype=None,
              agerange=None,
              region_child=None,
              value=None,
              date_updated=None,
              source_url=None,
              text_match=None):
    """
    A hackish wrapper around DataPoint,
    adding some validation and default
    arguments for this `namedtuple`.
    """

    assert datatype is not None
    region_parent = region_parent or ''
    agerange = agerange or ''
    region_child = region_child or ''
    assert date_updated
    assert source_url
    assert value is not None
    text_match = text_match or ''

    # Convert regions to ISO-3166-1/2 if possible
    if (region_schema, region_parent, region_child) in _mappings_to_iso_3166:
        region_schema, region_parent, region_child = \
            _mappings_to_iso_3166[region_schema, region_parent, region_child]

    region_parent, region_child = get_schema_type_info(
        region_schema
    ).convert_parent_child(region_parent, region_child)

    return _DataPoint(
        region_parent, region_schema, datatype,
        agerange, region_child, value,
        date_updated, source_url, text_match
    )


_DataPoint = namedtuple('DataPoint', [
    'region_parent',
    'region_schema',
    'datatype',
    'agerange',
    'region_child',
    'value',
    'date_updated',
    # The URL where the info came from
    'source_url',
    # The text which matched this (the x,y range and text itself)
    'text_match'
])
