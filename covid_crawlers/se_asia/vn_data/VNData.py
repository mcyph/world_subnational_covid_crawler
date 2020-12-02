import ssl
import json
import gzip
from pyquery import PyQuery as pq
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir

place_map = dict([i.split('\t')[::-1] for i in """
VN-44	An Giang
VN-43	Bà Rịa - Vũng Tàu
VN-54	Bắc Giang
VN-53	Bắc Kạn
VN-55	Bạc Liêu
VN-56	Bắc Ninh
VN-50	Bến Tre
VN-31	Bình Định
VN-57	Bình Dương
VN-58	Bình Phước
VN-40	Bình Thuận
VN-59	Cà Mau
VN-04	Cao Bằng
VN-33	Đắk Lắk
VN-72	Đắk Nông
VN-71	Điện Biên
VN-39	Đồng Nai
VN-45	Đồng Tháp
VN-30	Gia Lai
VN-03	Hà Giang
VN-63	Hà Nam
VN-23	Hà Tĩnh
VN-61	Hải Dương
VN-73	Hậu Giang
VN-14	Hòa Bình
VN-66	Hưng Yên
VN-34	Khánh Hòa
VN-47	Kiến Giang
VN-47	Kiên Giang
VN-28	Kon Tum
VN-01	Lai Châu
VN-35	Lâm Đồng
VN-09	Lạng Sơn
VN-02	Lào Cai
VN-41	Long An
VN-67	Nam Định
VN-22	Nghệ An
VN-18	Ninh Bình
VN-36	Ninh Thuận
VN-68	Phú Thọ
VN-32	Phú Yên
VN-24	Quảng Bình
VN-27	Quảng Nam
VN-29	Quảng Ngãi
VN-13	Quảng Ninh
VN-25	Quảng Trị
VN-52	Sóc Trăng
VN-05	Sơn La
VN-37	Tây Ninh
VN-20	Thái Bình
VN-69	Thái Nguyên
VN-21	Thanh Hóa
VN-26	Thừa Thiên Huế
VN-46	Tiền Giang
VN-51	Trà Vinh
VN-07	Tuyên Quang
VN-49	Vĩnh Long
VN-70	Vĩnh Phúc
VN-06	Yên Bái
VN-CT	Cần Thơ
VN-DN	Đà Nẵng
VN-HN	Hà Nội
VN-HP	Hai Phong
VN-SG	Hồ Chí Minh
VN-14	Hoà Bình
VN-62	Hải Phòng
""".strip().split('\n')])

highcharts_vn_ids = {
    '01': 'VN-HN',
    '02': 'VN-03',
    '04': 'VN-04',
    '08': 'VN-07',
    '10': 'VN-02',
    '11': 'VN-71',
    '12': 'VN-01',
    '14': 'VN-05',
    '15': 'VN-06',
    '17': 'VN-14',
    '19': 'VN-69',
    '20': 'VN-09',
    '22': 'VN-13',
    '24': 'VN-54',
    '25': 'VN-68',
    '26': 'VN-70',
    '27': 'VN-56',
    '30': 'VN-61',
    '31': 'VN-HP',
    '33': 'VN-',
    '34': 'VN-20',
    '35': 'VN-63',
    '36': 'VN-67',
    '37': 'VN-18',
    '38': 'VN-21',
    '40': 'VN-22',
    '42': 'VN-23',
    '44': 'VN-24',
    '45': 'VN-25',
    '46': 'VN-26',
    '48': 'VN-DN',
    '49': 'VN-27',
    '51': 'VN-29',
    '52': 'VN-31',
    '54': 'VN-32',
    '56': 'VN-34',
    '58': 'VN-36',
    '60': 'VN-40',
    '62': 'VN-28',
    '64': 'VN-30',
    '66': 'VN-33',
    '67': 'VN-72',
    '68': 'VN-35',
    '70': 'VN-58',
    '72': 'VN-37',
    '74': 'VN-57',
    '77': 'VN-43',
    '79': 'VN-SG',
    '80': 'VN-41',
    '82': 'VN-46',
    '83': 'VN-50',
    '84': 'VN-51',
    '86': 'VN-49',
    '87': 'VN-45',
    '89': 'VN-44',
    '91': 'VN-47',
    '92': 'VN-CT',
    '93': 'VN-73',
    '94': 'VN-52',
    '95': 'VN-55',
    '96': 'VN-59',
    'hs01': 'VN-57',
    'truongsa': 'VN-57',
    'vn-307': 'VN-',
    'vn-331': 'VN-',
    'vn-3655': 'VN-'
}



class VNData(URLBase):
    SOURCE_URL = 'https://ncov.moh.gov.vn/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'vn_moh'

    def __init__(self):
        # Disable ssl, only for this crawler!
        old_create = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'vn', 'vn-62'): None,
            },
            mode=MODE_STRICT
        )

        try:
            URLBase.__init__(self,
                output_dir=get_overseas_dir() / 'vn' / 'data',
                urls_dict={
                    'corona.html': URL('https://ncov.moh.gov.vn/',
                                       static_file=False)
                }
            )
            self.update()
        finally:
            ssl._create_default_https_context = old_create

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/corona.html'
            with open(path, 'rb') as f:
                data = f.read()

                try:
                    data = gzip.decompress(data)
                except:
                    pass
                    #import traceback
                    #traceback.print_exc()

                data = data.decode('utf-8')
                html = pq(data, parser='html')

            if 'var data = [' in data:
                for item in json.loads('[%s]' % data.split('var data = [')[1].split('];')[0]):
                    if not item['hc-key'] in highcharts_vn_ids:
                        print("VN WARNING - HC-KEY NOT FOUND:", item)
                        continue

                    region_child = highcharts_vn_ids[item['hc-key']]
                    if region_child == 'VN-':
                        continue  # ???

                    for datatype, value in (
                        (DataTypes.TOTAL, item['socakhoi']),
                        (DataTypes.STATUS_ACTIVE, item['socadangdieutri']),
                        (DataTypes.STATUS_RECOVERED, item['socakhoi']-item['socadangdieutri']),
                        (DataTypes.STATUS_DEATHS, item['socatuvong'])
                    ):
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='VN',
                            region_child=region_child,
                            datatype=datatype,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )
            else:
                for region, total, active, recovery, death in pq(html('#sailorTable')[0])('tbody tr'):
                    region = pq(region).text().strip()
                    if not region:
                        continue  # FIXME!
                    region = place_map[region]
                    death = int(pq(death).text().strip())
                    recovery = int(pq(recovery).text().strip())
                    active = int(pq(active).text().strip())
                    total = int(pq(total).text().strip())

                    for datatype, value in (
                        (DataTypes.TOTAL, total),
                        (DataTypes.STATUS_ACTIVE, active),
                        (DataTypes.STATUS_RECOVERED, recovery),
                        (DataTypes.STATUS_DEATHS, death)
                    ):
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='VN',
                            region_child=region,
                            datatype=datatype,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(VNData().get_datapoints())
