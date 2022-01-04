import csv
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
                #'world_gender_disaggregated.json': URL(url='https://api.globalhealth5050.org/api/v1/summary?data=historic',
                #                                       static_file=False),
                'world_gender_disaggregated.csv': URL(url='https://globalhealth5050.org/?_covid-data=datasettable&_extype=csv',
                                                      static_file=False)
            }
        )
        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        date = datetime.today().strftime('%Y_%m_%d')
        json_path = get_overseas_dir() / 'world_gender_disaggregated' / 'data' / date / 'world_gender_disaggregated.json'
        csv_path = get_overseas_dir() / 'world_gender_disaggregated' / 'data' / date / 'world_gender_disaggregated.csv'

        if json_path.exists():
            return self._get_json_datapoints(json_path)
        elif csv_path.exists():
            return self._get_csv_datapoints(csv_path)
        else:
            raise Exception()

    def _get_csv_datapoints(self, path):
        r = self.sdpf()

        with open(path, 'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                if '\ufeff"Country code"' in item:
                    item['Country code'] = item['\ufeff"Country code"']

                if not item['Country code'] or not item['Cases where sex-disaggregated data is available']:
                    print("IGNORING:", item)
                    continue
                elif item['Country code'] == 'BQ':
                    continue

                for datatype, date, value in (
                    # TODO: Support more gendered datatypes!
                    (DataTypes.TOTAL, item['Cases date'], int(item['Cases where sex-disaggregated data is available'])),
                    (DataTypes.TOTAL_MALE, item['Cases date'], int(item['Cases (% male)'].replace('%', ''))/100.0*int(item['Cases where sex-disaggregated data is available'])),
                    (DataTypes.TOTAL_FEMALE, item['Cases date'], int(item['Cases (% female)'].replace('%', ''))/100.0*int(item['Cases where sex-disaggregated data is available'])),
                ):
                    if not value:
                        continue
                    elif not date:
                        continue

                    i_date = self.convert_date(date, formats=('%Y/%m/%d',))
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_parent='',
                        region_child=item['Country code'],
                        datatype=datatype,
                        value=int(float(value)),
                        date_updated=i_date,
                        source_url=self.SOURCE_URL
                    )

        return r

    def _get_json_datapoints(self, path):
        r = self.sdpf()

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
