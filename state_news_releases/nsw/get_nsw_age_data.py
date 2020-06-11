import json
from os import makedirs
from os.path import exists
from urllib.request import urlretrieve
from datetime import datetime, timedelta

from covid_19_au_grab.get_package_dir import (
    get_data_dir
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    DT_TOTAL, DT_TOTAL_MALE, DT_TOTAL_FEMALE
)


def get_nsw_age_data():
    r = []
    date = (datetime.now() - timedelta(hours=20, minutes=30)).strftime('%Y_%m_%d')
    dir_ = get_data_dir() / 'nsw' / 'open_data' / date

    path_fatalitiesdata = dir_ / 'fatalitiesdata.json'
    path_agedata = dir_ / 'agedata.json'
    path_listing = dir_ / 'find-facts-about-covid-19.html'

    if not exists(dir_):
        makedirs(dir_)

    if not exists(path_fatalitiesdata) or not exists(path_agedata) or not exists(path_listing):
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


if __name__ == '__main__':
    items = get_nsw_age_data()
    for i in items:
        print(i)
