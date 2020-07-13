# https://covid19.data.gov.rs/infected
import json
import datetime
from os import makedirs, listdir
from os.path import exists
from urllib import request, parse
from collections import Counter

from covid_19_au_grab.overseas.GlobalBase import GlobalBase
from covid_19_au_grab.get_package_dir import get_overseas_dir
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1, DT_TESTS_TOTAL, DT_NEW,
    DT_TOTAL, DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)


# TODO: Also scrape from https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Serbia  !! =================================================


HEADERS = (
    ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'),
    ('Accept', '*/*'),
    ('Accept-Language', 'en-US,en;q=0.5'),
    ('Accept-Encoding', 'gzip, deflate, br'),
    ('Content-Type', 'application/json'),
    ('X-Requested-With', 'XMLHttpRequest'),
    ('Origin', 'https://covid19.data.gov.rs'),
    ('Connection', 'keep-alive'),
    ('Referer', 'https://covid19.data.gov.rs/infected'),
    ('Pragma', 'no-cache'),
    ('Cache-Control', 'no-cache'),
)


region_map = dict([i.split('\t')[::-1] for i in """
RS-KM	Косово и Метохия
RS-VO	Воеводина
RS-00	Белград
RS-11	Браничевский
RS-14	Борский
RS-23	Ябланичский
RS-09	Колубарский
RS-08	Мачванский
RS-17	Моравичский
RS-20	Нишавский
RS-24	Пчиньский
RS-10	Подунайский
RS-22	Пиротский
RS-13	Поморавский
RS-19	Расинский
RS-18	Рашский
RS-12	Шумадийский
RS-15	Заечарский
RS-21	Топличский
RS-16	Златиборский
RS-01	Северно-Бачский
RS-02	Средне-Банатский
RS-03	Северно-Банатский
RS-07	Сремский
RS-05	Западно-Бачский
RS-06	Южно-Бачский
RS-04	Южно-Банатский
RS-28	Косовско-Митровицкий
RS-26	Печский
RS-25	Косовский
RS-29	Косовско-Поморавский
RS-27	Призренский
RS-19	александровац
RS-20	алексинац
RS-12	аранђеловац
RS-16	ариље
RS-22	бабушница
RS-16	бајина башта
RS-12	баточина
RS-12	Крагујевац
RS-12	Аранђеловац
RS-12	Баточина
RS-12	Кнић
RS-12	Лапово
RS-12	Рача
RS-12	Топола
RS-22	бела паланка
RS-21	Прокупље
RS-21	Блаце
RS-21	Куршумлија
RS-21	Житорађа
RS-08	Шабац
RS-08	Лозница
RS-08	Богатић
RS-08	Владимирци
RS-08	Коцељева
RS-08	Мали Зворник
RS-08	Крупањ
RS-08	Љубовија
RS-08	Лесковац
RS-08	Власотинце
RS-08	Лебане
RS-08	Бојник
RS-08	Медвеђа
RS-08	Црна Трава
RS-15	Зајечар
RS-15	Бољевац
RS-15	Књажевац
RS-15	Сокобања
RS-14	бор
RS-24	Врање
RS-24	Владичин
RS-24	Сурдулица
RS-24	Босилеград
RS-24	Трговиште
RS-24	Бујановац
RS-24	Прешево
RS-19	Крушевац
RS-19	Варварин
RS-19	Трстеник
RS-19	Ћићевац
RS-19	Александровац
RS-19	Брус
RS-09	Ваљево
RS-09	Осечина
RS-09	Уб
RS-09	Лајковац
RS-09	Мионица
RS-09	Љиг
RS-10	Смедерево
RS-10	Смедеревска Паланка
RS-10	Велика Плана
RS-11	Пожаревац
RS-11	Велико Градиште
RS-11	Голубац
RS-11	Мало Црниће
RS-11	Жабари
RS-11	Петровац на Млави
RS-11	Кучево
RS-11	Жагубица
RS-24	Врање
RS-24	Владичин Хан
RS-24	Сурдулица
RS-24	Босилеград
RS-24	Трговиште
RS-24	Бујановац
RS-24	Прешево
RS-18	Краљево
RS-18	Нови Пазар
RS-18	Тутин
RS-18	Рашка
RS-18	Врњачка Бања
RS-20	Ниш
RS-20	Медијана
RS-20	Палилула
RS-20	Пантелеј
RS-20	Црвени Крст
RS-20	Нишка Бања
RS-20	Алексинац
RS-20	Сврљиг
RS-20	Мерошина
RS-20	Ражањ
RS-20	Дољевац
RS-20	Гаџин Хан
RS-17	Чачак
RS-17	Горњи Милановац
RS-17	Лучани
RS-17	Ивањица
RS-13	Јагодина
RS-13	Ћуприја
RS-13	Параћин
RS-13	Свилајнац
RS-13	Деспотовац
RS-13	Рековац
RS-22	Пирот
RS-22	Бела Паланка
RS-22	Бабушница
RS-22	Димитровград
RS-14	кладово
RS-16	Ужице
RS-16	Бајина Башта
RS-16	Косјерић
RS-16	Пожега
RS-16	Чајетина
RS-16	Ариље
RS-16	Прибој
RS-16	Нова Варош
RS-16	Пријепоље
RS-16	Сјеница
RS-14	мајданпек
RS-14	неготин
RS-11	костолац
RS-24	врањска бања
RS-16	севојно
RS-00	град београд
RS-20	град ниш
RS-00	ада
RS-04	Панчево
RS-04	Вршац
RS-04	Пландиште
RS-04	Опово
RS-04	Ковачица
RS-04	Алибунар
RS-04	Бела Црква
RS-04	Ковин
RS-05	Сомбор
RS-05	Апатин
RS-05	Оџаци
RS-05	Кула
RS-06	Бач
RS-06	Бачка Паланка
RS-06	Бачки Петровац
RS-06	Беочин
RS-06	Бечеј
RS-06	Врбас
RS-06	Жабаљ
RS-06	Нови Сад
RS-06	Србобран
RS-06	Темерин
RS-06	Тител
RS-06	Сремски Карловци
RS-06	петроварадин
RS-01	Суботица
RS-01	Бачка Топола
RS-01	Мали Иђош
RS-02	Зрењанин
RS-02	Нови Бечеј
RS-02	Нова Црња
RS-02	Житиште
RS-02	Сечањ
RS-07	Сремска Митровица
RS-07	Шид
RS-07	Инђија
RS-07	Ириг
RS-07	Рума
RS-07	Стара Пазова
RS-07	Пећинци
RS-03	Кањижа
RS-03	Сента
RS-03	Ада
RS-03	Чока
RS-03	Нови Кнежевац
RS-03	Кикинда
RS-29	витина
RS-29	вучитрн
RS-29	глоговац
RS-29	гњилане
RS-29	дечани
RS-29	ђаковица
RS-29	зубин поток
RS-29	исток
RS-29	качаник
RS-29	клина
RS-29	косово поље
RS-29	косовска каменица
RS-29	лепосавић
RS-29	липљан
RS-29	ново брдо
RS-29	обилић
RS-29	ораховац
RS-29	пећ
RS-29	подујево
RS-29	призрен
RS-29	приштина
RS-29	србица
RS-29	сува река
RS-29	косовска митровица
RS-29	урошевац
RS-29	штимље
RS-29	штрпце
RS-29	гора
RS-29	звечан
""".lower().strip().split('\n')])


class RSData(GlobalBase):
    SOURCE_URL = 'https://covid19.data.gov.rs'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'rs_gov'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        GlobalBase.__init__(self, output_dir=get_overseas_dir() / 'rs' / 'data')
        self.__today_dir = self.output_dir / datetime.datetime.now().strftime('%Y_%m_%d')
        self.update()

    #=======================================================================#
    #                           Download Statistics                         #
    #=======================================================================#

    def __download_statistic_ranking(self):
        request_data = """
        {"dataSetId":1,"refCodes":[{"id":1,"code":"COVID-19 statistics","values":[{"id":1,"name":"Daily New Cases"}]}],"territoryIds":[168,40,41,169,170,42,43,44,171,172,173,174,45,46,177,175,47,176,163,64,65,66,67,68,69,70,71,151,150,146,211,149,147,220,219,84,85,86,81,217,218,82,242,83,182,183,222,91,133,223,184,185,92,224,93,94,96,95,225,226,238,160,186,187,97,98,99,100,102,188,101,103,153,104,227,105,228,108,109,106,107,110,189,111,112,113,114,115,116,164,190,117,191,192,118,193,229,230,195,194,231,119,196,120,232,197,121,213,122,198,233,123,124,125,126,127,235,234,128,130,131,129,132,199,152,201,200,162,212,136,137,138,139,202,236,203,204,205,206,240,241,207,140,237,134,135,208,209,142,143,144,145,148,239,141,72,73,74,75,215,77,76,78,79,161,210,80,178,216,179,87,88,90,180,89,181,221,243],"territoryGroupId":5,"number":10}
        """.strip().encode('utf-8')
        url = "https://covid19.data.gov.rs/api/datasets/statistic/ranking"
        req = request.Request(url, data=request_data, headers=dict(HEADERS))
        response = request.urlopen(req)

        with open(self.__today_dir / 'statistic_ranking.json', 'wb') as f:
            f.write(response.read())

    def __download_statistic(self):
        request_data = """
        {"dataSetId":1,"refCodes":[{"id":1,"code":"COVID-19 statistics","values":[{"id":1,"name":"Daily New Cases"}]}],"territoryIds":[168,40,41,169,170,42,43,44,171,172,173,174,45,46,177,175,47,176,163,64,65,66,67,68,69,70,71,151,150,146,211,149,147,220,219,84,85,86,81,217,218,82,242,83,182,183,222,91,133,223,184,185,92,224,93,94,96,95,225,226,238,160,186,187,97,98,99,100,102,188,101,103,153,104,227,105,228,108,109,106,107,110,189,111,112,113,114,115,116,164,190,117,191,192,118,193,229,230,195,194,231,119,196,120,232,197,121,213,122,198,233,123,124,125,126,127,235,234,128,130,131,129,132,199,152,201,200,162,212,136,137,138,139,202,236,203,204,205,206,240,241,207,140,237,134,135,208,209,142,143,144,145,148,239,141,72,73,74,75,215,77,76,78,79,161,210,80,178,216,179,87,88,90,180,89,181,221,243]}
        """.strip().encode('utf-8')
        url = "https://covid19.data.gov.rs/api/datasets/statistic"
        req = request.Request(url, data=request_data, headers=dict(HEADERS))
        response = request.urlopen(req)

        with open(self.__today_dir / 'statistic.json', 'wb') as f:
            f.write(response.read())

    def update(self):
        if not exists(self.__today_dir):
            makedirs(self.__today_dir)
            self.__download_statistic_ranking()
            self.__download_statistic()

    #=======================================================================#
    #                       Get Statistic Datapoints                        #
    #=======================================================================#

    def get_datapoints(self):
        r = []
        r.extend(self.get_statistic_ranking())
        r.extend(self.get_statistic())
        return r

    def get_statistic_ranking(self):
        return []  # TODO: Does this provide useful info, aside from new values?

    def get_statistic(self):
        r = []
        data = json.loads(self.get_text('statistic.json', include_revision=True))
        by_region = Counter()

        for region_data in data:
            # {"dataSet":{"id":1,"code":"COVID19","name":"COVID19 statistics",
            # "shortName":"COVID19 stat","sourceUrl":"file:///tmp/covid19stat.txt",
            # "resourceUrl":null,"dataSetGroup":{"id":1,"name":"Default","pos":1,
            # "icon_resource":null},"pos":1,"isComparable":null,"delimiter":";"},
            print(region_data)

            for point_dict in region_data['points']:
                # {"abscissa":{"id":45862,"year":2020,"month":3,"day":10,
                # "name":"2020-03-10","date":"2020-03-10"},"ordinate":0.0}
                #print(point_dict['abscissa']['date'])
                if point_dict['ordinate'] is None:
                    continue

                region_child = region_map[region_data['name'].lower().strip()]
                value = int(point_dict['ordinate'])
                date = self.convert_date(point_dict['abscissa']['date'])
                by_region[date, region_child] += value

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='RS',
                    region_child=region_child,
                    datatype=DT_NEW,
                    value=value,
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        cumulative = Counter()
        for (date, region_child), value in sorted(by_region.items()):
            cumulative[region_child] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='RS',
                region_child=region_child,
                datatype=DT_TOTAL,
                value=cumulative[region_child],
                source_url=self.SOURCE_URL,
                date_updated=date
            ))
        return r


if __name__ == '__main__':
    from pprint import pprint
    RSData().get_datapoints()
    #pprint(RSData().get_datapoints())

