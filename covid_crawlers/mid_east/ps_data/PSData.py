from pyquery import PyQuery as pq
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir

place_map = {
    'قطاع غزة': 'PS-GZA', #'Gaza strip',
    'الخليل': 'PS-HBN', #'Hebron',
    'قلقيلية': 'PS-QQA', #'Qalqilya',
    'ضواحي القدس': 'PS-JEM', #'The outskirts of Jerusalem',
    'مدينة القدس': None, #'PS-JEM', # 'City of Jerusalem' TODO: FIGURE OUT WHAT TO DO ABOUT THIS. This value wasn't supplied prior to 21st June, and isn't displayed on their map either
    'رام الله والبيرة': 'PS-RBH', #'Ramallah and Al-Bireh',
    'بيت لحم': 'PS-BTH', #'Bethlehem',
    'نابلس': 'PS-NBS', #'Nablus',
    'طولكرم': 'PS-TKM', #'Tulkarm',
    'جنين': 'PS-JEN', #'Jenin',
    'أريحا': 'PS-JRH', #'Jericho',
    'سلفيت': 'PS-SLT', #'Salfit',
    'طوباس': 'PS-TBS', #'Tubas',
    'اريحا': 'PS-JRH', # 'Jericho'
}


class PSData(URLBase):
    SOURCE_URL = 'https://www.corona.ps/details'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ps_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'ps' / 'data',
            urls_dict={
                'ps_corona.html': URL('https://www.corona.ps/details',
                                      static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in self.iter_nonempty_dirs(base_dir):
            path = f'{base_dir}/{date}/ps_corona.html'
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    html = f.read()
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    html = brotli.decompress(f.read()).decode('utf-8')

            html = pq(html, parser='html')

            # There are quite a few more stats e.g. lower than governorate level etc =====================================

            for elements in html('#Table2 tbody tr'):
                try:
                    governorate, total, active, recovery, death = elements
                    new = None
                except ValueError:
                    governorate, total, new, active, recovery, death = elements
                    new = int(pq(new).text().strip())

                governorate = place_map[pq(governorate).text().strip()]
                death = int(pq(death).text().replace(',', '').strip())
                recovery = int(pq(recovery).text().replace(',', '').strip())
                active = int(pq(active).text().replace(',', '').strip())
                total = int(pq(total).text().replace(',', '').strip())

                if governorate is None:
                    continue

                if new is not None:
                    r.append(
                        region_schema=Schemas.PS_PROVINCE,
                        region_parent='PS',
                        region_child=governorate,
                        datatype=DataTypes.NEW,
                        value=int(new),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                r.append(
                    region_schema=Schemas.PS_PROVINCE,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DataTypes.TOTAL,
                    value=int(total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.PS_PROVINCE,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.PS_PROVINCE,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(recovery),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.PS_PROVINCE,
                    region_parent='PS',
                    region_child=governorate,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(death),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(PSData().get_datapoints())
