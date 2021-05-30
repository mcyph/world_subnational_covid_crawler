import json
import requests
from pyquery import PyQuery as pq
from dateutil.parser import parse as parse_datetime
from case_locations._base_classes.CacheBase import CacheBase
from case_locations._base_classes.datatypes import PublicTransportRoutePortion, VenueLocation

CASE_LOCATIONS_ALERTS_URL = 'https://www.dhhs.vic.gov.au/case-locations-and-outbreaks'


class _VicDHHSCaseLocations(CacheBase):
    STATE_NAME = 'vic'

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

        for table in pq(rq.text)('table:contains("Health advice")'):
            table_headers = [pq(i).text() for i in pq(table)('th')]
            data = [
                dict(zip(table_headers, [pq(j).text() for j in pq(i)('td')]))
                for i in pq(table)('tr')[1:]
            ]

            for item in data:
                if item['Site'].replace('\n', '. ').strip() == '-':
                    # Indicates nothing!!
                    continue

                date_time = item['Exposure period']
                date = date_time.split()[0]
                date = date.replace('0/2/2021', '1/2/2021')
                date = parse_datetime(date, dayfirst=True)
                time = ' '.join(date_time.split()[1:])
                description = item['Health advice'].partition('-')[-1]

                out.append(VenueLocation(
                    state=self.STATE_NAME.upper(),
                    type=item['Health advice'].partition('-')[0],
                    venue=item['Site'].replace('\n', '. '),
                    area=item['Location'],
                    date=date,
                    time=time,
                    description=(
                        f'{item["Notes"].rstrip(".")}. {description}'
                        if item['Notes']
                        else description
                    ),
                    long=None,
                    lat=None,
                ))

        return out


def get_vic_case_locations():
    out = []
    datapoints = _VicDHHSCaseLocations().get_datapoints()

    for datapoint in datapoints:
        out.append(datapoint.to_dict())
    return out


if __name__ == '__main__':
    print(json.dumps(get_vic_case_locations(), indent=2))
