import csv
import json
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_data_dir, get_package_dir
from covid_19_au_grab.geojson_data.LabelsToRegionChild import LabelsToRegionChild
from covid_19_au_grab.normalize_locality_name import normalize_locality_name
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


class VicCSV(URLBase):
    SOURCE_URL = 'https://www.dhhs.vic.gov.au/coronavirus'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'vic_dhhs_csv'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_data_dir() / 'vic' / 'csv_data',
             urls_dict={
                 'lga.json': URL('https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9oKYNQhJ6v85dQ9qsybfMfc-eaJ9oKVDZKx-VGUr6szNoTbvsLTzpEaJ3oW_LZTklZbz70hDBUt-d/pub?gid=0&single=true&output=csv',
                                 static_file=False),
                 'postcode.json': URL('https://docs.google.com/spreadsheets/d/e/2PACX-1vTwXSqlP56q78lZKxc092o6UuIyi7VqOIQj6RM4QmlVPgtJZfbgzv0a3X7wQQkhNu8MFolhVwMy4VnF/pub?gid=0&single=true&output=csv',
                                      static_file=False),
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_postcode_datapoints())
        r.extend(self._get_lga_datapoints())
        return r

    def _get_postcode_datapoints(self):
        # postcode	population	active	cases	rate	new	band	data_date
        # 	3000	37979	18	119	47.4	0	2	29/08/2020
        # 	3001	0	0	1	0	0	0	29/08/2020
        # 	3002	4957	2	14	40.3	0	2	29/08/2020
        # 	3003	5516	3	36	54.4	0	3	29/08/2020
        # 	3004	9311	6	63	64.4	2	3	29/08/2020
        # 	3005	523	0	0	0	0	0	29/08/2020
        # 	3006	18811	1	64	5.3	0	1	29/08/2020
        # 	3008	10438	2	49	19.2	0	1	29/08/2020
        # 	3010	1595	0	0	0	0	0	29/08/2020
        # 	3011	21464	36	164	167.7	2	4	29/08/2020

        r = DataPointMerger()

        for date in listdir(get_data_dir() / 'vic' / 'csv_data'):
            with open(get_data_dir() / 'vic' / 'csv_data' / date / 'postcode.json', 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    date_updated = self.convert_date(row['data_date'])

                    for datatype, value in (
                        (DataTypes.STATUS_ACTIVE, row['active']),
                        (DataTypes.TOTAL, row['cases'])
                    ):
                        r.append(DataPoint(
                            region_schema=Schemas.POSTCODE,
                            region_parent='AU-VIC',
                            region_child=row['postcode'],
                            datatype=datatype,
                            value=int(value),
                            date_updated=date_updated,
                            source_url=self.SOURCE_URL,
                            source_id=self.SOURCE_ID
                        ))

        return r

    def _get_lga_datapoints(self):
        # LGA	lga_pid	population	active	cases	rate	new	band	LGADisplay	data_date
        # 	Alpine (S)	VIC242	12814	0	1	0	0	0	Alpine	29/08/2020
        # 	Ararat (RC)	VIC220	11845	1	7	8.4	0	1	Ararat	29/08/2020
        # 	Ballarat (C)	VIC241	109505	6	61	5.5	0	1	Ballarat	29/08/2020
        # 	Banyule (C)	VIC188	131631	30	437	22.8	0	2	Banyule	29/08/2020
        # Bass Coast (S) VIC173	36320	0	11	0	0	0	Bass Coast	29/08/2020
        # 	Baw Baw (S)	VIC194	53396	1	15	1.9	0	1	Baw Baw	29/08/2020
        # 	Bayside (C)	VIC182	106862	72	227	67.4	6	3	Bayside	29/08/2020
        # 	Benalla (RC)	VIC199	14037	0	3	0	0	0	Benalla	29/08/2020

        r = DataPointMerger()

        for date in listdir(get_data_dir() / 'vic' / 'csv_data'):
            with open(get_data_dir() / 'vic' / 'csv_data' / date / 'lga.json', 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    date_updated = self.convert_date(row['data_date'])

                    for datatype, value in (
                        (DataTypes.STATUS_ACTIVE, row['active']),
                        (DataTypes.TOTAL, row['cases'])
                    ):
                        r.append(DataPoint(
                            region_schema=Schemas.LGA,
                            region_parent='AU-VIC',
                            region_child=normalize_locality_name(row['LGA'].split('(')[0].strip()),
                            datatype=datatype,
                            value=int(value),
                            date_updated=date_updated,
                            source_url=self.SOURCE_URL,
                            source_id=self.SOURCE_ID
                        ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(VicCSV().get_datapoints())
