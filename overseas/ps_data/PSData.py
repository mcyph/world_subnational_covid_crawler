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
    DT_TOTAL, DT_STATUS_RECOVERED,
    DT_STATUS_DEATHS, DT_STATUS_ACTIVE
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


place_map = {
    'قطاع غزة': 'PS-GZA', #'Gaza strip',
    'الخليل': 'PS-HBN', #'Hebron',
    'قلقيلية': 'PS-QQA', #'Qalqilya',
    'ضواحي القدس': 'PS-JEM', #'The outskirts of Jerusalem',
    'رام الله والبيرة': 'PS-RBH', #'Ramallah and Al-Bireh',
    'بيت لحم': 'PS-BTH', #'Bethlehem',
    'نابلس': 'PS-NBS', #'Nablus',
    'طولكرم': 'PS-TKM', #'Tulkarm',
    'جنين': 'PS-JEN', #'Jenin',
    'أريحا': 'PS-JRH', #'Jericho',
    'سلفيت': 'PS-SLT', #'Salfit',
    'طوباس': 'PS-TBS', #'Tubas',
}


class PSData(URLBase):
    SOURCE_URL = 'https://www.corona.ps/details'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ps_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'ps' / 'data',
            urls_dict={
                'ps_corona.html': URL('https://www.corona.ps/details',
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
            path = f'{base_dir}/{date}/ps_corona.html'
            with open(path, 'r', encoding='utf-8') as f:
                html = pq(f.read(), parser='html')

            # There are quite a few more stats e.g. lower than governorate level etc =====================================

            for governorate, total, active, recovery, death in html('#Table2 tbody tr'):
                governorate = place_map[pq(governorate).text().strip()]
                death = int(pq(death).text().strip())
                recovery = int(pq(recovery).text().strip())
                active = int(pq(active).text().strip())
                total = int(pq(total).text().strip())

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DT_TOTAL,
                    value=int(total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(recovery),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DT_STATUS_DEATHS,
                    value=int(death),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(PSData().get_datapoints())
