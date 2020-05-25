import csv
import json

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class KZData(URLBase):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / '' / 'data',
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
        first_line = True

        f = self.get_file('provinces_1.csv',
                          include_revision=True)

        for item in csv.DictReader(f):
            pass

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(KZData().get_datapoints())