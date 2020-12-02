import json
from os import listdir
from os.path import exists

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir

place_map = {
    'Иссык-Куль': 'KG-Y',
    'Ысык-Көл': 'KG-Y',
    'Джалал-Абад': 'KG-J',
    'Жалал-Абад': 'KG-J',
    'Талас': 'KG-T',
    'Баткен': 'KG-B',
    'Ош': 'KG-O',
    'Чуй': 'KG-C',
    'Чүй': 'KG-C',
    'Нарын': 'KG-N',
    'г. Бишкек': 'KG-GB',
    'Бишкек шаары': 'KG-GB',
    'г. Ош': 'KG-GO',
    'Ош шаары': 'KG-GO',
}


class KGData(URLBase):
    SOURCE_URL = 'https://covid.kg/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'kg_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'kg' / 'data',
            urls_dict={
                'kz_corona.html': URL('https://covid.kg/',
                                      static_file=False),
                'kz_corona_map.html': URL('https://covid.kg/map',
                                          static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'kg', 'kg-go'): ('MERGE', 'admin_1', 'kg', 'kg-o'),
                ('admin_1', 'kg', 'kg-o'): ('MERGE', 'admin_1', 'kg', 'kg-o'),
            },
            mode=MODE_STRICT
        )
        #self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        out = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()

            path = f'{base_dir}/{date}/kz_corona_map.html'
            if not exists(path):
                path = f'{base_dir}/{date}/kz_corona.html'

            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            if not 'data: ' in html or not 'name: ' in html:
                continue

            # TODO: Add other national stats from this page!
            chart_js = html.split(' options = {')[-1]
            dates = json.loads(
                chart_js.split('categories: ')[1]
                    .split('\n')[0]
                    .strip()
                    .strip(',')
            )

            for data in chart_js.split('data: ')[1:]:
                data, region = data.split('name: ')
                data = json.loads(data.strip().strip(','))
                region = region.split('\n')[0].strip().strip('"\', ')
                region = place_map[region.strip()]

                for date, i_data in zip(dates, data):
                    date = self.convert_date(date)
                    if i_data is None:
                        continue

                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='KG',
                        region_child=region,
                        datatype=DataTypes.TOTAL,
                        value=int(i_data),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

            out.extend(r)

        return out


if __name__ == '__main__':
    from pprint import pprint
    pprint(KGData().get_datapoints())
