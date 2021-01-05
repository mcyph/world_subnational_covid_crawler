import json
import requests
from dateutil.parser import parse as parse_datetime
from case_locations._base_classes.CacheBase import CacheBase
from case_locations._base_classes.datatypes import PublicTransportRoutePortion, VenueLocation

CASE_LOCATIONS_ALERTS_URL = 'https://e.infogram.com/1p57e073gwzv09hp136mgg99kda35yw19w0?src=embed'


class _VicCaseLocations(CacheBase):
    STATE_NAME = 'vic'

    def get_datapoints(self):
        revision_dir = self._get_new_dir()
        cla_rq = requests.get(CASE_LOCATIONS_ALERTS_URL)

        with open(revision_dir / 'infogram.html', 'w', encoding='utf-8') as f:
            f.write(cla_rq.text)

        r = []
        r.extend(self.__get_venue_locations(cla_rq))
        return r

    def __get_venue_locations(self, vd_rq):
        data = json.loads(vd_rq.text.partition('window.infographicData=')[-1].split('</script>')[0].rstrip().rstrip(';'))
        del data['elements'][2]['custom']['map_json']

        map_dict = {}
        for map_data in data['elements'][2]['data'][0]:
            lat, long = map_data[3].split()
            lat = float(lat)
            long = float(long)
            map_dict[int(map_data[4])] = {
                'lat': lat,
                'long': long,
                'place_names': map_data[5]
            }

        out = []
        prev_map_idx = None

        for idx, area, name, date_time in data['elements'][4]['data'][0][1:]:
            if isinstance(idx, dict):
                idx = prev_map_idx = int(idx['value'])
            elif idx:
                idx = prev_map_idx = int(idx)
            else:
                idx = prev_map_idx

            date = date_time.split()[0].strip(',')
            date = parse_datetime(date, dayfirst=True)
            time = date_time.partition(' ')[-1]

            map_item = map_dict[idx]
            out.append(VenueLocation(
                state=self.STATE_NAME.upper(),
                type='isolate',
                venue=name,
                area=area,
                date=date,
                time=time,
                description='Get tested immediately and self-isolate until you get a negative result',
                long=map_item['long'],
                lat=map_item['lat'],
            ))

        return out


def get_vic_case_locations():
    out = []
    datapoints = _VicCaseLocations().get_datapoints()

    for datapoint in datapoints:
        out.append(datapoint.to_dict())
    return out


if __name__ == '__main__':
    print(json.dumps(get_vic_case_locations(), indent=2))
