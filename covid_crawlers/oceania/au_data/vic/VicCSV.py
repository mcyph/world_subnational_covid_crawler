import csv
from os import listdir
from collections import Counter

from _utility.cache_by_date import cache_by_date
from _utility.get_package_dir import get_data_dir
from _utility.normalize_locality_name import normalize_locality_name
from covid_db.datatypes.DataPoint import DataPoint
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DatapointMerger import DataPointMerger
from covid_crawlers._base_classes.URLBase import URL, URLBase


class ExpiringCounter(Counter):
    def __init__(self, *args, **kw):
        Counter.__init__(self, *args, **kw)
        self.__changed = set()

    def items(self):
        for k in self.__changed:
            yield k, self[k]
        self.__changed = set()

    def __setitem__(self, key, value):
        Counter.__setitem__(self, key, value)
        self.__changed.add(key)


class VicCSV(URLBase):
    SOURCE_ID = 'au_vic_dhhs_csv'
    SOURCE_URL = 'https://www.dhhs.vic.gov.au/coronavirus'
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_data_dir() / 'vic' / 'csv_data',
             urls_dict={
                 'lga.json': URL('https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9oKYNQhJ6v85dQ9qsybfMfc-eaJ9oKVDZKx-VGUr6szNoTbvsLTzpEaJ3oW_LZTklZbz70hDBUt-d/pub?gid=0&single=true&output=csv',
                                 static_file=False),
                 'postcode.json': URL('https://docs.google.com/spreadsheets/d/e/2PACX-1vTwXSqlP56q78lZKxc092o6UuIyi7VqOIQj6RM4QmlVPgtJZfbgzv0a3X7wQQkhNu8MFolhVwMy4VnF/pub?gid=0&single=true&output=csv',
                                      static_file=False),
                 'agegroup.csv': URL('https://www.dhhs.vic.gov.au/ncov-covid-cases-by-age-group-csv',
                                     static_file=False),
                 'all_lga.csv': URL('https://www.dhhs.vic.gov.au/ncov-covid-cases-by-lga-csv',
                                    static_file=False),
                 'all_lga_acquired_source': URL('https://www.dhhs.vic.gov.au/ncov-covid-cases-by-lga-source-csv',
                                                static_file=False),
                 'all_acquired_source': URL('https://www.dhhs.vic.gov.au/ncov-covid-cases-by-source-csv',
                                            static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = DataPointMerger()
        for date in r.iter_unprocessed_dates(sorted(listdir(get_data_dir() / 'vic' / 'csv_data'))):
            r.extend(self._get_postcode_datapoints(date))
            r.extend(self._get_lga_datapoints(date))

            if (get_data_dir() / 'vic' / 'csv_data' / date / 'agegroup.csv').exists():
                r.extend(self._get_agegroup_datapoints(date))
            if (get_data_dir() / 'vic' / 'csv_data' / date / 'all_lga.csv').exists():
                r.extend(self._get_all_lga_datapoints(date))
            if (get_data_dir() / 'vic' / 'csv_data' / date / 'all_lga_acquired_source').exists():
                r.extend(self._get_all_lga_acquired_source_datapoints(date))
            if (get_data_dir() / 'vic' / 'csv_data' / date / 'all_acquired_source').exists():
                r.extend(self._get_all_acquired_source_datapoints(date))
        return r

    @cache_by_date(SOURCE_ID + '_all_lga_acquired_source')
    def _get_all_lga_acquired_source_datapoints(self, date):
        r = []
        current_date = None
        by_postcode = {}
        by_lga = {}

        sources = {
            'Acquired in Australia, unknown source': DataTypes.SOURCE_COMMUNITY,
            'Contact with a confirmed case': DataTypes.SOURCE_CONFIRMED,
            'Travel overseas': DataTypes.SOURCE_OVERSEAS,
            'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION
        }

        with open(get_data_dir() / 'vic' / 'csv_data' / date / 'all_lga_acquired_source', 'r', encoding='utf-8') as f:
            for row in sorted(csv.DictReader(f), key=lambda x: x['diagnosis_date']) + \
                       [{'diagnosis_date': '1111-01-01',
                         'Postcode': None,
                         'Localgovernmentarea': None,
                         'acquired': None}]:

                date_updated = self.convert_date(row['diagnosis_date'])

                if current_date != date_updated:
                    if current_date is not None:
                        #for postcode, by_source in by_postcode.items():
                        #    for source, value in by_source.items():
                        #        r.append(DataPoint(
                        #            region_schema=Schemas.POSTCODE,
                        #            region_parent='AU-VIC',
                        #            region_child=postcode,
                        #            datatype=sources[source],
                        #            value=int(value),
                        #            date_updated=current_date,
                        #            source_url=self.SOURCE_URL,
                        #            source_id=self.SOURCE_ID
                        #        ))
                        for lga, by_source in by_lga.items():
                            for source, value in by_source.items():
                                r.append(DataPoint(
                                    region_schema=Schemas.LGA,
                                    region_parent='AU-VIC',
                                    region_child=normalize_locality_name(lga),
                                    datatype=sources[source],
                                    value=int(value),
                                    date_updated=current_date,
                                    source_url=self.SOURCE_URL,
                                    source_id=self.SOURCE_ID
                                ))
                    current_date = date_updated

                if row['Localgovernmentarea']:
                    by_lga.setdefault(row['Localgovernmentarea'].split('(')[0].strip(), ExpiringCounter())[row['acquired']] += 1
                if row['Postcode']:
                    by_postcode.setdefault(row['Localgovernmentarea'].strip('_'), ExpiringCounter())[row['acquired']] += 1

        return r

    @cache_by_date(SOURCE_ID + '_all_acquired_source')
    def _get_all_acquired_source_datapoints(self, date):
        r = []
        current_date = None
        by_source = Counter()

        sources = {
            'Acquired in Australia, unknown source': DataTypes.SOURCE_COMMUNITY,
            'Contact with a confirmed case': DataTypes.SOURCE_CONFIRMED,
            'Travel overseas': DataTypes.SOURCE_OVERSEAS,
            'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION
        }

        with open(get_data_dir() / 'vic' / 'csv_data' / date / 'all_acquired_source', 'r', encoding='utf-8') as f:
            for row in sorted(csv.DictReader(f), key=lambda x: x['diagnosis_date']) + \
                       [{'diagnosis_date': '1111-01-01', 'acquired': None}]:

                date_updated = self.convert_date(row['diagnosis_date'])

                if current_date != date_updated:
                    if current_date is not None:
                        for source, value in by_source.items():
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='AU',
                                region_child='AU-VIC',
                                datatype=sources[source],
                                value=int(value),
                                date_updated=current_date,
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                    current_date = date_updated

                if row['acquired']:
                    by_source[row['acquired'].strip('_')] += 1
        return r

    @cache_by_date(SOURCE_ID + '_all_lga')
    def _get_all_lga_datapoints(self, date):
        r = []
        current_date = None
        by_agegroup = ExpiringCounter()

        with open(get_data_dir() / 'vic' / 'csv_data' / date / 'all_lga.csv', 'r', encoding='utf-8') as f:
            for row in sorted(csv.DictReader(f), key=lambda x: x['diagnosis_date']) + \
                       [{'diagnosis_date': '1111-01-01', 'Localgovernmentarea': None}]:

                date_updated = self.convert_date(row['diagnosis_date'])

                if current_date != date_updated:
                    if current_date is not None:
                        for lga, value in by_agegroup.items():
                            r.append(DataPoint(
                                region_schema=Schemas.LGA,
                                region_parent='AU-VIC',
                                region_child=normalize_locality_name(lga.split('(')[0].strip()),
                                datatype=DataTypes.TOTAL,
                                value=int(value),
                                date_updated=current_date,
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                    current_date = date_updated

                if row['Localgovernmentarea']:
                    by_agegroup[row['Localgovernmentarea'].strip('_')] += 1
        return r

    @cache_by_date(SOURCE_ID+'_agegroup')
    def _get_agegroup_datapoints(self, date):
        r = []
        current_date = None
        by_agegroup = Counter()

        with open(get_data_dir() / 'vic' / 'csv_data' / date / 'agegroup.csv', 'r', encoding='utf-8') as f:
            for row in sorted(csv.DictReader(f), key=lambda x: x['diagnosis_date']) + \
                       [{'diagnosis_date': '1111-01-01', 'agegroup': None}]:

                assert len(row['diagnosis_date']) == 10
                date_updated = self.convert_date(row['diagnosis_date'])

                if current_date != date_updated:
                    if current_date is not None:
                        for agerange, value in by_agegroup.items():
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='AU',
                                region_child='AU-VIC',
                                datatype=DataTypes.TOTAL,
                                agerange=agerange,
                                value=int(value),
                                date_updated=current_date,
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                    current_date = date_updated

                if row['agegroup']:
                    by_agegroup[row['agegroup'].strip('_')] += 1
        return r

    @cache_by_date(SOURCE_ID)
    def _get_postcode_datapoints(self, date):
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

        r = []
        print("PostCode:", get_data_dir() / 'vic' / 'csv_data' / date)

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

    @cache_by_date(SOURCE_ID+'_lga')
    def _get_lga_datapoints(self, date):
        # LGA	lga_pid	population	active	cases	rate	new	band	LGADisplay	data_date
        # 	Alpine (S)	VIC242	12814	0	1	0	0	0	Alpine	29/08/2020
        # 	Ararat (RC)	VIC220	11845	1	7	8.4	0	1	Ararat	29/08/2020
        # 	Ballarat (C)	VIC241	109505	6	61	5.5	0	1	Ballarat	29/08/2020
        # 	Banyule (C)	VIC188	131631	30	437	22.8	0	2	Banyule	29/08/2020
        # Bass Coast (S) VIC173	36320	0	11	0	0	0	Bass Coast	29/08/2020
        # 	Baw Baw (S)	VIC194	53396	1	15	1.9	0	1	Baw Baw	29/08/2020
        # 	Bayside (C)	VIC182	106862	72	227	67.4	6	3	Bayside	29/08/2020
        # 	Benalla (RC)	VIC199	14037	0	3	0	0	0	Benalla	29/08/2020

        r = []
        print("LGA:", get_data_dir() / 'vic' / 'csv_data' / date)

        with open(get_data_dir() / 'vic' / 'csv_data' / date / 'lga.json', 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                #print(row)
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
