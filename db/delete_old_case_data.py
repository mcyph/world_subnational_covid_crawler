import datetime
from shutil import rmtree
from os import listdir, unlink
from os.path import expanduser, isdir

COVID_ZIPS_DIR = expanduser('~/covid_data_zips')
COVID_UNZIPPED_DIR = expanduser('~/covid_data_zips')

ACTUALLY_DELETE = False
DELETE_BEFORE = (
    datetime.datetime.now() - datetime.timedelta(days=3)
)


def delete_old_case_data():
    # Delete archives (single files)
    for fnam in listdir(COVID_ZIPS_DIR):
        date = datetime.datetime.strptime(
            fnam.split('-')[0], '%Y_%m_%d'
        )

        if date <= DELETE_BEFORE:
            print("DELETING:", COVID_ZIPS_DIR, fnam)

            if ACTUALLY_DELETE:
                unlink(f'{COVID_ZIPS_DIR}/{fnam}')

    # Delete unzipped archives (complete directories)
    for dirname in listdir(COVID_UNZIPPED_DIR):
        if not isdir(f'{COVID_UNZIPPED_DIR}/{dirname}'):
            continue

        date = datetime.datetime.strptime(
            dirname.split('-')[0], '%Y_%m_%d'
        )

        if date <= DELETE_BEFORE:
            print("DELETING:", COVID_UNZIPPED_DIR, dirname)

            if ACTUALLY_DELETE:
                rmtree(f'{COVID_UNZIPPED_DIR}/{dirname}')


if __name__ == '__main__':
    delete_old_case_data()

