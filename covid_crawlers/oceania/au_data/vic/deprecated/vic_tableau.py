import json
from pprint import pprint
from os import listdir

from _utility.get_package_dir import get_data_dir

SOURCE_URL = 'https://www.dhhs.vic.gov.au/victorian-coronavirus-covid-19-data'


def get_vic_tableau_datapoints():
    r = []
    for date in listdir(get_data_dir() / 'vic' / 'tableau'):
        path = get_data_dir() / 'vic' / 'tableau' / date / 'output.json'
        with open(path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        r.extend(_get_agegroup(data['agegroup']))
        r.extend(_get_transmissions(data['transmissions_over_time']))  # Mix-up??
    return r


def _get_agegroup(url_contents):
    for url, s in url_contents:
        data = _get_from_multipart(s, '50-59')
        if data:
            break

    if not data:
        return []

    #pprint(data)

    r = []
    return r


def _get_transmissions(url_contents):
    for url, s in url_contents:
        data = _get_from_multipart(s, 'Contact with a confirmed case')
        if data:
            break

    if not data:
        return []

    #pprint(data)

    r = []
    return r


def _get_from_multipart(s, contains):
    if s.startswith('GIF89'):
        return

    while s:
        num_chars, _, s = s.partition(';')
        num_chars = int(num_chars)

        i_s = s[:num_chars]
        #print(i_s)
        s = s[num_chars:]

        if contains in i_s:
            #print("FOUND:", contains, i_s)
            return json.loads(i_s)


if __name__ == '__main__':
    pprint(get_vic_tableau_datapoints())
