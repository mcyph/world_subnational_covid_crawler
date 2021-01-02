from collections import namedtuple

VenueLocation = namedtuple('VenueLocation', [
    'type', 'venue', 'suburb', 'date', 'time', 'alert', 'long', 'lat'
])

PublicTransportRoutePortion = namedtuple('PublicTransportRoutePortion', [
    'by', 'route', 'date', 'time', 'start_loc', 'end_loc', 'health_advice'
])
