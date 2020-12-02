# https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_COVID-19_pandemisi

# Toplam vaka sayıları = total
# Toplam ölüm sayıları = deaths

import datetime
from os import listdir
from pyquery import PyQuery as pq

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URLBase, URL
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab._utility.set_locale import set_locale
from covid_19_au_grab.covid_db.datatypes.DatapointMerger import DataPointMerger

WIKI_URL = 'https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_b%C3%B6lgelere_g%C3%B6re_COVID-19_pandemisi'


class TRWikiData(URLBase):
    SOURCE_URL = 'https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27de_b%C3%B6lgelere_g%C3%B6re_COVID-19_pandemisi'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'tr_wikipedia'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'tr' / 'wikidata',
            urls_dict={
                'covid19_in_turkey.html': URL(WIKI_URL, static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = DataPointMerger()
        with set_locale('tr_TR.utf8'):
            for dir_ in sorted(listdir(self.output_dir)):
                with open(self.output_dir / dir_ / 'covid19_in_turkey.html', 'r', encoding='utf-8') as f:
                    html = f.read()

                r.extend(self._get_total_datapoints(html))
                r.extend(self._get_recovered_death_datapoints(html))
        return r

    def _get_total_datapoints(self, html):
        r = self.sdpf()

        if 'TOPLAM VAKA SAYILARI' in html:
            table = pq(html)('.wikitable:contains("TOPLAM VAKA SAYILARI")')
            region_headers = [
                pq(i).text().split('[')[0].strip()
                for i in pq(table)('tbody tr th')[2:]
            ]
            date_trs = pq(table)('tbody tr')

            for date_tr in date_trs:
                if date_tr[0].tag.lower() != 'td':
                    continue

                date_str = pq(date_tr[0]).text().strip().split('[')[0].strip()

                if '<b>+ 882</b>' in html:
                    value_tds = [date_tr[i] for i in range(len(date_tr)-1) if i % 2 == 1]
                else:
                    value_tds = date_tr[1:]

                for value, region in zip(value_tds, region_headers):
                    region = pq(region).text().strip()
                    #print(date_str, pq(value).text(), region)
                    date = datetime.datetime.strptime(date_str + ' 2020' if not ' 2020' in date_str else date_str, '%d %B %Y').strftime('%Y_%m_%d')
                    value = int(pq(value).text().strip().replace('.', ''))

                    if region.lower() == 'toplam':
                        continue

                    r.append(
                        region_schema=Schemas.TR_NUTS1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.TOTAL,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )
        else:
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

                    r.append(
                        region_schema=Schemas.TR_NUTS1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.TOTAL,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r

    def _get_recovered_death_datapoints(self, html):
        r = self.sdpf()

        if 'TOPLAM ÖLÜM SAYILARI' in html:
            table = pq(html)('.wikitable:contains("TOPLAM ÖLÜM SAYILARI")')
            region_headers = [
                pq(i).text().split('[')[0].strip()
                for i in pq(table)('tbody tr th')[2:]
            ]
            date_trs = pq(table)('tbody tr')

            for date_tr in date_trs:
                if date_tr[0].tag.lower() != 'td':
                    continue

                date_str = pq(date_tr[0]).text().strip().split('[')[0].strip()

                if '<b>+ 882</b>' in html:
                    value_tds = [date_tr[i] for i in range(len(date_tr)-1) if i % 2 == 1]
                else:
                    value_tds = date_tr[1:]

                for value, region in zip(value_tds, region_headers):
                    region = pq(region).text().strip()
                    date = datetime.datetime.strptime(date_str + ' 2020' if not ' 2020' in date_str else date_str, '%d %B %Y').strftime('%Y_%m_%d')
                    value = int(pq(value).text().strip().replace('.', ''))

                    if region.lower() == 'toplam':
                        continue

                    r.append(
                        region_schema=Schemas.TR_NUTS1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )
        else:
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

                    r.append(
                        region_schema=Schemas.TR_NUTS1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(TRWikiData().get_datapoints())
