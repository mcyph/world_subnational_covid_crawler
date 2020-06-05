import csv
from collections import Counter
from covid_19_au_grab.overseas.jp_city_data.extract_from_tokyo_pdf import (
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
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0,
    SCHEMA_ADMIN_1,
    SCHEMA_JP_CITY,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


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

    def update(self, force=False):
        ExtractFromTokyoPDF().download_pdfs(only_most_recent=True)
        URLBase.update(self, force)

    def get_datapoints(self):
        r = []
        r.extend(self._get_from_json())
        r.extend(ExtractFromTokyoPDF().get_from_pdfs())
        return r

    def _get_from_json(self):
        r = []

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

        #for item in json.loads(text)['features']:

        for item in csv.DictReader(f):
            print(item)
            #item = item['properties']

            if not item:
                continue
            elif not item['確定日']:
                continue  # WARNING!

            if item.get('年代') == '0-10':
                agerange = '0-9'
            elif item.get('年代') in ('不明', '', None):
                agerange = 'Unknown'
            else:
                agerange = (
                    str(int(item['年代'].strip('代'))) +
                    '-' +
                    str(int(item['年代'].strip('代')) + 9)
                )

            gender = {'男性': DT_TOTAL_MALE,
                      '男性\xa0': DT_TOTAL_MALE,
                      '女性\xa0': DT_TOTAL_FEMALE,
                      '女性': DT_TOTAL_FEMALE,
                      '不明': None,
                      '惰性': DT_TOTAL_MALE,  # Pretty sure this is a typo
                      '': None,
                      None: None}[item['性別']]

            #date_of_onset = self.convert_date(item['発症日'], formats=('%m/%d/%Y',))
            date_diagnosed = self.convert_date(item['確定日'], formats=('%m/%d/%Y',))   # TODO: Should we be recording this number??? ================
            #date_diagnosed = datetime.datetime.fromtimestamp(item['確定日']/1000).strftime('%Y_%m_%d')
            #diagnosed_in = item['Hospital Pref']
            #resident_of = item['Residential Pref']
            resident_of = item.get('Residential Pref') or item['居住都道府県']
            # e.g. 中富良野町 will be different to the English 'Release' field
            #announced_in = item['Release']
            city = item.get('居住市区町村') or 'Unknown'  # Japanese only
            #source = item['ソース'] or item['ソース2'] or item['ソース3'] or 'https://covid19.wlaboratory.com'

            # Maybe it's worth adding status info, but it can be vague e.g. "退院または死亡"
            # Occupation info is also present in many cases.

            by_date[date_diagnosed] += 1
            by_age[date_diagnosed, agerange] += 1
            by_prefecture[date_diagnosed, resident_of] += 1

            if gender is not None:
                by_gender[date_diagnosed, gender] += 1
                by_gender_age[date_diagnosed, gender, agerange] += 1
                by_prefecture_gender[date_diagnosed, resident_of, gender] += 1
                by_prefecture_age_gender[date_diagnosed, resident_of, agerange, gender] += 1

            by_prefecture_age[date_diagnosed, resident_of, agerange] += 1

            if resident_of == 'Tokyo' and city == 'Unknown':
                # Will add city-level data
                continue
            else:
                by_city[date_diagnosed, resident_of, city] += 1

                if gender is not None:
                    by_city_gender[date_diagnosed, resident_of, city, gender] += 1
                    by_city_age_gender[date_diagnosed, resident_of, city, agerange, gender] += 1

        cumulative = Counter()
        for date, value in sorted(by_date.items()):
            cumulative[date] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='Japan',
                datatype=DT_TOTAL,
                value=cumulative[date],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, agerange), value in sorted(by_age.items()):
            cumulative[date, agerange] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='Japan',
                datatype=DT_TOTAL,
                agerange=agerange,
                value=cumulative[date, agerange],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture), value in sorted(by_prefecture.items()):
            cumulative[date, prefecture] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=DT_TOTAL,
                value=cumulative[date, prefecture],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[date, gender] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='Japan',
                datatype=gender,
                value=cumulative[date, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, gender, agerange), value in sorted(by_gender_age.items()):
            cumulative[date, gender, agerange] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_0,
                region_child='Japan',
                datatype=gender,
                agerange=agerange,
                value=cumulative[date, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture, gender), value in sorted(by_prefecture_gender.items()):
            cumulative[date, prefecture, gender] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=gender,
                value=cumulative[date, prefecture, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture, agerange), value in sorted(by_prefecture_age.items()):
            cumulative[date, prefecture, agerange] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=DT_TOTAL,
                agerange=agerange,
                value=cumulative[date, prefecture, agerange],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture, agerange, gender), value in sorted(by_prefecture_age_gender.items()):
            cumulative[date, prefecture, agerange, gender] += value

            r.append(DataPoint(
                region_schema=SCHEMA_ADMIN_1,
                region_parent='Japan',
                region_child=prefecture,
                datatype=gender,
                agerange=agerange,
                value=cumulative[date, prefecture, agerange, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture, city), value in sorted(by_city.items()):
            cumulative[date, prefecture, city] += value

            r.append(DataPoint(
                region_schema=SCHEMA_JP_CITY,
                region_parent=prefecture,
                region_child=city,
                datatype=DT_TOTAL,
                value=cumulative[date, prefecture, city],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture, city, gender), value in sorted(by_city_gender.items()):
            cumulative[date, prefecture, city, gender] += value

            r.append(DataPoint(
                region_schema=SCHEMA_JP_CITY,
                region_parent=prefecture,
                region_child=city,
                datatype=gender,
                value=cumulative[date, prefecture, city, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        cumulative = Counter()
        for (date, prefecture, city, agerange, gender), value in sorted(by_city_age_gender.items()):
            cumulative[date, prefecture, city, agerange, gender] += value

            r.append(DataPoint(
                region_schema=SCHEMA_JP_CITY,
                region_parent=prefecture,
                region_child=city,
                datatype=gender,
                agerange=agerange,
                value=cumulative[date, prefecture, city, agerange, gender],
                date_updated=date,
                source_url=self.SOURCE_URL,  # FIXME!!
            ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(JPCityData().get_datapoints())
