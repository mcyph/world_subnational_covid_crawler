from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.get_package_dir import (
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


class INData(URLBase):
    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'jp' / 'covid19' / 'data',
             urls_dict={
                 'raw_data1.json': URL('api.covid19india.org/raw_data1.json',
                                      static_file=True),
                 'raw_data2.json': URL('api.covid19india.org/raw_data2.json',
                                      static_file=True),
                 'raw_data3.json': URL('api.covid19india.org/raw_data3.json',
                                      static_file=True),
                 'raw_data4.json': URL('api.covid19india.org/raw_data4.json',
                                      static_file=False),
                  'districts_daily.json': URL('https://api.covid19india.org/districts_daily.json',
                                              static_file=False),
                  'states_daily.json': URL('https://api.covid19india.org/states_daily.json',
                                           static_file=False)
            }
        )

    def get_datapoints(self):
        cases_by_date = {}

        for raw_data_idx in range(1, 5):
            for case_item in self.get_file(
                f'raw_data{raw_data_idx}.json',
                include_revision=raw_data_idx == 4,
                include_subid=False
            ):
                cases_by_date.setdefault(self.convert_date(case_item['dateannounced']), []).append(
                    case_item
                )

        r = []

        for date, case_items in sorted(cases_by_date.items()):
            for case_item in case_items:
                FIXME
