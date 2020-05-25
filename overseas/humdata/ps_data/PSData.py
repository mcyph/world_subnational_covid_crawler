# https://data.humdata.org/dataset/state-of-palestine-coronavirus-covid-19-subnational-cases


import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class PSData(URLBase):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / '' / '',
            urls_dict={
                '': URL(
                    '',
                    static_file=False
                )
            }
        )
        self.update()

    def get_datapoints(self):
        r = []

        f = self.get_file('',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date'])

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(PSData().get_datapoints())
