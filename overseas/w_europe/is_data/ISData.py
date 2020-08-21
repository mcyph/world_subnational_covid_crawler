import json
import gzip
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

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


place_map = dict([i.split('\t')[::-1] for i in """
IS-1	Höfuðborgarsvæðið
IS-1	Greater Reykjavík
IS-2	Suðurnes
IS-2	Suðurnes Peninsula
IS-3	Vesturland
IS-3	Western Region
IS-3	West  Iceland
IS-3	West Iceland
IS-4	Vestfirðir
IS-4	West  Fjords
IS-4	West Fjords
IS-5	Norðurland vestra
IS-5	Northwest  Iceland
IS-5	Northwest Iceland
IS-6	Norðurland eystra
IS-6	Northeast  Iceland
IS-6	Northeast Iceland
IS-7	Austurland
IS-7	East Iceland
IS-8	Suðurland
IS-8	South Iceland
Unknown	Unknown
Other	Abroad
""".strip().split('\n')])


class ISData(URLBase):
    SOURCE_URL = 'https://www.covid.is/data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'is_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'is' / 'data',
            urls_dict={
                'is_index.html': URL('https://e.infogram.com/e3205e42-19b3-4e3a-a452-84192884450d?src=embed',
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
            path = f'{base_dir}/{date}/is_index.html'
            with open(path, 'rb') as f:
                data = f.read()
                data = data.decode('utf-8')

            # TODO: There are quite a few more stats!!

            regional_stats = data.split('[[[null,{"font-weight":"700","value":"Infections"},'
                                        '{"font-weight":"700","value":"Quarantine"}],')[1].split(']]],')[0]
            #print(regional_stats)
            regional_stats = json.loads(f'[{regional_stats}]]')

            for region, infections_dict, quarantine_dict in regional_stats:
                region = place_map[region]

                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='IS',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    # This changed to be an int from a dict on 9 Jun
                    value=int(infections_dict['value']) if isinstance(infections_dict, dict) else int(infections_dict),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ISData().get_datapoints())

