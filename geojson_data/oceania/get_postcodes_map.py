import csv
from covid_19_au_grab.normalize_locality_name import normalize_locality_name
from covid_19_au_grab.geojson_data.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


def get_postcodes_map():
    postcodes_dict = {}

    with open(DATA_DIR / 'au' / 'postcode' / 'au_postcodes.csv', 'r', encoding='utf-8') as f:
        for i in csv.reader(f):
            postcodes_dict.setdefault(i[0], []).append(i[1])

    return postcodes_dict

