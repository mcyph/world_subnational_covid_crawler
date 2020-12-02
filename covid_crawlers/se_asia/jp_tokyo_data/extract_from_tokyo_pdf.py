import time
import datetime
from math import sqrt
from os import listdir
from os.path import exists
from pyquery import PyQuery as _pq
from urllib.request import urlopen

from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_db.datatypes.DataPoint import DataPoint
from covid_19_au_grab._utility.get_package_dir import get_package_dir
from covid_19_au_grab.covid_crawlers.se_asia.jp_data.jp_city_data import get_tokyo_cities_to_en_map
from covid_19_au_grab.covid_crawlers.se_asia.jp_tokyo_data.get_text_from_pdf import get_text_from_pdf
from covid_19_au_grab.covid_crawlers.se_asia.jp_tokyo_data.tokyo_pdf_stats_map import stats_map, CITY

_tokyo_cities_to_en = get_tokyo_cities_to_en_map()


def pq(*args, **kw):
    for x in range(5):
        try:
            return _pq(*args, **kw)
        except:
            if x == 4:
                raise
            time.sleep(1)


class ExtractFromTokyoPDF:
    def download_pdfs(self, only_most_recent=True):
        base_dir = get_package_dir() / 'covid_crawlers' / 'se_asia' / 'jp_tokyo_data' / 'tokyocities_pdf'

        current_month = datetime.datetime.now().month

        if only_most_recent:
            months = [current_month]
        else:
            months = [
                month for month in range(4, current_month+1)
            ]

        for month in months:
            url = 'https://www.metro.tokyo.lg.jp/tosei/' \
                  'hodohappyo/press/2020/%02d/index.html' % month
            print(url)
            html = pq(url, parser='html', encoding='utf-8')

            for a in html('a'):
                if not '新型コロナウイルスに関連した患者の発生' in pq(a).html():
                    continue
                print(pq(a).html())

                href = pq(a).attr('href')
                y, m, d = href.split('/')[-4:-1]
                d = int(d)
                m = int(m)
                y = int(y)
                out_path = base_dir / (f'tokyocities_%04d_%02d_%02d.pdf' % (y, m, d))

                if not exists(out_path):
                    self._download_pdfs_from_month_page(
                        'https://www.metro.tokyo.lg.jp'+href, out_path
                    )

    def _download_pdfs_from_month_page(self, url, out_path):
        # https://www.metro.tokyo.lg.jp/tosei/hodohappyo/press/2020/04/28/14.html
        html = pq(url, parser='html', encoding='utf-8')

        for a in html('a'):
            if not '別紙（PDF：' in pq(a).html():
                continue
            #print(pq(a).html())
            href = pq(a).attr('href')

            for x in range(5):
                try:
                    with open(out_path, 'wb') as f:
                        f.write(urlopen('https://www.metro.tokyo.lg.jp' + href).read())
                    break
                except:
                    if x == 4:
                        raise
                    time.sleep(1)

        time.sleep(5)

    def get_from_pdfs(self):
        base_dir = get_package_dir() / 'covid_crawlers' / 'se_asia' / 'jp_tokyo_data' / 'tokyocities_pdf'

        r = []
        for fnam in sorted(listdir(base_dir)):
            if not '.pdf' in fnam:
                continue
            #elif not '2020_08_09' in fnam:
            #    continue
            path = base_dir / fnam

            found_fumei = False
            text_items = get_text_from_pdf(path, [0])
            date = fnam.partition('_')[-1]
            date = date.split('.')[0]

            for text_item in text_items:
                if text_item.text != '不明' and not text_item.text in stats_map:
                    print("IGNORE:", text_item.text)
                    continue
                elif found_fumei and text_item.text == '不明':
                    continue # HACK!

                num_below = self._get_number_immediately_below(
                    text_items, text_item
                )
                r.append(self._to_datatype(
                    text_item, num_below, found_fumei, date
                ))
                if text_item.text == '不明':
                    found_fumei = True
        return r

    def _to_datatype(self, text_item, num_below, found_fumei, date_updated):

        if not found_fumei and text_item.text == '不明':
            i = stats_map['不明_1']
        elif found_fumei and text_item.text == '不明':
            i = stats_map['不明_2']
        else:
            i = stats_map[text_item.text]

        if i == CITY:
            if text_item.text == '調査中※':
                region_child = 'Unknown'
            elif text_item.text == '都外':
                region_child = 'Non-resident'
            else:
                region_child = text_item.text #_tokyo_cities_to_en[text_item.text]

            return DataPoint(
                region_schema=Schemas.JP_CITY,
                region_parent='Tokyo',  # CHECK ME - should this have "city" etc added?
                region_child=region_child,
                datatype=DataTypes.TOTAL,
                value=num_below,
                source_url='https://www.metro.tokyo.lg.jp', # FIXME!
                date_updated=date_updated
            )
        else:
            print(i)
            datatype, agerange = i
            return DataPoint(
                region_schema=Schemas.JP_CITY,
                region_parent='Tokyo',  # CHECK ME - should this have "city" etc added?
                region_child='unknown',
                agerange=agerange,
                datatype=datatype,
                value=num_below,
                source_url='https://www.metro.tokyo.lg.jp',  # FIXME!
                date_updated=date_updated
            )

    def _get_number_immediately_below(self, text_items, text_item):
        # coords needs to be
        dists = []

        for other_text_item in text_items:
            if other_text_item == text_item:
                continue

            try:
                num = int(other_text_item.text.replace(',', '').strip())
            except ValueError:
                continue

            if other_text_item.y1 > text_item.y1:
                coords1 = [
                    other_text_item.x1 + other_text_item.width / 2,
                    other_text_item.y1 + other_text_item.height / 2
                ]
                coords2 = [
                    text_item.x1 + text_item.width / 2,
                    text_item.y1 + text_item.height / 2
                ]

                a = coords1[0] - coords2[0]
                b = coords1[1] - coords2[1]
                c = sqrt(a * a + b * b)

                dists.append((c, num))

        dists.sort()
        return dists[0][1]


if __name__ == '__main__':
    from pprint import pprint
    #ExtractFromTokyoPDF().download_pdfs(only_most_recent=False)
    pprint(ExtractFromTokyoPDF().get_from_pdfs())
