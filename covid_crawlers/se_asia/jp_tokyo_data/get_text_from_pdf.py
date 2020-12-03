from collections import namedtuple

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTTextBoxHorizontal, LTFigure


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

                y1 = 1400 - y1
                y2 = 1400 - y2
                y1, y2 = y2, y1

                text = obj.get_text()
                width = obj.width
                height = obj.height

                text = text.replace('東久留米武蔵村山', '東久留米 武蔵村山')  # HACK!

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

            text_1_num = all(i.isnumeric() or i in ',()'
                             for i in text_item_1.text.strip())
            text_2_num = all(i.isnumeric() or i in ',()'
                             for i in text_item_2.text.strip())

            if not dist:
                continue
            elif text_1_num != text_2_num:
                continue
            elif y in merged:
                continue
            merged.add(y)

            if dist <= 18:  # NOTE ME: This threshold may need to be tuned!!! =====================================
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
