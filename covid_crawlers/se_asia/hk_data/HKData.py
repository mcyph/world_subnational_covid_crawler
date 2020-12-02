# https://chp-dashboard.geodata.gov.hk/covid-19/T2_Data.json
import json
from collections import Counter

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


class HKData(URLBase):
    SOURCE_URL = 'https://chp-dashboard.geodata.gov.hk/covid-19/en.html'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'hk_dash'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'hk' / 'data',
             urls_dict={
                 'T2_Data.json': URL(
                     'https://chp-dashboard.geodata.gov.hk/covid-19/T2_Data.json',
                     static_file=False
                 ),
                 'cases.json': URL(
                     """https://services8.arcgis.com/PXQv9PaDJHzt8rp0/arcgis/rest/services/Merge_Display_0227_View/FeatureServer/0/query?f=json&where=(Status = 'Existing' OR Status = 'History') AND (Case_no_ <> -1) AND (Status = 'History')&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=38&geometry={"xmin":12699553.627367351,"ymin":2543824.3013545386,"xmax":12719121.506608326,"ymax":2563392.180595517,"spatialReference":{"wkid":102100}}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile""".replace(' ', '%20'),
                     static_file=False
                 )
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('hk_district', 'hk', '黄大仙'): ('hk_district', 'hk', '黃大仙'),
                ('hk_district', 'hk', '荃灣區'): ('hk_district', 'hk', '荃灣'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_district_datapoints())
        return r

    def _get_district_datapoints(self):
        # "features":[{"attributes":{
        # "ObjectId":3178,"Case_no_":967,"Date_of_laboratory_confirmation":"09/04/2020",
        # "Date_of_onset":"25/03/2020","Gender":"M","Age":21,
        # "Name_of_hospital_admitted":"Queen Elizabeth Hospital",
        # "Hospitalised_Discharged_Decease":"Discharged",
        # "HK_Non_HK_resident":"HK resident",
        # "Case_classification":"Imported case",
        # "Confirmed_Probable":"Confirmed",
        # "個案編號":967,"實驗室確診報告日期":"09/04/2020",
        # "發病日期":"25/03/2020","性別":"男",
        # "年齡":21,"入住醫院名稱":"伊利沙伯醫院",
        # "住院_出院_死亡":"出院","香港_非香港居民":"香港居民",
        # "個案分類":"輸入個案","確定_懷疑":"確診",
        # "BuildingName":"Queen Elizabeth Hospital",
        # "District":"Yau Tsim Mong",
        # "Related_confirmed_cases":"967",
        # "地區":"油尖旺",
        # "大廈名單":"伊利沙伯醫院",
        # "相關確診個案":"967",
        # "Status":"History",
        # "DateoftheLastCase":1586361600000,
        # "最後有個案在出現病徵期間逗留的日期":1586361600000,
        # "Status_Chi":"過去"},
        # "geometry":{"x":12709863,"y":2548672}},

        # Case classification ->
        # * Epidemiologically linked with imported case
        # * Epidemiologically linked with local case
        # * Imported case
        # * Local case
        # * Possibly local case

        # Hospitalised_Discharged_Decease ->
        # * Discharged
        # * Deceased
        # * Hospitalised

        # Confirmed_Probable ->
        # * Confirmed
        # * Probable

        r = self.sdpf()
        path = self.get_current_revision_dir() / 'cases.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
        except UnicodeDecodeError:
            import brotli
            with open(path, 'rb') as f:
                data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

        by_total = Counter()
        by_confirmed = Counter()
        by_probable = Counter()

        by_age = Counter()
        by_gender = Counter()
        by_district = Counter()
        by_source_of_infection = Counter()

        gender_map = {
            'M': DataTypes.TOTAL_MALE,
            'F': DataTypes.TOTAL_FEMALE
        }

        for feature in data['features']:
            item = feature['attributes']
            date = self.convert_date(item['Date_of_laboratory_confirmation'])
            agerange = self._age_to_range(item['Age'])

            by_total[date] += 1
            by_district[date, item['地區'].replace(' ', '').strip() or 'unknown'] += 1
            by_age[date, agerange] += 1
            by_gender[date, gender_map[item['Gender']]] += 1

        cumulative = 0
        for date, value in sorted(by_total.items()):
            cumulative += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='HK',
                datatype=DataTypes.TOTAL,
                value=cumulative,
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (date, agerange), value in sorted(by_age.items()):
            cumulative[agerange] += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='HK',
                datatype=DataTypes.TOTAL,
                value=cumulative[agerange],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[gender] += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='HK',
                datatype=gender,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (date, district), value in sorted(by_district.items()):
            cumulative[district] += value
            #print(district)

            r.append(
                region_schema=Schemas.HK_DISTRICT,
                region_parent='HK',
                region_child=district,
                datatype=DataTypes.TOTAL,
                value=cumulative[district],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return r

    def _age_to_range(self, age):
        age = int(age)
        for x in range(0, 120, 10):
            if x <= age <= x+9:
                return f'{x}-{x+9}'
        raise Exception(age)


if __name__ == '__main__':
    from pprint import pprint
    pprint(HKData().get_datapoints())

