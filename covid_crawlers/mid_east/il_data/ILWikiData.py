from os import listdir
from pyquery import PyQuery as pq

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import (
    URLBase, URL
)
from covid_19_au_grab.covid_db.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import (
    get_overseas_dir
)


class ILWikiData(URLBase):
    SOURCE_URL = 'https://he.wikipedia.org/wiki/%D7%94%D7%AA%D7%A4%D7%A8%D7%A6%D7%95%D7%AA_%D7%A0%D7%92%D7%99%D7%A3_%D7%94%D7%A7%D7%95%D7%A8%D7%95%D7%A0%D7%94_%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'il_wikipedia'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'il' / 'wikidata',
            urls_dict={
                'covid19_in_israel.html': URL(self.SOURCE_URL, static_file=False)
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = []

        for dir_ in sorted(listdir(self.output_dir)):
            with open(self.output_dir / dir_ / 'covid19_in_israel.html', 'r', encoding='utf-8') as f:
                html = f.read()

            datatype_mappings = {
                'מקרי הדבקה': DataTypes.TOTAL,
                'ל-100,000 תושבים': None,
                'יישוב': 'LOCALITY',
                'מקרי מוות': DataTypes.STATUS_DEATHS,
                'הבריאו': DataTypes.STATUS_RECOVERED,
                'מקרים פעילים': DataTypes.STATUS_ACTIVE
            }

            table = pq(html)('div#corona2 table')  # Get from the longer table
            datatype_headers = [
                pq(i).text().split('[')[0].strip()
                for i in pq(table)('tbody tr th')[2:]
            ]
            region_trs = pq(table)('tbody tr')

            if datatype_headers[0] == 'יישוב':
                # HACK: There was a dot thing added sometime around 17 Aug
                region_trs = [region_tr[1:] for region_tr in region_trs]
                datatype_headers = datatype_headers[1:]

            for region_tr in region_trs:
                if not len(region_tr):
                    continue
                elif region_tr[0].tag.lower() != 'td':
                    continue

                vals = {}
                region = pq(region_tr[0]).text().strip()

                for datatype, value in zip(datatype_headers, region_tr[1:]):
                    datatype = datatype_mappings[pq(datatype).text().strip()]
                    if datatype is None:
                        continue

                    value = pq(value).text().replace(',', '').replace('?', '').strip()
                    if not value:
                        continue

                    value = int(value)
                    r.append(DataPoint(
                        region_schema=Schemas.IL_MUNICIPALITY,
                        region_parent='IL',
                        region_child=region,
                        datatype=datatype,
                        value=value,
                        date_updated=dir_, # FIXME!!!
                        source_url=self.SOURCE_URL
                    ))
                    vals[datatype] = value

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ILWikiData().get_datapoints())
