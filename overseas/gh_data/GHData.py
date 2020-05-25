# https://covid-19-data.unstatshub.org/datasets/62fb86d7606343e1a93baa70224a8a46_0/data?geometry=-21.685%2C4.147%2C19.623%2C11.757
# https://opendata.arcgis.com/datasets/62fb86d7606343e1a93baa70224a8a46_0.csv
# There's also geojson data there!

import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class GHData(URLBase):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'et' / 'data',
            urls_dict={
                'gh_data.csv': URL(
                    '',
                    static_file=False
                )
            }
        )
        self.update()

    def get_datapoints(self):
        r = []

        f = self.get_file('gh_data.csv',
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

    pprint(GHData().get_datapoints())
