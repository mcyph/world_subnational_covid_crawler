import csv
from world_geodata.ProcessGeoJSONBase import (
    DATA_DIR
)


def get_postcodes_map():
    postcodes_dict = {}

    with open(DATA_DIR / 'au' / 'postcode' / 'au_postcodes.csv', 'r', encoding='utf-8') as f:
        for i in csv.reader(f):
            postcodes_dict.setdefault(i[0], []).append(i[1])

    return postcodes_dict

