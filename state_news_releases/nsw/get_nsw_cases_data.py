import csv

from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_LGA, SCHEMA_POSTCODE, SCHEMA_LHD,
    DT_TOTAL,
    DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_INTERSTATE,
    DT_SOURCE_CONFIRMED, DT_SOURCE_COMMUNITY,
    DT_SOURCE_OVERSEAS
)


# notification_date,postcode,likely_source_of_infection,
#   lhd_2010_code,lhd_2010_name,lga_code19,lga_name19
# 2020-01-22,2134,Overseas,X700,Sydney,11300,Burwood (A)


def get_nsw_cases_data():
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
        'Locally acquired - contact of a confirmed case and/or in a known cluster': DT_SOURCE_CONFIRMED,
        'Under investigation': DT_SOURCE_UNDER_INVESTIGATION,
        'Interstate': DT_SOURCE_INTERSTATE
    }

    # HACK - should make get most recent!
    path = (
        get_data_dir() / 'nsw' / 'open_data' / '2020_04_30' /
        'covid-19-cases-by-notification-date-location-'
            'and-likely-source-of-infection.csv'
    )

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
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

    r = []

    def get_datapoints(schema, cases_dict):
        r = []
        for date, schema_dict in cases_dict.items():
            for region, cases in schema_dict.items():
                r.append(DataPoint(
                    schema=schema,
                    datatype=DT_TOTAL,
                    region=region or DEFAULT_REGION,
                    value=len(cases),  # TODO: Make cumulative!!! =======================================
                    date_updated=date,
                    source_url=SOURCE_URL,
                    text_match=None
                ))
        return r

    r.extend(get_datapoints(SCHEMA_POSTCODE, by_postcode))
    r.extend(get_datapoints(SCHEMA_LGA, by_lga))
    r.extend(get_datapoints(SCHEMA_LHD, by_lhd))

    def get_soi_datapoints(schema, cases_dict):
        r = []
        for date, schema_dict in cases_dict.items():
            for region, soi_dict in schema_dict.items():
                for soi, cases in soi_dict.items():
                    r.append(DataPoint(
                        schema=schema,
                        datatype=soi,
                        region=region or DEFAULT_REGION,
                        value=len(cases),
                        date_updated=date,
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
        return r

    r.extend(get_soi_datapoints(SCHEMA_POSTCODE, by_postcode_soi))
    r.extend(get_soi_datapoints(SCHEMA_LGA, by_lga_soi))
    r.extend(get_soi_datapoints(SCHEMA_LHD, by_lhd_soi))

    return r


if __name__ == '__main__':
    for i in get_nsw_cases_data():
        print(i)

