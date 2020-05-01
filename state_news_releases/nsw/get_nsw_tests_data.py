import csv
import datetime

from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_LGA, SCHEMA_POSTCODE, SCHEMA_LHD,
    DT_TOTAL,
    DT_TESTS_TOTAL, DT_TESTS_POSITIVE, DT_TESTS_NEGATIVE
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

    # HACK - should make get most recent!
    path = (
        get_data_dir() / 'nsw' / 'open_data' / '2020_04_30' /
        'covid-19-tests-by-date-and-location-and-result.csv'
    )

    posneg_map = {
        'Tested & excluded': DT_TESTS_NEGATIVE,
        'Case - Confirmed': DT_TESTS_POSITIVE
    }

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
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

    def get_datapoints(schema, cases_dict):
        r = []
        current_counts = {}

        for date, schema_dict in cases_dict.items():
            for region, tests in schema_dict.items():
                current_counts.setdefault(region, 0)
                current_counts[region] += len(tests)

                r.append(DataPoint(
                    schema=schema,
                    datatype=DT_TESTS_TOTAL,
                    region=region.split('(')[0].strip() or DEFAULT_REGION,
                    value=current_counts[region],
                    date_updated=date,
                    source_url=SOURCE_URL,
                    text_match=None
                ))
        return r

    r.extend(get_datapoints(SCHEMA_POSTCODE, by_postcode))
    r.extend(get_datapoints(SCHEMA_LGA, by_lga))
    r.extend(get_datapoints(SCHEMA_LHD, by_lhd))

    def get_posneg_datapoints(schema, cases_dict):
        r = []
        current_counts = {}

        for date, schema_dict in cases_dict.items():
            for region, posneg_dict in schema_dict.items():
                for posneg, tests in posneg_dict.items():
                    current_counts.setdefault((region, posneg), 0)
                    current_counts[region, posneg] += len(tests)

                    r.append(DataPoint(
                        schema=schema,
                        datatype=posneg,
                        region=region.split('(')[0].strip() or DEFAULT_REGION,
                        value=current_counts[region, posneg],
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
        return r

    r.extend(get_posneg_datapoints(SCHEMA_POSTCODE, by_postcode_posneg))
    r.extend(get_posneg_datapoints(SCHEMA_LGA, by_lga_posneg))
    r.extend(get_posneg_datapoints(SCHEMA_LHD, by_lhd_posneg))

    return r


if __name__ == '__main__':
    for i in get_nsw_tests_data():
        print(i)

