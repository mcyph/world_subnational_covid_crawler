import csv
from datetime import datetime, timedelta
from urllib.request import urlretrieve
from os import makedirs
from os.path import dirname, exists


from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_LGA, DT_TESTS_TOTAL, DT_TESTS_POSITIVE, DT_TESTS_NEGATIVE
)
from covid_19_au_grab.state_news_releases.gaps_filled_in import (
    gaps_filled_in
)


# test_date,postcode,lhd_2010_code,lhd_2010_name,lga_code19,lga_name19,result
# 2020-01-08,2071,X760,Northern Sydney,14500,Ku-ring-gai (A),Tested & excluded


def get_nsw_tests_data():
    DEFAULT_REGION = 'Unknown'
    SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data/tests'

    by_postcode = {}
    by_lhd = {}
    by_lga = {}

    by_postcode_posneg = {}
    by_lhd_posneg = {}
    by_lga_posneg = {}

    # Make dates from 8:30pm!
    date = (datetime.now() - timedelta(hours=20, minutes=30)).strftime('%Y_%m_%d')
    path = (
        get_data_dir() / 'nsw' / 'open_data' / date /
        'covid-19-tests-by-date-and-location-and-result.csv'
    )
    if not exists(dirname(path)):
        makedirs(dirname(path))
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
                dd, mm, yyyy = row['test_date'].split('/')
                date = f'{yyyy}_{mm}_{dd}'
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
                    datatype=DT_TESTS_TOTAL,
                    region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                    value=current_counts[region_child],
                    date_updated=date,
                    source_url=SOURCE_URL,
                    text_match=None
                ))
        return r

    # I'm really not sure there's much reason to get tests data
    # by postcode/LHD? It'll take too much space by postcode!

    #r.extend(get_datapoints(SCHEMA_POSTCODE, by_postcode))
    r.extend(get_datapoints(SCHEMA_LGA, by_lga))
    #r.extend(get_datapoints(SCHEMA_LHD, by_lhd))

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
                        datatype=posneg,
                        region_child=region_child.split('(')[0].strip() or DEFAULT_REGION,
                        value=current_counts[region_child, posneg],
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
        return r

    #r.extend(get_posneg_datapoints(SCHEMA_POSTCODE, by_postcode_posneg))
    r.extend(get_posneg_datapoints(SCHEMA_LGA, by_lga_posneg))
    #r.extend(get_posneg_datapoints(SCHEMA_LHD, by_lhd_posneg))

    return gaps_filled_in(r)


if __name__ == '__main__':
    for i in get_nsw_tests_data():
        print(i)

