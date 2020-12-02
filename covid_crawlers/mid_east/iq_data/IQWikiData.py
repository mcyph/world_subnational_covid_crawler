from os import listdir
from pyquery import PyQuery as pq

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URLBase, URL
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


class IQWikiData(URLBase):
    SOURCE_URL = 'https://ar.wikipedia.org/wiki/%D8%AC%D8%A7%D8%A6%D8%AD%D8%A9_%D9%81%D9%8A%D8%B1%D9%88%D8%B3_%D9%83%D9%88%D8%B1%D9%88%D9%86%D8%A7_%D9%81%D9%8A_%D8%A7%D9%84%D8%B9%D8%B1%D8%A7%D9%82_2020'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'iq_wikipedia'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'iq' / 'wikidata',
            urls_dict={
                'covid19_in_iraq.html': URL(self.SOURCE_URL, static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = self.sdpf()

        for dir_ in listdir(self.output_dir):
            with open(self.output_dir / dir_ / 'covid19_in_iraq.html', 'r', encoding='utf-8') as f:
                html = f.read()

            datatype_mappings = {
                'المجموع': DataTypes.TOTAL,
                'الحالات المؤكدة': DataTypes.TOTAL,
                'حالات الوفاة': DataTypes.STATUS_DEATHS,
                'الحالات المعافاة': DataTypes.STATUS_RECOVERED,
            }

            table = pq(html)('table:contains("المحافظة")')[0]
            datatype_headers = [
                datatype_mappings[pq(i).text().strip()]
                for i in pq(pq(table)('tbody tr')[0])('th')[1:]
            ]
            region_trs = pq(table)('tbody tr')

            for region_tr in region_trs:
                if region_tr[0].tag.lower() != 'td':
                    continue

                vals = {}
                region = pq(region_tr[0]).text().strip()

                for datatype, value in zip(datatype_headers, region_tr[1:]):
                    if datatype is None:
                        continue

                    region_map = {
                        'بغداد': 'IQ-BG',
                        'البصرة': 'IQ-BA',
                        'الديوانية': 'IQ-QA',
                        'بابل': 'IQ-BB',
                        'ديالى': 'IQ-DI',
                        'المثنى': 'IQ-MU',
                        'الأنبار': 'IQ-AN',
                    }

                    value = int(pq(value).text().replace(',', ''))
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='IQ',
                        region_child=region_map.get(region, region),
                        datatype=datatype,
                        value=value,
                        date_updated=dir_, # FIXME!!!
                        source_url=self.SOURCE_URL
                    )
                    vals[datatype] = value

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(IQWikiData().get_datapoints())
