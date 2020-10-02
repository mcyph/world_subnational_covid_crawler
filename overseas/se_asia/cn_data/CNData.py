import json
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT, MODE_DEV
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir


# http://www.geodata.cn/sari2020/web/yiqingMap.html
# http://www.geodata.cn/sari2020/api/ncpLastData?code=510000&jsonpCallback=dojo_request_script_callbacks.dojo_request_script0


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


class CNData(URLBase):
    SOURCE_URL = 'http://www.geodata.cn/sari2020/web/yiqingMap.html'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'cn_geodata'

    def __init__(self):
        urls_dict = {}
        for province_dict in provinces:
            url = f'http://www.geodata.cn/sari2020/api/ncpLastData?code={province_dict["value"]}' \
                  f'&jsonpCallback=dojo_request_script_callbacks.dojo_request_script0'
            urls_dict[province_dict["value"]+".json"] = URL(url, static_file=False)

        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'cn' / 'data',
             urls_dict=urls_dict,
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

        for date in listdir(get_overseas_dir() / 'cn' / 'data'):
            for province_dict in provinces:
                if province_dict["value"] in ('86', '88', '710000', '810000'):
                    continue

                path = get_overseas_dir() / 'cn' / 'data' / date / f'{province_dict["value"]}.json'
                with open(path, 'r', encoding='utf-8') as f:
                    json_data = f.read()
                    json_data = json_data.replace("dojo_request_script_callbacks.dojo_request_script0(", "")
                    json_data = json_data.rstrip().rstrip(");")
                    data = json.loads(json_data)

                # {"author":"geodata","city":"河南省","code":"410000","codeis":"410000",
                # "country":"中国","createAt":1599211044000,"day":"2020-09-03",
                # "id":"43030b8e44d35d00af7a25deb55524a4",
                # "nconfirm":0,"ndead":0,"nheal":0,"nsuspect":0,"params":{},
                # "province":"河南","publishAt":1599148740000,
                # "tconfirm":1276,"tdead":22,"theal":1254,"tsuspect":0,
                # "updateAt":1599211044000}

                for item in data:
                    i_date = self.convert_date(item['day'])

                    r.append(
                        region_schema=Schemas.CN_CITY,
                        region_parent='CN',#item['province'],
                        region_child=item['city'],
                        datatype=DataTypes.TOTAL,
                        value=int(item[f'tconfirm'])+int(item[f'tsuspect']),
                        date_updated=i_date,
                        source_url=self.SOURCE_URL
                    )
                    r.append(
                        region_schema=Schemas.CN_CITY,
                        region_parent='CN',#item['province'],
                        region_child=item['city'],
                        datatype=DataTypes.NEW,
                        value=int(item[f'nconfirm'])+int(item[f'nsuspect']),
                        date_updated=i_date,
                        source_url=self.SOURCE_URL
                    )

                    for total_datatype, new_datatype, key_suffix in (
                        (DataTypes.CONFIRMED, DataTypes.CONFIRMED_NEW, 'confirm'),
                        (DataTypes.PROBABLE, DataTypes.PROBABLE_NEW, 'suspect'),
                        (DataTypes.STATUS_RECOVERED, DataTypes.STATUS_RECOVERED_NEW, 'heal'),
                        (DataTypes.STATUS_DEATHS, DataTypes.STATUS_DEATHS_NEW, 'dead'),
                    ):
                        r.append(
                            region_schema=Schemas.CN_CITY,
                            region_parent='CN',#item['province'],
                            region_child=item['city'],
                            datatype=total_datatype,
                            value=int(item[f'n{key_suffix}']),
                            date_updated=i_date,
                            source_url=self.SOURCE_URL
                        )
                        r.append(
                            region_schema=Schemas.CN_CITY,
                            region_parent='CN',#item['province'],
                            region_child=item['city'],
                            datatype=new_datatype,
                            value=int(item[f't{key_suffix}']),
                            date_updated=i_date,
                            source_url=self.SOURCE_URL
                        )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(CNData().get_datapoints())
