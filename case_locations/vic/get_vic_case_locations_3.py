import json
import requests
from pyquery import PyQuery as pq
from dateutil.parser import parse as parse_datetime
from case_locations._base_classes.CacheBase import CacheBase
from case_locations._base_classes.datatypes import PublicTransportRoutePortion, VenueLocation

CASE_LOCATIONS_ALERTS_URL = 'https://www.coronavirus.vic.gov.au/sdp-ckan?resource_id=afb52611-6061-4a2b-9110-74c920bede77&limit=10000'


class _VicDHHSCaseLocations(CacheBase):
    STATE_NAME = 'vic'

    def get_datapoints(self):
        revision_dir = self._get_new_dir()
        rq = requests.get(CASE_LOCATIONS_ALERTS_URL)

        with open(revision_dir / 'caselocs.json', 'w', encoding='utf-8') as f:
            f.write(rq.text)

        r = []
        r.extend(self.__get_venue_locations(rq))
        return r

    def __get_venue_locations(self, rq):
        out = []

        for item in rq.json()['result']['records']:
            # "records": [{
            #   "_id":1,
            #   "Suburb":"Abbotsford",
            #   "Site_title":"Dukes Gym Abbotsford",
            #   "Site_streetaddress":"571-573 Victoria Street",
            #   "Site_state":"VIC",
            #   "Site_postcode":"3067",
            #   "Exposure_date_dtm":"2021-05-24",
            #   "Exposure_date":"24/05/2021",
            #   "Exposure_time":"6:15pm - 8:15pm",
            #   "Notes":"Case attended venue",
            #   "Added_date_dtm":"2021-05-26",
            #   "Added_date":"26/05/2021",
            #   "Added_time":"11:20 am",
            #   "Advice_title":"Tier 1 - Get tested immediately and quarantine for 14 days from exposure",
            #   "Advice_instruction":"Anyone who has visited this location during these times must get tested immediately and quarantine for 14 days from the exposure.",
            #   "Exposure_time_start_24":"18:15:00",
            #   "Exposure_time_end_24":"20:15:00"},

            date = parse_datetime(item['Exposure_date'], dayfirst=True)
            time = f'{item["Exposure_time_start_24"]} - {item["Exposure_time_end_24"]}'
            description = item['Notes'] + '. ' + item['Advice_title']

            if 'Tier 1' in item['Advice_title']:
                typ = 'isolate'
            elif 'Tier 2' in item['Advice_title']:
                typ = 'isolate'
            elif 'Tier 3' in item['Advice_title']:
                typ = 'monitor'
            else:
                raise Exception("Unknown Advice_title: "+item['Advice_title'])

            out.append(VenueLocation(
                state=self.STATE_NAME.upper(),
                type=typ,  # FIXME!!
                venue=item['Site_title'],
                area=item['Site_streetaddress'] + '\n' + item['Suburb'] + '\n' + ('Victoria' if item['Site_state'] == 'VIC' else item['Site_state']),
                date=date,
                time=time,
                description=description,
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
