import csv
import pycountry
from collections import namedtuple
from covid_19_au_grab.other_data.iso_3166_1.iso_3166_data import get_data_item_by_name as _get_3166_1_by_name
from covid_19_au_grab.get_package_dir import get_package_dir


DataItem = namedtuple('DataItem', [
    "country_code",
    "subdivision_name",
    "code"
])


def _get_data_items():
    r = []
    f = open(get_package_dir() /
             'other_data' /
             'iso_3166_2' /
             'IP2LOCATION-ISO3166-2.CSV', 'r', encoding='utf-8')

    added = set()
    for item in csv.DictReader(f):
        r.append(DataItem(**item))
        added.add((r[-1].code, r[-1].subdivision_name))

    for subdivision in pycountry.subdivisions:
        if (subdivision.code, subdivision.name) in added:
            continue

        r.append(DataItem(
            country_code=subdivision.country.alpha_2,
            subdivision_name=subdivision.name,
            code=subdivision.code
        ))

    return r


def _get_data_items_by_name():
    r = {}
    r2 = {}
    
    for i in _get_data_items():
        en_name = i.subdivision_name.lower()
        code = i.country_code.lower()
        
        if not en_name:
            continue

        #if r.get(en_name, i) != i:
        #    import warnings
        #    warnings.warn(str(((en_name, i, r.get(en_name)))))

        r[en_name] = i
        r2[code, en_name] = i
    return r, r2


def _get_data_items_by_code():
    r = {}
    for i in _get_data_items():
        code = i.code.lower()
        if not code.strip('-'):
            continue

        #assert r.get(code, i) == i, (code, i)
        r[code] = i
    return r


_data_items_by_name, _data_items_by_name_country = _get_data_items_by_name()
_data_items_by_code = _get_data_items_by_code()


def get_data_item_by_code(code):
    return _data_items_by_code[code.lower()]


def get_data_item_by_name(name, country=None):
    if country:
        # Best to use a country, in case of collisions!
        # TODO: Convret English country names to a code, first!
        if (country.lower(), name.lower()) not in _data_items_by_name_country:
            item = _get_3166_1_by_name(country)
            country = item.iso3166.a2

        return _data_items_by_name_country[country.lower(), name.lower()]
    return _data_items_by_name[name.lower()]


if __name__ == '__main__':
    from pprint import pprint
    pprint(_get_data_items_by_name())
    print(get_data_item_by_code('au-vic'))
    print(get_data_item_by_code('au-tas'))
    print(get_data_item_by_name('victoria'))
    print(get_data_item_by_name('victoria', country='Australia'))
    print(get_data_item_by_name('victoria', country='au'))
