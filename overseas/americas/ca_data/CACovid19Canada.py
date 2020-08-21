# https://github.com/ishaberry/Covid19Canada

import csv

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)
from covid_19_au_grab.overseas.americas.ca_data.hr_convert import (
    health_region_to_uid, province_to_iso_3166_2
)
from covid_19_au_grab.geojson_data.LabelsToRegionChild import (
    LabelsToRegionChild
)

_ltrc = LabelsToRegionChild()


class CACovid19Canada(GithubRepo):
    SOURCE_URL = 'https://github.com/ishaberry/Covid19Canada'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ca_covid_19_canada'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'ca' / 'Covid19Canada',
                            github_url='https://github.com/ishaberry/Covid19Canada')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases_by_health_region())
        r.extend(self._get_mortality_by_health_region())
        return r

    def _get_cases_by_health_region(self):
        # "province","health_region","date_report","cases","cumulative_cases"
        # "Alberta","Calgary","25-01-2020",0,0
        # "Alberta","Calgary","26-01-2020",0,0
        # "Alberta","Calgary","27-01-2020",0,0

        r = []
        with open(self.get_path_in_dir('timeseries_hr/cases_timeseries_hr.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                if item['province'] == 'Repatriated':
                    continue
                date = self.convert_date(item['date_report'])
                province = province_to_iso_3166_2(item['province'])

                r.append(DataPoint(
                    region_schema=Schemas.CA_HEALTH_REGION,
                    region_parent=province,
                    region_child=health_region_to_uid(province, item['health_region']),
                    datatype=DataTypes.NEW,
                    value=int(item['cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.CA_HEALTH_REGION,
                    region_parent=province,
                    region_child=health_region_to_uid(province, item['health_region']),
                    datatype=DataTypes.TOTAL,
                    value=int(item['cumulative_cases']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_mortality_by_health_region(self):
        # "province","health_region","date_death_report","deaths","cumulative_deaths"
        # "Alberta","Calgary","08-03-2020",0,0
        # "Alberta","Calgary","09-03-2020",0,0
        # "Alberta","Calgary","10-03-2020",0,0

        r = []
        with open(self.get_path_in_dir('timeseries_hr/mortality_timeseries_hr.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                date = self.convert_date(item['date_death_report'])
                province = province_to_iso_3166_2(item['province'])

                r.append(DataPoint(
                    region_schema=Schemas.CA_HEALTH_REGION,
                    region_parent=province,
                    region_child=health_region_to_uid(province, item['health_region']),
                    datatype=DataTypes.STATUS_DEATHS_NEW,
                    value=int(item['deaths']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.CA_HEALTH_REGION,
                    region_parent=province,
                    region_child=health_region_to_uid(province, item['health_region']),
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['cumulative_deaths']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(CACovid19Canada().get_datapoints())
