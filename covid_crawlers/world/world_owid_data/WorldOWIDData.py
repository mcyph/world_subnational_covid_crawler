# https://github.com/owid/covid-19-data

import csv

from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_crawlers._base_classes.GithubRepo import GithubRepo
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.covid_crawlers.world.world_jhu_data.get_county_to_code_map import get_county_to_code_map
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_crawlers.world.world_jhu_data.world_jhu_mappings import world_jhu_mappings

county_to_code_map = get_county_to_code_map()


class WorldOWIDData(GithubRepo):
    SOURCE_ID = 'world_owid'
    SOURCE_URL = 'https://github.com/owid/covid-19-data'
    SOURCE_DESCRIPTION = ''

    def __init__(self, do_update=True):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'world_owid' / 'covid-19-data',
                            github_url='https://github.com/owid/covid-19-data')
        self.spdf = StrictDataPointsFactory(
            region_mappings=world_jhu_mappings,
            mode=MODE_STRICT
        )
        if do_update:
            self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = self.spdf()

        with open(self.get_path_in_dir(f'public/data/owid-covid-data.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                # iso_code,continent,location,date,total_cases,new_cases,new_cases_smoothed,total_deaths,new_deaths,
                # new_deaths_smoothed,total_cases_per_million,new_cases_per_million,new_cases_smoothed_per_million,
                # total_deaths_per_million,new_deaths_per_million,new_deaths_smoothed_per_million,new_tests,total_tests,
                # total_tests_per_thousand,new_tests_per_thousand,new_tests_smoothed,new_tests_smoothed_per_thousand,
                # tests_per_case,positive_rate,tests_units,stringency_index,population,population_density,median_age,
                # aged_65_older,aged_70_older,gdp_per_capita,extreme_poverty,cardiovasc_death_rate,diabetes_prevalence,
                # female_smokers,male_smokers,handwashing_facilities,hospital_beds_per_thousand,life_expectancy
                #
                # ABW,North America,Aruba,2020-03-13,2.0,2.0,,0.0,0.0,,18.733,18.733,,0.0,0.0,,,,,,,,,,,0.0,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29
                # ABW,North America,Aruba,2020-03-19,,,0.286,,,0.0,,,2.676,,,0.0,,,,,,,,,,33.33,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29
                # ABW,North America,Aruba,2020-03-20,4.0,2.0,0.286,0.0,0.0,0.0,37.465,18.733,2.676,0.0,0.0,0.0,,,,,,,,,,33.33,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29
                # ABW,North America,Aruba,2020-03-21,,,0.286,,,0.0,,,2.676,,,0.0,,,,,,,,,,44.44,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29
                # ABW,North America,Aruba,2020-03-22,,,0.286,,,0.0,,,2.676,,,0.0,,,,,,,,,,44.44,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29
                # ABW,North America,Aruba,2020-03-23,,,0.286,,,0.0,,,2.676,,,0.0,,,,,,,,,,44.44,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29
                # ABW,North America,Aruba,2020-03-24,12.0,8.0,1.429,0.0,0.0,0.0,112.395,74.93,13.38,0.0,0.0,0.0,,,,,,,,,,44.44,106766.0,584.8,41.2,13.085,7.452,35973.781,,,11.62,,,,,76.29

                # Will only use tests+metadata

                if item['total_tests']:
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_parent='',
                        region_child=item['location'],
                        datatype=DataTypes.TESTS_TOTAL,
                        value=int(float(item['total_tests'])),
                        source_url=self.SOURCE_URL,
                        date_updated=self.convert_date(item['date'])
                    )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(WorldOWIDData().get_datapoints())
