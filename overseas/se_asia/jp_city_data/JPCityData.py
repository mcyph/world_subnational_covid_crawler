import csv
from pprint import pprint
from collections import Counter, defaultdict
from covid_19_au_grab.overseas.se_asia.jp_city_data.extract_from_tokyo_pdf import (
    ExtractFromTokyoPDF
)

# https://stopcovid19.metro.tokyo.lg.jp/
# https://github.com/tokyo-metropolitan-gov/covid19/blob/development/FORKED_SITES.md

# [
#   {
#     "通し": "1",
#     "厚労省NO": "1",
#     "無症状病原体保有者": "",
#     "国内": "A-1",
#     "チャーター便": "",
#     "年代": "30",
#     "性別": "男性",
#     "確定日": "1/15/2020",
#     "発症日": "1/3/2020",
#     "受診都道府県": "神奈川県",
#     "居住都道府県": "神奈川県",
#     "居住管内": "",
#     "居住市区町村": "",
#     "キー": "神奈川県",
#     "発表": "神奈川県",
#     "都道府県内症例番号": "1",
#     "市町村内症例番号": "",
#     "ステータス": "退院",
#     "備考": "",
#     "ソース": "https://www.mhlw.go.jp/stf/newpage_08906.html",
#     "ソース2": "https://www.pref.kanagawa.jp/docs/ga4/bukanshi/occurrence.html",
#     "ソース3": "",
#     "人数": "1",
#     "累計": "1",
#     "前日比": "1",
#     "発症数": "0",
#     "死者合計": "",
#     "退院数累計": "1",
#     "退院数": "1",
#     "PCR検査実施人数": "",
#     "PCR検査前日比": "",
#     "職業_正誤確認用": "",
#     "勤務先_正誤確認用": "",
#     "Hospital Pref": "Kanagawa",
#     "Residential Pref": "Kanagawa",
#     "Release": "Kanagawa Prefecture",
#     "Gender": "Male",
#     "X": "139.642347",
#     "Y": "35.447504",
#     "確定日YYYYMMDD": "2020/1/15",
#     "受診都道府県コード": "14",
#     "居住都道府県コード": "14",
#     "更新日時": "5/17/2020 13:42",
#     "Field2": "",
#     "Field4": "",
#     "Field5": "",
#     "Field6": "",
#     "Field7": "",
#     "Field8": "",
#     "Field9": "",
#     "Field10": ""
#   },


from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)
from covid_19_au_grab.geojson_data.LabelsToRegionChild import (
    LabelsToRegionChild
)
from covid_19_au_grab.datatypes.StrictDataPointsFactory import (
    StrictDataPointsFactory, MODE_STRICT, MODE_DEV
)


city_map = {
    '福岡市': 'fukuoka-shi higashi-ku', # 40
    '熊本市': 'kumamoto-shi nishi-ku', # 43
    '札幌市': 'sapporo-shi chuo-ku', # 01
    '群馬県': 'maebashi-shi', # 10
    'さいたま市': 'saitama-shi urawa-ku', # 11
    '千葉市': 'chiba-shi wakaba-ku', # 12
    '川崎市': 'kawasaki-shi tama-ku', # 14
    '横浜市': 'yokohama-shi tsudhuki-ku', # 14
    '相模原市': 'sagamihara-shi chuo-ku', # 14
    '浜松市': 'hamamatsu-shi higashi-ku', # 22
    '名古屋市': 'nagoya-shi nishi-ku', # 23
    '堺市': 'sakai-shi higashi-ku', # 27
    '大阪市': 'osaka-shi taisho-ku', # 27
    '新潟市': 'niigata-shi konan-ku', # 15
    '岡山市': 'okayama-shi kita-ku', # 33
    '千葉県': 'chiba-shi wakaba-ku', # 12
    '北九州市': 'kitakyushu-shi kokuraminami-ku', # 40
    '神戸市': 'kobe-shi tarumi-ku', # 28
    '静岡市': 'shizuoka-shi shimizu-ku', # 22
    '仙台市': 'sendai-shi wakabayashi-ku', # 04
    '広島市': 'hiroshima-shi naka-ku', # 34
    '栃木県': 'tochigi-shi', # 09
    '茨城県': 'kitaibaraki-shi', # 08
    '八千市': '八千代市', # 08
    '市川市の': '市川市',
    '糟屋郡': '宇美町', # 40
    '利根沼田保健所管内': '沼田市',
    '渋川保健所管内': '渋川',
    '松坂市': '松阪市',
    '瀬⼾市': '瀬戸市',
    '空知総合振興局管内': 'iwamizawa-shi', # 01
    '釧路総合振興局管内': 'kushiro-cho', # 01
    '北海道': 'sapporo-shi chuo-ku', # 01
    '青森県': 'aomori-shi', # 02
    '岩手県': 'iwate-machi', # 03
    '宮城県': 'sendai-shi wakabayashi-ku', # 04
    '秋田県': 'kitaakita-shi', # 05
    '山形県': 'yamagata-shi',
    '福島県': 'fukushima-shi',
    '埼玉県': 'saitama-shi',
    '福岡県': 'fukuoka-shi',
    '愛媛県': 'matsuyama-shi',
    '高知県': 'kochi-shi',
    '香川県': 'kagawa-shi',
    '徳島県': 'tokushima-shi',
    '広島県': 'hiroshima-shi',
    '岡山県': 'okayama-shi',
    '鳥取県': 'tottori-shi',
    '和歌山県': 'wakayama-shi',
    '奈良県': 'nara-shi',
    '兵庫県': 'hyogo-shi',
    '大分県': 'oita-shi',
    '鹿児島県': 'kagoshima-shi',
    '沖縄県': 'naha-shi', # 47

    #'京都市': 'kyoto-shi nakagyo-ku', # 26
    #'京都府': 'kyoto-shi nakagyo-ku', # 26

    '非公表': 'unknown',
    '不明': 'unknown',
    '調査中': 'unknown',
    '確認中': 'unknown',
    '大阪府外': 'other',
    '岐阜市外': 'other',
    '西宮市外': 'other',
    '川口市外': 'other',
    '府外': 'other',
    '県外': 'other',
    '中華人民共和国': 'other',
}


class JPCityData(URLBase):
    SOURCE_URL = 'https://jag-japan.com/covid19map-readme/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'jp_jag_japan'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             # TODO: SUPPORT TOKYO DATA AS WELL from !!!
             output_dir=get_overseas_dir() / 'jp_city_data' / 'data',
             urls_dict={
                 'jg-jpn.csv': URL('https://dl.dropboxusercontent.com/s/6mztoeb6xf78g5w/COVID-19.csv',
                                    static_file=False),
             }
        )
        self.update()
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                (Schemas.JP_CITY, 'jp-13', 'niigata-shi konan-ku'): (Schemas.JP_CITY, 'jp-15', '15104')  # HACK (??)
            },
            mode=MODE_DEV
        )
        self._labels_to_region_child = LabelsToRegionChild()

    def get_datapoints(self):
        r = []
        r.extend(self._get_from_json())
        return r

    def _get_from_json(self):
        r = self.sdpf()

        by_date = Counter()
        by_age = Counter()
        by_prefecture = Counter()
        by_city = Counter()

        by_gender = Counter()
        by_gender_age = Counter()

        by_prefecture_gender = Counter()
        by_city_gender = Counter()
        by_prefecture_age = Counter()
        by_city_age_gender = Counter()
        by_prefecture_age_gender = Counter()

        lat_long_counters = defaultdict(Counter)

        f = self.get_file('jg-jpn.csv', include_revision=True, encoding='utf-8-sig')

        #for item in json.loads(text)['features']:
        num_city = 0
        num_kyoto = 0

        not_found = {}

        for item in csv.DictReader(f):
            for k in item:
                item[k] = item[k].strip()

            for xxx in range(int(item.get('人数', '').strip() or 1)):
                #print(item)
                #item = item['properties']

                if not item:
                    print("NOT ITEM:", item)
                    continue
                elif not item['確定日']:
                    print("NOT 確定日", item)
                    assert not ''.join(item.values()).strip(), item
                    continue  # WARNING!

                if item.get('年代') == '0-10' or item.get('年代') == '10歳未満':
                    agerange = '0-9'
                elif item.get('年代') in ('不明', '', None):
                    agerange = 'Unknown'
                elif item.get('年代') in ('90以上',):
                    agerange = '90+'
                elif item.get('年代') in ('100歳以上',):
                    agerange = '100+'
                else:
                    agerange = (
                        str(int(item['年代'].strip('代'))) +
                        '-' +
                        str(int(item['年代'].strip('代')) + 9)
                    )

                gender = {
                    '男性': DataTypes.TOTAL_MALE,
                    '男性\xa0': DataTypes.TOTAL_MALE,
                    '女性\xa0': DataTypes.TOTAL_FEMALE,
                    '女性': DataTypes.TOTAL_FEMALE,
                    '不明': None,
                    '惰性': DataTypes.TOTAL_MALE,  # Pretty sure this is a typo
                    '未満 女性': DataTypes.TOTAL_FEMALE,
                    '女児': DataTypes.TOTAL_FEMALE,
                    '男児': DataTypes.TOTAL_MALE,
                    '': None,
                    None: None,
                }[item['性別']]

                #date_of_onset = self.convert_date(item['発症日'], formats=('%m/%d/%Y',))
                date_diagnosed = self.convert_date(item['確定日'], formats=('%m/%d/%Y',))   # TODO: Should we be recording this number??? ================
                #date_diagnosed = datetime.datetime.fromtimestamp(item['確定日']/1000).strftime('%Y_%m_%d')
                #diagnosed_in = item['Hospital Pref']
                #region_parent = item['Residential Pref']

                # May as well use English prefecture names to and allow the system to
                # auto-translate to ISO-3166-2 later
                region_parent = item['居住都道府県']
                if not region_parent:
                    assert item['居住都道府県コード'] == '#N/A', item
                    #continue # TODO: Add for other info!!! ===========================

                if (
                    (
                        region_parent.startswith('京都') or
                        region_parent == '福岡県' or
                        region_parent == '沖縄県' or
                        region_parent == '愛媛県' or
                        region_parent == '神奈川県' or
                        region_parent == '兵庫県' or
                        #region_parent == '奈良県' or
                        region_parent == '愛知県' or
                        region_parent == '高知県' or
                        region_parent == '山梨県' or
                        region_parent == '栃木県' or
                        #region_parent == '和歌山県' or
                        region_parent == '三重県' or
                        #region_parent == '大阪府'
                        region_parent == '長野県' or
                        region_parent == '熊本県' or
                        region_parent == '青森県' or
                        region_parent == '茨城県' or
                        region_parent == '静岡県' or
                        region_parent == '福島県' or
                        region_parent == '徳島県' or
                        region_parent == '群馬県' or
                        region_parent == '秋田県'
                    )
                    and item['備考']
                    and not item['居住市区町村']
                ):
                    #print(region_parent, item)

                    region_child = {
                        # Kyoto
                        '京都市': 'kyoto-shi',
                        '京都府': 'kyoto-shi',
                        '京都府内': 'kyoto-shi',
                        '右京区役所勤務': 'kyoto-shi',

                        '園児の保護者でPCR検査を実施、陽性となった': 'kyoto-shi',
                        'ナイル川クルーズ船ツアー参加': 'kyoto-shi',
                        '3/16オランダから帰国': 'kyoto-shi',
                        '3/15フランス、ルクセンブルク経由で帰国': 'kyoto-shi',
                        '3/15ルクセンブルグから帰国': 'kyoto-shi',
                        'キルギス': 'kyoto-shi',
                        '外国籍': 'other',

                        '丹後': 'tango-kan',
                        '丹後管内': 'tango-kan',
                        '丹後保健所管内': 'tango-kan',

                        '中丹管内': 'nakatan-kan',
                        '中丹西保健所管内': 'nakatan-kan',
                        '中丹東保健所': 'nakatan-kan',
                        '中丹東保健所管内': 'nakatan-kan',
                        '中丹西': 'nakatan-kan',
                        '中丹東': 'nakatan-kan',

                        '南丹管内': 'nantan-kan',
                        '南丹保健所': 'nantan-kan',
                        '南丹保健所管内': 'nantan-kan',
                        '南丹': 'nantan-kan',

                        '山城管内': 'yamashiro-kan',
                        '山城北保健所': 'yamashiro-kan',
                        '山城北保健所管内': 'yamashiro-kan',
                        '山城南保健所管内': 'yamashiro-kan',
                        '山城北保健所管内在住': 'yamashiro-kan',
                        '山城南保健所館内': 'yamashiro-kan',
                        '再陽性/山城北保健所管内': 'yamashiro-kan',
                        '山城南保健所': 'yamashiro-kan',
                        '山城市内': 'yamashiro-kan',
                        '山城北': 'yamashiro-kan',
                        '山城南': 'yamashiro-kan',

                        '乙訓管内': 'otokuni-kan',
                        '乙訓保健所': 'otokuni-kan',
                        '乙訓保健所管内': 'otokuni-kan',
                        '乙訓': 'otokuni-kan',
                        '乙君': 'otokuni-kan',

                        # Okinawa
                        '南部保健所管内': '南部保健所管',
                        '3/19スペイン（マドリード州）から帰国/成田空港検疫所/中部保健所管内在住': '中部保健所管',
                        '3/4ベルギーから帰国/中部保健所管内': '中部保健所管',
                        '中部保健所管内': '中部保健所管',
                        '中部保健所': '中部保健所管',
                        '南部保健所': '南部保健所管',
                        '北部保健所': '北部保健所管',
                        '八重山保健所': '八重山保健所管',
                        '北部保健所管内': '北部保健所管',

                        # Osaka
                        '3/11イタリア（ピエモンテ州）から帰国/関西空港検疫所': '',

                        # Fukuoka
                        '糟屋郡/3/18イギリス（ロンドン）から帰国': '糟屋郡',
                        '京都郡': '京都郡',
                        '糟屋郡': '糟屋郡',
                        '検疫官': 'unknown',
                        '八女郡': '八女郡',
                        '帰省先：岩国市': '岩国市',
                        '遠賀郡': '遠賀郡',
                        '嘉穂郡': '嘉穂郡',
                        '城南区': '城南区',
                        '東区': '東区',
                        '博多区': '博多区',
                        '西区': '西区',
                        '早良区': '早良区',
                        '中央区': '中央区',
                        'ボリビア': 'other',
                        '田川郡': '田川郡',
                        '三井郡': '三井郡',
                        '諫早市': '諫早市',
                        '三潴郡': '三潴郡',
                        '朝倉郡': '朝倉郡',
                        '糸島市': '糸島市',
                        '鞍手郡': '鞍手郡',

                        # Kanagawa
                        '鎌倉保健所管内': '鎌倉保健所管',
                        '厚木保健福祉事務所': '厚木保健福祉事務所管',
                        '厚木保健福祉事務所管内': '厚木保健福祉事務所管',
                        '横浜検疫所職員': 'other',
                        '鎌倉保健福祉事務所': '鎌倉保健福祉事務所管',
                        '平塚保健福祉事務所管内': '平塚保健福祉事務所管',
                        '小田原保健福祉事務所管内': '小田原保健福祉事務所管',
                        '鎌倉保健福祉事務所管内': '鎌倉保健福祉事務所管',
                        '茅ヶ崎保健所管内/鎌倉市内のスーパーに勤務': '茅ヶ崎保健所管内',
                        '平塚保健福祉事務所管内/フランス帰国者': '平塚保健福祉事務所管',
                        '3/8イタリア（ヴェネト州）から帰国/東京検疫所東京空港（羽田空港）検疫所支所': '',
                        '3/16アメリカ（ニューヨーク）から帰国/平塚保健福祉事務所管内': '平塚保健福祉事務所管',
                        '茅ヶ崎市保健所管内': '茅ヶ崎市保健所管',
                        '運転免許合宿': 'unknown',
                        '平塚保健福祉事務所': '平塚保健福祉事務所管',
                        '小田原保健福祉事務所': '小田原保健福祉事務所管',
                        'ブラジル': 'other',
                        'ペルー、メキシコ': 'other',
                        'アメリカ合衆国': 'other',
                        '中原区': '中原区',

                        # Aichi
                        '尾張地方': '尾張地方',
                        '三河地方': '三河地方',
                        '一宮保健所管内': '一宮保健所管',
                        '3/13スペイン（マドリード州）から帰国/東京検疫所東京空港（羽田空港）検疫所支所': '',
                        'フィリピン': 'other',
                        'パキスタン': 'other',
                        '愛知県内': 'other',  # TODO!

                        # Tochigi
                        '県南健康福祉センター管内/ダイヤモンド・プリンセス号2/19下船': '県南健康福祉センター管',
                        '県南健康福祉センター管内': '県南健康福祉センター管',
                        '3/15ポルトガルから帰国/県南健康福祉センター管内': '県南健康福祉センター管',
                        '安足健康福祉センター': '安足健康福祉センター管',
                        '県西健康福祉センター': '県西健康福祉センター管',
                        '県南健康福祉センター': '県南健康福祉センター管',
                        '県南保健福祉センター管内': '県南保健福祉センター管',
                        'アラブ首長国連邦': 'other',

                        # Kochi
                        '安芸福祉保健所管内': '安芸福祉保健所管',
                        '中央東福祉保健所管内': '中央東福祉保健所管',
                        '中央西福祉保健所管内': '中央西福祉保健所管',
                        '幡多福祉保健所管内': '幡多福祉保健所管',
                        '須崎福祉保健所管内': '須崎福祉保健所管',
                        '中央東': '中央東福祉保健所管',
                        '中央西': '中央西福祉保健所管',
                        'ペルー': 'other',

                        # Mie
                        '3/4ベトナムから帰国/名古屋検疫所中部空港検疫所支所': '',
                        '伊賀保健所管内': '伊賀保健所管',
                        'ダイヤモンド・プリンセス号を下船': 'unknown',

                        # Yamanashi
                        '南アルプス市〜昭和町が生活圏': '南アルプス市',
                        '生活圏：南アルプス市、中央市': '中央市',
                        '生活圏：南アルプス市、甲斐市': '甲斐市',
                        '生活圏：市川三郷町、富士川町': '富士川町',
                        '生活圏：甲府市、富士川町': '富士川町',
                        '生活圏：中央市': '中央市',
                        '生活圏：甲府市、甲州市': '甲州市',
                        '生活圏：甲州市': '甲州市',
                        '生活圏：南アルプス市': '南アルプス市',
                        '生活圏：南アルプス市、笛吹市': '笛吹市',
                        '生活圏：甲斐市、昭和町': '昭和町',
                        '生活圏：韮崎市、北杜市': '北杜市',
                        '生活圏：上野原市': '上野原市',
                        '生活圏：甲府市、甲斐市': '甲斐市',
                        '再陽性': 'unknown',
                        '生活圏：甲斐市': '甲斐市',
                        'イギリス': 'other',
                        '生活圏：北杜市、昭和町': '北杜市',
                        '生活圏：富士吉田市、富士河口湖町': '富士吉田市',
                        '生活圏：中北地域、峡南地域': '峡南地域',
                        '生活圏：見延町': '見延町',
                        '甲府市': '甲府市',
                        '甲府市、南アルプス市': '甲府市',
                        '東部地域': '東部地域',
                        '甲府市外（中北地域）': '中北地域',
                        '非公表': 'unknown',
                        '昭和町': '昭和町',
                        '南アルプス市': '南アルプス市',
                        '中北地域': '中北地域',
                        '生活圏：富士北麓地域': '富士北麓地域',
                        '生活圏：峡東地域': '峡東地域',
                        '生活圏:山梨市、甲州市': '甲州市',
                        '生活圏:甲府市、甲斐市': '甲斐市',
                        '生活圏:富士北麓地域': '富士北麓地域',

                        # Nara
                        '郡山保健所管内、本来陽性確定日は９日だが、厚生労働省のとりまとめが10日だったため、便宜上10日にしている': '郡山保健所管',
                        '3/16メキシコから帰国': 'unknown',
                        '中和保健所管内': '中和保健所管',
                        '郡山保健所管内': '郡山保健所管',
                        '3/29アメリカより帰国/郡山保健所管内': '郡山保健所管',

                        # Hyogo
                        '伊丹保健所管内': '伊丹保健所管',
                        '宝塚保健福祉事務所管内': '宝塚保健福祉事務所管',
                        '伊丹保健福祉事務所管内': '伊丹保健福祉事務所管',
                        '加東健康福祉事務所管内': '加東健康福祉事務所管',
                        '伊丹健康福祉事務所管内': '伊丹健康福祉事務所管',
                        '伊丹健康福祉事務所管内/「グリーンアルス伊丹」の利用者': '伊丹健康福祉事務所管',
                        '宝塚健康福祉事務所管内': '宝塚健康福祉事務所管',
                        '洲本健康福祉事務所管内': '洲本健康福祉事務所管',
                        '芦屋健高福祉事務所管内': '芦屋健高福祉事務所管',
                        '芦屋健康福祉事務所管内': '芦屋健康福祉事務所管',
                        '宝塚健康保健福祉事務所管内': '宝塚健康保健福祉事務所管',
                        '宝塚健康福祉事務所館内': '宝塚健康福祉事務所管',
                        '丹波健康福祉事務所管内': '丹波健康福祉事務所管',
                        '赤穂健康福祉事務所管内': '赤穂健康福祉事務所管',
                        '*': 'unknown',
                        '赤穂': '赤穂',
                        '加古川健康福祉事務所管内': '加古川健康福祉事務所管',
                        '龍野健康福祉事務所管内': '龍野健康福祉事務所管',
                        '豊岡健康福祉事務所管内': '豊岡健康福祉事務所管',

                        # Nagano
                        '松本保健所管内': '松本保健所管',
                        '松本保健所管内/厚労省NO140の家族': '松本保健所管',
                        '佐久保健所管内': '佐久保健所管',
                        '飯田保健所管内': '飯田保健所管',
                        '大町保健所管内': '大町保健所管',
                        '諏訪保健所管内': '諏訪保健所管',
                        '伊那保健所管内': '伊那保健所管',
                        '木曽保健所管内': '木曽保健所管',
                        '北信保健所管内': '北信保健所管',
                        'シンガポール': 'other',

                        # Kumamoto
                        '御船保健所管内': '御船保健所管',
                        '阿蘇保健所管内': '阿蘇保健所管',
                        '有明保健所管内': '有明保健所管',
                        '阿蘇郡市': '阿蘇郡市',
                        '天草保健所管内': '天草保健所管',
                        '有明保健所': '有明保健所管',
                        '菊池保健所': '菊池保健所管',
                        '八代保健所': '八代保健所管',

                        # Ibaraki
                        '東庄町所在の社会福祉施設': '',
                        '職員家族': 'unknown',
                        '古河保健所管内': '古河保健所管',
                        '龍ケ崎保健所管内': '龍ケ崎保健所管',
                        'つくば保健所管内': 'つくば保健所管',
                        '中央保健所管内': '中央保健所管',
                        '筑西保健所': '筑西保健所管',

                        # Aomori
                        '3/20アメリカから帰国': 'unknown',
                        '上十三保健所管内': '上十三保健所管',
                        '郡山市保健所管内': '郡山市保健所管',
                        '五所川原保健所管内': '五所川原保健所管',

                        # Shizuoka
                        '3/22イタリア（ロンバルディア州）から帰国': 'unknown',
                        '榛原郡': '榛原郡',
                        '賀茂郡': '賀茂郡',
                        '西部保健所管内': '西部保健所管',
                        '東部保健所管内': '東部保健所管',
                        '浜松市23〜52は1人を除きすべて浜松市在住': 'unknown',  # CHECK ME!
                        '西部保健所': '西部保健所管',
                        '富士保健所管内': '富士保健所管',
                        '御殿場保健所管内': '御殿場保健所管',
                        '熱海保健所管内': '熱海保健所管',

                        # Fukushima
                        'いわき市保健所管内': 'いわき市保健所管',
                        '県北保健所管内': '県北保健所管',
                        '築上郡': '築上郡',
                        'インドネシア': 'other',
                        '県南保健所': '県南保健所管',
                        '県南': '県南保健所管',
                        'いわき市': 'いわき市保健所管',

                        # Ehime
                        '東予地域': '東予地域',

                        # Tokushima
                        'ダイヤモンド・プリンセス号2/20下船': 'unknown',
                        '徳島保健所管内': '徳島保健所管',
                        '徳島': '徳島保健所管',
                        '阿南': '阿南',
                        '徳島/100歳以上': '徳島保健所管',

                        # Akita
                        '由利本荘保健所管内/外国籍': '由利本荘保健所管',
                        '由利本荘保健所管内': '由利本荘保健所管',
                        '湯沢保健所管内': '湯沢保健所管',
                        '能代保健所': '能代保健所管',
                        '由利本荘保健所': '由利本荘保健所管',
                        '大仙保健所管内': '大仙保健所管',
                        '秋田中央保健所管内': '秋田中央保健所管',

                        # Gunma
                        '渋川\n保健所管内': '保健所管',
                        '桐生保健所': '桐生保健所管',
                        '館林\n保健所管内': '保健所管',
                        '館林保健所管内': '館林保健所管',
                        '帰省先が佐久市': 'other',
                        '桐生\n保健所管内': '保健所管',
                        '富岡保健所管内': '富岡保健所管',
                        '伊勢崎保健所管内': '伊勢崎保健所管',
                        '吾妻保健所管内': '吾妻保健所管',
                        '利根沼田保健所管内': '利根沼田保健所管',
                        '渋川保健所管内': '渋川保健所管',
                    }[item['備考']]

                else:
                    if item['備考'] and not item['居住市区町村']:
                        print("BIKOU!!!", region_parent, item['備考'], item)

                    #assert region_parent, item
                    # e.g. 中富良野町 will be different to the English 'Release' field
                    #announced_in = item['Release']
                    region_child = (
                        item.get('居住市区町村') or
                        region_parent.replace('市', '県') or
                        'unknown'  # Japanese only
                    )
                
                #if region_child != 'Unknown':
                #    print(item)
                #source = item['ソース'] or item['ソース2'] or item['ソース3'] or 'https://covid19.wlaboratory.com'

                region_parent = region_parent.replace('市', '県')  # HACK!
                if region_parent in (
                    '中華人民共和国',
                    'アイルランド',
                    'スペイン',
                    'ジンバブエ共和国',
                    '南アフリカ共和国',
                    'フィリピン',
                    'アメリカ',
                    'カナダ',
                    'イギリス',
                    'フランス',
                    'インドネシア',
                    'アフガニスタン',
                ):
                    region_parent = 'other'
                elif region_parent in (
                    '不明',
                ):
                    region_parent = 'unknown'

                region_parent = self._labels_to_region_child.get_by_label(
                    Schemas.ADMIN_1, 'JP', region_parent, default=region_parent
                )
                region_child = city_map.get(region_child.strip().lower(), region_child)
                region_child = self._labels_to_region_child.get_by_label(
                    Schemas.JP_CITY, region_parent, region_child, default=region_child
                )

                #print(region_parent, region_child)
                if region_parent == 'jp-13' and region_child == 'niigata-shi konan-ku': region_parent = 'jp-15'
                elif region_parent == 'jp-10' and region_child == 'tochigi-shi': region_parent = 'jp-09'
                elif region_parent == 'jp-12' and region_child == 'kitaibaraki-shi': region_parent = 'jp-08'
                elif region_parent == 'jp-14' and region_child == 'nagoya-shi nishi-ku': region_parent = 'jp-23'
                elif region_parent == 'jp-13' and region_child == '宮崎市': region_parent = 'jp-45'
                elif region_parent == 'jp-17' and region_child == '富山市': region_parent = 'jp-16'
                elif region_parent == 'jp-40' and region_child == '中津市': region_parent = 'jp-44'
                elif region_parent == 'jp-46' and region_child == '上尾市': region_parent = 'jp-11'
                elif region_parent == 'jp-18' and region_child == '坂出市': region_parent = 'jp-37'
                elif region_parent == 'jp-28' and region_child == 'osaka-shi taisho-ku': region_parent = 'jp-27'
                elif region_child == '吹田市': region_parent = 'jp-27'
                elif region_child == '東京都': continue
                elif region_child in (
                    '宮町', '畑野氏', '大網白里市', '⻄尾市', '春日部恣意',
                    'ふじみ野市', '神奈川県', '滋賀県', '山郷町', '⻑久⼿市',
                    '愛⻄市', '古河市', '大阪府',
                ):  # ???
                    print("**IGNORING:", item)
                    region_child = 'unknown'

                if region_parent == 'jp-26':
                    print("KYOTO!!!", region_child)
                    num_kyoto += 1

                # Maybe it's worth adding status info, but it can be vague e.g. "退院または死亡"
                # Occupation info is also present in many cases.

                by_date[date_diagnosed] += 1
                by_age[date_diagnosed, agerange] += 1
                by_prefecture[date_diagnosed, region_parent] += 1

                if gender is not None:
                    by_gender[date_diagnosed, gender] += 1
                    by_gender_age[date_diagnosed, gender, agerange] += 1
                    by_prefecture_gender[date_diagnosed, region_parent, gender] += 1
                    by_prefecture_age_gender[date_diagnosed, region_parent, agerange, gender] += 1

                by_prefecture_age[date_diagnosed, region_parent, agerange] += 1

                if region_parent == 'tokyo' and region_child.lower() == 'unknown':
                    # Will add region_child-level data
                    continue
                else:
                    by_city[date_diagnosed, region_parent, region_child] += 1

                    if gender is not None:
                        by_city_gender[date_diagnosed, region_parent, region_child, gender] += 1
                        by_city_age_gender[date_diagnosed, region_parent, region_child, agerange, gender] += 1

                lat_long_counters[region_parent, region_child][item['X'], item['Y']] += 1

                if item.get('居住市区町村') and region_parent == 'jp-27':
                    #print(item)
                    num_city += 1

        #print('num_city:', num_city)

        cumulative = 0
        for date, value in sorted(by_date.items()):
            cumulative += value

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='Japan',
                datatype=DataTypes.TOTAL,
                value=cumulative,
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, agerange), value in sorted(by_age.items()):
            cumulative[agerange] += value

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='Japan',
                datatype=DataTypes.TOTAL,
                agerange=agerange,
                value=cumulative[agerange],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, prefecture), value in sorted(by_prefecture.items()):
            cumulative[prefecture] += value

            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=DataTypes.TOTAL,
                value=cumulative[prefecture],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[gender] += value

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='Japan',
                datatype=gender,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, gender, agerange), value in sorted(by_gender_age.items()):
            cumulative[gender, agerange] += value

            r.append(
                region_schema=Schemas.ADMIN_0,
                region_child='Japan',
                datatype=gender,
                agerange=agerange,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, prefecture, gender), value in sorted(by_prefecture_gender.items()):
            cumulative[prefecture, gender] += value

            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=gender,
                value=cumulative[prefecture, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, prefecture, agerange), value in sorted(by_prefecture_age.items()):
            cumulative[prefecture, agerange] += value

            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=DataTypes.TOTAL,
                agerange=agerange,
                value=cumulative[prefecture, agerange],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, prefecture, agerange, gender), value in sorted(by_prefecture_age_gender.items()):
            cumulative[prefecture, agerange, gender] += value

            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=gender,
                agerange=agerange,
                value=cumulative[prefecture, agerange, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, prefecture, region_child), value in sorted(by_city.items()):
            cumulative[prefecture, region_child] += value

            r.append(
                region_schema=Schemas.JP_CITY,
                region_parent=prefecture,
                region_child=region_child,
                datatype=DataTypes.TOTAL,
                value=cumulative[prefecture, region_child],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )
        #print("***TOTAL SUM:", sum(cumulative.values()))

        cumulative = Counter()
        for (date, prefecture, region_child, gender), value in sorted(by_city_gender.items()):
            cumulative[prefecture, region_child, gender] += value

            r.append(
                region_schema=Schemas.JP_CITY,
                region_parent=prefecture,
                region_child=region_child,
                datatype=gender,
                value=cumulative[prefecture, region_child, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        cumulative = Counter()
        for (date, prefecture, region_child, agerange, gender), value in sorted(by_city_age_gender.items()):
            cumulative[prefecture, region_child, agerange, gender] += value

            r.append(
                region_schema=Schemas.JP_CITY,
                region_parent=prefecture,
                region_child=region_child,
                datatype=gender,
                agerange=agerange,
                value=cumulative[prefecture, region_child, agerange, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            )

        from pprint import pprint
        pprint(lat_long_counters)

        return r


MAPPINGS = {('admin_0', '', 'japan'): ('admin_0', '', 'jp'),
 ('admin_0', '', 'jp'): ('admin_0', '', 'jp'),
 ('admin_1', 'japan', 'jp-01'): ('admin_1', 'jp', 'jp-01'),
 ('admin_1', 'japan', 'jp-02'): ('admin_1', 'jp', 'jp-02'),
 ('admin_1', 'japan', 'jp-03'): ('admin_1', 'jp', 'jp-03'),
 ('admin_1', 'japan', 'jp-04'): ('admin_1', 'jp', 'jp-04'),
 ('admin_1', 'japan', 'jp-05'): ('admin_1', 'jp', 'jp-05'),
 ('admin_1', 'japan', 'jp-06'): ('admin_1', 'jp', 'jp-06'),
 ('admin_1', 'japan', 'jp-07'): ('admin_1', 'jp', 'jp-07'),
 ('admin_1', 'japan', 'jp-08'): ('admin_1', 'jp', 'jp-08'),
 ('admin_1', 'japan', 'jp-09'): ('admin_1', 'jp', 'jp-09'),
 ('admin_1', 'japan', 'jp-10'): ('admin_1', 'jp', 'jp-10'),
 ('admin_1', 'japan', 'jp-11'): ('admin_1', 'jp', 'jp-11'),
 ('admin_1', 'japan', 'jp-12'): ('admin_1', 'jp', 'jp-12'),
 ('admin_1', 'japan', 'jp-13'): ('admin_1', 'jp', 'jp-13'),
 ('admin_1', 'japan', 'jp-14'): ('admin_1', 'jp', 'jp-14'),
 ('admin_1', 'japan', 'jp-15'): ('admin_1', 'jp', 'jp-15'),
 ('admin_1', 'japan', 'jp-16'): ('admin_1', 'jp', 'jp-16'),
 ('admin_1', 'japan', 'jp-17'): ('admin_1', 'jp', 'jp-17'),
 ('admin_1', 'japan', 'jp-18'): ('admin_1', 'jp', 'jp-18'),
 ('admin_1', 'japan', 'jp-19'): ('admin_1', 'jp', 'jp-19'),
 ('admin_1', 'japan', 'jp-20'): ('admin_1', 'jp', 'jp-20'),
 ('admin_1', 'japan', 'jp-21'): ('admin_1', 'jp', 'jp-21'),
 ('admin_1', 'japan', 'jp-22'): ('admin_1', 'jp', 'jp-22'),
 ('admin_1', 'japan', 'jp-23'): ('admin_1', 'jp', 'jp-23'),
 ('admin_1', 'japan', 'jp-24'): ('admin_1', 'jp', 'jp-24'),
 ('admin_1', 'japan', 'jp-25'): ('admin_1', 'jp', 'jp-25'),
 ('admin_1', 'japan', 'jp-26'): ('admin_1', 'jp', 'jp-26'),
 ('admin_1', 'japan', 'jp-27'): ('admin_1', 'jp', 'jp-27'),
 ('admin_1', 'japan', 'jp-28'): ('admin_1', 'jp', 'jp-28'),
 ('admin_1', 'japan', 'jp-29'): ('admin_1', 'jp', 'jp-29'),
 ('admin_1', 'japan', 'jp-30'): ('admin_1', 'jp', 'jp-30'),
 ('admin_1', 'japan', 'jp-31'): ('admin_1', 'jp', 'jp-31'),
 ('admin_1', 'japan', 'jp-32'): ('admin_1', 'jp', 'jp-32'),
 ('admin_1', 'japan', 'jp-33'): ('admin_1', 'jp', 'jp-33'),
 ('admin_1', 'japan', 'jp-34'): ('admin_1', 'jp', 'jp-34'),
 ('admin_1', 'japan', 'jp-35'): ('admin_1', 'jp', 'jp-35'),
 ('admin_1', 'japan', 'jp-36'): ('admin_1', 'jp', 'jp-36'),
 ('admin_1', 'japan', 'jp-37'): ('admin_1', 'jp', 'jp-37'),
 ('admin_1', 'japan', 'jp-38'): ('admin_1', 'jp', 'jp-38'),
 ('admin_1', 'japan', 'jp-39'): ('admin_1', 'jp', 'jp-39'),
 ('admin_1', 'japan', 'jp-40'): ('admin_1', 'jp', 'jp-40'),
 ('admin_1', 'japan', 'jp-41'): ('admin_1', 'jp', 'jp-41'),
 ('admin_1', 'japan', 'jp-42'): ('admin_1', 'jp', 'jp-42'),
 ('admin_1', 'japan', 'jp-43'): ('admin_1', 'jp', 'jp-43'),
 ('admin_1', 'japan', 'jp-44'): ('admin_1', 'jp', 'jp-44'),
 ('admin_1', 'japan', 'jp-45'): ('admin_1', 'jp', 'jp-45'),
 ('admin_1', 'japan', 'jp-46'): ('admin_1', 'jp', 'jp-46'),
 ('admin_1', 'japan', 'jp-47'): ('admin_1', 'jp', 'jp-47'),
 ('admin_1', 'japan', 'other'): ('admin_1', 'jp', 'other'),
 ('admin_1', 'japan', 'unknown'): ('admin_1', 'jp', 'unknown'),
 ('admin_1', 'jp', 'jp-01'): ('admin_1', 'jp', 'jp-01'),
 ('admin_1', 'jp', 'jp-02'): ('admin_1', 'jp', 'jp-02'),
 ('admin_1', 'jp', 'jp-03'): ('admin_1', 'jp', 'jp-03'),
 ('admin_1', 'jp', 'jp-04'): ('admin_1', 'jp', 'jp-04'),
 ('admin_1', 'jp', 'jp-05'): ('admin_1', 'jp', 'jp-05'),
 ('admin_1', 'jp', 'jp-06'): ('admin_1', 'jp', 'jp-06'),
 ('admin_1', 'jp', 'jp-07'): ('admin_1', 'jp', 'jp-07'),
 ('admin_1', 'jp', 'jp-08'): ('admin_1', 'jp', 'jp-08'),
 ('admin_1', 'jp', 'jp-09'): ('admin_1', 'jp', 'jp-09'),
 ('admin_1', 'jp', 'jp-10'): ('admin_1', 'jp', 'jp-10'),
 ('admin_1', 'jp', 'jp-11'): ('admin_1', 'jp', 'jp-11'),
 ('admin_1', 'jp', 'jp-12'): ('admin_1', 'jp', 'jp-12'),
 ('admin_1', 'jp', 'jp-13'): ('admin_1', 'jp', 'jp-13'),
 ('admin_1', 'jp', 'jp-14'): ('admin_1', 'jp', 'jp-14'),
 ('admin_1', 'jp', 'jp-15'): ('admin_1', 'jp', 'jp-15'),
 ('admin_1', 'jp', 'jp-16'): ('admin_1', 'jp', 'jp-16'),
 ('admin_1', 'jp', 'jp-17'): ('admin_1', 'jp', 'jp-17'),
 ('admin_1', 'jp', 'jp-18'): ('admin_1', 'jp', 'jp-18'),
 ('admin_1', 'jp', 'jp-19'): ('admin_1', 'jp', 'jp-19'),
 ('admin_1', 'jp', 'jp-20'): ('admin_1', 'jp', 'jp-20'),
 ('admin_1', 'jp', 'jp-21'): ('admin_1', 'jp', 'jp-21'),
 ('admin_1', 'jp', 'jp-22'): ('admin_1', 'jp', 'jp-22'),
 ('admin_1', 'jp', 'jp-23'): ('admin_1', 'jp', 'jp-23'),
 ('admin_1', 'jp', 'jp-24'): ('admin_1', 'jp', 'jp-24'),
 ('admin_1', 'jp', 'jp-25'): ('admin_1', 'jp', 'jp-25'),
 ('admin_1', 'jp', 'jp-26'): ('admin_1', 'jp', 'jp-26'),
 ('admin_1', 'jp', 'jp-27'): ('admin_1', 'jp', 'jp-27'),
 ('admin_1', 'jp', 'jp-28'): ('admin_1', 'jp', 'jp-28'),
 ('admin_1', 'jp', 'jp-29'): ('admin_1', 'jp', 'jp-29'),
 ('admin_1', 'jp', 'jp-30'): ('admin_1', 'jp', 'jp-30'),
 ('admin_1', 'jp', 'jp-31'): ('admin_1', 'jp', 'jp-31'),
 ('admin_1', 'jp', 'jp-32'): ('admin_1', 'jp', 'jp-32'),
 ('admin_1', 'jp', 'jp-33'): ('admin_1', 'jp', 'jp-33'),
 ('admin_1', 'jp', 'jp-34'): ('admin_1', 'jp', 'jp-34'),
 ('admin_1', 'jp', 'jp-35'): ('admin_1', 'jp', 'jp-35'),
 ('admin_1', 'jp', 'jp-36'): ('admin_1', 'jp', 'jp-36'),
 ('admin_1', 'jp', 'jp-37'): ('admin_1', 'jp', 'jp-37'),
 ('admin_1', 'jp', 'jp-38'): ('admin_1', 'jp', 'jp-38'),
 ('admin_1', 'jp', 'jp-39'): ('admin_1', 'jp', 'jp-39'),
 ('admin_1', 'jp', 'jp-40'): ('admin_1', 'jp', 'jp-40'),
 ('admin_1', 'jp', 'jp-41'): ('admin_1', 'jp', 'jp-41'),
 ('admin_1', 'jp', 'jp-42'): ('admin_1', 'jp', 'jp-42'),
 ('admin_1', 'jp', 'jp-43'): ('admin_1', 'jp', 'jp-43'),
 ('admin_1', 'jp', 'jp-44'): ('admin_1', 'jp', 'jp-44'),
 ('admin_1', 'jp', 'jp-45'): ('admin_1', 'jp', 'jp-45'),
 ('admin_1', 'jp', 'jp-46'): ('admin_1', 'jp', 'jp-46'),
 ('admin_1', 'jp', 'jp-47'): ('admin_1', 'jp', 'jp-47'),
 ('admin_1', 'jp', 'other'): ('admin_1', 'jp', 'other'),
 ('admin_1', 'jp', 'unknown'): ('admin_1', 'jp', 'unknown'),
 ('jp_city', 'jp-01', '01101'): ('jp_city', 'jp-01', '01101'),
 ('jp_city', 'jp-01', '01202'): ('jp_city', 'jp-01', '01202'),
 ('jp_city', 'jp-01', '01203'): ('jp_city', 'jp-01', '01203'),
 ('jp_city', 'jp-01', '01204'): ('jp_city', 'jp-01', '01204'),
 ('jp_city', 'jp-01', '01205'): ('jp_city', 'jp-01', '01205'),
 ('jp_city', 'jp-01', '01206'): ('jp_city', 'jp-01', '01206'),
 ('jp_city', 'jp-01', '01207'): ('jp_city', 'jp-01', '01207'),
 ('jp_city', 'jp-01', '01208'): ('jp_city', 'jp-01', '01208'),
 ('jp_city', 'jp-01', '01210'): ('jp_city', 'jp-01', '01210'),
 ('jp_city', 'jp-01', '01212'): ('jp_city', 'jp-01', '01212'),
 ('jp_city', 'jp-01', '01213'): ('jp_city', 'jp-01', '01213'),
 ('jp_city', 'jp-01', '01215'): ('jp_city', 'jp-01', '01215'),
 ('jp_city', 'jp-01', '01217'): ('jp_city', 'jp-01', '01217'),
 ('jp_city', 'jp-01', '01223'): ('jp_city', 'jp-01', '01223'),
 ('jp_city', 'jp-01', '01224'): ('jp_city', 'jp-01', '01224'),
 ('jp_city', 'jp-01', '01225'): ('jp_city', 'jp-01', '01225'),
 ('jp_city', 'jp-01', '01228'): ('jp_city', 'jp-01', '01228'),
 ('jp_city', 'jp-01', '01229'): ('jp_city', 'jp-01', '01229'),
 ('jp_city', 'jp-01', '01230'): ('jp_city', 'jp-01', '01230'),
 ('jp_city', 'jp-01', '01231'): ('jp_city', 'jp-01', '01231'),
 ('jp_city', 'jp-01', '01234'): ('jp_city', 'jp-01', '01234'),
 ('jp_city', 'jp-01', '01235'): ('jp_city', 'jp-01', '01235'),
 ('jp_city', 'jp-01', '01333'): ('jp_city', 'jp-01', '01333'),
 ('jp_city', 'jp-01', '01334'): ('jp_city', 'jp-01', '01334'),
 ('jp_city', 'jp-01', '01337'): ('jp_city', 'jp-01', '01337'),
 ('jp_city', 'jp-01', '01346'): ('jp_city', 'jp-01', '01346'),
 ('jp_city', 'jp-01', '01371'): ('jp_city', 'jp-01', '01371'),
 ('jp_city', 'jp-01', '01400'): ('jp_city', 'jp-01', '01400'),
 ('jp_city', 'jp-01', '01430'): ('jp_city', 'jp-01', '01430'),
 ('jp_city', 'jp-01', '01456'): ('jp_city', 'jp-01', '01456'),
 ('jp_city', 'jp-01', '01459'): ('jp_city', 'jp-01', '01459'),
 ('jp_city', 'jp-01', '01460'): ('jp_city', 'jp-01', '01460'),
 ('jp_city', 'jp-01', '01461'): ('jp_city', 'jp-01', '01461'),
 ('jp_city', 'jp-01', '01519'): ('jp_city', 'jp-01', '01519'),
 ('jp_city', 'jp-01', '01555'): ('jp_city', 'jp-01', '01555'),
 ('jp_city', 'jp-01', '01564'): ('jp_city', 'jp-01', '01564'),
 ('jp_city', 'jp-01', '01610'): ('jp_city', 'jp-01', '01610'),
 ('jp_city', 'jp-01', '01662'): ('jp_city', 'jp-01', '01662'),
 ('jp_city', 'jp-01', 'unknown'): ('jp_city', 'jp-01', 'unknown'),
 ('jp_city', 'jp-01', '空知総合振興局管内'): ('jp_city', 'jp-01', '空知総合振興局管内'),
 ('jp_city', 'jp-01', '釧路総合振興局管内'): ('jp_city', 'jp-01', '釧路総合振興局管内'),
 ('jp_city', 'jp-02', '02201'): ('jp_city', 'jp-02', '02201'),
 ('jp_city', 'jp-02', '02203'): ('jp_city', 'jp-02', '02203'),
 ('jp_city', 'jp-02', 'unknown'): ('jp_city', 'jp-02', 'unknown'),
 ('jp_city', 'jp-03', '03201'): ('jp_city', 'jp-03', '03201'),
 ('jp_city', 'jp-03', '03202'): ('jp_city', 'jp-03', '03202'),
 ('jp_city', 'jp-03', '03207'): ('jp_city', 'jp-03', '03207'),
 ('jp_city', 'jp-03', '03301'): ('jp_city', 'jp-03', '03301'),
 ('jp_city', 'jp-03', '03322'): ('jp_city', 'jp-03', '03322'),
 ('jp_city', 'jp-03', 'unknown'): ('jp_city', 'jp-03', 'unknown'),
 ('jp_city', 'jp-04', '04103'): ('jp_city', 'jp-04', '04103'),
 ('jp_city', 'jp-04', '04202'): ('jp_city', 'jp-04', '04202'),
 ('jp_city', 'jp-04', '04203'): ('jp_city', 'jp-04', '04203'),
 ('jp_city', 'jp-04', '04205'): ('jp_city', 'jp-04', '04205'),
 ('jp_city', 'jp-04', '04207'): ('jp_city', 'jp-04', '04207'),
 ('jp_city', 'jp-04', '04209'): ('jp_city', 'jp-04', '04209'),
 ('jp_city', 'jp-04', '04212'): ('jp_city', 'jp-04', '04212'),
 ('jp_city', 'jp-04', '04215'): ('jp_city', 'jp-04', '04215'),
 ('jp_city', 'jp-04', '04362'): ('jp_city', 'jp-04', '04362'),
 ('jp_city', 'jp-04', '04404'): ('jp_city', 'jp-04', '04404'),
 ('jp_city', 'jp-04', '04423'): ('jp_city', 'jp-04', '04423'),
 ('jp_city', 'jp-04', '04445'): ('jp_city', 'jp-04', '04445'),
 ('jp_city', 'jp-04', '04505'): ('jp_city', 'jp-04', '04505'),
 ('jp_city', 'jp-04', 'unknown'): ('jp_city', 'jp-04', 'unknown'),
 ('jp_city', 'jp-05', '05201'): ('jp_city', 'jp-05', '05201'),
 ('jp_city', 'jp-05', '05203'): ('jp_city', 'jp-05', '05203'),
 ('jp_city', 'jp-05', '05204'): ('jp_city', 'jp-05', '05204'),
 ('jp_city', 'jp-05', 'unknown'): ('jp_city', 'jp-05', 'unknown'),
 ('jp_city', 'jp-06', '06201'): ('jp_city', 'jp-06', '06201'),
 ('jp_city', 'jp-06', '06202'): ('jp_city', 'jp-06', '06202'),
 ('jp_city', 'jp-06', '06203'): ('jp_city', 'jp-06', '06203'),
 ('jp_city', 'jp-06', '06204'): ('jp_city', 'jp-06', '06204'),
 ('jp_city', 'jp-06', '06205'): ('jp_city', 'jp-06', '06205'),
 ('jp_city', 'jp-06', '06207'): ('jp_city', 'jp-06', '06207'),
 ('jp_city', 'jp-06', '06209'): ('jp_city', 'jp-06', '06209'),
 ('jp_city', 'jp-06', '06210'): ('jp_city', 'jp-06', '06210'),
 ('jp_city', 'jp-06', '06213'): ('jp_city', 'jp-06', '06213'),
 ('jp_city', 'jp-06', '06302'): ('jp_city', 'jp-06', '06302'),
 ('jp_city', 'jp-06', '06365'): ('jp_city', 'jp-06', '06365'),
 ('jp_city', 'jp-06', '06381'): ('jp_city', 'jp-06', '06381'),
 ('jp_city', 'jp-06', '06403'): ('jp_city', 'jp-06', '06403'),
 ('jp_city', 'jp-06', 'unknown'): ('jp_city', 'jp-06', 'unknown'),
 ('jp_city', 'jp-07', '07201'): ('jp_city', 'jp-07', '07201'),
 ('jp_city', 'jp-07', '07203'): ('jp_city', 'jp-07', '07203'),
 ('jp_city', 'jp-07', '07204'): ('jp_city', 'jp-07', '07204'),
 ('jp_city', 'jp-07', '07205'): ('jp_city', 'jp-07', '07205'),
 ('jp_city', 'jp-07', '07207'): ('jp_city', 'jp-07', '07207'),
 ('jp_city', 'jp-07', '07209'): ('jp_city', 'jp-07', '07209'),
 ('jp_city', 'jp-07', '07210'): ('jp_city', 'jp-07', '07210'),
 ('jp_city', 'jp-07', '07211'): ('jp_city', 'jp-07', '07211'),
 ('jp_city', 'jp-07', '07212'): ('jp_city', 'jp-07', '07212'),
 ('jp_city', 'jp-07', '07214'): ('jp_city', 'jp-07', '07214'),
 ('jp_city', 'jp-07', '07322'): ('jp_city', 'jp-07', '07322'),
 ('jp_city', 'jp-07', '07466'): ('jp_city', 'jp-07', '07466'),
 ('jp_city', 'jp-07', '07503'): ('jp_city', 'jp-07', '07503'),
 ('jp_city', 'jp-07', '07505'): ('jp_city', 'jp-07', '07505'),
 ('jp_city', 'jp-07', '07541'): ('jp_city', 'jp-07', '07541'),
 ('jp_city', 'jp-07', 'unknown'): ('jp_city', 'jp-07', 'unknown'),
 ('jp_city', 'jp-08', '08201'): ('jp_city', 'jp-08', '08201'),
 ('jp_city', 'jp-08', '08202'): ('jp_city', 'jp-08', '08202'),
 ('jp_city', 'jp-08', '08203'): ('jp_city', 'jp-08', '08203'),
 ('jp_city', 'jp-08', '08204'): ('jp_city', 'jp-08', '08204'),
 ('jp_city', 'jp-08', '08205'): ('jp_city', 'jp-08', '08205'),
 ('jp_city', 'jp-08', '08207'): ('jp_city', 'jp-08', '08207'),
 ('jp_city', 'jp-08', '08208'): ('jp_city', 'jp-08', '08208'),
 ('jp_city', 'jp-08', '08210'): ('jp_city', 'jp-08', '08210'),
 ('jp_city', 'jp-08', '08211'): ('jp_city', 'jp-08', '08211'),
 ('jp_city', 'jp-08', '08212'): ('jp_city', 'jp-08', '08212'),
 ('jp_city', 'jp-08', '08215'): ('jp_city', 'jp-08', '08215'),
 ('jp_city', 'jp-08', '08216'): ('jp_city', 'jp-08', '08216'),
 ('jp_city', 'jp-08', '08217'): ('jp_city', 'jp-08', '08217'),
 ('jp_city', 'jp-08', '08219'): ('jp_city', 'jp-08', '08219'),
 ('jp_city', 'jp-08', '08220'): ('jp_city', 'jp-08', '08220'),
 ('jp_city', 'jp-08', '08221'): ('jp_city', 'jp-08', '08221'),
 ('jp_city', 'jp-08', '08222'): ('jp_city', 'jp-08', '08222'),
 ('jp_city', 'jp-08', '08223'): ('jp_city', 'jp-08', '08223'),
 ('jp_city', 'jp-08', '08224'): ('jp_city', 'jp-08', '08224'),
 ('jp_city', 'jp-08', '08225'): ('jp_city', 'jp-08', '08225'),
 ('jp_city', 'jp-08', '08226'): ('jp_city', 'jp-08', '08226'),
 ('jp_city', 'jp-08', '08227'): ('jp_city', 'jp-08', '08227'),
 ('jp_city', 'jp-08', '08228'): ('jp_city', 'jp-08', '08228'),
 ('jp_city', 'jp-08', '08229'): ('jp_city', 'jp-08', '08229'),
 ('jp_city', 'jp-08', '08231'): ('jp_city', 'jp-08', '08231'),
 ('jp_city', 'jp-08', '08232'): ('jp_city', 'jp-08', '08232'),
 ('jp_city', 'jp-08', '08233'): ('jp_city', 'jp-08', '08233'),
 ('jp_city', 'jp-08', '08234'): ('jp_city', 'jp-08', '08234'),
 ('jp_city', 'jp-08', '08235'): ('jp_city', 'jp-08', '08235'),
 ('jp_city', 'jp-08', '08236'): ('jp_city', 'jp-08', '08236'),
 ('jp_city', 'jp-08', '08302'): ('jp_city', 'jp-08', '08302'),
 ('jp_city', 'jp-08', '08309'): ('jp_city', 'jp-08', '08309'),
 ('jp_city', 'jp-08', '08310'): ('jp_city', 'jp-08', '08310'),
 ('jp_city', 'jp-08', '08341'): ('jp_city', 'jp-08', '08341'),
 ('jp_city', 'jp-08', '08442'): ('jp_city', 'jp-08', '08442'),
 ('jp_city', 'jp-08', '08443'): ('jp_city', 'jp-08', '08443'),
 ('jp_city', 'jp-08', '08521'): ('jp_city', 'jp-08', '08521'),
 ('jp_city', 'jp-08', '08542'): ('jp_city', 'jp-08', '08542'),
 ('jp_city', 'jp-08', '08546'): ('jp_city', 'jp-08', '08546'),
 ('jp_city', 'jp-08', '08564'): ('jp_city', 'jp-08', '08564'),
 ('jp_city', 'jp-08', 'kitaibaraki-shi'): ('jp_city', 'jp-08', '08215'),
 ('jp_city', 'jp-08', 'unknown'): ('jp_city', 'jp-08', 'unknown'),
 ('jp_city', 'jp-08', 'yokohama-shi tsudhuki-ku'): ('jp_city', 'jp-08', 'yokohama-shi tsudhuki-ku'),
 ('jp_city', 'jp-09', '09201'): ('jp_city', 'jp-09', '09201'),
 ('jp_city', 'jp-09', '09202'): ('jp_city', 'jp-09', '09202'),
 ('jp_city', 'jp-09', '09203'): ('jp_city', 'jp-09', '09203'),
 ('jp_city', 'jp-09', '09204'): ('jp_city', 'jp-09', '09204'),
 ('jp_city', 'jp-09', '09205'): ('jp_city', 'jp-09', '09205'),
 ('jp_city', 'jp-09', '09206'): ('jp_city', 'jp-09', '09206'),
 ('jp_city', 'jp-09', '09208'): ('jp_city', 'jp-09', '09208'),
 ('jp_city', 'jp-09', '09209'): ('jp_city', 'jp-09', '09209'),
 ('jp_city', 'jp-09', '09210'): ('jp_city', 'jp-09', '09210'),
 ('jp_city', 'jp-09', '09211'): ('jp_city', 'jp-09', '09211'),
 ('jp_city', 'jp-09', '09213'): ('jp_city', 'jp-09', '09213'),
 ('jp_city', 'jp-09', '09214'): ('jp_city', 'jp-09', '09214'),
 ('jp_city', 'jp-09', '09215'): ('jp_city', 'jp-09', '09215'),
 ('jp_city', 'jp-09', '09216'): ('jp_city', 'jp-09', '09216'),
 ('jp_city', 'jp-09', '09301'): ('jp_city', 'jp-09', '09301'),
 ('jp_city', 'jp-09', '09342'): ('jp_city', 'jp-09', '09342'),
 ('jp_city', 'jp-09', '09345'): ('jp_city', 'jp-09', '09345'),
 ('jp_city', 'jp-09', '09361'): ('jp_city', 'jp-09', '09361'),
 ('jp_city', 'jp-09', '09364'): ('jp_city', 'jp-09', '09364'),
 ('jp_city', 'jp-09', '09386'): ('jp_city', 'jp-09', '09386'),
 ('jp_city', 'jp-09', 'maebashi-shi'): ('jp_city', 'jp-09', 'maebashi-shi'),
 ('jp_city', 'jp-09', 'tochigi-shi'): ('jp_city', 'jp-09', '09203'),
 ('jp_city', 'jp-09', 'unknown'): ('jp_city', 'jp-09', 'unknown'),
 ('jp_city', 'jp-10', '10201'): ('jp_city', 'jp-10', '10201'),
 ('jp_city', 'jp-10', '10202'): ('jp_city', 'jp-10', '10202'),
 ('jp_city', 'jp-10', '10203'): ('jp_city', 'jp-10', '10203'),
 ('jp_city', 'jp-10', '10204'): ('jp_city', 'jp-10', '10204'),
 ('jp_city', 'jp-10', '10205'): ('jp_city', 'jp-10', '10205'),
 ('jp_city', 'jp-10', '10206'): ('jp_city', 'jp-10', '10206'),
 ('jp_city', 'jp-10', '10207'): ('jp_city', 'jp-10', '10207'),
 ('jp_city', 'jp-10', '10208'): ('jp_city', 'jp-10', '10208'),
 ('jp_city', 'jp-10', '10209'): ('jp_city', 'jp-10', '10209'),
 ('jp_city', 'jp-10', '10210'): ('jp_city', 'jp-10', '10210'),
 ('jp_city', 'jp-10', '10211'): ('jp_city', 'jp-10', '10211'),
 ('jp_city', 'jp-10', '10212'): ('jp_city', 'jp-10', '10212'),
 ('jp_city', 'jp-10', '10384'): ('jp_city', 'jp-10', '10384'),
 ('jp_city', 'jp-10', '10421'): ('jp_city', 'jp-10', '10421'),
 ('jp_city', 'jp-10', '10464'): ('jp_city', 'jp-10', '10464'),
 ('jp_city', 'jp-10', '10524'): ('jp_city', 'jp-10', '10524'),
 ('jp_city', 'jp-10', 'unknown'): ('jp_city', 'jp-10', 'unknown'),
 ('jp_city', 'jp-11', '11107'): ('jp_city', 'jp-11', '11107'),
 ('jp_city', 'jp-11', '11201'): ('jp_city', 'jp-11', '11201'),
 ('jp_city', 'jp-11', '11202'): ('jp_city', 'jp-11', '11202'),
 ('jp_city', 'jp-11', '11203'): ('jp_city', 'jp-11', '11203'),
 ('jp_city', 'jp-11', '11206'): ('jp_city', 'jp-11', '11206'),
 ('jp_city', 'jp-11', '11207'): ('jp_city', 'jp-11', '11207'),
 ('jp_city', 'jp-11', '11208'): ('jp_city', 'jp-11', '11208'),
 ('jp_city', 'jp-11', '11209'): ('jp_city', 'jp-11', '11209'),
 ('jp_city', 'jp-11', '11210'): ('jp_city', 'jp-11', '11210'),
 ('jp_city', 'jp-11', '11211'): ('jp_city', 'jp-11', '11211'),
 ('jp_city', 'jp-11', '11212'): ('jp_city', 'jp-11', '11212'),
 ('jp_city', 'jp-11', '11214'): ('jp_city', 'jp-11', '11214'),
 ('jp_city', 'jp-11', '11215'): ('jp_city', 'jp-11', '11215'),
 ('jp_city', 'jp-11', '11216'): ('jp_city', 'jp-11', '11216'),
 ('jp_city', 'jp-11', '11217'): ('jp_city', 'jp-11', '11217'),
 ('jp_city', 'jp-11', '11218'): ('jp_city', 'jp-11', '11218'),
 ('jp_city', 'jp-11', '11219'): ('jp_city', 'jp-11', '11219'),
 ('jp_city', 'jp-11', '11221'): ('jp_city', 'jp-11', '11221'),
 ('jp_city', 'jp-11', '11222'): ('jp_city', 'jp-11', '11222'),
 ('jp_city', 'jp-11', '11223'): ('jp_city', 'jp-11', '11223'),
 ('jp_city', 'jp-11', '11224'): ('jp_city', 'jp-11', '11224'),
 ('jp_city', 'jp-11', '11225'): ('jp_city', 'jp-11', '11225'),
 ('jp_city', 'jp-11', '11227'): ('jp_city', 'jp-11', '11227'),
 ('jp_city', 'jp-11', '11228'): ('jp_city', 'jp-11', '11228'),
 ('jp_city', 'jp-11', '11229'): ('jp_city', 'jp-11', '11229'),
 ('jp_city', 'jp-11', '11230'): ('jp_city', 'jp-11', '11230'),
 ('jp_city', 'jp-11', '11231'): ('jp_city', 'jp-11', '11231'),
 ('jp_city', 'jp-11', '11232'): ('jp_city', 'jp-11', '11232'),
 ('jp_city', 'jp-11', '11233'): ('jp_city', 'jp-11', '11233'),
 ('jp_city', 'jp-11', '11234'): ('jp_city', 'jp-11', '11234'),
 ('jp_city', 'jp-11', '11235'): ('jp_city', 'jp-11', '11235'),
 ('jp_city', 'jp-11', '11237'): ('jp_city', 'jp-11', '11237'),
 ('jp_city', 'jp-11', '11238'): ('jp_city', 'jp-11', '11238'),
 ('jp_city', 'jp-11', '11239'): ('jp_city', 'jp-11', '11239'),
 ('jp_city', 'jp-11', '11240'): ('jp_city', 'jp-11', '11240'),
 ('jp_city', 'jp-11', '11241'): ('jp_city', 'jp-11', '11241'),
 ('jp_city', 'jp-11', '11242'): ('jp_city', 'jp-11', '11242'),
 ('jp_city', 'jp-11', '11243'): ('jp_city', 'jp-11', '11243'),
 ('jp_city', 'jp-11', '11245'): ('jp_city', 'jp-11', '11245'),
 ('jp_city', 'jp-11', '11246'): ('jp_city', 'jp-11', '11246'),
 ('jp_city', 'jp-11', '11301'): ('jp_city', 'jp-11', '11301'),
 ('jp_city', 'jp-11', '11324'): ('jp_city', 'jp-11', '11324'),
 ('jp_city', 'jp-11', '11326'): ('jp_city', 'jp-11', '11326'),
 ('jp_city', 'jp-11', '11327'): ('jp_city', 'jp-11', '11327'),
 ('jp_city', 'jp-11', '11341'): ('jp_city', 'jp-11', '11341'),
 ('jp_city', 'jp-11', '11342'): ('jp_city', 'jp-11', '11342'),
 ('jp_city', 'jp-11', '11343'): ('jp_city', 'jp-11', '11343'),
 ('jp_city', 'jp-11', '11346'): ('jp_city', 'jp-11', '11346'),
 ('jp_city', 'jp-11', '11347'): ('jp_city', 'jp-11', '11347'),
 ('jp_city', 'jp-11', '11348'): ('jp_city', 'jp-11', '11348'),
 ('jp_city', 'jp-11', '11349'): ('jp_city', 'jp-11', '11349'),
 ('jp_city', 'jp-11', '11362'): ('jp_city', 'jp-11', '11362'),
 ('jp_city', 'jp-11', '11363'): ('jp_city', 'jp-11', '11363'),
 ('jp_city', 'jp-11', '11369'): ('jp_city', 'jp-11', '11369'),
 ('jp_city', 'jp-11', '11381'): ('jp_city', 'jp-11', '11381'),
 ('jp_city', 'jp-11', '11383'): ('jp_city', 'jp-11', '11383'),
 ('jp_city', 'jp-11', '11385'): ('jp_city', 'jp-11', '11385'),
 ('jp_city', 'jp-11', '11408'): ('jp_city', 'jp-11', '11408'),
 ('jp_city', 'jp-11', '11442'): ('jp_city', 'jp-11', '11442'),
 ('jp_city', 'jp-11', '11464'): ('jp_city', 'jp-11', '11464'),
 ('jp_city', 'jp-11', '11465'): ('jp_city', 'jp-11', '11465'),
 ('jp_city', 'jp-11', 'other'): ('jp_city', 'jp-11', 'other'),
 ('jp_city', 'jp-11', 'unknown'): ('jp_city', 'jp-11', 'unknown'),
 ('jp_city', 'jp-11', '上尾市'): ('jp_city', 'jp-11', '11219'),
 ('jp_city', 'jp-11', '川口市外'): ('jp_city', 'jp-11', '川口市外'),
 ('jp_city', 'jp-12', '12104'): ('jp_city', 'jp-12', '12104'),
 ('jp_city', 'jp-12', '12202'): ('jp_city', 'jp-12', '12202'),
 ('jp_city', 'jp-12', '12203'): ('jp_city', 'jp-12', '12203'),
 ('jp_city', 'jp-12', '12204'): ('jp_city', 'jp-12', '12204'),
 ('jp_city', 'jp-12', '12205'): ('jp_city', 'jp-12', '12205'),
 ('jp_city', 'jp-12', '12206'): ('jp_city', 'jp-12', '12206'),
 ('jp_city', 'jp-12', '12207'): ('jp_city', 'jp-12', '12207'),
 ('jp_city', 'jp-12', '12208'): ('jp_city', 'jp-12', '12208'),
 ('jp_city', 'jp-12', '12210'): ('jp_city', 'jp-12', '12210'),
 ('jp_city', 'jp-12', '12211'): ('jp_city', 'jp-12', '12211'),
 ('jp_city', 'jp-12', '12212'): ('jp_city', 'jp-12', '12212'),
 ('jp_city', 'jp-12', '12213'): ('jp_city', 'jp-12', '12213'),
 ('jp_city', 'jp-12', '12215'): ('jp_city', 'jp-12', '12215'),
 ('jp_city', 'jp-12', '12216'): ('jp_city', 'jp-12', '12216'),
 ('jp_city', 'jp-12', '12217'): ('jp_city', 'jp-12', '12217'),
 ('jp_city', 'jp-12', '12218'): ('jp_city', 'jp-12', '12218'),
 ('jp_city', 'jp-12', '12219'): ('jp_city', 'jp-12', '12219'),
 ('jp_city', 'jp-12', '12220'): ('jp_city', 'jp-12', '12220'),
 ('jp_city', 'jp-12', '12221'): ('jp_city', 'jp-12', '12221'),
 ('jp_city', 'jp-12', '12222'): ('jp_city', 'jp-12', '12222'),
 ('jp_city', 'jp-12', '12223'): ('jp_city', 'jp-12', '12223'),
 ('jp_city', 'jp-12', '12224'): ('jp_city', 'jp-12', '12224'),
 ('jp_city', 'jp-12', '12225'): ('jp_city', 'jp-12', '12225'),
 ('jp_city', 'jp-12', '12227'): ('jp_city', 'jp-12', '12227'),
 ('jp_city', 'jp-12', '12228'): ('jp_city', 'jp-12', '12228'),
 ('jp_city', 'jp-12', '12229'): ('jp_city', 'jp-12', '12229'),
 ('jp_city', 'jp-12', '12230'): ('jp_city', 'jp-12', '12230'),
 ('jp_city', 'jp-12', '12231'): ('jp_city', 'jp-12', '12231'),
 ('jp_city', 'jp-12', '12232'): ('jp_city', 'jp-12', '12232'),
 ('jp_city', 'jp-12', '12233'): ('jp_city', 'jp-12', '12233'),
 ('jp_city', 'jp-12', '12234'): ('jp_city', 'jp-12', '12234'),
 ('jp_city', 'jp-12', '12235'): ('jp_city', 'jp-12', '12235'),
 ('jp_city', 'jp-12', '12236'): ('jp_city', 'jp-12', '12236'),
 ('jp_city', 'jp-12', '12237'): ('jp_city', 'jp-12', '12237'),
 ('jp_city', 'jp-12', '12238'): ('jp_city', 'jp-12', '12238'),
 ('jp_city', 'jp-12', '12322'): ('jp_city', 'jp-12', '12322'),
 ('jp_city', 'jp-12', '12329'): ('jp_city', 'jp-12', '12329'),
 ('jp_city', 'jp-12', '12347'): ('jp_city', 'jp-12', '12347'),
 ('jp_city', 'jp-12', '12349'): ('jp_city', 'jp-12', '12349'),
 ('jp_city', 'jp-12', '12403'): ('jp_city', 'jp-12', '12403'),
 ('jp_city', 'jp-12', '12409'): ('jp_city', 'jp-12', '12409'),
 ('jp_city', 'jp-12', '12410'): ('jp_city', 'jp-12', '12410'),
 ('jp_city', 'jp-12', '12421'): ('jp_city', 'jp-12', '12421'),
 ('jp_city', 'jp-12', '12424'): ('jp_city', 'jp-12', '12424'),
 ('jp_city', 'jp-12', '12427'): ('jp_city', 'jp-12', '12427'),
 ('jp_city', 'jp-12', '12441'): ('jp_city', 'jp-12', '12441'),
 ('jp_city', 'jp-12', 'unknown'): ('jp_city', 'jp-12', 'unknown'),
 ('jp_city', 'jp-13', '13104'): ('jp_city', 'jp-13', '13104'),
 ('jp_city', 'jp-13', '13112'): ('jp_city', 'jp-13', '13112'),
 ('jp_city', 'jp-13', '13121'): ('jp_city', 'jp-13', '13121'),
 ('jp_city', 'jp-13', '13122'): ('jp_city', 'jp-13', '13122'),
 ('jp_city', 'jp-13', 'fukuoka-shi higashi-ku'): ('jp_city', 'jp-13', 'fukuoka-shi higashi-ku'),
 ('jp_city', 'jp-13', 'unknown'): ('jp_city', 'jp-13', 'unknown'),
 ('jp_city', 'jp-14', '14118'): ('jp_city', 'jp-14', '14118'),
 ('jp_city', 'jp-14', '14135'): ('jp_city', 'jp-14', '14135'),
 ('jp_city', 'jp-14', '14152'): ('jp_city', 'jp-14', '14152'),
 ('jp_city', 'jp-14', '14201'): ('jp_city', 'jp-14', '14201'),
 ('jp_city', 'jp-14', '14203'): ('jp_city', 'jp-14', '14203'),
 ('jp_city', 'jp-14', '14204'): ('jp_city', 'jp-14', '14204'),
 ('jp_city', 'jp-14', '14205'): ('jp_city', 'jp-14', '14205'),
 ('jp_city', 'jp-14', '14206'): ('jp_city', 'jp-14', '14206'),
 ('jp_city', 'jp-14', '14207'): ('jp_city', 'jp-14', '14207'),
 ('jp_city', 'jp-14', '14208'): ('jp_city', 'jp-14', '14208'),
 ('jp_city', 'jp-14', '14210'): ('jp_city', 'jp-14', '14210'),
 ('jp_city', 'jp-14', '14211'): ('jp_city', 'jp-14', '14211'),
 ('jp_city', 'jp-14', '14212'): ('jp_city', 'jp-14', '14212'),
 ('jp_city', 'jp-14', '14213'): ('jp_city', 'jp-14', '14213'),
 ('jp_city', 'jp-14', '14214'): ('jp_city', 'jp-14', '14214'),
 ('jp_city', 'jp-14', '14215'): ('jp_city', 'jp-14', '14215'),
 ('jp_city', 'jp-14', '14216'): ('jp_city', 'jp-14', '14216'),
 ('jp_city', 'jp-14', '14217'): ('jp_city', 'jp-14', '14217'),
 ('jp_city', 'jp-14', '14218'): ('jp_city', 'jp-14', '14218'),
 ('jp_city', 'jp-14', '14301'): ('jp_city', 'jp-14', '14301'),
 ('jp_city', 'jp-14', '14321'): ('jp_city', 'jp-14', '14321'),
 ('jp_city', 'jp-14', '14342'): ('jp_city', 'jp-14', '14342'),
 ('jp_city', 'jp-14', '14362'): ('jp_city', 'jp-14', '14362'),
 ('jp_city', 'jp-14', '14364'): ('jp_city', 'jp-14', '14364'),
 ('jp_city', 'jp-14', '14366'): ('jp_city', 'jp-14', '14366'),
 ('jp_city', 'jp-14', '14382'): ('jp_city', 'jp-14', '14382'),
 ('jp_city', 'jp-14', '14383'): ('jp_city', 'jp-14', '14383'),
 ('jp_city', 'jp-14', '14384'): ('jp_city', 'jp-14', '14384'),
 ('jp_city', 'jp-14', '14401'): ('jp_city', 'jp-14', '14401'),
 ('jp_city', 'jp-14', 'unknown'): ('jp_city', 'jp-14', 'unknown'),
 ('jp_city', 'jp-15', '15104'): ('jp_city', 'jp-15', '15104'),
 ('jp_city', 'jp-15', '15202'): ('jp_city', 'jp-15', '15202'),
 ('jp_city', 'jp-15', '15204'): ('jp_city', 'jp-15', '15204'),
 ('jp_city', 'jp-15', '15205'): ('jp_city', 'jp-15', '15205'),
 ('jp_city', 'jp-15', '15208'): ('jp_city', 'jp-15', '15208'),
 ('jp_city', 'jp-15', '15209'): ('jp_city', 'jp-15', '15209'),
 ('jp_city', 'jp-15', '15213'): ('jp_city', 'jp-15', '15213'),
 ('jp_city', 'jp-15', '15216'): ('jp_city', 'jp-15', '15216'),
 ('jp_city', 'jp-15', '15222'): ('jp_city', 'jp-15', '15222'),
 ('jp_city', 'jp-15', '15223'): ('jp_city', 'jp-15', '15223'),
 ('jp_city', 'jp-15', '15224'): ('jp_city', 'jp-15', '15224'),
 ('jp_city', 'jp-15', '15227'): ('jp_city', 'jp-15', '15227'),
 ('jp_city', 'jp-15', '15307'): ('jp_city', 'jp-15', '15307'),
 ('jp_city', 'jp-15', '15361'): ('jp_city', 'jp-15', '15361'),
 ('jp_city', 'jp-15', 'niigata-shi konan-ku'): ('jp_city', 'jp-15', '15104'),
 ('jp_city', 'jp-16', '16201'): ('jp_city', 'jp-16', '16201'),
 ('jp_city', 'jp-16', '16202'): ('jp_city', 'jp-16', '16202'),
 ('jp_city', 'jp-16', '16204'): ('jp_city', 'jp-16', '16204'),
 ('jp_city', 'jp-16', '16205'): ('jp_city', 'jp-16', '16205'),
 ('jp_city', 'jp-16', '16206'): ('jp_city', 'jp-16', '16206'),
 ('jp_city', 'jp-16', '16207'): ('jp_city', 'jp-16', '16207'),
 ('jp_city', 'jp-16', '16209'): ('jp_city', 'jp-16', '16209'),
 ('jp_city', 'jp-16', '16210'): ('jp_city', 'jp-16', '16210'),
 ('jp_city', 'jp-16', '16211'): ('jp_city', 'jp-16', '16211'),
 ('jp_city', 'jp-16', '16322'): ('jp_city', 'jp-16', '16322'),
 ('jp_city', 'jp-16', '16323'): ('jp_city', 'jp-16', '16323'),
 ('jp_city', 'jp-16', '16342'): ('jp_city', 'jp-16', '16342'),
 ('jp_city', 'jp-16', '16343'): ('jp_city', 'jp-16', '16343'),
 ('jp_city', 'jp-16', 'unknown'): ('jp_city', 'jp-16', 'unknown'),
 ('jp_city', 'jp-16', '富山市'): ('jp_city', 'jp-16', '16201'),
 ('jp_city', 'jp-17', '17201'): ('jp_city', 'jp-17', '17201'),
 ('jp_city', 'jp-17', '17202'): ('jp_city', 'jp-17', '17202'),
 ('jp_city', 'jp-17', '17203'): ('jp_city', 'jp-17', '17203'),
 ('jp_city', 'jp-17', '17206'): ('jp_city', 'jp-17', '17206'),
 ('jp_city', 'jp-17', '17207'): ('jp_city', 'jp-17', '17207'),
 ('jp_city', 'jp-17', '17209'): ('jp_city', 'jp-17', '17209'),
 ('jp_city', 'jp-17', '17210'): ('jp_city', 'jp-17', '17210'),
 ('jp_city', 'jp-17', '17211'): ('jp_city', 'jp-17', '17211'),
 ('jp_city', 'jp-17', '17212'): ('jp_city', 'jp-17', '17212'),
 ('jp_city', 'jp-17', '17324'): ('jp_city', 'jp-17', '17324'),
 ('jp_city', 'jp-17', '17361'): ('jp_city', 'jp-17', '17361'),
 ('jp_city', 'jp-17', '17365'): ('jp_city', 'jp-17', '17365'),
 ('jp_city', 'jp-17', '17386'): ('jp_city', 'jp-17', '17386'),
 ('jp_city', 'jp-17', '17407'): ('jp_city', 'jp-17', '17407'),
 ('jp_city', 'jp-17', 'unknown'): ('jp_city', 'jp-17', 'unknown'),
 ('jp_city', 'jp-18', '18201'): ('jp_city', 'jp-18', '18201'),
 ('jp_city', 'jp-18', '18202'): ('jp_city', 'jp-18', '18202'),
 ('jp_city', 'jp-18', '18205'): ('jp_city', 'jp-18', '18205'),
 ('jp_city', 'jp-18', '18207'): ('jp_city', 'jp-18', '18207'),
 ('jp_city', 'jp-18', '18208'): ('jp_city', 'jp-18', '18208'),
 ('jp_city', 'jp-18', '18209'): ('jp_city', 'jp-18', '18209'),
 ('jp_city', 'jp-18', '18210'): ('jp_city', 'jp-18', '18210'),
 ('jp_city', 'jp-18', '18322'): ('jp_city', 'jp-18', '18322'),
 ('jp_city', 'jp-18', '18404'): ('jp_city', 'jp-18', '18404'),
 ('jp_city', 'jp-18', '18501'): ('jp_city', 'jp-18', '18501'),
 ('jp_city', 'jp-19', '19201'): ('jp_city', 'jp-19', '19201'),
 ('jp_city', 'jp-19', '19202'): ('jp_city', 'jp-19', '19202'),
 ('jp_city', 'jp-19', '19205'): ('jp_city', 'jp-19', '19205'),
 ('jp_city', 'jp-19', '19208'): ('jp_city', 'jp-19', '19208'),
 ('jp_city', 'jp-19', '19209'): ('jp_city', 'jp-19', '19209'),
 ('jp_city', 'jp-19', '19211'): ('jp_city', 'jp-19', '19211'),
 ('jp_city', 'jp-19', '19212'): ('jp_city', 'jp-19', '19212'),
 ('jp_city', 'jp-19', '19213'): ('jp_city', 'jp-19', '19213'),
 ('jp_city', 'jp-19', '19384'): ('jp_city', 'jp-19', '19384'),
 ('jp_city', 'jp-19', 'unknown'): ('jp_city', 'jp-19', 'unknown'),
 ('jp_city', 'jp-20', '20201'): ('jp_city', 'jp-20', '20201'),
 ('jp_city', 'jp-20', '20202'): ('jp_city', 'jp-20', '20202'),
 ('jp_city', 'jp-20', '20203'): ('jp_city', 'jp-20', '20203'),
 ('jp_city', 'jp-20', '20204'): ('jp_city', 'jp-20', '20204'),
 ('jp_city', 'jp-20', '20205'): ('jp_city', 'jp-20', '20205'),
 ('jp_city', 'jp-20', '20206'): ('jp_city', 'jp-20', '20206'),
 ('jp_city', 'jp-20', '20207'): ('jp_city', 'jp-20', '20207'),
 ('jp_city', 'jp-20', '20208'): ('jp_city', 'jp-20', '20208'),
 ('jp_city', 'jp-20', '20211'): ('jp_city', 'jp-20', '20211'),
 ('jp_city', 'jp-20', '20212'): ('jp_city', 'jp-20', '20212'),
 ('jp_city', 'jp-20', '20220'): ('jp_city', 'jp-20', '20220'),
 ('jp_city', 'jp-20', '20309'): ('jp_city', 'jp-20', '20309'),
 ('jp_city', 'jp-20', '20321'): ('jp_city', 'jp-20', '20321'),
 ('jp_city', 'jp-20', '20323'): ('jp_city', 'jp-20', '20323'),
 ('jp_city', 'jp-20', '20383'): ('jp_city', 'jp-20', '20383'),
 ('jp_city', 'jp-20', '20385'): ('jp_city', 'jp-20', '20385'),
 ('jp_city', 'jp-20', '20448'): ('jp_city', 'jp-20', '20448'),
 ('jp_city', 'jp-20', '20452'): ('jp_city', 'jp-20', '20452'),
 ('jp_city', 'jp-20', '20521'): ('jp_city', 'jp-20', '20521'),
 ('jp_city', 'jp-20', '20561'): ('jp_city', 'jp-20', '20561'),
 ('jp_city', 'jp-20', 'unknown'): ('jp_city', 'jp-20', 'unknown'),
 ('jp_city', 'jp-21', '21201'): ('jp_city', 'jp-21', '21201'),
 ('jp_city', 'jp-21', '21202'): ('jp_city', 'jp-21', '21202'),
 ('jp_city', 'jp-21', '21204'): ('jp_city', 'jp-21', '21204'),
 ('jp_city', 'jp-21', '21205'): ('jp_city', 'jp-21', '21205'),
 ('jp_city', 'jp-21', '21206'): ('jp_city', 'jp-21', '21206'),
 ('jp_city', 'jp-21', '21207'): ('jp_city', 'jp-21', '21207'),
 ('jp_city', 'jp-21', '21208'): ('jp_city', 'jp-21', '21208'),
 ('jp_city', 'jp-21', '21209'): ('jp_city', 'jp-21', '21209'),
 ('jp_city', 'jp-21', '21210'): ('jp_city', 'jp-21', '21210'),
 ('jp_city', 'jp-21', '21211'): ('jp_city', 'jp-21', '21211'),
 ('jp_city', 'jp-21', '21212'): ('jp_city', 'jp-21', '21212'),
 ('jp_city', 'jp-21', '21213'): ('jp_city', 'jp-21', '21213'),
 ('jp_city', 'jp-21', '21214'): ('jp_city', 'jp-21', '21214'),
 ('jp_city', 'jp-21', '21216'): ('jp_city', 'jp-21', '21216'),
 ('jp_city', 'jp-21', '21218'): ('jp_city', 'jp-21', '21218'),
 ('jp_city', 'jp-21', '21220'): ('jp_city', 'jp-21', '21220'),
 ('jp_city', 'jp-21', '21221'): ('jp_city', 'jp-21', '21221'),
 ('jp_city', 'jp-21', '21302'): ('jp_city', 'jp-21', '21302'),
 ('jp_city', 'jp-21', '21303'): ('jp_city', 'jp-21', '21303'),
 ('jp_city', 'jp-21', '21341'): ('jp_city', 'jp-21', '21341'),
 ('jp_city', 'jp-21', '21361'): ('jp_city', 'jp-21', '21361'),
 ('jp_city', 'jp-21', '21381'): ('jp_city', 'jp-21', '21381'),
 ('jp_city', 'jp-21', '21382'): ('jp_city', 'jp-21', '21382'),
 ('jp_city', 'jp-21', '21401'): ('jp_city', 'jp-21', '21401'),
 ('jp_city', 'jp-21', '21403'): ('jp_city', 'jp-21', '21403'),
 ('jp_city', 'jp-21', '21404'): ('jp_city', 'jp-21', '21404'),
 ('jp_city', 'jp-21', '21421'): ('jp_city', 'jp-21', '21421'),
 ('jp_city', 'jp-21', '21501'): ('jp_city', 'jp-21', '21501'),
 ('jp_city', 'jp-21', '21502'): ('jp_city', 'jp-21', '21502'),
 ('jp_city', 'jp-21', '21503'): ('jp_city', 'jp-21', '21503'),
 ('jp_city', 'jp-21', '21505'): ('jp_city', 'jp-21', '21505'),
 ('jp_city', 'jp-21', '21506'): ('jp_city', 'jp-21', '21506'),
 ('jp_city', 'jp-21', '21507'): ('jp_city', 'jp-21', '21507'),
 ('jp_city', 'jp-21', '21521'): ('jp_city', 'jp-21', '21521'),
 ('jp_city', 'jp-21', 'nagoya-shi nishi-ku'): ('jp_city', 'jp-21', 'nagoya-shi nishi-ku'),
 ('jp_city', 'jp-21', 'other'): ('jp_city', 'jp-21', 'other'),
 ('jp_city', 'jp-21', 'unknown'): ('jp_city', 'jp-21', 'unknown'),
 ('jp_city', 'jp-21', '城川町'): ('jp_city', 'jp-21', '城川町'),
 ('jp_city', 'jp-21', '美激城市'): ('jp_city', 'jp-21', '美激城市'),
 ('jp_city', 'jp-21', '美濆加茂市'): ('jp_city', 'jp-21', '美濆加茂市'),
 ('jp_city', 'jp-22', '22103'): ('jp_city', 'jp-22', '22103'),
 ('jp_city', 'jp-22', '22132'): ('jp_city', 'jp-22', '22132'),
 ('jp_city', 'jp-22', '22203'): ('jp_city', 'jp-22', '22203'),
 ('jp_city', 'jp-22', '22205'): ('jp_city', 'jp-22', '22205'),
 ('jp_city', 'jp-22', '22206'): ('jp_city', 'jp-22', '22206'),
 ('jp_city', 'jp-22', '22207'): ('jp_city', 'jp-22', '22207'),
 ('jp_city', 'jp-22', '22208'): ('jp_city', 'jp-22', '22208'),
 ('jp_city', 'jp-22', '22209'): ('jp_city', 'jp-22', '22209'),
 ('jp_city', 'jp-22', '22210'): ('jp_city', 'jp-22', '22210'),
 ('jp_city', 'jp-22', '22211'): ('jp_city', 'jp-22', '22211'),
 ('jp_city', 'jp-22', '22212'): ('jp_city', 'jp-22', '22212'),
 ('jp_city', 'jp-22', '22213'): ('jp_city', 'jp-22', '22213'),
 ('jp_city', 'jp-22', '22214'): ('jp_city', 'jp-22', '22214'),
 ('jp_city', 'jp-22', '22215'): ('jp_city', 'jp-22', '22215'),
 ('jp_city', 'jp-22', '22216'): ('jp_city', 'jp-22', '22216'),
 ('jp_city', 'jp-22', '22219'): ('jp_city', 'jp-22', '22219'),
 ('jp_city', 'jp-22', '22222'): ('jp_city', 'jp-22', '22222'),
 ('jp_city', 'jp-22', '22223'): ('jp_city', 'jp-22', '22223'),
 ('jp_city', 'jp-22', '22224'): ('jp_city', 'jp-22', '22224'),
 ('jp_city', 'jp-22', '22304'): ('jp_city', 'jp-22', '22304'),
 ('jp_city', 'jp-22', '22305'): ('jp_city', 'jp-22', '22305'),
 ('jp_city', 'jp-22', '22341'): ('jp_city', 'jp-22', '22341'),
 ('jp_city', 'jp-22', '22342'): ('jp_city', 'jp-22', '22342'),
 ('jp_city', 'jp-22', 'unknown'): ('jp_city', 'jp-22', 'unknown'),
 ('jp_city', 'jp-23', '23104'): ('jp_city', 'jp-23', '23104'),
 ('jp_city', 'jp-23', '23201'): ('jp_city', 'jp-23', '23201'),
 ('jp_city', 'jp-23', '23202'): ('jp_city', 'jp-23', '23202'),
 ('jp_city', 'jp-23', '23203'): ('jp_city', 'jp-23', '23203'),
 ('jp_city', 'jp-23', '23204'): ('jp_city', 'jp-23', '23204'),
 ('jp_city', 'jp-23', '23205'): ('jp_city', 'jp-23', '23205'),
 ('jp_city', 'jp-23', '23206'): ('jp_city', 'jp-23', '23206'),
 ('jp_city', 'jp-23', '23207'): ('jp_city', 'jp-23', '23207'),
 ('jp_city', 'jp-23', '23208'): ('jp_city', 'jp-23', '23208'),
 ('jp_city', 'jp-23', '23209'): ('jp_city', 'jp-23', '23209'),
 ('jp_city', 'jp-23', '23210'): ('jp_city', 'jp-23', '23210'),
 ('jp_city', 'jp-23', '23211'): ('jp_city', 'jp-23', '23211'),
 ('jp_city', 'jp-23', '23212'): ('jp_city', 'jp-23', '23212'),
 ('jp_city', 'jp-23', '23213'): ('jp_city', 'jp-23', '23213'),
 ('jp_city', 'jp-23', '23214'): ('jp_city', 'jp-23', '23214'),
 ('jp_city', 'jp-23', '23215'): ('jp_city', 'jp-23', '23215'),
 ('jp_city', 'jp-23', '23216'): ('jp_city', 'jp-23', '23216'),
 ('jp_city', 'jp-23', '23217'): ('jp_city', 'jp-23', '23217'),
 ('jp_city', 'jp-23', '23219'): ('jp_city', 'jp-23', '23219'),
 ('jp_city', 'jp-23', '23220'): ('jp_city', 'jp-23', '23220'),
 ('jp_city', 'jp-23', '23221'): ('jp_city', 'jp-23', '23221'),
 ('jp_city', 'jp-23', '23222'): ('jp_city', 'jp-23', '23222'),
 ('jp_city', 'jp-23', '23223'): ('jp_city', 'jp-23', '23223'),
 ('jp_city', 'jp-23', '23224'): ('jp_city', 'jp-23', '23224'),
 ('jp_city', 'jp-23', '23225'): ('jp_city', 'jp-23', '23225'),
 ('jp_city', 'jp-23', '23226'): ('jp_city', 'jp-23', '23226'),
 ('jp_city', 'jp-23', '23227'): ('jp_city', 'jp-23', '23227'),
 ('jp_city', 'jp-23', '23228'): ('jp_city', 'jp-23', '23228'),
 ('jp_city', 'jp-23', '23229'): ('jp_city', 'jp-23', '23229'),
 ('jp_city', 'jp-23', '23230'): ('jp_city', 'jp-23', '23230'),
 ('jp_city', 'jp-23', '23231'): ('jp_city', 'jp-23', '23231'),
 ('jp_city', 'jp-23', '23232'): ('jp_city', 'jp-23', '23232'),
 ('jp_city', 'jp-23', '23233'): ('jp_city', 'jp-23', '23233'),
 ('jp_city', 'jp-23', '23234'): ('jp_city', 'jp-23', '23234'),
 ('jp_city', 'jp-23', '23235'): ('jp_city', 'jp-23', '23235'),
 ('jp_city', 'jp-23', '23236'): ('jp_city', 'jp-23', '23236'),
 ('jp_city', 'jp-23', '23237'): ('jp_city', 'jp-23', '23237'),
 ('jp_city', 'jp-23', '23238'): ('jp_city', 'jp-23', '23238'),
 ('jp_city', 'jp-23', '23302'): ('jp_city', 'jp-23', '23302'),
 ('jp_city', 'jp-23', '23342'): ('jp_city', 'jp-23', '23342'),
 ('jp_city', 'jp-23', '23361'): ('jp_city', 'jp-23', '23361'),
 ('jp_city', 'jp-23', '23362'): ('jp_city', 'jp-23', '23362'),
 ('jp_city', 'jp-23', '23424'): ('jp_city', 'jp-23', '23424'),
 ('jp_city', 'jp-23', '23425'): ('jp_city', 'jp-23', '23425'),
 ('jp_city', 'jp-23', '23441'): ('jp_city', 'jp-23', '23441'),
 ('jp_city', 'jp-23', '23442'): ('jp_city', 'jp-23', '23442'),
 ('jp_city', 'jp-23', '23445'): ('jp_city', 'jp-23', '23445'),
 ('jp_city', 'jp-23', '23446'): ('jp_city', 'jp-23', '23446'),
 ('jp_city', 'jp-23', '23447'): ('jp_city', 'jp-23', '23447'),
 ('jp_city', 'jp-23', '23501'): ('jp_city', 'jp-23', '23501'),
 ('jp_city', 'jp-23', 'nagoya-shi nishi-ku'): ('jp_city', 'jp-23', '23104'),
 ('jp_city', 'jp-23', 'unknown'): ('jp_city', 'jp-23', 'unknown'),
 ('jp_city', 'jp-23', '可児市'): ('jp_city', 'jp-23', '可児市'),
 ('jp_city', 'jp-23', '岐阜県'): ('jp_city', 'jp-23', '岐阜県'),
 ('jp_city', 'jp-24', '24201'): ('jp_city', 'jp-24', '24201'),
 ('jp_city', 'jp-24', '24202'): ('jp_city', 'jp-24', '24202'),
 ('jp_city', 'jp-24', '24203'): ('jp_city', 'jp-24', '24203'),
 ('jp_city', 'jp-24', '24204'): ('jp_city', 'jp-24', '24204'),
 ('jp_city', 'jp-24', '24205'): ('jp_city', 'jp-24', '24205'),
 ('jp_city', 'jp-24', '24207'): ('jp_city', 'jp-24', '24207'),
 ('jp_city', 'jp-24', '24208'): ('jp_city', 'jp-24', '24208'),
 ('jp_city', 'jp-24', '24209'): ('jp_city', 'jp-24', '24209'),
 ('jp_city', 'jp-24', '24210'): ('jp_city', 'jp-24', '24210'),
 ('jp_city', 'jp-24', '24214'): ('jp_city', 'jp-24', '24214'),
 ('jp_city', 'jp-24', '24215'): ('jp_city', 'jp-24', '24215'),
 ('jp_city', 'jp-24', '24216'): ('jp_city', 'jp-24', '24216'),
 ('jp_city', 'jp-24', '24324'): ('jp_city', 'jp-24', '24324'),
 ('jp_city', 'jp-24', '24341'): ('jp_city', 'jp-24', '24341'),
 ('jp_city', 'jp-24', '24343'): ('jp_city', 'jp-24', '24343'),
 ('jp_city', 'jp-24', '24442'): ('jp_city', 'jp-24', '24442'),
 ('jp_city', 'jp-24', '24443'): ('jp_city', 'jp-24', '24443'),
 ('jp_city', 'jp-24', '24543'): ('jp_city', 'jp-24', '24543'),
 ('jp_city', 'jp-24', '24561'): ('jp_city', 'jp-24', '24561'),
 ('jp_city', 'jp-24', 'unknown'): ('jp_city', 'jp-24', 'unknown'),
 ('jp_city', 'jp-25', '25201'): ('jp_city', 'jp-25', '25201'),
 ('jp_city', 'jp-25', '25202'): ('jp_city', 'jp-25', '25202'),
 ('jp_city', 'jp-25', '25203'): ('jp_city', 'jp-25', '25203'),
 ('jp_city', 'jp-25', '25204'): ('jp_city', 'jp-25', '25204'),
 ('jp_city', 'jp-25', '25206'): ('jp_city', 'jp-25', '25206'),
 ('jp_city', 'jp-25', '25207'): ('jp_city', 'jp-25', '25207'),
 ('jp_city', 'jp-25', '25208'): ('jp_city', 'jp-25', '25208'),
 ('jp_city', 'jp-25', '25209'): ('jp_city', 'jp-25', '25209'),
 ('jp_city', 'jp-25', '25210'): ('jp_city', 'jp-25', '25210'),
 ('jp_city', 'jp-25', '25211'): ('jp_city', 'jp-25', '25211'),
 ('jp_city', 'jp-25', '25212'): ('jp_city', 'jp-25', '25212'),
 ('jp_city', 'jp-25', '25213'): ('jp_city', 'jp-25', '25213'),
 ('jp_city', 'jp-25', '25214'): ('jp_city', 'jp-25', '25214'),
 ('jp_city', 'jp-25', '25383'): ('jp_city', 'jp-25', '25383'),
 ('jp_city', 'jp-25', '25384'): ('jp_city', 'jp-25', '25384'),
 ('jp_city', 'jp-25', '25441'): ('jp_city', 'jp-25', '25441'),
 ('jp_city', 'jp-25', '25442'): ('jp_city', 'jp-25', '25442'),
 ('jp_city', 'jp-25', 'unknown'): ('jp_city', 'jp-25', 'unknown'),
 ('jp_city', 'jp-26', '26104'): ('jp_city', 'jp-26', '26104'),
 ('jp_city', 'jp-26', '26203'): ('jp_city', 'jp-26', '26203'),
 ('jp_city', 'jp-26', '26204'): ('jp_city', 'jp-26', '26204'),
 ('jp_city', 'jp-26', '26209'): ('jp_city', 'jp-26', '26209'),
 ('jp_city', 'jp-26', '26211'): ('jp_city', 'jp-26', '26211'),
 ('jp_city', 'jp-26', 'unknown'): ('jp_city', 'jp-26', 'unknown'),
 ('jp_city', 'jp-27', '27108'): ('jp_city', 'jp-27', '27108'),
 ('jp_city', 'jp-27', '27143'): ('jp_city', 'jp-27', '27143'),
 ('jp_city', 'jp-27', '27202'): ('jp_city', 'jp-27', '27202'),
 ('jp_city', 'jp-27', '27203'): ('jp_city', 'jp-27', '27203'),
 ('jp_city', 'jp-27', '27204'): ('jp_city', 'jp-27', '27204'),
 ('jp_city', 'jp-27', '27205'): ('jp_city', 'jp-27', '27205'),
 ('jp_city', 'jp-27', '27206'): ('jp_city', 'jp-27', '27206'),
 ('jp_city', 'jp-27', '27207'): ('jp_city', 'jp-27', '27207'),
 ('jp_city', 'jp-27', '27208'): ('jp_city', 'jp-27', '27208'),
 ('jp_city', 'jp-27', '27209'): ('jp_city', 'jp-27', '27209'),
 ('jp_city', 'jp-27', '27210'): ('jp_city', 'jp-27', '27210'),
 ('jp_city', 'jp-27', '27211'): ('jp_city', 'jp-27', '27211'),
 ('jp_city', 'jp-27', '27212'): ('jp_city', 'jp-27', '27212'),
 ('jp_city', 'jp-27', '27213'): ('jp_city', 'jp-27', '27213'),
 ('jp_city', 'jp-27', '27214'): ('jp_city', 'jp-27', '27214'),
 ('jp_city', 'jp-27', '27215'): ('jp_city', 'jp-27', '27215'),
 ('jp_city', 'jp-27', '27216'): ('jp_city', 'jp-27', '27216'),
 ('jp_city', 'jp-27', '27217'): ('jp_city', 'jp-27', '27217'),
 ('jp_city', 'jp-27', '27218'): ('jp_city', 'jp-27', '27218'),
 ('jp_city', 'jp-27', '27219'): ('jp_city', 'jp-27', '27219'),
 ('jp_city', 'jp-27', '27220'): ('jp_city', 'jp-27', '27220'),
 ('jp_city', 'jp-27', '27221'): ('jp_city', 'jp-27', '27221'),
 ('jp_city', 'jp-27', '27222'): ('jp_city', 'jp-27', '27222'),
 ('jp_city', 'jp-27', '27223'): ('jp_city', 'jp-27', '27223'),
 ('jp_city', 'jp-27', '27224'): ('jp_city', 'jp-27', '27224'),
 ('jp_city', 'jp-27', '27225'): ('jp_city', 'jp-27', '27225'),
 ('jp_city', 'jp-27', '27226'): ('jp_city', 'jp-27', '27226'),
 ('jp_city', 'jp-27', '27227'): ('jp_city', 'jp-27', '27227'),
 ('jp_city', 'jp-27', '27228'): ('jp_city', 'jp-27', '27228'),
 ('jp_city', 'jp-27', '27229'): ('jp_city', 'jp-27', '27229'),
 ('jp_city', 'jp-27', '27230'): ('jp_city', 'jp-27', '27230'),
 ('jp_city', 'jp-27', '27231'): ('jp_city', 'jp-27', '27231'),
 ('jp_city', 'jp-27', '27232'): ('jp_city', 'jp-27', '27232'),
 ('jp_city', 'jp-27', '27301'): ('jp_city', 'jp-27', '27301'),
 ('jp_city', 'jp-27', '27321'): ('jp_city', 'jp-27', '27321'),
 ('jp_city', 'jp-27', '27322'): ('jp_city', 'jp-27', '27322'),
 ('jp_city', 'jp-27', '27341'): ('jp_city', 'jp-27', '27341'),
 ('jp_city', 'jp-27', '27361'): ('jp_city', 'jp-27', '27361'),
 ('jp_city', 'jp-27', '27362'): ('jp_city', 'jp-27', '27362'),
 ('jp_city', 'jp-27', '27366'): ('jp_city', 'jp-27', '27366'),
 ('jp_city', 'jp-27', '27381'): ('jp_city', 'jp-27', '27381'),
 ('jp_city', 'jp-27', '27382'): ('jp_city', 'jp-27', '27382'),
 ('jp_city', 'jp-27', '27383'): ('jp_city', 'jp-27', '27383'),
 ('jp_city', 'jp-27', 'osaka-shi taisho-ku'): ('jp_city', 'jp-27', '27108'),
 ('jp_city', 'jp-27', 'other'): ('jp_city', 'jp-27', 'other'),
 ('jp_city', 'jp-27', 'unknown'): ('jp_city', 'jp-27', 'unknown'),
 ('jp_city', 'jp-27', '吹田市'): ('jp_city', 'jp-27', '27205'),
 ('jp_city', 'jp-28', '28108'): ('jp_city', 'jp-28', '28108'),
 ('jp_city', 'jp-28', '28201'): ('jp_city', 'jp-28', '28201'),
 ('jp_city', 'jp-28', '28202'): ('jp_city', 'jp-28', '28202'),
 ('jp_city', 'jp-28', '28203'): ('jp_city', 'jp-28', '28203'),
 ('jp_city', 'jp-28', '28204'): ('jp_city', 'jp-28', '28204'),
 ('jp_city', 'jp-28', '28206'): ('jp_city', 'jp-28', '28206'),
 ('jp_city', 'jp-28', '28207'): ('jp_city', 'jp-28', '28207'),
 ('jp_city', 'jp-28', '28210'): ('jp_city', 'jp-28', '28210'),
 ('jp_city', 'jp-28', '28212'): ('jp_city', 'jp-28', '28212'),
 ('jp_city', 'jp-28', '28213'): ('jp_city', 'jp-28', '28213'),
 ('jp_city', 'jp-28', '28214'): ('jp_city', 'jp-28', '28214'),
 ('jp_city', 'jp-28', '28215'): ('jp_city', 'jp-28', '28215'),
 ('jp_city', 'jp-28', '28216'): ('jp_city', 'jp-28', '28216'),
 ('jp_city', 'jp-28', '28217'): ('jp_city', 'jp-28', '28217'),
 ('jp_city', 'jp-28', '28218'): ('jp_city', 'jp-28', '28218'),
 ('jp_city', 'jp-28', '28219'): ('jp_city', 'jp-28', '28219'),
 ('jp_city', 'jp-28', '28220'): ('jp_city', 'jp-28', '28220'),
 ('jp_city', 'jp-28', '28223'): ('jp_city', 'jp-28', '28223'),
 ('jp_city', 'jp-28', '28224'): ('jp_city', 'jp-28', '28224'),
 ('jp_city', 'jp-28', '28225'): ('jp_city', 'jp-28', '28225'),
 ('jp_city', 'jp-28', '28226'): ('jp_city', 'jp-28', '28226'),
 ('jp_city', 'jp-28', '28228'): ('jp_city', 'jp-28', '28228'),
 ('jp_city', 'jp-28', '28301'): ('jp_city', 'jp-28', '28301'),
 ('jp_city', 'jp-28', '28381'): ('jp_city', 'jp-28', '28381'),
 ('jp_city', 'jp-28', '28382'): ('jp_city', 'jp-28', '28382'),
 ('jp_city', 'jp-28', '28443'): ('jp_city', 'jp-28', '28443'),
 ('jp_city', 'jp-28', 'unknown'): ('jp_city', 'jp-28', 'unknown'),
 ('jp_city', 'jp-28', '西宮市外'): ('jp_city', 'jp-28', '西宮市外'),
 ('jp_city', 'jp-29', '29201'): ('jp_city', 'jp-29', '29201'),
 ('jp_city', 'jp-29', '29202'): ('jp_city', 'jp-29', '29202'),
 ('jp_city', 'jp-29', '29203'): ('jp_city', 'jp-29', '29203'),
 ('jp_city', 'jp-29', '29204'): ('jp_city', 'jp-29', '29204'),
 ('jp_city', 'jp-29', '29205'): ('jp_city', 'jp-29', '29205'),
 ('jp_city', 'jp-29', '29206'): ('jp_city', 'jp-29', '29206'),
 ('jp_city', 'jp-29', '29207'): ('jp_city', 'jp-29', '29207'),
 ('jp_city', 'jp-29', '29209'): ('jp_city', 'jp-29', '29209'),
 ('jp_city', 'jp-29', '29210'): ('jp_city', 'jp-29', '29210'),
 ('jp_city', 'jp-29', '29211'): ('jp_city', 'jp-29', '29211'),
 ('jp_city', 'jp-29', '29212'): ('jp_city', 'jp-29', '29212'),
 ('jp_city', 'jp-29', '29342'): ('jp_city', 'jp-29', '29342'),
 ('jp_city', 'jp-29', '29343'): ('jp_city', 'jp-29', '29343'),
 ('jp_city', 'jp-29', '29344'): ('jp_city', 'jp-29', '29344'),
 ('jp_city', 'jp-29', '29361'): ('jp_city', 'jp-29', '29361'),
 ('jp_city', 'jp-29', '29362'): ('jp_city', 'jp-29', '29362'),
 ('jp_city', 'jp-29', '29363'): ('jp_city', 'jp-29', '29363'),
 ('jp_city', 'jp-29', '29401'): ('jp_city', 'jp-29', '29401'),
 ('jp_city', 'jp-29', '29424'): ('jp_city', 'jp-29', '29424'),
 ('jp_city', 'jp-29', '29425'): ('jp_city', 'jp-29', '29425'),
 ('jp_city', 'jp-29', '29426'): ('jp_city', 'jp-29', '29426'),
 ('jp_city', 'jp-29', '29427'): ('jp_city', 'jp-29', '29427'),
 ('jp_city', 'jp-29', '29442'): ('jp_city', 'jp-29', '29442'),
 ('jp_city', 'jp-29', 'unknown'): ('jp_city', 'jp-29', 'unknown'),
 ('jp_city', 'jp-30', '30201'): ('jp_city', 'jp-30', '30201'),
 ('jp_city', 'jp-30', 'unknown'): ('jp_city', 'jp-30', 'unknown'),
 ('jp_city', 'jp-31', '31201'): ('jp_city', 'jp-31', '31201'),
 ('jp_city', 'jp-31', '31202'): ('jp_city', 'jp-31', '31202'),
 ('jp_city', 'jp-31', '31203'): ('jp_city', 'jp-31', '31203'),
 ('jp_city', 'jp-31', '31370'): ('jp_city', 'jp-31', '31370'),
 ('jp_city', 'jp-31', 'unknown'): ('jp_city', 'jp-31', 'unknown'),
 ('jp_city', 'jp-32', '32201'): ('jp_city', 'jp-32', '32201'),
 ('jp_city', 'jp-32', '32203'): ('jp_city', 'jp-32', '32203'),
 ('jp_city', 'jp-32', '32204'): ('jp_city', 'jp-32', '32204'),
 ('jp_city', 'jp-32', '32209'): ('jp_city', 'jp-32', '32209'),
 ('jp_city', 'jp-33', '33101'): ('jp_city', 'jp-33', '33101'),
 ('jp_city', 'jp-33', '33202'): ('jp_city', 'jp-33', '33202'),
 ('jp_city', 'jp-33', '33203'): ('jp_city', 'jp-33', '33203'),
 ('jp_city', 'jp-33', '33204'): ('jp_city', 'jp-33', '33204'),
 ('jp_city', 'jp-33', '33209'): ('jp_city', 'jp-33', '33209'),
 ('jp_city', 'jp-33', '33212'): ('jp_city', 'jp-33', '33212'),
 ('jp_city', 'jp-33', '33213'): ('jp_city', 'jp-33', '33213'),
 ('jp_city', 'jp-33', '33216'): ('jp_city', 'jp-33', '33216'),
 ('jp_city', 'jp-33', '33423'): ('jp_city', 'jp-33', '33423'),
 ('jp_city', 'jp-33', '33445'): ('jp_city', 'jp-33', '33445'),
 ('jp_city', 'jp-33', 'unknown'): ('jp_city', 'jp-33', 'unknown'),
 ('jp_city', 'jp-34', '34101'): ('jp_city', 'jp-34', '34101'),
 ('jp_city', 'jp-34', '34202'): ('jp_city', 'jp-34', '34202'),
 ('jp_city', 'jp-34', '34204'): ('jp_city', 'jp-34', '34204'),
 ('jp_city', 'jp-34', '34205'): ('jp_city', 'jp-34', '34205'),
 ('jp_city', 'jp-34', '34207'): ('jp_city', 'jp-34', '34207'),
 ('jp_city', 'jp-34', '34208'): ('jp_city', 'jp-34', '34208'),
 ('jp_city', 'jp-34', '34209'): ('jp_city', 'jp-34', '34209'),
 ('jp_city', 'jp-34', '34210'): ('jp_city', 'jp-34', '34210'),
 ('jp_city', 'jp-34', '34212'): ('jp_city', 'jp-34', '34212'),
 ('jp_city', 'jp-34', '34213'): ('jp_city', 'jp-34', '34213'),
 ('jp_city', 'jp-34', '34215'): ('jp_city', 'jp-34', '34215'),
 ('jp_city', 'jp-34', '34302'): ('jp_city', 'jp-34', '34302'),
 ('jp_city', 'jp-34', '34304'): ('jp_city', 'jp-34', '34304'),
 ('jp_city', 'jp-34', '34307'): ('jp_city', 'jp-34', '34307'),
 ('jp_city', 'jp-34', '34431'): ('jp_city', 'jp-34', '34431'),
 ('jp_city', 'jp-34', 'unknown'): ('jp_city', 'jp-34', 'unknown'),
 ('jp_city', 'jp-34', '岡山県'): ('jp_city', 'jp-34', '岡山県'),
 ('jp_city', 'jp-34', '広島県'): ('jp_city', 'jp-34', '広島県'),
 ('jp_city', 'jp-35', '35201'): ('jp_city', 'jp-35', '35201'),
 ('jp_city', 'jp-35', '35202'): ('jp_city', 'jp-35', '35202'),
 ('jp_city', 'jp-35', '35203'): ('jp_city', 'jp-35', '35203'),
 ('jp_city', 'jp-35', '35206'): ('jp_city', 'jp-35', '35206'),
 ('jp_city', 'jp-35', '35207'): ('jp_city', 'jp-35', '35207'),
 ('jp_city', 'jp-35', '35208'): ('jp_city', 'jp-35', '35208'),
 ('jp_city', 'jp-35', '35210'): ('jp_city', 'jp-35', '35210'),
 ('jp_city', 'jp-35', '35215'): ('jp_city', 'jp-35', '35215'),
 ('jp_city', 'jp-35', '35216'): ('jp_city', 'jp-35', '35216'),
 ('jp_city', 'jp-36', 'unknown'): ('jp_city', 'jp-36', 'unknown'),
 ('jp_city', 'jp-37', '37201'): ('jp_city', 'jp-37', '37201'),
 ('jp_city', 'jp-37', '37202'): ('jp_city', 'jp-37', '37202'),
 ('jp_city', 'jp-37', '37203'): ('jp_city', 'jp-37', '37203'),
 ('jp_city', 'jp-37', '37205'): ('jp_city', 'jp-37', '37205'),
 ('jp_city', 'jp-37', '37206'): ('jp_city', 'jp-37', '37206'),
 ('jp_city', 'jp-37', '37207'): ('jp_city', 'jp-37', '37207'),
 ('jp_city', 'jp-37', '37208'): ('jp_city', 'jp-37', '37208'),
 ('jp_city', 'jp-37', '37322'): ('jp_city', 'jp-37', '37322'),
 ('jp_city', 'jp-37', '37341'): ('jp_city', 'jp-37', '37341'),
 ('jp_city', 'jp-37', '37404'): ('jp_city', 'jp-37', '37404'),
 ('jp_city', 'jp-37', '37406'): ('jp_city', 'jp-37', '37406'),
 ('jp_city', 'jp-37', 'unknown'): ('jp_city', 'jp-37', 'unknown'),
 ('jp_city', 'jp-37', '坂出市'): ('jp_city', 'jp-37', '37203'),
 ('jp_city', 'jp-38', '38201'): ('jp_city', 'jp-38', '38201'),
 ('jp_city', 'jp-38', '38202'): ('jp_city', 'jp-38', '38202'),
 ('jp_city', 'jp-38', '38205'): ('jp_city', 'jp-38', '38205'),
 ('jp_city', 'jp-38', '38214'): ('jp_city', 'jp-38', '38214'),
 ('jp_city', 'jp-38', '38215'): ('jp_city', 'jp-38', '38215'),
 ('jp_city', 'jp-38', '38401'): ('jp_city', 'jp-38', '38401'),
 ('jp_city', 'jp-38', '38402'): ('jp_city', 'jp-38', '38402'),
 ('jp_city', 'jp-38', '38422'): ('jp_city', 'jp-38', '38422'),
 ('jp_city', 'jp-38', '38506'): ('jp_city', 'jp-38', '38506'),
 ('jp_city', 'jp-38', 'unknown'): ('jp_city', 'jp-38', 'unknown'),
 ('jp_city', 'jp-39', '39201'): ('jp_city', 'jp-39', '39201'),
 ('jp_city', 'jp-39', 'unknown'): ('jp_city', 'jp-39', 'unknown'),
 ('jp_city', 'jp-40', '40107'): ('jp_city', 'jp-40', '40107'),
 ('jp_city', 'jp-40', '40131'): ('jp_city', 'jp-40', '40131'),
 ('jp_city', 'jp-40', '40202'): ('jp_city', 'jp-40', '40202'),
 ('jp_city', 'jp-40', '40203'): ('jp_city', 'jp-40', '40203'),
 ('jp_city', 'jp-40', '40204'): ('jp_city', 'jp-40', '40204'),
 ('jp_city', 'jp-40', '40205'): ('jp_city', 'jp-40', '40205'),
 ('jp_city', 'jp-40', '40206'): ('jp_city', 'jp-40', '40206'),
 ('jp_city', 'jp-40', '40207'): ('jp_city', 'jp-40', '40207'),
 ('jp_city', 'jp-40', '40210'): ('jp_city', 'jp-40', '40210'),
 ('jp_city', 'jp-40', '40211'): ('jp_city', 'jp-40', '40211'),
 ('jp_city', 'jp-40', '40212'): ('jp_city', 'jp-40', '40212'),
 ('jp_city', 'jp-40', '40213'): ('jp_city', 'jp-40', '40213'),
 ('jp_city', 'jp-40', '40214'): ('jp_city', 'jp-40', '40214'),
 ('jp_city', 'jp-40', '40215'): ('jp_city', 'jp-40', '40215'),
 ('jp_city', 'jp-40', '40216'): ('jp_city', 'jp-40', '40216'),
 ('jp_city', 'jp-40', '40217'): ('jp_city', 'jp-40', '40217'),
 ('jp_city', 'jp-40', '40218'): ('jp_city', 'jp-40', '40218'),
 ('jp_city', 'jp-40', '40219'): ('jp_city', 'jp-40', '40219'),
 ('jp_city', 'jp-40', '40220'): ('jp_city', 'jp-40', '40220'),
 ('jp_city', 'jp-40', '40221'): ('jp_city', 'jp-40', '40221'),
 ('jp_city', 'jp-40', '40223'): ('jp_city', 'jp-40', '40223'),
 ('jp_city', 'jp-40', '40224'): ('jp_city', 'jp-40', '40224'),
 ('jp_city', 'jp-40', '40225'): ('jp_city', 'jp-40', '40225'),
 ('jp_city', 'jp-40', '40226'): ('jp_city', 'jp-40', '40226'),
 ('jp_city', 'jp-40', '40227'): ('jp_city', 'jp-40', '40227'),
 ('jp_city', 'jp-40', '40228'): ('jp_city', 'jp-40', '40228'),
 ('jp_city', 'jp-40', '40229'): ('jp_city', 'jp-40', '40229'),
 ('jp_city', 'jp-40', '40230'): ('jp_city', 'jp-40', '40230'),
 ('jp_city', 'jp-40', '40305'): ('jp_city', 'jp-40', '40305'),
 ('jp_city', 'jp-40', '40341'): ('jp_city', 'jp-40', '40341'),
 ('jp_city', 'jp-40', 'unknown'): ('jp_city', 'jp-40', 'unknown'),
 ('jp_city', 'jp-41', '41201'): ('jp_city', 'jp-41', '41201'),
 ('jp_city', 'jp-41', '41202'): ('jp_city', 'jp-41', '41202'),
 ('jp_city', 'jp-41', '41203'): ('jp_city', 'jp-41', '41203'),
 ('jp_city', 'jp-41', '41204'): ('jp_city', 'jp-41', '41204'),
 ('jp_city', 'jp-41', '41205'): ('jp_city', 'jp-41', '41205'),
 ('jp_city', 'jp-41', '41206'): ('jp_city', 'jp-41', '41206'),
 ('jp_city', 'jp-41', '41208'): ('jp_city', 'jp-41', '41208'),
 ('jp_city', 'jp-41', '41209'): ('jp_city', 'jp-41', '41209'),
 ('jp_city', 'jp-41', '41210'): ('jp_city', 'jp-41', '41210'),
 ('jp_city', 'jp-41', '41327'): ('jp_city', 'jp-41', '41327'),
 ('jp_city', 'jp-41', '41341'): ('jp_city', 'jp-41', '41341'),
 ('jp_city', 'jp-41', '41346'): ('jp_city', 'jp-41', '41346'),
 ('jp_city', 'jp-41', '41387'): ('jp_city', 'jp-41', '41387'),
 ('jp_city', 'jp-41', '41401'): ('jp_city', 'jp-41', '41401'),
 ('jp_city', 'jp-41', '41423'): ('jp_city', 'jp-41', '41423'),
 ('jp_city', 'jp-41', '41424'): ('jp_city', 'jp-41', '41424'),
 ('jp_city', 'jp-41', '41425'): ('jp_city', 'jp-41', '41425'),
 ('jp_city', 'jp-41', 'unknown'): ('jp_city', 'jp-41', 'unknown'),
 ('jp_city', 'jp-42', '42201'): ('jp_city', 'jp-42', '42201'),
 ('jp_city', 'jp-42', '42202'): ('jp_city', 'jp-42', '42202'),
 ('jp_city', 'jp-42', '42203'): ('jp_city', 'jp-42', '42203'),
 ('jp_city', 'jp-42', '42204'): ('jp_city', 'jp-42', '42204'),
 ('jp_city', 'jp-42', '42205'): ('jp_city', 'jp-42', '42205'),
 ('jp_city', 'jp-42', '42207'): ('jp_city', 'jp-42', '42207'),
 ('jp_city', 'jp-42', '42208'): ('jp_city', 'jp-42', '42208'),
 ('jp_city', 'jp-42', '42209'): ('jp_city', 'jp-42', '42209'),
 ('jp_city', 'jp-42', '42210'): ('jp_city', 'jp-42', '42210'),
 ('jp_city', 'jp-42', '42211'): ('jp_city', 'jp-42', '42211'),
 ('jp_city', 'jp-42', '42212'): ('jp_city', 'jp-42', '42212'),
 ('jp_city', 'jp-42', '42213'): ('jp_city', 'jp-42', '42213'),
 ('jp_city', 'jp-42', '42307'): ('jp_city', 'jp-42', '42307'),
 ('jp_city', 'jp-42', '42308'): ('jp_city', 'jp-42', '42308'),
 ('jp_city', 'jp-42', '42321'): ('jp_city', 'jp-42', '42321'),
 ('jp_city', 'jp-42', 'unknown'): ('jp_city', 'jp-42', 'unknown'),
 ('jp_city', 'jp-43', '43103'): ('jp_city', 'jp-43', '43103'),
 ('jp_city', 'jp-43', '43202'): ('jp_city', 'jp-43', '43202'),
 ('jp_city', 'jp-43', '43203'): ('jp_city', 'jp-43', '43203'),
 ('jp_city', 'jp-43', '43204'): ('jp_city', 'jp-43', '43204'),
 ('jp_city', 'jp-43', '43206'): ('jp_city', 'jp-43', '43206'),
 ('jp_city', 'jp-43', '43208'): ('jp_city', 'jp-43', '43208'),
 ('jp_city', 'jp-43', '43210'): ('jp_city', 'jp-43', '43210'),
 ('jp_city', 'jp-43', '43211'): ('jp_city', 'jp-43', '43211'),
 ('jp_city', 'jp-43', '43212'): ('jp_city', 'jp-43', '43212'),
 ('jp_city', 'jp-43', '43213'): ('jp_city', 'jp-43', '43213'),
 ('jp_city', 'jp-43', '43216'): ('jp_city', 'jp-43', '43216'),
 ('jp_city', 'jp-43', '43364'): ('jp_city', 'jp-43', '43364'),
 ('jp_city', 'jp-43', '43368'): ('jp_city', 'jp-43', '43368'),
 ('jp_city', 'jp-43', '43403'): ('jp_city', 'jp-43', '43403'),
 ('jp_city', 'jp-43', '43404'): ('jp_city', 'jp-43', '43404'),
 ('jp_city', 'jp-43', '43423'): ('jp_city', 'jp-43', '43423'),
 ('jp_city', 'jp-43', '43441'): ('jp_city', 'jp-43', '43441'),
 ('jp_city', 'jp-43', '43442'): ('jp_city', 'jp-43', '43442'),
 ('jp_city', 'jp-43', '43443'): ('jp_city', 'jp-43', '43443'),
 ('jp_city', 'jp-43', 'unknown'): ('jp_city', 'jp-43', 'unknown'),
 ('jp_city', 'jp-44', '44201'): ('jp_city', 'jp-44', '44201'),
 ('jp_city', 'jp-44', '44202'): ('jp_city', 'jp-44', '44202'),
 ('jp_city', 'jp-44', '44203'): ('jp_city', 'jp-44', '44203'),
 ('jp_city', 'jp-44', '44204'): ('jp_city', 'jp-44', '44204'),
 ('jp_city', 'jp-44', '44205'): ('jp_city', 'jp-44', '44205'),
 ('jp_city', 'jp-44', '44206'): ('jp_city', 'jp-44', '44206'),
 ('jp_city', 'jp-44', '44208'): ('jp_city', 'jp-44', '44208'),
 ('jp_city', 'jp-44', '44209'): ('jp_city', 'jp-44', '44209'),
 ('jp_city', 'jp-44', '44210'): ('jp_city', 'jp-44', '44210'),
 ('jp_city', 'jp-44', '44211'): ('jp_city', 'jp-44', '44211'),
 ('jp_city', 'jp-44', 'unknown'): ('jp_city', 'jp-44', 'unknown'),
 ('jp_city', 'jp-44', '中津市'): ('jp_city', 'jp-44', '44203'),
 ('jp_city', 'jp-45', '45201'): ('jp_city', 'jp-45', '45201'),
 ('jp_city', 'jp-45', '45202'): ('jp_city', 'jp-45', '45202'),
 ('jp_city', 'jp-45', '45203'): ('jp_city', 'jp-45', '45203'),
 ('jp_city', 'jp-45', '45204'): ('jp_city', 'jp-45', '45204'),
 ('jp_city', 'jp-45', '45205'): ('jp_city', 'jp-45', '45205'),
 ('jp_city', 'jp-45', '45206'): ('jp_city', 'jp-45', '45206'),
 ('jp_city', 'jp-45', '45208'): ('jp_city', 'jp-45', '45208'),
 ('jp_city', 'jp-45', '45382'): ('jp_city', 'jp-45', '45382'),
 ('jp_city', 'jp-45', '45401'): ('jp_city', 'jp-45', '45401'),
 ('jp_city', 'jp-45', '45402'): ('jp_city', 'jp-45', '45402'),
 ('jp_city', 'jp-45', '45404'): ('jp_city', 'jp-45', '45404'),
 ('jp_city', 'jp-45', '45405'): ('jp_city', 'jp-45', '45405'),
 ('jp_city', 'jp-45', '45406'): ('jp_city', 'jp-45', '45406'),
 ('jp_city', 'jp-45', '45421'): ('jp_city', 'jp-45', '45421'),
 ('jp_city', 'jp-45', '45441'): ('jp_city', 'jp-45', '45441'),
 ('jp_city', 'jp-45', 'unknown'): ('jp_city', 'jp-45', 'unknown'),
 ('jp_city', 'jp-45', '宮崎市'): ('jp_city', 'jp-45', '45201'),
 ('jp_city', 'jp-45', '熊本県'): ('jp_city', 'jp-45', '熊本県'),
 ('jp_city', 'jp-46', '46201'): ('jp_city', 'jp-46', '46201'),
 ('jp_city', 'jp-46', '46203'): ('jp_city', 'jp-46', '46203'),
 ('jp_city', 'jp-46', '46204'): ('jp_city', 'jp-46', '46204'),
 ('jp_city', 'jp-46', '46210'): ('jp_city', 'jp-46', '46210'),
 ('jp_city', 'jp-46', '46215'): ('jp_city', 'jp-46', '46215'),
 ('jp_city', 'jp-46', '46216'): ('jp_city', 'jp-46', '46216'),
 ('jp_city', 'jp-46', '46218'): ('jp_city', 'jp-46', '46218'),
 ('jp_city', 'jp-46', '46220'): ('jp_city', 'jp-46', '46220'),
 ('jp_city', 'jp-46', '46221'): ('jp_city', 'jp-46', '46221'),
 ('jp_city', 'jp-46', '46222'): ('jp_city', 'jp-46', '46222'),
 ('jp_city', 'jp-46', '46223'): ('jp_city', 'jp-46', '46223'),
 ('jp_city', 'jp-46', '46224'): ('jp_city', 'jp-46', '46224'),
 ('jp_city', 'jp-46', '46225'): ('jp_city', 'jp-46', '46225'),
 ('jp_city', 'jp-46', '46468'): ('jp_city', 'jp-46', '46468'),
 ('jp_city', 'jp-46', '46482'): ('jp_city', 'jp-46', '46482'),
 ('jp_city', 'jp-46', '46533'): ('jp_city', 'jp-46', '46533'),
 ('jp_city', 'jp-46', '46535'): ('jp_city', 'jp-46', '46535'),
 ('jp_city', 'jp-46', 'unknown'): ('jp_city', 'jp-46', 'unknown'),
 ('jp_city', 'jp-47', '47201'): ('jp_city', 'jp-47', '47201'),
 ('jp_city', 'jp-47', '47205'): ('jp_city', 'jp-47', '47205'),
 ('jp_city', 'jp-47', '47207'): ('jp_city', 'jp-47', '47207'),
 ('jp_city', 'jp-47', '47208'): ('jp_city', 'jp-47', '47208'),
 ('jp_city', 'jp-47', '47209'): ('jp_city', 'jp-47', '47209'),
 ('jp_city', 'jp-47', '47210'): ('jp_city', 'jp-47', '47210'),
 ('jp_city', 'jp-47', '47211'): ('jp_city', 'jp-47', '47211'),
 ('jp_city', 'jp-47', '47212'): ('jp_city', 'jp-47', '47212'),
 ('jp_city', 'jp-47', '47213'): ('jp_city', 'jp-47', '47213'),
 ('jp_city', 'jp-47', '47214'): ('jp_city', 'jp-47', '47214'),
 ('jp_city', 'jp-47', '47215'): ('jp_city', 'jp-47', '47215'),
 ('jp_city', 'jp-47', 'chiba-shi wakaba-ku'): ('jp_city', 'jp-47', 'chiba-shi wakaba-ku'),
 ('jp_city', 'jp-47', 'unknown'): ('jp_city', 'jp-47', 'unknown'),
 ('jp_city', 'jp-47', '確認中'): ('jp_city', 'jp-47', '確認中'),
 ('jp_city', 'other', 'unknown'): ('jp_city', 'other', 'unknown'),
 ('jp_city', 'unknown', 'other'): ('jp_city', 'unknown', 'other'),
 ('jp_city', 'unknown', 'unknown'): ('jp_city', 'unknown', 'unknown'),
 (17, 'jp-13', 'niigata-shi konan-ku'): (17, 'jp-15', '15104')}


if __name__ == '__main__':
    from pprint import pprint
    inst = JPCityData()
    datapoints = inst.get_datapoints()
    #pprint(datapoints)
    #inst.sdpf.print_mappings()
