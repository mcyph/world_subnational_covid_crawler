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
    'Нұр-Сұлтан қаласы': 'KZ-AST',
    'Алматы қаласы': 'KZ-ALA',
    'Шымкент қаласы': 'KZ-SHY',
    'Ақмола облысы': 'KZ-AKM',
    'Ақтөбе облысы': 'KZ-AKT',
    'Алматы облысы': 'KZ-ALM',
    'Атырау облысы': 'KZ-ATY',
    'Шығыс Қазақстан облысы': 'KZ-VOS',
    'Жамбыл облысы': 'KZ-ZHA',
    'Батыс Қазақстан облысы': 'KZ-ZAP',
    'Қарағанды облысы': 'KZ-KAR',
    'Қостанай облысы': 'KZ-KUS',
    'Қызылорда облысы': 'KZ-KZY',
    'Маңғыстау облысы': 'KZ-MAN',
    'Павлодар облысы': 'KZ-PAV',
    'Солтүстік Қазақстан облысы': 'KZ-SEV',
    'Түркістан облысы': 'KZ-YUZ',
}


class KZData(URLBase):
    SOURCE_URL = 'https://www.coronavirus2020.kz/kz'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'kz' / 'data',
            urls_dict={
                'kz_corona.html': URL('https://www.coronavirus2020.kz/kz',
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
                html = pq(f.read(), parser='html')

            for div in html('.last_info_covid_bl .city_cov div'):
                region, num = pq(div).text().split('–')
                region = place_map[region.strip()]

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Kazakhstan',
                    region_child=region,
                    datatype=DT_TOTAL,
                    value=int(num),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            for div in html('.red_line_covid_bl .city_cov div'):
                region, num = pq(div).text().split('–')
                region = place_map[region.strip()]

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Kazakhstan',
                    region_child=region,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(num),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

            for div in html('.deaths_bl .city_cov div'):
                region, num = pq(div).text().split('–')
                region = place_map[region.strip()]

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Kazakhstan',
                    region_child=region,
                    datatype=DT_STATUS_DEATHS,
                    value=int(num),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(KZData().get_datapoints())
