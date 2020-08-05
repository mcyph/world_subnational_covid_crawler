import datetime
from os import listdir, unlink

DB_DIR = '/mnt/ssd_970pro_512gb/covid_19_au_grab/output/'

ACTUALLY_DELETE = True
DELETE_BEFORE = (
    datetime.datetime.now() - datetime.timedelta(days=3)
)


def delete_old_dbs():
    for fnam in listdir(DB_DIR):
        date = datetime.datetime.strptime(
            fnam.split('-')[0], '%Y_%m_%d'
        )

        if date <= DELETE_BEFORE:
            print("DELETING:", fnam)

            if ACTUALLY_DELETE:
                unlink(f'{DB_DIR}/{fnam}')


if __name__ == '__main__':
    delete_old_dbs()
