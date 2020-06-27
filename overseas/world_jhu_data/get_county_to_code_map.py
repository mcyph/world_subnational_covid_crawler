import csv
from covid_19_au_grab.get_package_dir import get_package_dir

PATH = get_package_dir() / 'overseas' / 'world_jhu_data' / 'state_and_county_fips.csv'


def get_county_to_code_map():
    r = {}

    with open(PATH, 'r', encoding='utf-8') as f:
        for d in csv.DictReader(f):
            # fips,name,state
            assert not d['name'] in r, d['name']
            d['name'] = d['name'].lower()
            r[d['state'], d['name']] = d['fips']
            r[d['state'], d['name'].replace(' county', '')] = d['fips']
            r[d['state'], d['name'].replace(' borough', '')] = d['fips']
            r[d['state'], d['name'].replace(' census area', '')] = d['fips']
            r[d['state'], d['name'].replace(' municipality', '')] = d['fips']
            r[d['state'], d['name'].replace(' parish', '')] = d['fips']
            r[d['state'], d['name'].replace(' city', '')] = d['fips']
            r[d['state'], d['name'].replace(' city and borough', '')] = d['fips']

    return r


if __name__ == '__main__':
    get_county_to_code_map()
