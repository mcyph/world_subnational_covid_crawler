# https://covid19.ncdc.gov.ng/

import json
import datetime
from os import listdir
from pyquery import PyQuery as pq
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URLBase, URL
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


class NGData(URLBase):
    SOURCE_URL = 'https://covid19.ncdc.gov.ng/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ng_ncdc'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'ng' / 'data',
            urls_dict={
                'index.html': URL('https://covid19.ncdc.gov.ng/', static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_total_datapoints())
        return r

    def _get_total_datapoints(self):
        r = []
        base_dir = self.get_path_in_dir('')

        datatype_map = {
            'No. of Cases (Lab Confirmed)': DataTypes.CONFIRMED,
            'No. of Cases (on admission)': DataTypes.PROBABLE,
            'No. Discharged': None,
            'No. of Deaths': DataTypes.STATUS_DEATHS
        }

        for date in sorted(listdir(base_dir)):
            with open(base_dir / date / 'index.html',
                      'r', encoding='utf-8') as f:
                html = f.read()

            table = pq(html)('table:contains("States Affected")')
            datatypes = [
                datatype_map[pq(i).text().strip()]
                for i in pq(table)('thead tr th')[1:]
            ]
            region_trs = pq(table)('tbody tr')

            for region_tr in region_trs:
                region = pq(region_tr[0]).text().strip()
                vals = {}

                for datatype, value in zip(datatypes, region_tr[1:]):
                    if not datatype:
                        continue

                    value = int(pq(value).text().replace(',', ''))
                    vals[datatype] = value

                    r.append(DataPoint(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='NG',
                        region_child=region,
                        datatype=datatype,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                r.append(DataPoint(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='NG',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    value=vals[DataTypes.CONFIRMED]+vals[DataTypes.PROBABLE],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(NGData().get_datapoints())
