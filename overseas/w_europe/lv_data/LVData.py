# https://covid19.gov.lv/covid-19/covid-19-statistika/covid-19-izplatiba-latvija
import json
import datetime
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


#REGIONS_URL = 'https://e.infogram.com/api/live/flex/fd882665-1d1a-4706-9b74-e36f4767d2b5/e0023a48-5a9a-427c-b123-76caef50513a'
REGIONS_URL = 'https://e.infogram.com/d3e1b3ca-f610-456b-b5e0-62ac19d01dfc?src=embed'


regions_map = {
    'kocēnu novads',
    'līgatnes novads',
    'pārgaujas novads',
    'priekuļu novads',
    'rūjienas novads',
    'strenču novads',
    'varakļānu novads',
    'viļānu novads'
}


class LVData(URLBase):
    SOURCE_URL = 'https://covid19.gov.lv/covid-19/covid-19-statistika/covid-19-izplatiba-latvija'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'lv_infogram'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'lv' / 'data',
            urls_dict={
                'regions_data.json': URL(REGIONS_URL, static_file=False),
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'lv', 'daugavpils novads'): None,
                ('admin_1', 'lv', 'jelgavas novads'): None,
                ('admin_1', 'lv', 'jēkabpils novads'): None,
                ('admin_1', 'lv', 'kocēnu novads'): None,
                ('admin_1', 'lv', 'līgatnes novads'): None,
                ('admin_1', 'lv', 'pārgaujas novads'): None,
                ('admin_1', 'lv', 'pārgaujas novads'): None,
                ('admin_1', 'lv', 'priekuļu novads'): None,
                ('admin_1', 'lv', 'rēzeknes novads'): None,
                ('admin_1', 'lv', 'rūjienas novads'): None,
                ('admin_1', 'lv', 'strenču novads'): None,
                ('admin_1', 'lv', 'varakļānu novads'): None,
                ('admin_1', 'lv', 'ventspils novads'): None,
                ('admin_1', 'lv', 'viļānu novads'): None,
            },
            mode=MODE_STRICT
        )
        #self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_regions_data())
        return r

    def _get_regions_data(self):
        # # {"data":[[["Aglonas novads",0,"0","56.0965 27.114","Aglonas novads"],
        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()
            path = f'{base_dir}/{date}/regions_data.json'
            print(path)
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
                if '<!DOCTYPE HTML>' in data:
                    continue   # WARNING!!! - TODO: Add agegroup data, etc from the new page!!! ===================================================
                data = json.loads(data)

            for i_data in data['data']:
                for region_name, value, *leftover in i_data:
                    print(region_name)

                    # Only confirmed and deaths are shown in the dashboard
                    date = datetime.datetime.fromtimestamp(data['refreshed']/1000.0).strftime('%Y_%m_%d')

                    if value is not None:
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='LV',
                            region_child=region_name,
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

            out.extend(r)
        return out


if __name__ == '__main__':
    from pprint import pprint
    pprint(LVData().get_datapoints())
