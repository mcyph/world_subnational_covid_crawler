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
                type='isolate',
                venue=name,
                suburb=area,
                date=date,
                time=time,
                alert='Get tested immediately and self-isolate until you get a negative result',
                long=map_item['long'],
                lat=map_item['lat'],
            ))

        return out


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
    datapoints = _VicCaseLocations().get_datapoints()
    for datapoint in datapoints:
        if not isinstance(datapoint, VenueLocation):
            continue

        out.append({
            'state': 'VIC',
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
