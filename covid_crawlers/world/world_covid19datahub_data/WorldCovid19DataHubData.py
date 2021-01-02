import csv
from datetime import datetime

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV


class WorldCovid19DataHubData(URLBase):
    SOURCE_ID = 'world_covid19datahub'
    SOURCE_URL = 'https://covid19datahub.io/articles/data.html'
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'world_covid19datahub' / 'data',
            urls_dict={
                'rawdata-1.csv': URL(url='https://storage.covid19datahub.io/rawdata-1.csv', static_file=False),
                'rawdata-2.csv': URL(url='https://storage.covid19datahub.io/rawdata-2.csv', static_file=False),
                'rawdata-3.csv': URL(url='https://storage.covid19datahub.io/rawdata-3.csv', static_file=False),
            }
        )
        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_DEV)  # NOTE ME!!!

    def get_datapoints(self):
        r = []
        date = datetime.today().strftime('%Y_%m_%d')
        r.extend(self._get_admin0(date))
        r.extend(self._get_admin1(date))
        r.extend(self._get_admin2(date))
        return r

    def _get_admin0(self, date):
        # id	date	tests	confirmed	recovered	deaths	hosp
        # vent	icu	population	school_closing	workplace_closing
        # cancel_events	gatherings_restrictions	transport_closing
        # stay_home_restrictions	internal_movement_restrictions
        # international_movement_restrictions	information_campaigns
        # testing_policy	contact_tracing	stringency_index
        # iso_alpha_3	iso_alpha_2	iso_numeric	currency
        # administrative_area_level	administrative_area_level_1
        # administrative_area_level_2	administrative_area_level_3
        # latitude	longitude	key	key_apple_mobility	key_google_mobility
        # AFG	2020-01-22								37172386	0	0	0	0	0	0	0	0	0	0	0	0	AFG	AF	4	AFN	1	Afghanistan			33	65			AF

        r = self.sdpf()
        path = get_overseas_dir() / 'world_covid19datahub' / 'data' / date / 'rawdata-1.csv'

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                self._add_datapoints(r,
                                     region_schema=Schemas.ADMIN_0,
                                     region_parent='',
                                     region_child=item['administrative_area_level_1'],
                                     item=item)
        return r

    def _get_admin1(self, date):
        # id	date	tests	confirmed	recovered	deaths	hosp
        # vent	icu	population	school_closing	workplace_closing
        # cancel_events	gatherings_restrictions	transport_closing
        # stay_home_restrictions	internal_movement_restrictions
        # international_movement_restrictions	information_campaigns
        # testing_policy	contact_tracing	stringency_index
        # iso_alpha_3	iso_alpha_2	iso_numeric	currency
        # administrative_area_level	administrative_area_level_1
        # administrative_area_level_2	administrative_area_level_3
        # latitude	longitude	key	key_google_mobility	key_apple_mobility
        # key_numeric	key_alpha_2
        # 0023de7a	2020-01-22								29802								0	1	1	0	5.56	GBR	GB	826	GBP	2	United Kingdom	British Virgin Islands		18.4207	-64.64

        r = self.sdpf()
        path = get_overseas_dir() / 'world_covid19datahub' / 'data' / date / 'rawdata-2.csv'

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                self._add_datapoints(r,
                                     region_schema=Schemas.ADMIN_1,
                                     region_parent=item['administrative_area_level_1'],
                                     region_child=item['administrative_area_level_2'],
                                     item=item)
        return r

    def _get_admin2(self, date):
        # id	date	tests	confirmed	recovered	deaths	hosp
        # vent	icu	population	school_closing	workplace_closing
        # cancel_events	gatherings_restrictions	transport_closing
        # stay_home_restrictions	internal_movement_restrictions
        # international_movement_restrictions	information_campaigns
        # testing_policy	contact_tracing	stringency_index
        # iso_alpha_3	iso_alpha_2	iso_numeric	currency
        # administrative_area_level	administrative_area_level_1
        # administrative_area_level_2	administrative_area_level_3
        # latitude	longitude	key	key_numeric	key_google_mobility
        # key_apple_mobility	key_alpha_2
        # 0007cb93	2020-03-30		1		0				5257	3	2	1	3	0	2	1	3	2	1	1	62.96	USA	US	840	USN	3	United States	Georgia	Schley	32.2654021	-84.31258912		13249	Georgia, Schley County

        r = self.sdpf()
        path = get_overseas_dir() / 'world_covid19datahub' / 'data' / date / 'rawdata-3.csv'

        with open(path, 'r', encoding='utf-8-sig') as f:
            for item in csv.DictReader(f):
                admin0 = item['administrative_area_level_1']

                if admin0 == 'United States': schema = Schemas.US_COUNTY
                elif admin0 == 'Netherlands': continue
                elif admin0 == 'Colombia': schema = Schemas.CO_MUNICIPALITY
                elif admin0 == 'Germany': schema = Schemas.DE_KREIS
                elif admin0 == 'Czech Republic': schema = Schemas.CZ_OKRES
                elif admin0 == 'Chile': continue
                elif admin0 == 'Brazil': schema = Schemas.BR_CITY
                elif admin0 == 'United Kingdom': continue #schema = Schemas.UK_AREA
                elif admin0 == 'Poland': continue
                elif admin0 == 'Austria': continue
                elif admin0 == 'France': continue
                elif admin0 == 'Italy': schema = Schemas.IT_PROVINCE
                elif admin0 == 'Puerto Rico': continue
                else: raise ValueError(admin0)

                self._add_datapoints(r,
                                     region_schema=schema,
                                     region_parent=item['administrative_area_level_2'],
                                     region_child=item['administrative_area_level_3'],
                                     item=item)
        return r

    def _add_datapoints(self, r, region_schema, region_parent, region_child, item):
        date = self.convert_date(item['date'])

        d = {}
        if item['tests']:
            d[DataTypes.TESTS_TOTAL] = int(float(item['tests']))
        if item['confirmed']:
            d[DataTypes.TOTAL] = int(float(item['confirmed']))
        if item['recovered']:
            d[DataTypes.STATUS_RECOVERED] = int(float(item['recovered']))
        if item['deaths']:
            d[DataTypes.STATUS_DEATHS] = int(float(item['deaths']))
        if item['hosp']:
            d[DataTypes.STATUS_HOSPITALIZED] = int(float(item['hosp']))
        if item['vent']:
            d[DataTypes.STATUS_ICU_VENTILATORS] = int(float(item['vent']))
        if item['icu']:
            d[DataTypes.STATUS_ICU] = int(float(item['icu']))

        if DataTypes.TOTAL in d and \
           DataTypes.STATUS_RECOVERED in d and \
           DataTypes.STATUS_DEATHS in d:

            d[DataTypes.STATUS_ACTIVE] = \
                d[DataTypes.TOTAL] - \
                d[DataTypes.STATUS_RECOVERED] - \
                d[DataTypes.STATUS_DEATHS]

        for datatype, value in d.items():
            r.append(
                region_schema=region_schema,
                region_parent=region_parent,
                region_child=region_child,
                datatype=datatype,
                value=value,
                date_updated=date,
            )


if __name__ == '__main__':
    from pprint import pprint
    pprint(WorldCovid19DataHubData().get_datapoints())
