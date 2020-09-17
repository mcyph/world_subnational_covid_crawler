# https://www.koronavirus.hr/
import json
import gzip
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir


region_map = {
    'bjelovarsko-bilogorska': 'HR-07',
    'brodsko-posavska': 'HR-12',
    'dubrovacko-neretvanska': 'HR-19',
    'grad-zagreb': 'HR-21',
    'istarska': 'HR-18',
    'karlovacka': 'HR-04',
    'koprivnicko-krizevacka': 'HR-06',
    'krapinsko-zagorska-zupanija': 'HR-02',
    'licko-senjska': 'HR-09',
    'medjimurska': 'HR-20',
    'osjecko-baranjska': 'HR-14',
    'pozesko-slavonska': 'HR-11',
    'primorsko-goranska': 'HR-08',
    'sibensko-kninska': 'HR-15',
    'sisacko-moslavacka': 'HR-03',
    'splitsko-dalmatinska': 'HR-17',
    'varazdinska': 'HR-05',
    'viroviticko-podravska': 'HR-10',
    'vukovarsko-srijemska': 'HR-16',
    'zadarska': 'HR-13',
    'zagrebacka': 'HR-01',
}


class HRData(URLBase):
    SOURCE_URL = 'https://www.koronavirus.hr/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'hr_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'hr' / 'data',
            urls_dict={
                'index.html': URL('https://www.koronavirus.hr/',
                                  static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'hr', 'hr-11'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        # <circle class='zarazeni' data-url='https://www.koronavirus.hr/licko-senjska/156' cx='216' cy='295' r='10' stroke='black' stroke-width='0' fill='rgba(255, 0, 0, 0.60)' />
        # <text class='zarazeni' data-url='https://www.koronavirus.hr/licko-senjska/156' x='216' y='295' stroke='transparent' text-anchor='middle' dy='0.35em' style='font-size: 10px;'>22</text>
        # <circle class='aktivni' data-url='https://www.koronavirus.hr/licko-senjska/156' cx='216' cy='295' r='10' stroke='black' stroke-width='0' fill='rgba(255, 132, 8, 0.8)' />
        # <text class='aktivni' data-url='https://www.koronavirus.hr/licko-senjska/156' x='216' y='295' stroke='transparent' text-anchor='middle' dy='0.35em' style='font-size: 10px;'>2</text>

        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/index.html'

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    data = brotli.decompress(f.read()).decode('utf-8')

            for text_elm in pq(data)('text.zarazeni'):
                if not text_elm.get('data-url').strip():
                    continue
                value = int(pq(text_elm).text().replace('.', ''))
                region_child = region_map[text_elm.get('data-url').split('/')[-2]]
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='HR',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            for text_elm in pq(data)('text.aktivni'):
                if not text_elm.get('data-url').strip():
                    continue
                value = int(pq(text_elm).text().replace('.', ''))
                region_child = region_map[text_elm.get('data-url').split('/')[-2]]
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='HR',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(HRData().get_datapoints())

