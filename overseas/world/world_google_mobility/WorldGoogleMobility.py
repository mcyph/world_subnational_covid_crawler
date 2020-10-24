import csv
from datetime import datetime

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV
from covid_19_au_grab.normalize_locality_name import normalize_locality_name


class WorldGoogleMobility(URLBase):
    SOURCE_URL = 'https://www.google.com/covid19/mobility/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'world_google_mobility'

    def __init__(self):
        URLBase.__init__(self,
                         output_dir=get_overseas_dir() / 'world_google_mobility' / 'data',
                         urls_dict={
                             'mobility.csv': URL(url='https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv',
                                                 static_file=False)
                         })

        self.update()
        self.sdpf = StrictDataPointsFactory(mode=MODE_DEV)

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        # country_region_code,country_region,sub_region_1,sub_region_2,metro_area,iso_3166_2_code,census_fips_code,
        # date,
        # retail_and_recreation_percent_change_from_baseline,
        # grocery_and_pharmacy_percent_change_from_baseline,
        # parks_percent_change_from_baseline,
        # transit_stations_percent_change_from_baseline,
        # workplaces_percent_change_from_baseline,
        # residential_percent_change_from_baseline

        # AE,United Arab Emirates,,,,,,2020-02-15,0,4,5,0,2,1
        # AE,United Arab Emirates,,,,,,2020-02-16,1,4,4,1,2,1
        # AE,United Arab Emirates,,,,,,2020-02-17,-1,1,5,1,2,1
        # AE,United Arab Emirates,,,,,,2020-02-18,-2,1,5,0,2,1

        r = self.sdpf()

        date = datetime.today().strftime('%Y_%m_%d')
        path = get_overseas_dir() / 'world_google_mobility' / 'data' / date / 'mobility.csv'

        with open(path, 'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                if item['iso_3166_2_code']:
                    region_schema = Schemas.ADMIN_1
                    region_parent = item['country_region_code']
                    region_child = item['iso_3166_2_code']
                elif item['sub_region_2'] and item['country_region_code'] == 'AU':
                    region_schema = Schemas.LGA
                    region_parent = item['sub_region_1']
                    region_child = normalize_locality_name(item['sub_region_2'])
                elif not item['sub_region_1'] and not item['sub_region_2']:
                    region_schema = Schemas.ADMIN_0
                    region_parent = ''
                    region_child = item['country_region_code']
                else:
                    continue

                for datatype, value in (
                    (DataTypes.GOOGLE_MOBILITY_RETAIL_RECREATION, item['retail_and_recreation_percent_change_from_baseline']),
                    (DataTypes.GOOGLE_MOBILITY_SUPERMARKET_PHARMACY, item['grocery_and_pharmacy_percent_change_from_baseline']),
                    (DataTypes.GOOGLE_MOBILITY_PARKS, item['parks_percent_change_from_baseline']),
                    (DataTypes.GOOGLE_MOBILITY_PUBLIC_TRANSPORT, item['transit_stations_percent_change_from_baseline']),
                    (DataTypes.GOOGLE_MOBILITY_WORKPLACES, item['workplaces_percent_change_from_baseline']),
                    (DataTypes.GOOGLE_MOBILITY_RESIDENTIAL, item['residential_percent_change_from_baseline'])
                ):
                    if not value:
                        continue

                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=datatype,
                        value=int(value),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r


if __name__ == "__main__":
    from pprint import pprint
    inst = WorldGoogleMobility()
    pprint(inst.get_datapoints())
