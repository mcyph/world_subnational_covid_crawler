import csv
from glob import glob
from covid_19_au_grab._utility.get_package_dir import get_package_dir


BASE_PATH = get_package_dir() / 'misc_data_scripts' / 'other_data' / 'abs_data' / 'lga'


def get_lga_to_state_and_name_dict():
    r = {}

    state_dict = {
        'New South Wales': 'AU-NSW',
        'Australian Capital Territory': 'AU-NSW',
        'Northern Territory': 'AU-NT',
        'Other Territories': None,
        'Queensland': 'AU-QLD',
        'South Australia': 'AU-SA',
        'Tasmania': 'AU-TAS',
        'Victoria': 'AU-VIC',
        'Western Australia': 'AU-WA'
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
