import json
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1, DT_TESTS_TOTAL,
    DT_TOTAL, DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


place_map = {
    'Иссык-Куль': 'KG-Y',
    'Джалал-Абад': 'KG-J',
    'Талас': 'KG-T',
    'Баткен': 'KG-B',
    'Ош': 'KG-O',
    'Чуй': 'KG-C',
    'Нарын': 'KG-N',
    'г. Бишкек': 'KG-GB',
    'г. Ош': 'KG-GO',
}


class KGData(URLBase):
    SOURCE_URL = 'https://covid.kg/'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'kg' / 'data',
            urls_dict={
                'kz_corona.html': URL('https://covid.kg/',
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
            path = f'{base_dir}/{date}/kz_corona.html'
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()

            # TODO: Add other national stats from this page!
            chart_js = html.split('var options = {')[-1]
            dates = json.loads(
                chart_js.split('categories: ')[1]
                    .split('\n')[0]
                    .strip()
                    .strip(',')
            )

            for data in chart_js.split('data: ')[1:]:
                data, region = data.split('name: ')
                data = json.loads(data.strip().strip(','))
                region = region.split('\n')[0].strip().strip('"\', ')
                region = place_map[region.strip()]

                for date, i_data in zip(dates, data):
                    date = self.convert_date(date)
                    if i_data is None:
                        continue

                    r.append(DataPoint(
                        region_schema=SCHEMA_ADMIN_1,
                        region_parent='KG',
                        region_child=region,
                        datatype=DT_TOTAL,
                        value=int(i_data),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(KGData().get_datapoints())
