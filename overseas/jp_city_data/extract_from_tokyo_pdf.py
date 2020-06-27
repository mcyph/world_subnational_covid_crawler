import csv
import time
import datetime
from math import sqrt
from os import listdir
from os.path import exists
from pyquery import PyQuery as _pq
from collections import namedtuple
from urllib.request import urlopen
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextBoxHorizontal, LTFigure
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

from covid_19_au_grab.datatypes.constants import (
    SCHEMA_JP_CITY,
    DT_NEW, DT_TOTAL,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_SOURCE_CONFIRMED, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_OVERSEAS,
    DT_STATUS_ICU, DT_STATUS_DEATHS
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.get_package_dir import (
    get_package_dir
)


TextItem = namedtuple('TextItem', [
    'x1', 'y1', 'x2', 'y2',
    'width', 'height',
    'text'
])


def get_text_from_pdf(path, page_nums=None):
    r = []

    fp = open(path, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp, pagenos=page_nums)

    def parse_obj(lt_objs):
        # https://stackoverflow.com/questions/31819862/python-pdf-mining-get-position-of-text-on-every-line
        # loop over the object list

        for obj in lt_objs:
            if isinstance(obj, LTTextLine):
                x1, y1, x2, y2 = obj.bbox
                assert x1 < x2
                assert y1 < y2

                # x1 = 800-x1
                # x2 = 800-x2
                y1 = 1400 - y1
                y2 = 1400 - y2
                y1, y2 = y2, y1

                text = obj.get_text()
                width = obj.width
                height = obj.height

                text = text.replace('東久留米武蔵村山', '東久留米 武蔵村山')  # HACK!

                #if '\n' in text:
                #    WARNING: Some have trailing newlines!!!! =====================================
                #    print("\\N!", [text])

                for line_i, line in enumerate(text.split('\n')):   # CHECK WHETHER THIS IS NEEDED!
                    for word_j, word in enumerate(line.split()):
                        each_height = height / text.count('\n')
                        i_y1 = y1 + each_height * line_i
                        i_y2 = y2 + each_height * (line_i + 1)

                        each_width = width / len(line.split())
                        i_x1 = x1 + each_width * word_j
                        i_x2 = x2 + each_width * (word_j + 1)

                        r.append(TextItem(
                            text=word,
                            x1=i_x1, y1=i_y1,
                            x2=i_x2, y2=i_y2,
                            width=each_width,
                            height=each_height
                        ))

                        #if r[-1].text in ('10', '29'):
                        #    print("LINE:", [line_i, line])
                        #    print(r[-1], x1, y1, x2, y2, each_width, word_j)

            # if it's a textbox, also recurse
            if isinstance(obj, LTTextBoxHorizontal):
                parse_obj(obj._objs)

            # if it's a container, recurse
            elif isinstance(obj, LTFigure):
                parse_obj(obj._objs)

    for page in pages:
        print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()

        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                parse_obj(lobj)

    for xx in range(5):
        dists = []

        for x in range(len(r)):
            for y in range(len(r)):
                text_item_1 = r[x]
                text_item_2 = r[y]

                dists.append(
                    (abs(text_item_1.y1-text_item_2.y1), x, y)
                )

        merged = set()
        for dist, x, y in sorted(dists):
            text_item_1 = r[x]
            text_item_2 = r[y]

            text_1_num = all(i.isnumeric() or i == ','
                             for i in text_item_1.text.strip())
            text_2_num = all(i.isnumeric() or i == ','
                             for i in text_item_2.text.strip())

            if not dist:
                continue
            elif text_1_num != text_2_num:
                continue
            elif y in merged:
                continue
            merged.add(y)

            if dist <= 30:
                r[y] = TextItem(
                    text=text_item_2.text,
                    x1=text_item_2.x1,
                    y1=text_item_1.y1,
                    x2=text_item_2.x2,
                    y2=text_item_1.y1+text_item_2.height,
                    width=text_item_2.width,
                    height=text_item_2.height
                )

    r.sort(key=lambda x: (x.y1, x.x1, x.x2, x.y2))
    #for i in r:
    #    print(i)
    return r


def pq(*args, **kw):
    for x in range(5):
        try:
            return _pq(*args, **kw)
        except:
            if x == 4:
                raise
            time.sleep(1)


class CITY:
    pass  # Just for by reference

class UNKNOWN_GENDER:
    pass  # TODO!


stats_map = {
    '総数': (DT_NEW, None),
    '濃厚接触者※１': (DT_SOURCE_CONFIRMED, None),
    '海外渡航歴': (DT_SOURCE_OVERSEAS, None),
    '調査中': (DT_SOURCE_UNDER_INVESTIGATION, None),
    #'うち重症者': (DT_STATUS_ICU, None),  # CHECK ME! =========================

    '10歳未満': (DT_TOTAL, '0-9'),
    '10代': (DT_TOTAL, '10-19'),
    '20代': (DT_TOTAL, '20-29'),
    '30代': (DT_TOTAL, '30-39'),
    '40代': (DT_TOTAL, '40-49'),
    '50代': (DT_TOTAL, '50-59'),
    '60代': (DT_TOTAL, '60-69'),
    '70代': (DT_TOTAL, '70-79'),
    '80代': (DT_TOTAL, '80-89'),
    '90代': (DT_TOTAL, '90-99'),
    '100歳以上': (DT_TOTAL, '100+'),
    '不明_1': (DT_TOTAL, 'Unknown'),  # FIXME!!! ===============================================

    '男性': (DT_TOTAL_MALE, None),
    '女性': (DT_TOTAL_FEMALE, None),
    '不明_2': UNKNOWN_GENDER,  # FIXME!!! ===============================================

    '総数（累計）': (DT_TOTAL, None),
    '重症者': (DT_STATUS_ICU, None),
    '死亡（累計）': (DT_STATUS_DEATHS, None),
    #'退院（累計）': (DT_STATUS_RELEASED),

    '千代田': CITY,
    '中央': CITY,
    '港': CITY,
    '新宿': CITY,
    '文京': CITY,
    '台東': CITY,
    '墨田': CITY,
    '江東': CITY,
    '品川': CITY,
    '目黒': CITY,
    '大田': CITY,
    '世田谷': CITY,
    '渋谷': CITY,
    '中野': CITY,
    '杉並': CITY,
    '豊島': CITY,
    '北': CITY,
    '荒川': CITY,
    '板橋': CITY,
    '練馬': CITY,
    '足立': CITY,
    '葛飾': CITY,
    '江戸川': CITY,
    '八王子': CITY,
    '立川': CITY,
    '武蔵野': CITY,
    '三鷹': CITY,
    '青梅': CITY,
    '府中': CITY,
    '昭島': CITY,
    '調布': CITY,
    '町田': CITY,
    '小金井': CITY,
    '小平': CITY,
    '日野': CITY,
    '東村山': CITY,
    '国分寺': CITY,
    '国立': CITY,
    '福生': CITY,
    '狛江': CITY,
    '東大和': CITY,
    '清瀬': CITY,
    '東久留米': CITY,
    '武蔵村山': CITY,
    '多摩': CITY,
    '稲城': CITY,
    '羽村': CITY,
    'あきる野': CITY,
    '西東京': CITY,
    '瑞穂': CITY,
    '日の出': CITY,
    '檜原': CITY,
    '奥多摩': CITY,
    '大島': CITY,
    '利島': CITY,
    '新島': CITY,
    '神津島': CITY,
    '三宅': CITY,
    '御蔵島': CITY,
    '八丈': CITY,
    '青ヶ島': CITY,
    '小笠原': CITY,

    '都外': CITY,
    '調査中※': CITY,
}


def get_tokyo_cities_to_en_map():
    r = {}
    with open(get_package_dir() /
              'overseas' /
              'jp_city_data'/
              'tokyo_cities.csv', 'r', encoding='utf-8') as f:

        for item in csv.DictReader(f, delimiter='\t'):
            r[item['ja'].strip()] = item['en'].strip()
            for c in '区町村市島':
                r[item['ja'].strip().rstrip(c)] = item['en'].strip()
    return r


_tokyo_cities_to_en = get_tokyo_cities_to_en_map()


class ExtractFromTokyoPDF:
    def download_pdfs(self, only_most_recent=True):
        base_dir = get_package_dir() / \
                   'overseas' / \
                   'jp_city_data' / \
                   'tokyocities_pdf'

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
        base_dir = get_package_dir() / \
                   'overseas' / \
                   'jp_city_data' / \
                   'tokyocities_pdf'

        r = []
        for fnam in sorted(listdir(base_dir)):
            if not '.pdf' in fnam:
                continue
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
                region_parent='Tokyo',  # CHECK ME - should this have "city" etc added?
                region_schema=SCHEMA_JP_CITY,
                region_child=region_child,
                datatype=DT_TOTAL,
                value=num_below,
                source_url='https://www.metro.tokyo.lg.jp', # FIXME!
                date_updated=date_updated
            )
        else:
            print(i)
            datatype, agerange = i
            return DataPoint(
                region_parent='Tokyo',  # CHECK ME - should this have "city" etc added?
                region_schema=SCHEMA_JP_CITY,
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


