import csv
import json
from os.path import exists
from os import makedirs, listdir
from collections import Counter
from urllib.request import urlretrieve
from datetime import datetime, timedelta

from _utility.get_package_dir import get_data_dir, get_package_dir
from _utility.cache_by_date import cache_by_date
from covid_db.datatypes.DataPoint import DataPoint
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DatapointMerger import DataPointMerger


POSTCODE_TO_LGA_PATH = \
    get_package_dir() / 'covid_crawlers' / 'oceania' / \
    'au_data' / 'nsw' / 'postcode_to_lga.json'

with open(POSTCODE_TO_LGA_PATH, 'r', encoding='utf-8') as f:
    POSTCODE_TO_LGA = json.loads(f.read())


class NSWJSONOpenData:
    SOURCE_ID = 'au_nsw_open_data'
    SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data'
    SOURCE_DESCRIPTION = ''

    def get_datapoints(self):
        date = (
            datetime.now() - timedelta(hours=20, minutes=30)
        ).strftime('%Y_%m_%d')

        dates = sorted(listdir(get_data_dir() / 'nsw' / 'open_data'))
        if not date in dates:
            dates.append(date)

        open_data = DataPointMerger()
        for i_date in dates:
            download = i_date == date
            for datapoint in self.__get_open_datapoints(i_date, download=download):
                open_data.append(datapoint)

        r = []
        r.extend(open_data)
        return r

    @cache_by_date(SOURCE_ID)
    def __get_open_datapoints(self, date, download=True):
        dir_ = get_data_dir() / 'nsw' / 'open_data' / date
        if not exists(dir_):
            makedirs(dir_)

        # Add open data
        open_data = []
        open_data.extend(self.get_nsw_cases_data(dir_, download=download))
        open_data.extend(self.get_nsw_tests_data(dir_, download=download))
        open_data.extend(self.__postcode_datapoints_to_lga('https://data.nsw.gov.au/nsw-covid-19-data', open_data,
                                                           source_id=self.SOURCE_ID))
        return open_data

    def __postcode_datapoints_to_lga(self, SOURCE_URL, r, source_id):
        # Convert postcode to LGA where possible
        new_r = DataPointMerger()
        added_to_lga = set()
        processed_postcode = set()
        mapping = Counter()

        for datapoint in sorted(r, key=lambda i: i.date_updated):
            if datapoint.region_schema == Schemas.LGA:
                added_to_lga.add((
                    datapoint.region_child,
                    datapoint.datatype
                ))
                continue
            elif datapoint.region_schema != Schemas.POSTCODE:
                continue
            elif datapoint.region_child in POSTCODE_TO_LGA:
                lga = POSTCODE_TO_LGA[datapoint.region_child]
            else:
                lga = 'unknown'
                if datapoint.region_child != 'unknown':
                    print("NOT FOUND:", datapoint.region_child)
                # continue  # WARNINIG!!! ================================================================================

            if (datapoint.region_child, datapoint.datatype, datapoint.date_updated) in processed_postcode:
                #print("IGNORING DOUBLE-UP:", datapoint)
                continue
            processed_postcode.add((datapoint.region_child, datapoint.datatype, datapoint.date_updated))

            #if lga == 'cumberland':
            #    print('USING:', datapoint)

            mapping[
                lga,
                datapoint.datatype,
                datapoint.date_updated
            ] += datapoint.value

        new_r.extend(r)

        for (lga, datatype, date_updated), value in mapping.items():
            if (lga, datatype) in added_to_lga:
                # Don't add to LGA if available using direct data!
                continue

            new_r.append(DataPoint(
                region_schema=Schemas.LGA,
                region_parent='AU-NSW',
                region_child=lga,
                datatype=datatype,
                value=value,
                date_updated=date_updated,
                source_url=SOURCE_URL,
                source_id=source_id
            ))

        return new_r

    #=============================================================================#
    # Postcode-level open cases json data
    #=============================================================================#

    # notification_date,postcode,likely_source_of_infection,
    #   lhd_2010_code,lhd_2010_name,lga_code19,lga_name19
    # 2020-01-22,2134,Overseas,X700,Sydney,11300,Burwood (A)

    def get_nsw_cases_data(self, dir_, download=True):
        DEFAULT_REGION = 'Unknown'
        SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data/cases'

        by_postcode = {}
        by_lhd = {}
        by_lga = {}

        # soi=source of infection
        by_postcode_soi = {}
        by_lhd_soi = {}
        by_lga_soi = {}
        by_admin_1_soi = {}  # Statewide

        soi_map = {
            'Overseas': DataTypes.SOURCE_OVERSEAS,
            'Locally acquired - contact not identified': DataTypes.SOURCE_COMMUNITY,
            'Locally acquired - contact not yet identified': DataTypes.SOURCE_COMMUNITY,
            'Locally acquired - source not identified': DataTypes.SOURCE_COMMUNITY,
            'Locally acquired - no links to known case or cluster': DataTypes.SOURCE_COMMUNITY,
            'Locally acquired - contact of a confirmed case and/or in a known cluster': DataTypes.SOURCE_CONFIRMED,
            'Locally acquired - linked to known case or cluster': DataTypes.SOURCE_CONFIRMED,
            'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION,
            'Interstate': DataTypes.SOURCE_INTERSTATE
        }

        # Make dates from 8:30pm!
        path = (
            dir_ / 'covid-19-cases-by-notification-date-location-and-likely-source-of-infection.csv'
        )

        if not exists(path):
            if not download:
                return []
            urlretrieve(
                'https://data.nsw.gov.au/data/dataset/97ea2424-abaf-4f3e-a9f2-b5c883f42b6a/resource/2776dbb8-f807-4fb2-b1ed-184a6fc2c8aa/download/covid-19-cases-by-notification-date-location-and-likely-source-of-infection.csv',
                path
            )

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if '/' in row['notification_date']:
                    pad = lambda i: '%02d' % int(i)
                    dd, mm, yyyy = row['notification_date'].split('/')
                    date = f'{yyyy}_{pad(mm)}_{pad(dd)}'
                else:
                    # Date already in the format I use, aside from hyphens
                    date = row['notification_date'].replace('-', '_')

                by_postcode.setdefault(date, {}) \
                    .setdefault(row['postcode'], []) \
                    .append(row)
                by_lhd.setdefault(date, {}) \
                    .setdefault(row['lhd_2010_name'], []) \
                    .append(row)
                by_lga.setdefault(date, {}) \
                    .setdefault(row['lga_name19'], []) \
                    .append(row)

                soi = soi_map[row['likely_source_of_infection']]
                by_postcode_soi.setdefault(date, {}) \
                    .setdefault(row['postcode'], {}) \
                    .setdefault(soi, []).append(row)
                by_lhd_soi.setdefault(date, {}) \
                    .setdefault(row['lhd_2010_name'], {}) \
                    .setdefault(soi, []).append(row)
                by_lga_soi.setdefault(date, {}) \
                    .setdefault(row['lga_name19'], {}) \
                    .setdefault(soi, []).append(row)
                by_admin_1_soi.setdefault(date, {}) \
                    .setdefault('AU-NSW', {}) \
                    .setdefault(soi, []).append(row)

                lga = row['lga_name19'].split('(')[0].strip().lower() or 'unknown'
                if row['postcode'] in POSTCODE_TO_LGA:
                    assert POSTCODE_TO_LGA[row['postcode']] == lga, lga
                else:
                    POSTCODE_TO_LGA[row['postcode']] = lga

        r = []

        # Add general totals
        for region_schema, cases_dict in (
            (Schemas.POSTCODE, by_postcode),
            (Schemas.LGA, by_lga),
            (Schemas.LHD, by_lhd)
        ):
            current_counts = {}

            for date, schema_dict in sorted(cases_dict.items()):
                for region_child, cases in schema_dict.items():
                    current_counts.setdefault(region_child, 0)
                    current_counts[region_child] += len(cases)

                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent='AU-NSW',
                        region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                        datatype=DataTypes.TOTAL,
                        value=current_counts[region_child],
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None,
                        source_id=self.SOURCE_ID
                    ))

        # Add by source of infection
        for region_schema, cases_dict in (
            (Schemas.POSTCODE, by_postcode_soi),
            (Schemas.LGA, by_lga_soi),
            (Schemas.LHD, by_lhd_soi),
            (Schemas.ADMIN_1, by_admin_1_soi)
        ):
            current_counts = {}

            for date, schema_dict in sorted(cases_dict.items()):
                for region_child, soi_dict in schema_dict.items():
                    for soi, cases in soi_dict.items():
                        current_counts.setdefault((region_child, soi), 0)
                        current_counts[region_child, soi] += len(cases)

                        r.append(DataPoint(
                            region_schema=region_schema,
                            region_parent=(
                                 'AU-NSW'
                                 if region_schema == Schemas.ADMIN_1
                                 else 'AU'
                            ),
                            region_child=(
                                region_child.split('(')[0].strip() or
                                DEFAULT_REGION
                            ),
                            datatype=soi,
                            value=current_counts[region_child, soi],
                            date_updated=date,
                            source_url=SOURCE_URL,
                            text_match=None,
                            source_id=self.SOURCE_ID
                        ))

        return r

    #=============================================================================#
    # Postcode-level open tests json data
    #=============================================================================#

    # test_date,postcode,lhd_2010_code,lhd_2010_name,lga_code19,lga_name19,result
    # 2020-01-08,2071,X760,Northern Sydney,14500,Ku-ring-gai (A),Tested & excluded

    def get_nsw_tests_data(self, dir_, download=True):
        DEFAULT_REGION = 'Unknown'
        SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data/tests'

        by_postcode = {}
        by_lhd = {}
        by_lga = {}

        by_postcode_posneg = {}
        by_lhd_posneg = {}
        by_lga_posneg = {}

        # Make dates from 8:30pm!
        path = (
            dir_ / 'covid-19-tests-by-date-and-location-and-result.csv'
        )

        if not exists(path) and download:
            urlretrieve(
                'https://data.nsw.gov.au/data/dataset/5424aa3b-550d-4637-ae50-7f458ce327f4/resource/227f6b65-025c-482c-9f22-a25cf1b8594f/download/covid-19-tests-by-date-and-location-and-result.csv',
                path
            )
        elif not exists(path):
            return []

        posneg_map = {
            'Tested & excluded': DataTypes.TESTS_NEGATIVE,
            'Case - Confirmed': DataTypes.TESTS_POSITIVE
        }

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if '/' in row['test_date']:
                    pad = lambda i: '%02d' % int(i)
                    dd, mm, yyyy = row['test_date'].split('/')
                    date = f'{yyyy}_{pad(mm)}_{pad(dd)}'
                else:
                    # Date already in the format I use, aside from hyphens
                    date = row['test_date'].replace('-', '_')

                by_postcode.setdefault(date, {}) \
                    .setdefault(row['postcode'], []) \
                    .append(row)
                by_lhd.setdefault(date, {}) \
                    .setdefault(row['lhd_2010_name'], []) \
                    .append(row)
                by_lga.setdefault(date, {}) \
                    .setdefault(row['lga_name19'], []) \
                    .append(row)

                if row['result'] is None:
                    print("WARNING!!!")
                    continue

                posneg = posneg_map[row['result']]
                by_postcode_posneg.setdefault(date, {}) \
                    .setdefault(row['postcode'], {}) \
                    .setdefault(posneg, []).append(row)
                by_lhd_posneg.setdefault(date, {}) \
                    .setdefault(row['lhd_2010_name'], {}) \
                    .setdefault(posneg, []).append(row)
                by_lga_posneg.setdefault(date, {}) \
                    .setdefault(row['lga_name19'], {}) \
                    .setdefault(posneg, []).append(row)

                lga = row['lga_name19'].split('(')[0].strip().lower() or 'unknown'
                if row['postcode'] in POSTCODE_TO_LGA:
                    assert POSTCODE_TO_LGA[row['postcode']] == lga, lga
                else:
                    POSTCODE_TO_LGA[row['postcode']] = lga

        r = []

        # Add general totals
        for region_schema, cases_dict in (
            # I'm really not sure there's much reason to get tests data
            # by postcode/LHD? It'll take too much space by postcode!
            (Schemas.POSTCODE, by_postcode),
            (Schemas.LGA, by_lga),
            (Schemas.LHD, by_lhd)
        ):
            current_counts = {}

            for date, schema_dict in cases_dict.items():
                for region_child, tests in schema_dict.items():
                    if region_child is None:
                        continue

                    current_counts.setdefault(region_child, 0)
                    current_counts[region_child] += len(tests)

                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent='AU-NSW',
                        region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                        datatype=DataTypes.TESTS_TOTAL,
                        value=current_counts[region_child],
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None,
                        source_id=self.SOURCE_ID
                    ))

        # Add general totals
        for region_schema, cases_dict in (
            #(Schemas.POSTCODE, by_postcode_posneg),
            #(Schemas.LGA, by_lga_posneg),
            #(Schemas.LHD, by_lhd_posneg)
        ):
            current_counts = {}

            for date, schema_dict in cases_dict.items():
                for region_child, posneg_dict in schema_dict.items():
                    for posneg, tests in posneg_dict.items():
                        current_counts.setdefault((region_child, posneg), 0)
                        current_counts[region_child, posneg] += len(tests)

                        r.append(DataPoint(
                            region_schema=region_schema,
                            region_parent='AU-NSW',
                            region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                            datatype=posneg,
                            value=current_counts[region_child, posneg],
                            date_updated=date,
                            source_url=SOURCE_URL,
                            text_match=None,
                            source_id=self.SOURCE_ID
                        ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = NSWJSONOpenData()
    pprint(inst.get_datapoints())
