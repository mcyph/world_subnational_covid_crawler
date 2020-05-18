import time
import datetime
from os import listdir
from os.path import exists
from pyquery import PyQuery as _pq
from collections import namedtuple
from urllib.request import urlopen, urlretrieve
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

from covid_19_au_grab.state_news_releases.constants import (
    DT_TOTAL, DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_SOURCE_CONFIRMED, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_OVERSEAS,
    DT_STATUS_ICU
)


TextItem = namedtuple('TextItem', [
    'text',
    'x', 'y',
    'width', 'height'
])


def get_text_from_pdf(path, page_nums=None):
    fp = open(path, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    if page_nums:
        pages = [pages[i] for i in page_nums]

    r = []
    for page in pages:
        print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()

        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                print('At %r is text: %s' % ((x, y), text))

                r.append(TextItem(
                    text=text,
                    x=x, y=y,
                    width=lobj.bbox[1],
                    height=lobj.bbox[2]
                ))
    return r


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
                out_path = f'tokyocities_pdf/tokyocities_%04d_%02d_%02d.pdf' \
                               % (y, m, d)

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
            print(pq(a).html())
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
        for fnam in listdir('tokyocities_pdf'):
            if not '.pdf' in fnam:
                continue
            path = f'tokyocities_pdf/{fnam}'
            print(get_text_from_pdf(path, 0))

    def _get_number_immediately_below(self, text_items, text_item):
        # coords needs to be
        pass


if __name__ == '__main__':
    #ExtractFromTokyoPDF().download_pdfs(only_most_recent=False)
    ExtractFromTokyoPDF().get_from_pdfs()


class CITY:
    pass  # Just for by reference

class UNKNOWN_GENDER:
    pass  # TODO!


map = {
    '総数': (DT_TOTAL, None),
    '濃厚接触者※１': (DT_SOURCE_CONFIRMED, None),
    '海外渡航歴': (DT_SOURCE_OVERSEAS, None),
    '調査中': (DT_SOURCE_UNDER_INVESTIGATION, None),
    'うち重症者': (DT_STATUS_ICU, None),  # CHECK ME! =========================

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

    '総数（累計）': (),
    '重症者': (),
    '死亡（累計）': (),
    '退院（累計）': (),

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
