from collections import namedtuple


DataPoint = namedtuple('DataPoint', [
    'datatype',
    'value',
    'date_updated',
    # The URL where the info came from
    'source_url',
    # The text which matched this (the x,y range and text itself)
    'text_match'
])

