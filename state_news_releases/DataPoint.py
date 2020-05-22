from collections import namedtuple
from covid_19_au_grab.state_news_releases.constants import SCHEMA_ADMIN_1


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
