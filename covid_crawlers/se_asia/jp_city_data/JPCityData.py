import csv
from collections import Counter

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.world_geodata.LabelsToRegionChild import LabelsToRegionChild
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_DEV

from covid_19_au_grab.covid_crawlers.se_asia.jp_city_data.JPCityDataCityMap import city_map
from covid_19_au_grab.covid_crawlers.se_asia.jp_city_data.JPCityDataBikouMap import bikou_map


# https://stopcovid19.metro.tokyo.lg.jp/
# https://github.com/tokyo-metropolitan-gov/covid19/blob/development/FORKED_SITES.md


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

        f = self.get_file('jg-jpn.csv', include_revision=True, encoding='utf-8-sig')

        num_city = 0
        num_kyoto = 0

        for item in csv.DictReader(f):
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
                    '⼥性': DataTypes.TOTAL_FEMALE,
                    '不明': None,
                    '惰性': DataTypes.TOTAL_MALE,  # Pretty sure this is a typo
                    '未満 女性': DataTypes.TOTAL_FEMALE,
                    '女児': DataTypes.TOTAL_FEMALE,
                    '男児': DataTypes.TOTAL_MALE,
                    '': None,
                    None: None,
                }[item['性別']]

                date_diagnosed = self.convert_date(item['確定日'], formats=('%m/%d/%Y',))

                # May as well use English prefecture names to and allow the system to
                # auto-translate to ISO-3166-2 later
                region_parent = item['居住都道府県']
                if not region_parent:
                    assert item['居住都道府県コード'] == '#N/A', item

                if (
                    (
                        # region_parent == '奈良県' or
                        # region_parent == '和歌山県' or
                        # region_parent == '大阪府'
                        region_parent.startswith('京都') or
                        region_parent in ('福岡県', '沖縄県', '愛媛県', '神奈川県', '兵庫県', '愛知県', '高知県',
                                          '山梨県', '栃木県', '三重県', '長野県', '熊本県', '青森県', '茨城県',
                                          '静岡県', '福島県', '徳島県', '群馬県', '秋田県',)
                    )
                    and item['備考']
                    and not item['居住市区町村']
                ):
                    print(region_parent, item)
                    region_child = bikou_map[item['備考']]

                else:
                    if item['備考'] and not item['居住市区町村']:
                        print("BIKOU!!!", region_parent, item['備考'], item)

                    # e.g. 中富良野町 will be different to the English 'Release' field
                    region_child = (
                        item.get('居住市区町村') or
                        region_parent.replace('市', '県') or
                        'unknown'  # Japanese only
                    )

                region_parent = region_parent.replace('市', '県')  # HACK!
                if region_parent in ('中華人民共和国', 'アイルランド', 'スペイン', 'ジンバブエ共和国',
                                     '南アフリカ共和国', 'フィリピン', 'アメリカ', 'カナダ', 'イギリス',
                                     'フランス', 'インドネシア', 'アフガニスタン',):
                    region_parent = 'other'
                elif region_parent in ('不明',):
                    region_parent = 'unknown'

                region_parent = self._labels_to_region_child.get_by_label(Schemas.ADMIN_1, 'JP', region_parent, default=region_parent)
                region_child = city_map.get(region_child.strip().lower(), region_child)
                region_child = self._labels_to_region_child.get_by_label(Schemas.JP_CITY, region_parent, region_child, default=region_child)

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

                if item.get('居住市区町村') and region_parent == 'jp-27':
                    num_city += 1

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

        return r


if __name__ == '__main__':
    inst = JPCityData()
    datapoints = inst.get_datapoints()
    #pprint(datapoints)
    #inst.sdpf.print_mappings()
