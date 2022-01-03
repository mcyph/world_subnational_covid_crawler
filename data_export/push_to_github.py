import os
from _utility.get_package_dir import get_global_subnational_covid_data_dir


def push_to_github():
    repo_dir = str(get_global_subnational_covid_data_dir()).rstrip('/')
    old_dir = os.getcwd()
    os.chdir(repo_dir)

    try:
        os.system('git add .')
        os.system('git commit -m "update data"')
        os.system('git push')
    finally:
        os.chdir(old_dir)
