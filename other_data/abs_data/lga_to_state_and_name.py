from os.path import expanduser
import csv
from glob import glob
from covid_19_au_grab.get_package_dir import get_package_dir


BASE_PATH = get_package_dir() / 'other_data' / 'abs_data' / 'lga'


def get_lga_to_state_and_name_dict():
    r = {}

    state_dict = {
        'New South Wales': 'nsw',
        'Australian Capital Territory': 'act',
        'Northern Territory': 'nt',
        'Other Territories': 'ot',
        'Queensland': 'qld',
        'South Australia': 'sa',
        'Tasmania': 'tas',
        'Victoria': 'vic',
        'Western Australia': 'wa'
    }

    for path in glob(str(BASE_PATH / '*.csv')):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                r[int(row['LGA_CODE_2016'])] = (
                    state_dict[row['STATE_NAME_2016']],
                    row['LGA_NAME_2016'].split('(')[0].strip()
                )
    return r
