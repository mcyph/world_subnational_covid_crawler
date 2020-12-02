import json

from covid_crawlers._base_classes.URLBase import (
    URL, URLBase
)
from covid_db.datatypes.DataPoint import (
    DataPoint
)
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import (
    get_overseas_dir
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


# TODO: Fix Dadra and Nagar Haveli and Daman and Diu!!
states_map = dict([i.split('\t')[::-1] for i in """
IN-AP	Andhra Pradesh
IN-AR	Arunachal Pradesh
IN-AS	Assam
IN-BR	Bihar
IN-CT	Chhattisgarh
IN-GA	Goa
IN-GJ	Gujarat
IN-HR	Haryana
IN-HP	Himachal Pradesh
IN-JH	Jharkhand
IN-KA	Karnataka
IN-KL	Kerala
IN-MP	Madhya Pradesh
IN-MH	Maharashtra
IN-MN	Manipur
IN-ML	Meghalaya
IN-MZ	Mizoram
IN-NL	Nagaland
IN-OR	Odisha
IN-PB	Punjab
IN-RJ	Rajasthan
IN-SK	Sikkim
IN-TN	Tamil Nadu
IN-TG	Telangana
IN-TR	Tripura
IN-UT	Uttarakhand
IN-UP	Uttar Pradesh
IN-WB	West Bengal
IN-AN	Andaman and Nicobar Islands
IN-AN	Andaman & Nicobar
IN-CH	Chandigarh
IN-DN	Dadra and Nagar Haveli
IN-DN	Daman and Diu
IN-DN	Dadra and Nagar Haveli and Daman and Diu
IN-DL	Delhi
IN-JK	Jammu and Kashmir
IN-JK	Jammu & Kashmir
IN-LA	Ladakh
IN-LD	Lakshadweep
IN-PY	Puducherry
IN-TT	Unknown
""".strip().split('\n')])

reverse_states_map = {
    v: k for k, v in states_map.items()
}


class INData(URLBase):
    SOURCE_URL = 'https://api.covid19india.org'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'in_covid_19_india'

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
                                      static_file=True),
                 'raw_data5.json': URL('https://api.covid19india.org/raw_data5.json',
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

        for parent_regions, district_dict in data['districtsDaily'].items():
            for district, status_dicts in district_dict.items():
                for status_dict in status_dicts:
                    date = self.convert_date(status_dict['date'])
                    parent_region = states_map[parent_regions]

                    r.append(DataPoint(
                        region_parent=parent_region,
                        region_schema=Schemas.IN_DISTRICT,
                        datatype=DataTypes.TOTAL,
                        region_child=district,
                        value=int(status_dict['confirmed']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        region_parent=parent_region,
                        region_schema=Schemas.IN_DISTRICT,
                        datatype=DataTypes.STATUS_ACTIVE,
                        region_child=district,
                        value=int(status_dict['active']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        region_parent=parent_region,
                        region_schema=Schemas.IN_DISTRICT,
                        datatype=DataTypes.STATUS_DEATHS,
                        region_child=district,
                        value=int(status_dict['deceased']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        region_parent=parent_region,
                        region_schema=Schemas.IN_DISTRICT,
                        datatype=DataTypes.STATUS_RECOVERED,
                        region_child=district,
                        value=int(status_dict['recovered']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
        return r

    def _get_by_state(self):
        # {
        #	"states_daily": [
        #		{
        #			"an": "0",
        #			"ap": "1",
        #			"ar": "0",
        #			"as": "0",
        #			"br": "0",
        #			"ch": "0",
        #			"ct": "0",
        #			"date": "14-Mar-20",
        #			"dd": "0",
        #			"dl": "7",
        #			"dn": "0",
        #			"ga": "0",
        #			"gj": "0",
        #			"hp": "0",
        #			"hr": "14",
        #			"jh": "0",
        #			"jk": "2",
        #			"ka": "6",
        #			"kl": "19",
        #			"la": "0",
        #			"ld": "0",
        #			"mh": "14",
        #			"ml": "0",
        #			"mn": "0",
        #			"mp": "0",
        #			"mz": "0",
        #			"nl": "0",
        #			"or": "0",
        #			"pb": "1",
        #			"py": "0",
        #			"rj": "3",
        #			"sk": "0",
        #			"status": "Confirmed",
        #			"tg": "1",
        #			"tn": "1",
        #			"tr": "0",
        #			"tt": "81",
        #			"up": "12",
        #			"ut": "0",
        #			"wb": "0"
        #		},
        r = []
        text = self.get_text('states_daily.json',
                            include_revision=True)
        data = json.loads(text)

        for parent_regions, status_dicts in data.items():
            for status_dict in status_dicts:
                #print(status_dict['date'])
                date = self.convert_date(status_dict['date'])
                datatype = {
                    'Confirmed': DataTypes.TOTAL,
                    'Recovered': DataTypes.STATUS_RECOVERED,
                    'Deceased': DataTypes.STATUS_DEATHS,
                    'Active': DataTypes.STATUS_ACTIVE
                }[status_dict['status']]

                del status_dict['date']
                del status_dict['status']

                for district_code, value in status_dict.items():
                    if value in (None, ''):
                        continue
                    assert ('IN-'+district_code.upper()) in reverse_states_map, district_code

                    if district_code.upper() == 'TT':
                        region_child = 'Unknown'
                    else:
                        region_child = 'IN-' + district_code.upper()

                    r.append(DataPoint(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='IN',
                        region_child=region_child,
                        datatype=datatype,
                        value=int(value),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(INData().get_datapoints())
