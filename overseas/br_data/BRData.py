import csv

from covid_19_au_grab.state_news_releases.overseas.KaggleDataset import (
    KaggleDataset
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    SCHEMA_BR_CITY,
    DT_TOTAL,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class BRData(KaggleDataset):
    SOURCE_URL = 'https://www.kaggle.com/unanimad/corona-virus-brazil'
    SOURCE_LICENSE = 'CC0: Public Domain'

    GEO_DIR = 'br'
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        KaggleDataset.__init__(self,
             output_dir=get_overseas_dir() / 'br' / 'data',
             dataset='unanimad/corona-virus-brazil'
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_covid19())
        r.extend(self._get_covid19_cities())
        r.extend(self._get_covid19_macro())
        return r

    def _get_covid19(self):
        r = []

        # brazil_covid19.csv
        # date,region_child,state,cases,deaths
        # 2020-02-26,Sudeste,São Paulo,1,0
        # 2020-02-27,Sudeste,São Paulo,1,0
        # 2020-02-28,Sudeste,São Paulo,1,0

        with self.get_file('brazil_covid19.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Brazil',
                    region_child=item['state'],
                    datatype=DT_TOTAL,
                    value=int(item['cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Brazil',
                    region_child=item['state'],
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r

    def _get_covid19_cities(self):
        r = []

        # brazil_covid19_cities.csv
        # date,state,name,code,cases,deaths
        # 2020-03-28,Acre,Rio Branco,120040,25,0
        # 2020-03-28,Alagoas,Maceió,270430,13,0
        # 2020-03-28,Alagoas,Porto Real do Colégio,270750,1,0

        with self.get_file('brazil_covid19_cities.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_schema=SCHEMA_BR_CITY,
                    region_parent=item['state'],
                    region_child=item['name'],
                    datatype=DT_TOTAL,
                    value=int(item['cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

                r.append(DataPoint(
                    region_schema=SCHEMA_BR_CITY,
                    region_parent=item['state'],
                    region_child=item['name'],
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r

    def _get_covid19_macro(self):
        r = []

        # brazil_covid19_macro.csv
        # date,country,week,cases,deaths,recovered,monitoring
        # 2020-02-26,Brazil,9,1,0,0,0
        # 2020-02-27,Brazil,9,1,0,0,0
        # 2020-02-28,Brazil,9,1,0,0,0

        with self.get_file('brazil_covid19_macro.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Brazil',
                    datatype=DT_TOTAL,
                    value=int(item['cases']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Brazil',
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Brazil',
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['recovered']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Brazil',
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['cases'])-int(item['recovered']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(BRData().get_datapoints())
