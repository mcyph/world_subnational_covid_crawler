# https://github.com/kaz-ogiwara/covid19
import csv
import json

from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.overseas.GithubRepo import GithubRepo
from covid_19_au_grab.get_package_dir import get_overseas_dir


_prefectures = {
    '北海道': 'Hokkaido',
    '愛知県': 'Aichi',
    '東京都': 'Tokyo',
    '大阪府': 'Osaka',
    '兵庫県': 'Hyogo',
    '神奈川県': 'Kanagawa',
    '埼玉県': 'Saitama',
    '千葉県': 'Chiba',
    '京都府': 'Kyoto',
    '新潟県': 'Niigata',
    '和歌山県': 'Wakayama',
    '高知県': 'Kochi',
    '群馬県': 'Gunma',
    '熊本県': 'Kumamoto',
    '石川県': 'Ishikawa',
    '三重県': 'Mie',
    '福岡県': 'Fukuoka',
    '奈良県': 'Nara',
    '滋賀県': 'Shiga',
    '岐阜県': 'Gifu',
    '栃木県': 'Tochigi',
    '沖縄県': 'Okinawa',
    '長野県': 'Nagano',
    '静岡県': 'Shizuoka',
    '宮崎県': 'Miyazaki',
    '愛媛県': 'Ehime',
    '茨城県': 'Ibaraki',
    '山梨県': 'Yamanashi',
    '福島県': 'Fukushima',
    '福井県': 'Fukui',
    '秋田県': 'Akita',
    '宮城県': 'Miyagi',
    '大分県': 'Oita',
    '山口県': 'Yamaguchi',
    '広島県': 'Hiroshima',
    '香川県': 'Kagawa',
    '佐賀県': 'Saga',
    '青森県': 'Aomori',
    '岩手県': 'Iwate',
    '山形県': 'Yamagata',
    '富山県': 'Toyama',
    '鳥取県': 'Tottori',
    '島根県': 'Shimane',
    '岡山県': 'Okayama',
    '徳島県': 'Tokushima',
    '長崎県': 'Nagasaki',
    '鹿児島県': 'Kagoshima',
    '東京県': 'Tokyo',
    '京都県': 'Kyoto',
    '大阪県': 'Osaka',
}


def get_prefecture(s):
    return _prefectures.get(s) or _prefectures[s+'県']


class JPData(GithubRepo):
    SOURCE_URL = ''
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'jp_ministry_unofficial'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'jp' / 'covid19' / 'data',
                            github_url='https://github.com/kaz-ogiwara/covid19')
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        #r.extend(self._get_base_data())
        r.extend(self._get_prefectures_data())
        #r.extend(self._get_prefectures_2_data())
        #r.extend(self._get_summary_data())
        r.extend(self._get_demography_data())
        return r

    def _get_base_data(self):
        r = []
        # carriers, cases, discharged, deaths, pcrtested, pcrtests
        # demography[???],
        # prefectures-map,
        # prefectures-data
        return r

    def _get_prefectures_data(self):
        r = self.sdpf()
        with open(self.get_path_in_dir('prefectures.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                pad = lambda d: '%02d' % int(d)
                date = f'{item["year"]}_{pad(item["month"])}_{pad(item["date"])}'
                prefecture = get_prefecture(item['prefectureNameJ'])

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Japan',
                    region_child=prefecture,
                    datatype=DataTypes.TOTAL,
                    value=int(item["testedPositive"]),
                    date_updated=date,
                    source_url=self.github_url
                )

                if item['peopleTested']:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='Japan',
                        region_child=prefecture,
                        datatype=DataTypes.TESTS_TOTAL,
                        value=int(item['peopleTested']),
                        date_updated=date,
                        source_url=self.github_url
                    )

                #r.append(
                #    region_schema=Schemas.ADMIN_1,
                #    region_parent='Japan',
                #    region_child=prefecture,
                #    datatype=DataTypes.STATUS_HOSPITALIZED,
                #    value=int(item["患者数（2020年3月28日からは感染者数）"]),
                #    date_updated=date,
                #    source_url=self.github_url
                #)

                if item["discharged"].strip('-'):
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='Japan',
                        region_child=prefecture,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(item["discharged"]),
                        date_updated=date,
                        source_url=self.github_url
                    )

                if item['deaths'].strip('-'):
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='Japan',
                        region_child=prefecture,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(item["deaths"]),
                        date_updated=date,
                        source_url=self.github_url
                    )

        return r

    def _get_prefectures_2_data(self):
        r = self.sdpf()
        with open(self.get_path_in_dir('prefectures-2.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                pad = lambda d: '%02d' % int(d)
                date = f'{item["年"]}_{pad(item["月"])}_{pad(item["日"])}'
                prefecture = get_prefecture(item['都道府県'])

                # Not sure why PCR検査陽性者数 slightly differs
                # from the total 患者数 in "prefectures.csv"
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Japan',
                    region_child=prefecture,
                    datatype=DataTypes.TOTAL,
                    value=int(item["PCR検査陽性者数"]),
                    date_updated=date,
                    source_url=self.github_url
                )

                if item["PCR検査人数"].strip('-'):
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='Japan',
                        region_child=prefecture,
                        datatype=DataTypes.TESTS_TOTAL,
                        value=int(item["PCR検査人数"]),
                        date_updated=date,
                        source_url=self.github_url
                    )
        return r

    def _get_summary_data(self):
        r = []

        with open(self.get_path_in_dir('prefectures.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                pass  # TODO!
                #r.append(DataPoint(

                #)

        return r

    def _get_demography_data(self):
        r = self.sdpf()
        age_map = {
            '10歳未満': '0-9',
            '10代': '10-19',
            '20代': '20-29',
            '30代': '30-39',
            '40代': '40-49',
            '50代': '50-59',
            '60代': '60-69',
            '70代': '70-79',
            '80代以上': '80+',
            '不明': 'Unknown',
        }
        with open(self.get_path_in_dir('data.json'),
                  'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        #{"updated": {"last": {"ja": "最終更新：2020年5月13日", "en": "Last updated: 13 May 2020"}}
        date = self.convert_date(
            data['updated']['last']['en'].split(':')[-1].strip()
        )

        with open(self.get_path_in_dir('demography.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                print(item)

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='Japan',
                    agerange=age_map[item['age_group']],
                    datatype=DataTypes.TOTAL,
                    value=int(item["tested_positive"]),
                    date_updated=date,
                    source_url=self.github_url
                )

                if item.get("death"):
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Japan',
                        agerange=age_map[item['age_group']],
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(item["death"]),
                        date_updated=date,
                        source_url=self.github_url
                    )

                if item.get("重症"):
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Japan',
                        agerange=age_map[item['age_group']],
                        datatype=DataTypes.STATUS_ICU,
                        value=int(item["重症"]),  # WARNING: NOT REALLY ICU - but likely mostly is!! =====================
                        date_updated=date,
                        source_url=self.github_url
                    )

        return r

if __name__ == '__main__':
    from pprint import pprint
    pprint(JPData().get_datapoints())
