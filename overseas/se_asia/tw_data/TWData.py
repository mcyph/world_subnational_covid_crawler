import json
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


place_map = dict([i.split('\t')[::-1] for i in """
TW-CHA	Changhua county
TW-CYI	Chiayi city
TW-CYQ	Chiayi county
TW-HSZ	Hsinchu city
TW-HSQ	Hsinchu county
TW-HUA	Hualien county
TW-KHH	Kaohsiung city
TW-KEE	Keelung city
TW-KIN	Kinmen county
TW-LIE	Lienchiang county
TW-MIA	Miaoli county
TW-NAN	Nantou county
TW-NWT	New Taipei city
TW-PEN	Penghu county
TW-PIF	Pingtung county
TW-TXG	Taichung city
TW-TNN	Tainan city
TW-TPE	Taipei city
TW-TTT	Taitung county
TW-TAO	Taoyuan city
TW-ILA	Yilan county
TW-YUN	Yunlin county
""".strip().lower().split('\n')])


class TWData(URLBase):
    SOURCE_URL = 'https://nidss.cdc.gov.tw/en/NIDSS_DiseaseMap.aspx?dc=1&dt=5&disease=19CoV'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'tw_cdc'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'tw' / 'data',
            urls_dict={
                'tw_corona.html': URL('https://nidss.cdc.gov.tw/en/NIDSS_DiseaseMap.aspx?dc=1&dt=5&disease=19CoV',
                                      static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'tw', 'tw-nwt'): None,
                ('admin_1', 'tw', 'tw-lie'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()
            path = f'{base_dir}/{date}/tw_corona.html'
            print(path)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    html = f.read()
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    html = brotli.decompress(f.read()).decode('utf-8')

            new_data_template = '.geojson","series":[{'
            if new_data_template in html:
                data = '[{%s}]' % html.split(new_data_template)[-1].split('}],')[0]
            else:
                data = html.split('var jdata1 = ')[-1].split('\n')[0].strip().strip(';').replace("'", '"')

            for item in json.loads(data):
                # [{'code':'Taipei City', 'value':118}, ...]
                region = place_map[item['code'].strip().lower()]

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='TW',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    value=int(item['value']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            out.extend(r)
        return out


if __name__ == '__main__':
    from pprint import pprint
    pprint(TWData().get_datapoints())
