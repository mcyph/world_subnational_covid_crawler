import json
import requests
from pyquery import PyQuery as pq
from dateutil.parser import parse as parse_datetime
from case_locations._base_classes.CacheBase import CacheBase
from case_locations._base_classes.datatypes import PublicTransportRoutePortion, VenueLocation

# https://transitfeeds.com/p/transport-for-nsw/237

CASE_LOCATIONS_ALERTS_URL = 'https://www.health.nsw.gov.au/Infectious/covid-19/Pages/case-locations-and-alerts.aspx'
# https://www.health.nsw.gov.au/Infectious/covid-19/Documents/data/venue-data-20201226.js


class _NSWCaseLocations(CacheBase):
    STATE_NAME = 'nsw'

    def get_datapoints(self):
        revision_dir = self._get_new_dir()
        cla_rq = requests.get(CASE_LOCATIONS_ALERTS_URL)

        with open(revision_dir / 'case_locations_and_alerts.html', 'w', encoding='utf-8') as f:
            f.write(cla_rq.text)

        vd_url = cla_rq.text.split('/Infectious/covid-19/Documents/data/venue-data-')[1].split('.js')[0]
        vd_url = f'https://www.health.nsw.gov.au/Infectious/covid-19/Documents/data/venue-data-{vd_url}.js'
        vd_rq = requests.get(vd_url)

        with open(revision_dir / 'venue-data.js', 'w', encoding='utf-8') as f:
            f.write(vd_rq.text)

        r = []
        r.extend(self.__get_venue_locations(vd_rq))
        r.extend(self.__get_public_transport_route_portions(cla_rq))
        return r

    def __get_public_transport_route_portions(self, cla_rq):
        r = []
        tr_elms = pq(cla_rq.text)('table#tbl-casual-contacts-transport tbody tr')
        for by, route, date, time, start_loc, end_loc, health_advice in tr_elms:
            r.append(PublicTransportRoutePortion(
                by=pq(by).text(),
                route=pq(route).text(),
                date=parse_datetime(pq(date).text(), dayfirst=True),
                time=pq(time).text(),
                start_loc=pq(start_loc).text(),
                end_loc=pq(end_loc).text(),
                health_advice=pq(health_advice).text()
            ))
        return r

    def __get_venue_locations(self, vd_rq):
        r = []

        data = json.loads(vd_rq.text.partition('var venue_data = ')[-1])
        # TODO: What to do with the updated date?
        # date_updated = data['date']

        for k, v in data['data'].items():
            for i in v:
                try:
                    date = parse_datetime(i['Date'], dayfirst=True)
                except:
                    date = parse_datetime(i['Date'].partition(' ')[-1],
                                          dayfirst=True)

                r.append(VenueLocation(
                    type=k,
                    venue=i['Venue'],
                    suburb=i['Suburb'],
                    date=date,
                    time=i['Time'],
                    alert=i['Alert'],
                    long=float(i['Lon']) if float(i['Lon']) >= 100.0 else float(i['Lat']),
                    lat=float(i['Lat']) if float(i['Lat']) < 100.0 else float(i['Lon']),
                ))
        return r


if __name__ == '__main__':

    #   {
    #     "state": "NSW",
    #     "area": "",
    #     "name": "St Brendan’s Catholic Church Bankstown",
    #     "date": "16/07/20",
    #     "time": "for one hour from 6.30pm",
    #     "description": "St Brendan’s Catholic Church Bankstown for one hour from 6.30pm on July 16",
    #     "coor": [-33.9220903,151.0277432]
    #   },

    out = []
    datapoints = _NSWCaseLocations().get_datapoints()
    for datapoint in datapoints:
        if not isinstance(datapoint, VenueLocation):
            continue

        out.append({
            'state': 'NSW',
            'area': datapoint.suburb,
            'name': f"{datapoint.type.title()}: {datapoint.venue}",
            'venue': datapoint.venue,
            'type': datapoint.type,
            'date': datapoint.date.strftime('%d/%m/%y'),
            'time': datapoint.time,
            'description': datapoint.alert,
            'coor': [datapoint.lat, datapoint.long]
        })

    print(json.dumps(out, indent=2))
    #pprint(datapoints)
