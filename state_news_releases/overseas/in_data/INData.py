import json

from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_IN_STATE, SCHEMA_IN_DISTRICT,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)

# {
#     "agebracket": "",
#     "contractedfromwhichpatientsuspected": "",
#     "currentstatus": "Hospitalized",
#     "dateannounced": "10/05/2020",
#     "detectedcity": "",
#     "detecteddistrict": "Ajmer",
#     "detectedstate": "Rajasthan",
#     "entryid": "10009",
#     "gender": "",
#     "nationality": "",
#     "notes": "",
#     "numcases": "2",
#     "patientnumber": "37900",
#     "source1": "https://twitter.com/ANI/status/1259331384851775488?s=09",
#     "source2": "",
#     "source3": "",
#     "statecode": "RJ",
#     "statepatientnumber": "",
#     "statuschangedate": "",
#     "typeoftransmission": ""
# }, ...

# since raw_data3.json : When a new report/bulletin is released from a state regarding confirmed cases :
#
#     If patient level information is available (from several states like KA,KL,BH etc.), that is captured.
#     If only districtwise information is available, one row is entered for each district, and “numcases” field mentions the number of cases in that district
#
#     If only statewise information is available, one row is added added for the entire state (DL 👀)
#     Recoveries and Deceased information is also available through raw_data3.json now. Use the “Current Status” field to extract that information.


with open(get_package_dir() / 'state_news_releases' /
          'overseas' / 'in_data' /
          'india_states.csv', 'r', encoding='utf-8') as f:

    _state_codes = {}
    for _line in f:
        _line = _line.strip()
        _code, _name = _line.split('\t')
        _state_codes[_code.strip()] = _name.strip()


class INData(URLBase):
    SOURCE_URL = 'https://api.covid19india.org'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'in' / 'data',
             urls_dict={
                 'raw_data1.json': URL('https://api.covid19india.org/raw_data1.json',
                                      static_file=True),
                 'raw_data2.json': URL('https://api.covid19india.org/raw_data2.json',
                                      static_file=True),
                 'raw_data3.json': URL('https://api.covid19india.org/raw_data3.json',
                                      static_file=True),
                 'raw_data4.json': URL('https://api.covid19india.org/raw_data4.json',
                                      static_file=False),
                  'districts_daily.json': URL('https://api.covid19india.org/districts_daily.json',
                                              static_file=False),
                  'states_daily.json': URL('https://api.covid19india.org/states_daily.json',
                                           static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_by_district())
        r.extend(self._get_by_state())
        return r

    def _get_by_district(self):
        # {
        #   "districtsDaily": {
        #     "Andaman and Nicobar Islands": {
        #       "North and Middle Andaman": [
        #         {
        #           "active": 0,
        #           "confirmed": 1,
        #           "deceased": 0,
        #           "recovered": 1,
        #           "date": "2020-04-21"
        #         },
        r = []

        text = self.get_text('districts_daily.json',
                             include_revision=True)
        data = json.loads(text)

        for state_name, district_dict in data['districtsDaily'].items():
            for district, status_dicts in district_dict.items():
                for status_dict in status_dicts:
                    date = self.convert_date(status_dict['date'])

                    r.append(DataPoint(
                        statename=state_name,
                        schema=SCHEMA_IN_DISTRICT,
                        datatype=DT_TOTAL,
                        region=district,
                        value=int(status_dict['confirmed']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        statename=state_name,
                        schema=SCHEMA_IN_DISTRICT,
                        datatype=DT_STATUS_ACTIVE,
                        region=district,
                        value=int(status_dict['active']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        statename=state_name,
                        schema=SCHEMA_IN_DISTRICT,
                        datatype=DT_STATUS_DEATHS,
                        region=district,
                        value=int(status_dict['deceased']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        statename=state_name,
                        schema=SCHEMA_IN_DISTRICT,
                        datatype=DT_STATUS_RECOVERED,
                        region=district,
                        value=int(status_dict['recovered']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
        return r

    def _get_by_state(self):
        # {
        # 	"states_daily": [
        # 		{
        # 			"an": "0",
        # 			"ap": "1",
        # 			"ar": "0",
        # 			"as": "0",
        # 			"br": "0",
        # 			"ch": "0",
        # 			"ct": "0",
        # 			"date": "14-Mar-20",
        # 			"dd": "0",
        # 			"dl": "7",
        # 			"dn": "0",
        # 			"ga": "0",
        # 			"gj": "0",
        # 			"hp": "0",
        # 			"hr": "14",
        # 			"jh": "0",
        # 			"jk": "2",
        # 			"ka": "6",
        # 			"kl": "19",
        # 			"la": "0",
        # 			"ld": "0",
        # 			"mh": "14",
        # 			"ml": "0",
        # 			"mn": "0",
        # 			"mp": "0",
        # 			"mz": "0",
        # 			"nl": "0",
        # 			"or": "0",
        # 			"pb": "1",
        # 			"py": "0",
        # 			"rj": "3",
        # 			"sk": "0",
        # 			"status": "Confirmed",
        # 			"tg": "1",
        # 			"tn": "1",
        # 			"tr": "0",
        # 			"tt": "81",
        # 			"up": "12",
        # 			"ut": "0",
        # 			"wb": "0"
        # 		},
        r = []
        text = self.get_text('states_daily.json',
                            include_revision=True)
        data = json.loads(text)

        for state_name, status_dicts in data.items():
            for status_dict in status_dicts:
                print(status_dict['date'])
                date = self.convert_date(status_dict['date'])
                datatype = {
                    'Confirmed': DT_TOTAL,
                    'Recovered': DT_STATUS_RECOVERED,
                    'Deceased': DT_STATUS_DEATHS,
                    'Active': DT_STATUS_ACTIVE
                }[status_dict['status']]

                del status_dict['date']
                del status_dict['status']

                for district_code, value in status_dict.items():
                    if value in (None, ''):
                        continue

                    r.append(DataPoint(
                        schema=SCHEMA_IN_STATE,
                        datatype=datatype,
                        region=_state_codes[district_code.upper()],
                        value=int(value),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(INData().get_datapoints())
