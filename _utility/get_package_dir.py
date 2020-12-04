import os
import dotenv
from pathlib import Path
from os import environ
from os.path import expanduser


dotenv.load_dotenv(override=True)

DATA_DIR = Path(expanduser(environ['DATA_DIR']))
OVERSEAS_DIR = Path(expanduser(environ['OVERSEAS_DIR']))
OUTPUT_DIR = Path(expanduser(environ['OUTPUT_DIR']))
GLOBAL_SUBNATIONAL_COVID_DATA_DIR = Path(expanduser(environ['GLOBAL_SUBNATIONAL_COVID_DATA_DIR']))
CACHE_DIR = Path(expanduser(environ['CACHE_DIR']))


def get_package_dir():
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def get_data_dir():
    # Perhaps this shouldn't be hardcoded, but putting all this
    # data in source control can slow down the IDE substantially!
    return DATA_DIR


def get_overseas_dir():
    return OVERSEAS_DIR


def get_output_dir():
    return OUTPUT_DIR


def get_global_subnational_covid_data_dir():
    return GLOBAL_SUBNATIONAL_COVID_DATA_DIR


def get_cache_dir():
    return CACHE_DIR
