# https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5
# https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1

# {"ret":0,"data":
# "{\"lastUpdateTime\":\"2020-09-27 17:16:40\",\"chinaTotal\":
#   {\"confirm\":90972,\"heal\":85851,\"dead\":4746,\"nowConfirm\":375,\"suspect\":2,\"nowSevere\":3,\"importedCase\":2802,\"noInfect\":391},
# \"chinaAdd\":
#   {\"confirm\":15,\"heal\":24,\"dead\":0,\"nowConfirm\":-3,\"suspect\":0,\"nowSevere\":0,\"importedCase\":14,\"noInfect\":26},
# \"isShowAdd\":true,
# \"showAddSwitch\":{\"all\":true,\"confirm\":true,\"suspect\":true,\"dead\":true,\"heal\":true,\"nowConfirm\":true,\"nowSevere\":true,\"importedCase\":true,\"noInfect\":true},
# \"areaTree\":[{\"name\":\"中国\",\"today\":{\"confirm\":15,\"isUpdated\":true},
# \"total\":{\"nowConfirm\":375,\"confirm\":90972,\"suspect\":2,\"dead\":4746,\"deadRate\":\"5.22\",\"showRate\":false,\"heal\":85851,\"healRate\":\"94.37\",\"showHeal\":true},
# \"children\":[{\"name\":\"香港\",\"today\":{\"confirm\":1,\"confirmCuts\":0,\"isUpdated\":true,\"tip\":\"\"},
# \"total\":{\"nowConfirm\":174,\"confirm\":5065,\"suspect\":0,\"dead\":105,\"deadRate\":\"2.07\",\"showRate\":false,\"heal\":4786,\"healRate\":\"94.49\",\"showHeal\":true},
# \"children\":[{\"name\":\"地区待确认\",\"today\":{\"confirm\":1,\"confirmCuts\":0,\"isUpdated\":true},
# \"total\":{\"nowConfirm\":174,\"confirm\":5065,\"suspect\":0,\"dead\":105,\"deadRate\":\"2.07\",\"showRate\":false,\"heal\":4786,\"healRate\":\"94.49\",\"showHeal\":true}}]},{\"name\":\"上海\",\"today\":{\"confirm\":1,\"confirmCuts\":0,\"isUpdated\":true,\"tip\":\"上海累计报告境外输入确诊病例640例。\"}


import json
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_DEV
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir


provinces = [
    {"value": "88", "label": "全球"},
    {"value": "86", "label": "中国"},
    {"value": "420000", "label": "湖北"},
    {"value": "440000", "label": "广东"},
    {"value": "410000", "label": "河南"},
    {"value": "330000", "label": "浙江"},
    {"value": "430000", "label": "湖南"},
    {"value": "340000", "label": "安徽"},
    {"value": "360000", "label": "江西"},
    {"value": "370000", "label": "山东"},
    {"value": "320000", "label": "江苏"},
    {"value": "500000", "label": "重庆"},
    {"value": "510000", "label": "四川"},
    {"value": "230000", "label": "黑龙江"},
    {"value": "110000", "label": "北京"},
    {"value": "310000", "label": "上海"},
    {"value": "130000", "label": "河北"},
    {"value": "350000", "label": "福建"},
    {"value": "450000", "label": "广西"},
    {"value": "610000", "label": "陕西"},
    {"value": "530000", "label": "云南"},
    {"value": "460000", "label": "海南"},
    {"value": "520000", "label": "贵州"},
    {"value": "120000", "label": "天津"},
    {"value": "140000", "label": "山西"},
    {"value": "210000", "label": "辽宁"},
    {"value": "220000", "label": "吉林"},
    {"value": "810000", "label": "香港"},
    {"value": "620000", "label": "甘肃"},
    {"value": "650000", "label": "新疆"},
    {"value": "150000", "label": "内蒙古"},
    {"value": "640000", "label": "宁夏"},
    {"value": "710000", "label": "台湾"},
    {"value": "630000", "label": "青海"},
    {"value": "820000", "label": "澳门"},
    {"value": "540000", "label": "西藏"},
]


class CNQQData(URLBase):
    SOURCE_URL = 'https://news.qq.com/zt2020/page/feiyan.htm'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'cn_qq'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'cn' / 'qqdata',
             urls_dict={
                 'data.json': URL('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5', static_file=False)
             },
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={},
            mode=MODE_DEV
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = self.sdpf()

        for date in self.iter_nonempty_dirs(self.output_dir):
            with open(self.output_dir / date / 'data.json', 'r', encoding='utf-8') as f:
                data = f.read()
                data = json.loads(data)
                assert data['ret'] == 0
                data = json.loads(data['data'])

            from pprint import pprint
            pprint(data)
            assert len(data['areaTree']) == 1

            for province_dict in data['areaTree'][0]['children']:
                # 'name': '海南',
                # 'today': {'confirm': 0,
                #           'confirmCuts': 0,
                #           'isUpdated': True,
                #           'tip': '海南省累计报告境外输入确诊病例2例。'},
                #           'total': {'confirm': 171,
                #                     'dead': 6,
                #                     'deadRate': '3.51',
                #                     'heal': 165,
                #                     'healRate': '96.49',
                #                     'nowConfirm': 0,
                #                     'showHeal': True,
                #                     'showRate': False,
                #                     'suspect': 0}},
                #                     {'children': [{'name': '境外输入',
                #                                    'today': {'confirm': 0,
                #                                              'confirmCuts': 0,
                #                                              'isUpdated': False},
                #                                    'total': {'confirm': 4,
                #                                              'dead': 0,
                #                                              'deadRate': '0.00',
                #                                              'heal': 4,
                #                                              'healRate': '100.00',
                #                                              'nowConfirm': 0,
                #                                              'showHeal': True,
                #                                              'showRate': False,
                #                                              'suspect': 0}},
                print("PROVINCE:", province_dict)

                for datatype, value in (
                    (DataTypes.NEW, province_dict['today']['confirm']),
                    (DataTypes.CONFIRMED, province_dict['total']['confirm']),
                    (DataTypes.PROBABLE, province_dict['total']['suspect']),
                    (DataTypes.TOTAL, province_dict['total']['confirm'] + province_dict['total']['suspect']),
                    (DataTypes.STATUS_DEATHS, province_dict['total']['dead']),
                    (DataTypes.STATUS_RECOVERED, province_dict['total']['suspect']),
                ):
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='CN',
                        region_child=province_dict['name'],
                        datatype=datatype,
                        value=value,
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                for city_dict in province_dict['children']:
                    print("CITY:", city_dict)

                    for datatype, value in (
                        (DataTypes.NEW, city_dict['today']['confirm']),
                        (DataTypes.CONFIRMED, city_dict['total']['confirm']),
                        (DataTypes.PROBABLE, city_dict['total']['suspect']),
                        (DataTypes.TOTAL, city_dict['total']['confirm'] + city_dict['total']['suspect']),
                        (DataTypes.STATUS_DEATHS, city_dict['total']['dead']),
                        (DataTypes.STATUS_RECOVERED, city_dict['total']['suspect']),
                    ):
                        r.append(
                            region_schema=Schemas.CN_CITY,
                            region_parent='CN',
                            region_child=city_dict['name'],
                            datatype=datatype,
                            value=value,
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

        return r


if __name__ == '__main__':
    from pprint import pprint
    datapoints = CNQQData().get_datapoints()
    #pprint(datapoints)
