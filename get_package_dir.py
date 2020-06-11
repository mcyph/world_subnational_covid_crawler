import os
from pathlib import Path


def get_package_dir():
    return Path(os.path.dirname(os.path.realpath(__file__)))


def get_data_dir():
    # Perhaps this shouldn't be hardcoded, but putting all this
    # data in source control can slow down the IDE substantially!
    return Path(os.path.expanduser(f'~/dev/covid_19_data/'))


def get_overseas_dir():
    return Path(os.path.expanduser(f'~/dev/covid_19_gitdata'))


def get_output_dir():
    return Path('/mnt/ssd_970pro_512gb/covid_19_au_grab')

