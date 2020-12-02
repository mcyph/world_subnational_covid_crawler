import json
from datetime import datetime

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_crawlers.world.world_jhu_data.get_county_to_code_map import get_county_to_code_map
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT

county_to_code_map = get_county_to_code_map()


class WorldGenderDisaggregated(URLBase):
    SOURCE_ID = 'world_gender_disaggregated'
    SOURCE_URL = ''
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'world_gender_disaggregated' / 'data',
            urls_dict={
                'world_gender_disaggregated.json': URL(url='https://api.globalhealth5050.org/api/v1/summary?data=historic',
                                                       static_file=False),
            }
        )
        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = self.sdpf()
        date = datetime.today().strftime('%Y_%m_%d')
        path = get_overseas_dir() / 'world_gender_disaggregated' / 'data' / date / 'world_gender_disaggregated.json'

        with open(path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        for k, items in data['data'].items():
            print(k, items)
            #date = self.convert_date(item['Date_reported'])

            for item in items:
                #print(item)
                if not item['country_code']:
                    print("IGNORING:", item)
                    continue

                for datatype, date, value in (
                    # TODO: Support more gendered datatypes!
                    (
                        DataTypes.TESTS_TOTAL, item['date_tests'],
                        int(item['tests_male'])+int(item['tests_female'])
                        if item['tests_male'] and item['tests_female']
                        else ''
                    ),
                    (DataTypes.TOTAL, item['date_cases'], item['cases_total']),
                    (DataTypes.TOTAL_MALE, item['date_cases'], item['cases_male']),
                    (DataTypes.TOTAL_FEMALE, item['date_cases'], item['cases_female']),
                    (DataTypes.STATUS_DEATHS, item['date_deaths'], item['deaths_total']),
                    (DataTypes.STATUS_ICU, item['hosp_date'], item['hosp_total']),
                ):
                    if not value:
                        continue

                    date = date or item['date']
                    print(datatype, date, value)
                    if not date:
                        continue

                    i_date = self.convert_date(date, formats=('%m/%d/%y', '%m/%d/%Y'))
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_parent='',
                        region_child=item['country_code'],
                        datatype=datatype,
                        value=int(float(value)),
                        date_updated=i_date,
                        source_url=self.SOURCE_URL
                    )

        return r


if __name__ == '__main__':
    datapoints = WorldGenderDisaggregated().get_datapoints()
    #pprint(datapoints)
