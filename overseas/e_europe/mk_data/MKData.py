# https://koronavirus.gov.mk/vesti/218046
import re
import json
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir


region_map = dict([i.split('\t')[::-1] for i in """
MK-01	Аеродром
MK-02	Арачиново
MK-03	Берово
MK-04	Битола
MK-05	Богданци
MK-06	Боговиње
MK-07	Босилово
MK-08	Брвеница
MK-09	Бутел
MK-10	Валандово
MK-11	Василево
MK-12	Вевчани
MK-13	Велес
MK-14	Виница
MK-15	Вранештица
MK-16	Врапчиште
MK-17	Гази Баба
MK-18	Гевгелија
MK-19	Гостивар
MK-20	Градско
MK-21	Дебар
MK-22	Дебрца
MK-23	Делчево
MK-24	Демир Капија
MK-25	Демир Хисар
MK-26	Дојран
MK-27	Долнени
MK-28	Другово
MK-29	Ѓорче Петров
MK-30	Желино
MK-31	Зајас
MK-32	Зелениково
MK-33	Зрновци
MK-34	Илинден
MK-35	Јегуновце
MK-36	Кавадарци
MK-37	Карбинци
MK-38	Карпош
MK-39	Кисела Вода
MK-40	Кичево
MK-41	Конче
MK-42	Кочани
MK-43	Кратово
MK-44	Крива Паланка
MK-45	Кривогаштани
MK-46	Крушево
MK-47	Куманово
MK-48	Липково
MK-49	Лозово
MK-50	Маврово и Ростуше
MK-51	Македонска Каменица
MK-52	Македонски Брод
MK-53	Могила
MK-54	Неготино
MK-55	Новаци
MK-56	Ново Село
MK-57	Осломеј
MK-58	Охрид
MK-59	Петровец
MK-60	Пехчево
MK-61	Пласница
MK-62	Прилеп
MK-63	Пробиштип
MK-64	Радовиш
MK-65	Ранковце
MK-66	Ресен
MK-67	Росоман
MK-68	Сарај
MK-69	Свети Николе
MK-70	Сопиште
MK-71	Старо Нагоричане
MK-72	Струга
MK-73	Струмица
MK-74	Студеничани
MK-75	Теарце
MK-76	Тетово
MK-77	Центар
MK-78	Центар Жупа
MK-79	Чаир
MK-80	Чашка
MK-81	Чешиново-Облешево
MK-82	Чучер-Сандево
MK-83	Штип
MK-84	Шуто Оризари
MK-85	скопје
""".lower().strip().split('\n')])

MK_RE = re.compile(
    '•&nbsp; &nbsp; &nbsp; &nbsp;(?P<city>.*?) (?P<total>[0-9,]+), активни (?P<active>[0-9,]+)',
    re.UNICODE
)


class MKData(URLBase):
    SOURCE_URL = 'https://koronavirus.gov.mk/vesti/218055'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'mk_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'mk' / 'data',
            urls_dict={
                'mk_corona.html': URL('https://koronavirus.gov.mk/vesti/218055',
                                      static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/mk_corona.html'
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()

            for match in MK_RE.finditer(html):
                match = match.groupdict()

                region_child = region_map[match['city'].strip().lower()]
                total = int(match['total'].replace(',', ''))
                active = int(match['active'].replace(',', ''))

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='MK',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=total,
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='MK',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=active,
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MKData().get_datapoints())
