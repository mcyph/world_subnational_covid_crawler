import json
import requests
from pyquery import PyQuery as pq
from dateutil.parser import parse as parse_datetime
from case_locations._base_classes.CacheBase import CacheBase
from case_locations._base_classes.datatypes import PublicTransportRoutePortion, VenueLocation

CASE_LOCATIONS_ALERTS_URL = 'https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/contact-tracing'


class _QLDCaseLocations(CacheBase):
    STATE_NAME = 'qld'

    def get_datapoints(self):
        revision_dir = self._get_new_dir()
        rq = requests.get(CASE_LOCATIONS_ALERTS_URL)

        with open(revision_dir / 'caselocs.html', 'w', encoding='utf-8') as f:
            f.write(rq.text)

        r = []
        r.extend(self.__get_venue_locations(rq))
        return r

    def __get_venue_locations(self, rq):
        out = []

        for table in pq(rq.text)('table:contains("Suburb")'):
            table_headers = [pq(i).text().strip() for i in pq(table)('th')]
            data = [
                dict(zip(table_headers, [pq(j).text() for j in pq(i)('td')]))
                for i in pq(table)('tr')[1:]
            ]
            msg = pq(rq.text)('p:contains("Anyone who has been in the below locations")').text()
            description = msg.replace('\xa0', ' ')
            description = ' '.join(description.split())

            typ = 'monitor'

            for item in data:
                date = item['Date']
                date = parse_datetime(date, dayfirst=True)
                time = item['Arrival time']+'-'+item['Departure time'].strip('-')

                out.append(VenueLocation(
                    state=self.STATE_NAME.upper(),
                    type=typ,
                    venue=item['Place'].replace('\n', '. '),
                    area=item['Suburb'],
                    date=date,
                    time=time,
                    description=description,
                    long=None,
                    lat=None,
                ))

        return out


def get_qld_case_locations():
    out = []
    datapoints = _QLDCaseLocations().get_datapoints()

    for datapoint in datapoints:
        out.append(datapoint.to_dict())
    return out


if __name__ == '__main__':
    print(json.dumps(get_qld_case_locations(), indent=2))
