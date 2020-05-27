import csv
from collections import namedtuple


DataItem = namedtuple('DataItem', [
    "country_code",
    "subdivision_name",
    "code"
])


def _get_data_items():
    r = []
    f = open('IP2LOCATION-ISO3166-2.CSV', 'r', encoding='utf-8')

    for item in csv.DictReader(f):
        r.append(DataItem(**item))

    return r


def _get_data_items_by_name():
    r = {}
    r2 = {}
    
    for i in _get_data_items():
        en_name = i.subdivision_name.lower()
        code = i.country_code.lower()
        
        if not en_name:
            continue

        if r.get(en_name, i) != i:
            import warnings
            warnings.warn(str(((en_name, i, r.get(en_name)))))

        r[en_name] = i
        r2[code, en_name] = i
    return r, r2


def _get_data_items_by_code():
    r = {}
    for i in _get_data_items():
        code = i.code.lower()
        if not code.strip('-'):
            continue

        assert r.get(code, i) == i, (code, i)
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
        return _data_items_by_name_country[country.lower(), name.lower()]
    return _data_items_by_name[name.lower()]


if __name__ == '__main__':
    from pprint import pprint
    pprint(_get_data_items_by_name())
    print(get_data_item_by_code('au-vic'))
    print(get_data_item_by_code('au-tas'))
    print(get_data_item_by_name('victoria'))
