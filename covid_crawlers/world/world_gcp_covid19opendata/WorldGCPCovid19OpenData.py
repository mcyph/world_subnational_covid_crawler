import csv

from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV
from covid_crawlers._base_classes.URLBase import URL, URLBase


class WorldGCPCovid19OpenData(URLBase):
    SOURCE_URL = 'https://github.com/GoogleCloudPlatform/covid-19-open-data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'world_gcp_covid19opendata'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'world' / 'world_gcp_covid19opendata',
             urls_dict={
                 'main.csv':
                     #URL('https://storage.googleapis.com/covid19-open-data/v2/main.csv',
                     #    static_file=False),
                     URL('https://storage.googleapis.com/covid19-open-data/v2/latest/main.csv',
                         static_file=False),
             }
        )
        self.spdf = StrictDataPointsFactory(
            {}, MODE_DEV
        )
        self.update()

    def get_datapoints(self):
        # key	date	wikidata	datacommons	country_code	country_name
        # subregion1_code	subregion1_name	subregion2_code	subregion2_name
        # locality_code	locality_name	3166-1-alpha-2	3166-1-alpha-3
        # aggregation_level	new_confirmed	new_deceased	new_recovered
        # new_tested	total_confirmed	total_deceased	total_recovered
        # total_tested	new_hospitalized	total_hospitalized	current_hospitalized
        # new_intensive_care	total_intensive_care	current_intensive_care
        # new_ventilator	total_ventilator	current_ventilator	population
        # population_male	population_female	rural_population	urban_population
        # largest_city_population	clustered_population	population_density
        # human_development_index	population_age_00_09	population_age_10_19
        # population_age_20_29	population_age_30_39	population_age_40_49
        # population_age_50_59	population_age_60_69	population_age_70_79
        # population_age_80_89	population_age_90_99	population_age_80_and_older
        # gdp	gdp_per_capita	human_capital_index	open_street_maps
        # latitude	longitude	elevation	area	rural_area	urban_area
        # life_expectancy	smoking_prevalence	diabetes_prevalence	infant_mortality_rate
        # adult_male_mortality_rate	adult_female_mortality_rate	pollution_mortality_rate
        # comorbidity_mortality_rate	hospital_beds	nurses	physicians	health_expenditure
        # out_of_pocket_health_expenditure	mobility_retail_and_recreation
        # mobility_grocery_and_pharmacy	mobility_parks	mobility_transit_stations
        # mobility_workplaces	mobility_residential	school_closing	workplace_closing
        # cancel_public_events	restrictions_on_gatherings	public_transport_closing
        # stay_at_home_requirements	restrictions_on_internal_movement
        # international_travel_controls	income_support	debt_relief	fiscal_measures
        # international_support	public_information_campaigns	testing_policy
        # contact_tracing	emergency_investment_in_healthcare	investment_in_vaccines
        # stringency_index	noaa_station	noaa_distance	average_temperature
        # minimum_temperature	maximum_temperature	rainfall	snowfall	dew_point
        # relative_humidity
        # AD	2021-01-03	Q228	country/AND	AD	Andorra
        # AD	AND	0	68	0			8117	84
        # 77142	58625	55581	9269	67873			163.842553	0.858	9370	12022
        # 10727	12394	21001	20720	14433	8657	3904	976	4881	3154057987	40886
        # 9407	42.558333	1.555278		470				33.5	7.7	2.7
        # 4.0128	3.3333	4040.786621	1688.12146							1	2	2	4	1
        # 1	0	2	2	2	0	0	2	3	2	0	0	59.26	8117099999	39.866801
        # 4.12963	-0.37037	9.805556	10.541	50.8	-0.796296	71.713644

        r = self.spdf()

        for date in self.iter_nonempty_dirs(self.output_dir):
            with open(self.output_dir / date / 'main.csv', 'r',
                      encoding='utf-8') as f:

                for item in csv.DictReader(f):
                    date = self.convert_date(item['date'])
                    admin0 = item['3166-1-alpha-2']
                    admin1 = item['subregion1_name']
                    admin2 = item['subregion2_name']
                    admin_level = int(item['aggregation_level'])

                    for datatype, value in (
                        (DataTypes.TOTAL, item['total_confirmed']),
                        (DataTypes.STATUS_DEATHS, item['total_deceased']),
                        (DataTypes.STATUS_RECOVERED, item['total_recovered']),
                        (DataTypes.TESTS_TOTAL, item['total_tested']),
                        (DataTypes.STATUS_HOSPITALIZED, item['current_hospitalized']),
                        (DataTypes.STATUS_HOSPITALIZED_RUNNINGTOTAL, item['total_hospitalized']),
                        (DataTypes.STATUS_ICU, item['current_intensive_care']),
                        (DataTypes.STATUS_ICU_RUNNINGTOTAL, item['total_intensive_care']),
                        (DataTypes.STATUS_ICU_VENTILATORS, item['current_ventilator']),
                        (DataTypes.STATUS_ICU_VENTILATORS_RUNNINGTOTAL, item['total_ventilator']),

                        (DataTypes.NEW, item['new_confirmed']),
                        (DataTypes.STATUS_DEATHS_NEW, item['new_deceased']),
                        (DataTypes.STATUS_RECOVERED_NEW, item['new_recovered']),
                        (DataTypes.TESTS_NEW, item['new_tested']),
                        (DataTypes.STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW, item['new_hospitalized']),
                        (DataTypes.STATUS_ICU_RUNNINGTOTAL_NEW, item['new_intensive_care']),
                        (DataTypes.STATUS_ICU_VENTILATORS_RUNNINGTOTAL_NEW, item['new_ventilator']),
                    ):
                        if not value:
                            continue

                        if admin_level == 0:
                            r.append(
                                region_schema=Schemas.ADMIN_0,
                                region_parent='',
                                region_child=admin0,
                                datatype=datatype,
                                value=int(value),
                                date_updated=date,
                                source_url=self.SOURCE_URL
                            )
                        elif admin_level == 1:
                            r.append(
                                region_schema=Schemas.ADMIN_1,
                                region_parent=admin0,
                                region_child=admin1,
                                datatype=datatype,
                                value=int(value),
                                date_updated=date,
                                source_url=self.SOURCE_URL
                            )
                        elif admin_level == 2:
                            continue  # TODO!!! =====================================================
                        elif admin_level == 3:
                            continue  # TODO!
                        else:
                            raise Exception(admin_level)
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(WorldGCPCovid19OpenData().get_datapoints())
