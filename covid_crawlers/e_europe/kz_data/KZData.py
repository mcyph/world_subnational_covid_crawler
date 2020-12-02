from pyquery import PyQuery as pq
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir

place_map = {
    'Нұр-Сұлтан қаласы': 'KZ-AST',
    'Алматы қаласы': 'KZ-ALA',
    'Шымкент қаласы': 'KZ-SHY',
    'Ақмола облысы': 'KZ-AKM',
    'Ақтөбе облысы': 'KZ-AKT',
    'Алматы облысы': 'KZ-ALM',
    'Атырау облысы': 'KZ-ATY',
    'Шығыс Қазақстан облысы': 'KZ-VOS',
    'Жамбыл облысы': 'KZ-ZHA',
    'Батыс Қазақстан облысы': 'KZ-ZAP',
    'Қарағанды облысы': 'KZ-KAR',
    'Қостанай облысы': 'KZ-KUS',
    'Қызылорда облысы': 'KZ-KZY',
    'Маңғыстау облысы': 'KZ-MAN',
    'Павлодар облысы': 'KZ-PAV',
    'Солтүстік Қазақстан облысы': 'KZ-SEV',
    'Түркістан облысы': 'KZ-YUZ',
}


class KZData(URLBase):
    SOURCE_URL = 'https://www.coronavirus2020.kz/kz'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'kz_gov'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'kz' / 'data',
            urls_dict={
                'kz_corona.html': URL('https://www.coronavirus2020.kz/kz',
                                      static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'kz', 'kz-shy'): None,
                ('admin_1', 'kz', 'kz-alm'): None
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            #print(date)
            path = f'{base_dir}/{date}/kz_corona.html'
            with open(path, 'r', encoding='utf-8') as f:
                html = pq(f.read(), parser='html')

            def get_num_region(div):
                #print(pq(div).text())
                region, num = pq(div).text().replace(' - ', '–').split('–')
                region = place_map[region.strip()]
                # TODO: Add "new" values!!
                return int(num.split('(')[0].strip()), region

            for div in html('.last_info_covid_bl .city_cov')[0]:
                if div.tag != 'div':
                    continue

                value, region = get_num_region(div)
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KZ',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            for div in html('.red_line_covid_bl .city_cov')[0]:
                if div.tag != 'div':
                    continue

                value, region = get_num_region(div)
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KZ',
                    region_child=region,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            for div in html('.deaths_bl .city_cov')[0]:
                if div.tag != 'div':
                    continue

                value, region = get_num_region(div)
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='KZ',
                    region_child=region,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=value,
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(KZData().get_datapoints())
