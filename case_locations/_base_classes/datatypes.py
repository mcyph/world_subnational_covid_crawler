from collections import namedtuple

PublicTransportRoutePortion = namedtuple('PublicTransportRoutePortion', [
    'by', 'route', 'date', 'time', 'start_loc', 'end_loc', 'health_advice'
])


class VenueLocation:
    def __init__(self, state, type, venue, suburb, date, time, alert, long, lat):
        self.state = state
        self.type = type
        self.venue = venue
        self.suburb = suburb
        self.date = date
        self.time = time
        self.alert = alert
        self.long = long
        self.lat = lat

    def to_dict(self):
        return {
            'state': self.state,
            'area': self.suburb,
            'name': f"{self.type.title()}: {self.venue}",
            'venue': self.venue,
            'type': self.type,
            'date': self.date.strftime('%d/%m/%y'),
            'time': self.time,
            'description': self.alert,
            'coor': [self.lat, self.long]
        }
