# https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_COVID-19_pandemisi

# Toplam vaka sayıları = total
# Toplam ölüm sayıları = deaths

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
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_TR_NUTS1,
    DT_TESTS_TOTAL, DT_NEW,
    DT_TOTAL, DT_STATUS_RECOVERED,
    DT_STATUS_DEATHS, DT_STATUS_ACTIVE,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)
from covid_19_au_grab.set_locale import set_locale

WIKI_URL = 'https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_COVID-19_pandemisi'


class TRWikiData(URLBase):
    SOURCE_URL = 'https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_COVID-19_pandemisi'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'tr_wikipedia'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'tr' / 'wikidata',
            urls_dict={
                'covid19_in_turkey.html': URL(WIKI_URL, static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        with set_locale('tr_TR.utf8'):
            for dir_ in listdir(self.output_dir):
                with open(self.output_dir / dir_ / 'covid19_in_turkey.html', 'r', encoding='utf-8') as f:
                    html = f.read()

                r.extend(self._get_total_datapoints(html))
                r.extend(self._get_recovered_death_datapoints(html))
        return r

    def _get_total_datapoints(self, html):
        r = []
        table = pq(html)('.wikitable:contains("Toplam vaka sayıları")')
        headers = [
            pq(i).text().split('[')[0].strip()
            for i in pq(table)('tbody tr th')[2:]
        ]
        region_trs = pq(table)('tbody tr')

        for region_tr in region_trs:
            if region_tr[0].tag.lower() != 'td':
                continue

            region = pq(region_tr[0]).text().strip()

            for date_str, value in zip(headers, region_tr[1:]):
                date = datetime.datetime.strptime(date_str+' 2020', '%d %B %Y').strftime('%Y_%m_%d')
                value = int(pq(value).text().replace('.', ''))

                r.append(DataPoint(
                    region_schema=SCHEMA_TR_NUTS1,
                    region_parent='TR',
                    region_child=region,
                    datatype=DT_TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_recovered_death_datapoints(self, html):
        r = []

        table = pq(html)('.wikitable:contains("Toplam ölüm sayıları")')
        headers = [
            pq(i).text().split('[')[0].strip()
            for i in pq(table)('tbody tr th')[2:]
        ]
        region_trs = pq(table)('tbody tr')

        for region_tr in region_trs:
            if region_tr[0].tag.lower() != 'td':
                continue

            region = pq(region_tr[0]).text().strip()

            for date_str, value in zip(headers, region_tr[1:]):
                date = datetime.datetime.strptime(date_str + ' 2020', '%d %B %Y').strftime('%Y_%m_%d')
                value = int(pq(value).text().replace('.', ''))

                r.append(DataPoint(
                    region_schema=SCHEMA_TR_NUTS1,
                    region_parent='TR',
                    region_child=region,
                    datatype=DT_STATUS_DEATHS,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(TRWikiData().get_datapoints())
