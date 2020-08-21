# https://covidata.2m.ma/#/ar/stats
# https://covid.hespress.com/
import json
from os import listdir

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class MAData(URLBase):
    SOURCE_URL = 'https://covid.hespress.com/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ma_hespress'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'ma' / 'data',
            urls_dict={
                'index.html': URL('https://covid.hespress.com/',
                                  static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/index.html'
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()

            regions = json.loads(
                '{'+html.split('var regionsValues = {')[1].split('};')[0]+'}'
            )

            for region, value in regions.items():
                region = region.lower()
                if not '-' in region:
                    region = region.replace('ma', 'ma-')
                else:
                    continue  # TODO: Add support for these admin2-level values! =======================================

                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='MA',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MAData().get_datapoints())
