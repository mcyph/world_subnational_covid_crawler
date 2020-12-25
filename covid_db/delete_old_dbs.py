import datetime
from _utility.get_package_dir import get_output_dir


DB_DIR = get_output_dir() / 'output'

ACTUALLY_DELETE = True
DELETE_BEFORE = datetime.datetime.now() - datetime.timedelta(days=1)


def delete_old_dbs():
    for path in DB_DIR.iterdir():
        date = datetime.datetime.strptime(path.name.split('-')[0], '%Y_%m_%d')

        if date <= DELETE_BEFORE:
            print("DELETING:", path)

            if ACTUALLY_DELETE:
                path.unlink()


if __name__ == '__main__':
    delete_old_dbs()
