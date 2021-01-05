from collections import namedtuple


PublicTransportRoutePortion = namedtuple('PublicTransportRoutePortion', [
    'by', 'route', 'date', 'time', 'start_loc', 'end_loc', 'health_advice'
])


class VenueLocation:
    def __init__(self, state, type, venue, area, date, time, description, long, lat):
        self.state = state
        self.type = type
        self.venue = venue
        self.area = area
        self.date = date
        self.time = time
        self.description = description
        self.long = long
        self.lat = lat

    @staticmethod
    def from_dict(d):
        return VenueLocation(**d)

    def to_dict(self):
        return {
            'state': self.state,
            'area': self.area,
            'venue': self.venue,
            'type': self.type,
            'date': self.date.strftime('%d/%m/%y'),
            'time': self.time,
            'description': self.description,
            'long': self.long,
            'lat': self.lat
        }

    def get_geocoord_key(self):
        return self.state, self.area, self.venue
