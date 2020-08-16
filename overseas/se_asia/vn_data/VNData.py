import ssl
import json
import gzip
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1, DT_TESTS_TOTAL,
    DT_TOTAL, DT_STATUS_RECOVERED,
    DT_STATUS_DEATHS, DT_STATUS_ACTIVE
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


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
""".strip().split('\n')])


class VNData(URLBase):
    SOURCE_URL = 'https://ncov.moh.gov.vn/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'vn_moh'

    def __init__(self):
        # Disable ssl, only for this crawler!
        old_create = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context

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
        r = []
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

            # There are quite a few more stats e.g. lower than governorate level etc =====================================

            for region, total, active, recovery, death in pq(html('#sailorTable')[0])('tbody tr'):
                region = pq(region).text().strip()
                if not region:
                    continue  # FIXME!
                region = place_map[region]
                death = int(pq(death).text().strip())
                recovery = int(pq(recovery).text().strip())
                active = int(pq(active).text().strip())
                total = int(pq(total).text().strip())

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='VN',
                    region_child=region,
                    datatype=DT_TOTAL,
                    value=int(total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='VN',
                    region_child=region,
                    datatype=DT_STATUS_ACTIVE,
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='VN',
                    region_child=region,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(recovery),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='VN',
                    region_child=region,
                    datatype=DT_STATUS_DEATHS,
                    value=int(death),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(VNData().get_datapoints())
