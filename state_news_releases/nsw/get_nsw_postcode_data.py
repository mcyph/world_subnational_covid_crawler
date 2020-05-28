import csv
import json
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
    SCHEMA_POSTCODE, DT_TOTAL, DT_TESTS_TOTAL,
    DT_STATUS_ACTIVE, DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.state_news_releases.gaps_filled_in import (
    gaps_filled_in
)


def get_nsw_postcode_data():
    r = []

    SOURCE_URL = 'https://data.nsw.gov.au/nsw-covid-19-data/tests'

    # {"data":[{"Recovered":5,"POA_NAME16":"2106","Deaths":0,"Cases":5,"Date":"14-May"},

    date = datetime.now().strftime('%Y_%m_%d')
    dir_ = get_data_dir() / 'nsw' / 'open_data' / date
    path_totals = dir_ / 'covid_19_cases_by_postcode_totals.json'
    path_active_deaths = dir_ / 'covid_19_cases_by_postcode_active_deaths.json'
    path_tests = dir_ / 'covid_19_tests_by_postcode.json'

    if not exists(dir_):
        makedirs(dir_)

    if not exists(path_totals) or not exists(path_active_deaths):
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

    with open(path_active_deaths, 'r', encoding='utf-8') as f:
        for item in json.loads(f.read())['data']:
            date = datetime.strptime(item['Date']+'-20', '%d-%b-%y').strftime('%Y_%m_%d')
            recovered = int(item['Recovered'])
            deaths = int(item['Deaths'])
            cases = int(item['Cases'])
            active = cases-recovered
            postcode = int(item['POA_NAME16']) if item['POA_NAME16'] else 'Unknown'

            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_child=postcode,
                datatype=DT_TOTAL,
                value=cases,
                date_updated=date,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_child=postcode,
                datatype=DT_STATUS_ACTIVE,
                value=active,
                date_updated=date,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_child=postcode,
                datatype=DT_STATUS_RECOVERED,
                value=recovered,
                date_updated=date,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_child=postcode,
                datatype=DT_STATUS_DEATHS,
                value=deaths,
                date_updated=date,
                source_url=SOURCE_URL
            ))

    with open(path_tests, 'r', encoding='utf-8') as f:
        for item in json.loads(f.read())['data']:
            date = datetime.strptime(item['Date']+'-20', '%d-%b-%y').strftime('%Y_%m_%d')
            number = int(item['Number'])
            #recent = item['Recent'] # TODO: ADD ME!!! ========================================================
            postcode = int(item['POA_NAME16']) if item['POA_NAME16'] else 'Unknown'

            r.append(DataPoint(
                region_schema=SCHEMA_POSTCODE,
                region_child=postcode,
                datatype=DT_TESTS_TOTAL,
                value=number,
                date_updated=date,
                source_url=SOURCE_URL
            ))

    return gaps_filled_in(r)


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_nsw_postcode_data())
