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

        for msg, table in zip(
            pq(rq.text)('p:contains("If you have visited any of the locations")'),
            pq(rq.text)('table:contains("Exposure period")')
        ):
            table_headers = [pq(i).text() for i in pq(table)('th')]
            data = [
                dict(zip(table_headers, [pq(j).text() for j in pq(i)('td')]))
                for i in pq(table)('tr')[1:]
            ]
            description = pq(msg).text().replace('\xa0', ' ')
            description = ' '.join(description.split())

            if 'quarantine for 14 days' in description:
                typ = 'isolate'
            elif 'quarantine until you receive a negative result' in description:
                typ = 'monitor'
            elif 'tested and isolate until you receive a negative result' in description:
                typ = 'monitor'  # CHECK ME!!!
            else:
                raise Exception(description)

            for item in data:
                date_time = item['Exposure period']
                date = date_time.split()[0].strip(',')
                date = parse_datetime(date, dayfirst=True)
                time = date_time.partition(' ')[-1]

                out.append(VenueLocation(
                    state=self.STATE_NAME.upper(),
                    type=typ,
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
