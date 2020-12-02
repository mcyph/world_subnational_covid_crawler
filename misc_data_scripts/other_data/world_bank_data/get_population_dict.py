import csv
from covid_19_au_grab.misc_data_scripts.other_data.iso_3166_1.iso_3166_data import get_data_item_by_code
from covid_19_au_grab._utility.get_package_dir import get_package_dir


def get_population_dict(year):
    """
    Get the population of a country

    :param country: the country name (not code),
                    e.g. "Australia" or "United States"
    :param from_year:
    :param to_year:
    :return: a two-tuple of ((year, population), ...)
    """

    r = {}

    with open(get_package_dir() / 'other_data/world_bank_data/world_bank_popdata.csv',
              'r', encoding='utf-8-sig') as f:

        for item in csv.DictReader(f):
            for k, v in item.items():
                # Columns are years
                try:
                    int(k)
                except ValueError:
                    continue

                if not year == int(k):
                    continue

                try:
                    data_item = get_data_item_by_code(item['Country Code'])
                except KeyError:
                    print("KeyError:", item['Country Code'])
                    continue

                if v:
                    r[data_item.iso3166.a2.lower()] = int(v)
                elif data_item.iso3166.a2 == 'ER':
                    r[data_item.iso3166.a2.lower()] = 3213972  # HACK!
                else:
                    print("No data:", data_item.iso3166.a2)

    return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_population_dict(2019))

