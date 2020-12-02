import csv
from _utility.get_package_dir import get_package_dir


def get_population_map():
    r = {}
    with open(get_package_dir() / 'world_geodata' / 'geojson_pop.tsv', 'r', encoding='utf-8') as f:
        for item in csv.DictReader(f, delimiter='\t'):
            r[item['region_schema'], item['region_parent'], item['region_child']] = int(item['pop_2020'])
    return r
