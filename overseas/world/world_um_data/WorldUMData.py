# https://covidmap.umd.edu/api.html
import requests
from datetime import datetime, timedelta

from requests import get
from os import makedirs, listdir
from os.path import exists
from http import HTTPStatus
from json import loads, dumps

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)
from covid_19_au_grab.overseas.w_europe.uk_data.uk_place_map import (
    place_map
)
from covid_19_au_grab.datatypes.StrictDataPointsFactory import (
    StrictDataPointsFactory, MODE_STRICT, MODE_DEV
)
from covid_19_au_grab.normalize_locality_name import (
    normalize_locality_name
)


TYPE = 'smoothed'  # Can also use "daily"

#FROM_DATE = '20200101'
FROM_DATE = (datetime.now() - timedelta(days=14)).strftime('%Y%m%d')


class WorldUMData(URLBase):
    SOURCE_URL = 'https://covidmap.umd.edu'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'world_umd_covidmap'

    def __init__(self):
        URLBase.__init__(self,
                         output_dir=get_overseas_dir() / 'uk' / 'covid-19-uk-data' / 'data',
                         urls_dict={})

        self.update()
        self.__download_dataset()
        self.sdpf = StrictDataPointsFactory(mode=MODE_DEV)

    def get_datapoints(self):
        r = []
        for date in listdir(get_overseas_dir() / 'world_um' / 'api_data'):
            r.extend(self._get_datapoints(date))
        return r

    def _get_datapoints(self, date):
        r = self.sdpf()
        path = get_overseas_dir() / 'world_um' / 'api_data' / date / 'data.json'

        with open(path, 'r', encoding='utf-8') as f:
            data = loads(f.read())
            #print(data)

            for country, country_data_dict in data['covid'].items():
                for country_dict in country_data_dict['countries']:
                    print(country_dict)
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_parent='',
                        region_child=country,
                        datatype=DataTypes.FACEBOOK_COVID_SYMPTOMS,
                        value=round(country_dict['smoothed_cli']*100000),
                        date_updated=self.convert_date(country_dict['survey_date'],
                                                       formats=('%Y%m%d',)),
                        source_url=self.SOURCE_URL
                    )

                for region_dict in country_data_dict['regions']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent=country,
                        region_child=region_dict['region'],
                        datatype=DataTypes.FACEBOOK_COVID_SYMPTOMS,
                        value=round(region_dict['smoothed_cli']*100000),
                        date_updated=self.convert_date(region_dict['survey_date'],
                                                       formats=('%Y%m%d',)),
                        source_url=self.SOURCE_URL
                    )

            for country, country_data_dict in data['flu'].items():
                for country_dict in country_data_dict['countries']:
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_parent='',
                        region_child=country,
                        datatype=DataTypes.FACEBOOK_FLU_SYMPTOMS,
                        value=round(country_dict['smoothed_ili']*100000),
                        date_updated=self.convert_date(country_dict['survey_date'],
                                                       formats=('%Y%m%d',)),
                        source_url=self.SOURCE_URL
                    )

                for region_dict in country_data_dict['regions']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent=country,
                        region_child=region_dict['region'],
                        datatype=DataTypes.FACEBOOK_FLU_SYMPTOMS,
                        value=round(region_dict['smoothed_ili']*100000),
                        date_updated=self.convert_date(region_dict['survey_date'],
                                                       formats=('%Y%m%d',)),
                        source_url=self.SOURCE_URL
                    )

        return r

    def __download_dataset(self):
        """
        Extracts paginated data by requesting all of the pages
        and combining the results.
        """
        date = datetime.now().strftime('%Y_%m_%d')
        dir_ = get_overseas_dir() / 'world_um' / 'api_data' / date
        if not exists(dir_):
            makedirs(dir_)

        path = dir_ / f'data.json'
        if exists(path):
            # Don't download if already downloaded!
            return

        out = {
            'covid': {},
            'flu': {}
        }
        response = requests.get("https://covidmap.umd.edu/api/country")

        for country_dict in response.json()['data']:
            for indicator in ('covid', 'flu'):
                # Get country-level data
                response = requests.get("https://covidmap.umd.edu/api/resources?"
                                        f"indicator={indicator}&"
                                        f"type={TYPE}&"
                                        f"country={country_dict['country']}&"
                                        "region=all&"
                                        f"daterange={FROM_DATE}-{datetime.now().strftime('%Y%m%d')}")
                region_data = response.json()['data']

                response = requests.get("https://covidmap.umd.edu/api/resources?"
                                        f"indicator={indicator}&"
                                        f"type={TYPE}&"
                                        f"country={country_dict['country']}&"
                                        f"daterange={FROM_DATE}-{datetime.now().strftime('%Y%m%d')}")
                country_data = response.json()['data']

                out[indicator][country_dict['country']] = {
                    'regions': region_data,
                    'countries': country_data
                }

        with open(path, 'w', encoding='utf-8') as f:
            f.write(dumps(out))


if __name__ == "__main__":
    from pprint import pprint
    inst = WorldUMData()
    pprint(inst.get_datapoints())
