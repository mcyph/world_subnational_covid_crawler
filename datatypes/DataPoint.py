import csv
import unidecode
from collections import namedtuple

from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.other_data.iso_3166_1 import iso_3166_data
from covid_19_au_grab.other_data.iso_3166_2 import iso_3166_2_data
from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.datatypes.SchemaTypeInfo import get_schema_type_info
from covid_19_au_grab.geojson_data.LabelsToRegionChild import LabelsToRegionChild


def _get_mappings_to_iso_3166():
    r = {}

    with open(get_package_dir() / 'datatypes' / 'schema_mappings.csv',
              'r', encoding='utf-8') as f:
        for item in csv.DictReader(f, delimiter='\t'):
            r[Schemas(item['original_schema'].strip()), item['original_parent'].strip(), item['original_child'].strip()] = (
                Schemas(item['schema'].strip()), item['parent'].strip(), item['child'].strip()
            )

    return r


_mappings_to_iso_3166 = _get_mappings_to_iso_3166()
_labels_to_region_child = LabelsToRegionChild()


def DataPoint(region_schema=Schemas.ADMIN_1,
              region_parent=None,
              region_child=None,

              date_updated=None,
              datatype=None,
              agerange=None,

              value=None,
              source_url=None,
              text_match=None):
    """
    A hackish wrapper around DataPoint,
    adding some validation and default
    arguments for this `namedtuple`.
    """

    assert isinstance(region_schema, Schemas), region_schema
    assert isinstance(datatype, DataTypes), datatype

    region_parent = (region_parent or '').strip()
    region_child = (region_child or '').strip()
    agerange = agerange or ''
    value = int(value)

    if region_schema == Schemas.ADMIN_1:
        if region_parent and region_parent.lower() == 'china':
            region_parent = 'cn'
        elif region_parent:
            region_parent = _labels_to_region_child.get_by_label(
                Schemas.ADMIN_0, None, region_parent,
                default=region_parent
            )

    if text_match:
        text_match = str(text_match)
    else:
        text_match = ''

    assert date_updated.count('_') == 2, date_updated
    assert len(date_updated) == 10, date_updated
    assert datatype is not None
    assert source_url, source_url
    assert value is not None

    # Convert regions to ISO-3166-1/2 if possible
    if (region_schema, region_parent, region_child) in _mappings_to_iso_3166:
        region_schema, region_parent, region_child = \
            _mappings_to_iso_3166[region_schema, region_parent, region_child]

    region_parent, region_child = get_schema_type_info(
        region_schema
    ).convert_parent_child(region_parent, region_child)

    region_child = _labels_to_region_child.get_by_label(
        region_schema, region_parent, region_child,
        default=region_child
    )

    region_parent = region_parent.lower()
    region_child = region_child.lower()

    return _DataPoint(
        region_schema,
        region_parent,
        region_child,

        date_updated,
        datatype,
        agerange,

        value,

        source_url,
        text_match
    )


_DataPoint = namedtuple('DataPoint', [
    'region_schema',
    'region_parent',
    'region_child',

    'date_updated',
    'datatype',
    'agerange',

    'value',

    # The URL where the info came from
    'source_url',
    # The text which matched this (the x,y range and text itself)
    'text_match',
])
