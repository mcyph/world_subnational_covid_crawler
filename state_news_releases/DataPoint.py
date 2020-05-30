import unidecode
from collections import namedtuple

from covid_19_au_grab.state_news_releases.constants import SCHEMA_ADMIN_0, SCHEMA_ADMIN_1
from covid_19_au_grab.other_data.iso_3166_1 import iso_3166_data
from covid_19_au_grab.other_data.iso_3166_2 import iso_3166_2_data


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

    if region_schema == SCHEMA_ADMIN_1 and region_parent and region_child:
        # Convert names to ISO codes
        try:
            item = iso_3166_2_data.get_data_item_by_name(
                unidecode.unidecode(region_child), region_parent
            )
            region_parent = item.country_code
            region_child = item.code
        except KeyError:
            pass
    elif region_schema == SCHEMA_ADMIN_0 and region_child:
        assert not region_parent, region_parent
        try:
            item = iso_3166_data.get_data_item_by_name(
                region_child
            )
            region_child = item.iso3166.a2
        except KeyError:
            pass

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


class _DataPointProcessor:
    def process(self):
        pass

    def convert_admin_0(self):
        pass

    def convert_admin_1(self):
        pass



