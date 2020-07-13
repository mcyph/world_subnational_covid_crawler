import csv
import json
from collections import Counter
from datetime import datetime, timedelta
from urllib.request import urlretrieve
from os import makedirs, listdir
from os.path import exists, dirname

from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_LGA, SCHEMA_POSTCODE, SCHEMA_LHD,
    DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_INTERSTATE,
    DT_SOURCE_CONFIRMED, DT_SOURCE_COMMUNITY,
    DT_SOURCE_OVERSEAS,

    DT_TESTS_TOTAL,
    DT_STATUS_ACTIVE, DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_TOTAL, DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TESTS_POSITIVE, DT_TESTS_NEGATIVE
)


class NSWJSONData:
    def __init__(self):
        self.postcode_to_lga = {}

    def get_datapoints(self):
        date = (datetime.now() - timedelta(hours=20, minutes=30)).strftime('%Y_%m_%d')
        dir_ = get_data_dir() / 'nsw' / 'open_data' / date
        if not exists(dir_):
            makedirs(dir_)

        r = []
        self.get_nsw_cases_data(dir_)  # Just for the postcode->lga data
        self.get_nsw_tests_data(dir_)
        r.extend(self.get_nsw_postcode_data(dir_))
        r.extend(self.__postcode_datapoints_to_lga('https://data.nsw.gov.au/nsw-covid-19-data', r))
        r.extend(self.get_nsw_age_data(dir_, date, download=True))

        for i_date in listdir(get_data_dir() / 'nsw' / 'open_data'):
            if i_date == date:
                continue
            i_dir = get_data_dir() / 'nsw' / 'open_data' / date
            r.extend(self.get_nsw_age_data(i_dir, i_date, download=False))
        return r

    def __postcode_datapoints_to_lga(self, SOURCE_URL, r):
        # Convert postcode to LGA where possible
        new_r = []
        added_to_lga = set()
        processed_postcode = set()
        mapping = Counter()

        for datapoint in sorted(r, key=lambda i: i.date_updated):
            if datapoint.region_schema == SCHEMA_LGA:
                added_to_lga.add((
                    datapoint.region_child,
                    datapoint.datatype
                ))
                continue
            elif datapoint.region_schema != SCHEMA_POSTCODE:
                continue
            elif datapoint.region_child in self.postcode_to_lga:
                lga = self.postcode_to_lga[datapoint.region_child]
            else:
                lga = 'unknown'
                if datapoint.region_child != 'unknown':
                    print("NOT FOUND:", datapoint.region_child)
                # continue  # WARNINIG!!! ================================================================================

            if (datapoint.region_child, datapoint.datatype, datapoint.date_updated) in processed_postcode:
                #print("IGNORING DOUBLE-UP:", datapoint)
                continue
            processed_postcode.add((datapoint.region_child, datapoint.datatype, datapoint.date_updated))

            if lga == 'cumberland':
                print('USING:', datapoint)

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
                region_schema=SCHEMA_LGA,
                region_parent='AU-NSW',
                region_child=lga,
                datatype=datatype,
                value=value,
                date_updated=date_updated,
                source_url=SOURCE_URL
            ))

        return new_r

    #=============================================================================#
    # Postcode-level website json data
    #=============================================================================#

    def get_nsw_age_data(self, dir_, date, download=True):
        r = []

        path_fatalitiesdata = dir_ / 'fatalitiesdata.json'
        path_agedata = dir_ / 'agedata.json'
        path_listing = dir_ / 'find-facts-about-covid-19.html'

        if not exists(path_fatalitiesdata) or not exists(path_agedata) or not exists(path_listing):
            if not download:
                return []

            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/fatalitiesdata.json',
                path_fatalitiesdata
            )
            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/agedata.json',
                path_agedata
            )
            urlretrieve(
                'https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                path_listing
            )

        with open(path_listing, 'r', encoding='utf-8') as f:
            html = f.read()
            try:
                _date = html.split('Last updated')[1].strip().partition(' ')[-1].split('.')[0].strip()
                date = datetime.strptime(_date, '%d %B %Y').strftime('%Y_%m_%d')
            except IndexError:
                # It seems this info isn't always supplied(?) =============================================================
                import traceback
                traceback.print_exc()

        with open(path_agedata, 'r', encoding='utf-8') as f:
            # {"data":[{"ageGroup":"0-9","Males":null,"Females":null},
            agedata = json.loads(f.read())

            for age_dict in agedata['data']:
                r.append(DataPoint(
                    datatype=DT_TOTAL_MALE,
                    value=age_dict['Males'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None
                ))
                r.append(DataPoint(
                    datatype=DT_TOTAL_FEMALE,
                    value=age_dict['Females'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None
                ))
                r.append(DataPoint(
                    datatype=DT_TOTAL,
                    value=(age_dict['Females'] or 0) + (age_dict['Males'] or 0),
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None
                ))

        """
        with open(path_fatalitiesdata, 'r', encoding='utf-8') as f:
            agedata = json.loads(f.read())

            for age_dict in agedata['data']:
                r.append(DataPoint(
                    datatype=DT_STATUS_DEATHS_MALE,
                    value=age_dict['Males'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_DEATHS_FEMALE,
                    value=age_dict['Females'] or 0,
                    agerange=age_dict['ageGroup'],
                    date_updated=date,
                    source_url='https://www.nsw.gov.au/covid-19/find-facts-about-covid-19',
                    text_match=None
                ))
        """

        return r

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

        soi_map = {
            'Overseas': DT_SOURCE_OVERSEAS,
            'Locally acquired - contact not identified': DT_SOURCE_COMMUNITY,
            'Locally acquired - contact not yet identified': DT_SOURCE_COMMUNITY,
            'Locally acquired - source not identified': DT_SOURCE_COMMUNITY,
            'Locally acquired - contact of a confirmed case and/or in a known cluster': DT_SOURCE_CONFIRMED,
            'Under investigation': DT_SOURCE_UNDER_INVESTIGATION,
            'Interstate': DT_SOURCE_INTERSTATE
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
                # Date already in the format I use, aside from hyphens
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

                lga = row['lga_name19'].split('(')[0].strip().lower() or 'unknown'
                if row['postcode'] in self.postcode_to_lga:
                    assert self.postcode_to_lga[row['postcode']] == lga, lga
                else:
                    self.postcode_to_lga[row['postcode']] = lga

        r = []

        # Add general totals
        for region_schema, cases_dict in (
            (SCHEMA_POSTCODE, by_postcode),
            (SCHEMA_LGA, by_lga),
            (SCHEMA_LHD, by_lhd)
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
                        datatype=DT_TOTAL,
                        value=current_counts[region_child],
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None
                    ))

        # Add by source of infection
        for region_schema, cases_dict in (
            (SCHEMA_POSTCODE, by_postcode_soi),
            (SCHEMA_LGA, by_lga_soi),
            (SCHEMA_LHD, by_lhd_soi)
        ):
            current_counts = {}

            for date, schema_dict in sorted(cases_dict.items()):
                for region_child, soi_dict in schema_dict.items():
                    for soi, cases in soi_dict.items():
                        current_counts.setdefault((region_child, soi), 0)
                        current_counts[region_child, soi] += len(cases)

                        r.append(DataPoint(
                            region_schema=region_schema,
                            region_parent='AU-NSW',
                            region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                            datatype=soi,
                            value=current_counts[region_child, soi],
                            date_updated=date,
                            source_url=SOURCE_URL,
                            text_match=None
                        ))

        return r

    #=============================================================================#
    # Postcode-level website tests json data
    #=============================================================================#

    def get_nsw_postcode_data(self, dir_):
        # {"data":[{"Recovered":5,"POA_NAME16":"2106","Deaths":0,"Cases":5,"Date":"14-May"},

        path_totals = dir_ / 'covid_19_cases_by_postcode_totals.json'
        path_active_deaths = dir_ / 'covid_19_cases_by_postcode_active_deaths.json'
        path_tests = dir_ / 'covid_19_tests_by_postcode.json'
        path_active = dir_ / 'covid_19_cases_by_postcode_active.json'

        if not exists(path_totals) or not exists(path_active_deaths) or not exists(path_active) or not exists(path_tests):
            # Retrieve these, just in cases...
            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/data_Cases2.json',
                path_active_deaths
            )
            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/data_Cases.json',
                path_totals
            )
            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/data_tests.json',
                path_tests
            )
            urlretrieve(
                'https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/active_cases.json',
                path_active
            )

        r = []
        SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data/tests'
        active_data = self.__get_active_data(path_active)
        r.extend(self.__get_active_deaths_datapoints(SOURCE_URL, path_active_deaths, active_data))
        r.extend(self.__get_tests_datapoints(SOURCE_URL, path_tests))
        r.extend(self.__get_totals_datapoints(SOURCE_URL, path_totals))
        return r

    def __get_active_data(self, path_active):
        r = {}
        with open(path_active, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                # {"data":[{
                #   "Day11":0,"Day12":0,"Day13":0,"POA_NAME16":"2541",
                #   "Day0":0,"Day1":0,"Day2":0,"Day3":0,"Day10":0,"Day4":0,
                #   "Day5":0,"Day6":0,"Day7":0,"Day8":0,"Day9":0},
                for x in range(14):
                    r.setdefault(item['POA_NAME16'], []).append(item[f'Day{x}'])
        return r

    def __get_active_deaths_datapoints(self, SOURCE_URL, path_active_deaths, active_data):
        r = []

        with open(path_active_deaths, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                date = datetime.strptime(item['Date'] + '-20', '%d-%b-%y').strftime('%Y_%m_%d')
                recovered = int(item['Recovered'])
                deaths = int(item['Deaths'])
                cases = int(item['Cases'])
                censored = int(item.get('censored',
                                        0))  # NOTE ME:  From 12 June, this heatmap reporting of active cases has changed. Cases that are not recorded as recovered or deceased after six weeks are not included.
                active = cases - recovered - deaths - censored
                postcode = item['POA_NAME16'] if item['POA_NAME16'] else 'Unknown'

                r.append(DataPoint(
                    region_schema=SCHEMA_POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DT_TOTAL,
                    value=cases,
                    date_updated=date,
                    source_url=SOURCE_URL
                ))
                #r.append(DataPoint(
                #    region_schema=SCHEMA_POSTCODE,
                #    region_parent='AU-NSW',
                #    region_child=postcode,
                #    datatype=DT_STATUS_ACTIVE,
                #    value=active,
                #    date_updated=date,
                #    source_url=SOURCE_URL
                #))

                if postcode in active_data:
                    num_active = active_data[postcode].pop()

                    r.append(DataPoint(
                        region_schema=SCHEMA_POSTCODE,
                        region_parent='AU-NSW',
                        region_child=postcode,
                        datatype=DT_STATUS_ACTIVE,
                        value=num_active, # CHECK ME!!!!! =====================================
                        date_updated=date,
                        source_url=SOURCE_URL
                    ))

                    r.append(DataPoint(
                        region_schema=SCHEMA_POSTCODE,
                        region_parent='AU-NSW',
                        region_child=postcode,
                        datatype=DT_STATUS_RECOVERED,
                        value=cases-num_active-deaths,  # CHECK ME!!!!! =====================================
                        date_updated=date,
                        source_url=SOURCE_URL
                    ))

                #r.append(DataPoint(
                #    region_schema=SCHEMA_POSTCODE,
                #    region_parent='AU-NSW',
                #    region_child=postcode,
                #    datatype=DT_STATUS_RECOVERED,
                #    value=recovered,
                #    date_updated=date,
                #    source_url=SOURCE_URL
                #))
                r.append(DataPoint(
                    region_schema=SCHEMA_POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DT_STATUS_DEATHS,
                    value=deaths,
                    date_updated=date,
                    source_url=SOURCE_URL
                ))

        return r

    def __get_tests_datapoints(self, SOURCE_URL, path_tests):
        r = []

        with open(path_tests, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                date = datetime.strptime(item['Date'] + '-20', '%d-%b-%y').strftime('%Y_%m_%d')
                number = int(item['Number'])
                # recent = item['Recent'] # TODO: ADD ME!!! ========================================================
                postcode = item['POA_NAME16'] if item['POA_NAME16'] else 'Unknown'

                r.append(DataPoint(
                    region_schema=SCHEMA_POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DT_TESTS_TOTAL,
                    value=number,
                    date_updated=date,
                    source_url=SOURCE_URL
                ))

        return r

    def __get_totals_datapoints(self, SOURCE_URL, path_totals):
        # Pretty sure this is dupe data (for now)
        # Don't uncomment this without making sure this won't double the result(!)
        r = []

        with open(path_totals, 'r', encoding='utf-8') as f:
            for item in json.loads(f.read())['data']:
                date = datetime.strptime(item['Date'] + '-20', '%d-%b-%y').strftime('%Y_%m_%d')
                number = int(item['Number'])
                postcode = item['POA_NAME16'] if item['POA_NAME16'] else 'Unknown'

                r.append(DataPoint(
                    region_schema=SCHEMA_POSTCODE,
                    region_parent='AU-NSW',
                    region_child=postcode,
                    datatype=DT_TOTAL,
                    value=number,
                    date_updated=date,
                    source_url=SOURCE_URL
                ))

        return r

    #=============================================================================#
    # Postcode-level open tests json data
    #=============================================================================#

    # test_date,postcode,lhd_2010_code,lhd_2010_name,lga_code19,lga_name19,result
    # 2020-01-08,2071,X760,Northern Sydney,14500,Ku-ring-gai (A),Tested & excluded

    def get_nsw_tests_data(self, dir_):
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

        if not exists(path):
            urlretrieve(
                'https://data.nsw.gov.au/data/dataset/5424aa3b-550d-4637-ae50-7f458ce327f4/resource/227f6b65-025c-482c-9f22-a25cf1b8594f/download/covid-19-tests-by-date-and-location-and-result.csv',
                path
            )

        posneg_map = {
            'Tested & excluded': DT_TESTS_NEGATIVE,
            'Case - Confirmed': DT_TESTS_POSITIVE
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
                if row['postcode'] in self.postcode_to_lga:
                    assert self.postcode_to_lga[row['postcode']] == lga, lga
                else:
                    self.postcode_to_lga[row['postcode']] = lga

        r = []

        def get_datapoints(region_schema, cases_dict):
            r = []
            current_counts = {}

            for date, schema_dict in cases_dict.items():
                for region_child, tests in schema_dict.items():
                    current_counts.setdefault(region_child, 0)
                    current_counts[region_child] += len(tests)

                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent='AU-NSW',
                        region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                        datatype=DT_TESTS_TOTAL,
                        value=current_counts[region_child],
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
            return r

        # I'm really not sure there's much reason to get tests data
        # by postcode/LHD? It'll take too much space by postcode!

        r.extend(get_datapoints(SCHEMA_POSTCODE, by_postcode))
        r.extend(get_datapoints(SCHEMA_LGA, by_lga))
        r.extend(get_datapoints(SCHEMA_LHD, by_lhd))

        def get_posneg_datapoints(region_schema, cases_dict):
            r = []
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
                            text_match=None
                        ))
            return r

        #r.extend(get_posneg_datapoints(SCHEMA_POSTCODE, by_postcode_posneg))
        #r.extend(get_posneg_datapoints(SCHEMA_LGA, by_lga_posneg))
        #r.extend(get_posneg_datapoints(SCHEMA_LHD, by_lhd_posneg))

        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = NSWJSONData()
    #pprint(inst.get_datapoints())

    for datapoint in inst.get_datapoints():
        #if datapoint.datatype == DT_STATUS_ACTIVE and datapoint.region_schema == SCHEMA_LGA:
        #    print(datapoint)

        if datapoint.agerange:
            print(datapoint)

