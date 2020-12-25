import time
import datetime
from math import sqrt
from os import listdir
from os.path import exists
from pyquery import PyQuery as _pq
from urllib.request import urlopen
from _utility.cache_by_date import cache_by_date

from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DataPoint import DataPoint
from _utility.get_package_dir import get_overseas_dir
from covid_crawlers.se_asia.jp_data.jp_city_data import get_tokyo_cities_to_en_map
from covid_crawlers.se_asia.jp_tokyo_data.get_text_from_pdf import get_text_from_pdf
from covid_crawlers.se_asia.jp_tokyo_data.tokyo_pdf_stats_map import stats_map, CITY

_tokyo_cities_to_en = get_tokyo_cities_to_en_map()


def pq(*args, **kw):
    for x in range(5):
        try:
            return _pq(*args, **kw)
        except:
            if x == 4:
                raise
            time.sleep(1)


PDFS_BASE_DIR = get_overseas_dir() / 'jp_city_data' / 'pdfs'


class ExtractFromTokyoPDF:
    def download_pdfs(self, only_most_recent=True):
        current_month = datetime.datetime.now().month

        if only_most_recent:
            months = [current_month]
        else:
            months = [
                month for month in range(4, current_month+1)
            ]

        for month in months:
            url = 'https://www.metro.tokyo.lg.jp/tosei/' \
                  'hodohappyo/press/%s/%02d/index.html' % (datetime.datetime.now().year, month)
            print(url)

            html = pq(url, parser='html', encoding='utf-8')

            for a in html('a'):
                if not '新型コロナウイルスに関連した患者の発生' in pq(a).html():
                    continue
                print(pq(a).html())

                href = pq(a).attr('href')
                if '2020/12/06/01.html' in href:
                    # HACK: This day didn't have the normal "by city" tables!
                    continue

                y, m, d = href.split('/')[-4:-1]
                d = int(d)
                m = int(m)
                y = int(y)
                out_path = PDFS_BASE_DIR / (f'tokyocities_%04d_%02d_%02d.pdf' % (y, m, d))

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
        r = []
        for fnam in sorted(listdir(PDFS_BASE_DIR)):
            if not '.pdf' in fnam:
                continue
            elif fnam == 'tokyocities_2020_12_06.pdf':
                continue  # HACK!
            r.extend(self._get_from_pdfs(fnam))
        return r

    @cache_by_date(source_id='jp_tokyo_city', validate_date=False)  # NOTE ME!!
    def _get_from_pdfs(self, fnam):
        r = []

        #elif not '2020_08_09' in fnam:
        #    continue
        path = PDFS_BASE_DIR / fnam
        print("Getting from PDF:", path)

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

            num_below = self._get_number_immediately_below(text_items, text_item, brackets=False)
            try:
                num_below_brackets = self._get_number_immediately_below(text_items, text_item, brackets=True)
            except IndexError:
                # No number in brackets available!
                num_below_brackets = None

            r.extend(self._to_datatype(text_item, num_below, num_below_brackets, found_fumei, date))

            if text_item.text == '不明':
                found_fumei = True

        return r

    def _to_datatype(self, text_item, num_below, num_below_brackets, found_fumei, date_updated):
        r = []

        if not found_fumei and text_item.text == '不明':
            i = stats_map['不明_1']
        elif found_fumei and text_item.text == '不明':
            i = stats_map['不明_2']
        else:
            i = stats_map[text_item.text]

        if i == CITY:
            if date_updated >= '2020_08_03':
                # As far as I know, the number in brackets
                # is always provided except before this date
                assert num_below_brackets is not None, \
                    (date_updated, text_item, num_below, num_below_brackets, found_fumei)

            if text_item.text == '調査中※':
                region_child = 'Unknown'
            elif text_item.text == '都外':
                region_child = 'Non-resident'
            else:
                region_child = text_item.text #_tokyo_cities_to_en[text_item.text]

            r.append(DataPoint(
                region_schema=Schemas.JP_CITY,
                region_parent='Tokyo',  # CHECK ME - should this have "city" etc added?
                region_child=region_child,
                datatype=DataTypes.TOTAL,
                value=num_below,
                source_url='https://www.metro.tokyo.lg.jp', # FIXME!
                date_updated=date_updated
            ))

            if num_below_brackets is not None:
                r.append(DataPoint(
                    region_schema=Schemas.JP_CITY,
                    region_parent='Tokyo',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DISCHARGED_DEATHS,
                    value=num_below_brackets,
                    source_url='https://www.metro.tokyo.lg.jp',  # FIXME!
                    date_updated=date_updated
                ))

                # CHECK THIS: is there a better way of getting the active numbers for each city?
                r.append(DataPoint(
                    region_schema=Schemas.JP_CITY,
                    region_parent='Tokyo',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=num_below - num_below_brackets,
                    source_url='https://www.metro.tokyo.lg.jp',  # FIXME!
                    date_updated=date_updated
                ))
        else:
            print(i)
            datatype, agerange = i
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='jp',  # CHECK ME - should this have "city" etc added?
                region_child='jp-13',
                agerange=agerange,
                datatype=datatype,
                value=num_below,
                source_url='https://www.metro.tokyo.lg.jp',  # FIXME!
                date_updated=date_updated
            ))

        return r

    def _get_number_immediately_below(self, text_items, text_item, brackets=False):
        # coords needs to be
        dists = []

        for other_text_item in text_items:
            # Brackets: for discharged or deaths
            is_bracket = other_text_item.text[0] == '(' or other_text_item.text[-1] == ')'
            #print('OTHER TEXT:', other_text_item.text, is_bracket)

            if other_text_item == text_item:
                continue
            elif brackets and not is_bracket:
                # Don't process if enclosed and not in bracket mode
                continue
            elif not brackets and is_bracket:
                # Don't process if not enclosed and in bracket mode
                continue

            try:
                num = other_text_item.text.replace(',', '').strip()
                if brackets:
                    num = num.replace(')', '').replace('(', '').strip()
                num = int(num)
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
    dp = ExtractFromTokyoPDF().get_from_pdfs()
    pprint(dp)
