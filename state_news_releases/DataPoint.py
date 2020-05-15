from collections import namedtuple
from covid_19_au_grab.state_news_releases.constants import SCHEMA_STATEWIDE


def DataPoint(statename=None,
              schema=SCHEMA_STATEWIDE,
              datatype=None,
              agerange=None,
              region=None,
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
    agerange = agerange or ''
    region = region or ''
    assert date_updated
    assert source_url
    assert value is not None
    text_match = text_match or ''

    return _DataPoint(
        statename, schema, datatype,
        agerange, region, value,
        date_updated, source_url, text_match
    )


_DataPoint = namedtuple('DataPoint', [
    'statename',
    'schema',
    'datatype',
    'agerange',
    'region',
    'value',
    'date_updated',
    # The URL where the info came from
    'source_url',
    # The text which matched this (the x,y range and text itself)
    'text_match'
])
