import csv

from covid_crawlers._base_classes.KaggleDataset import KaggleDataset
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from _utility.get_package_dir import get_overseas_dir
from covid_crawlers.americas.br_data.br_region_mappings import br_region_mappings


class BRData(KaggleDataset):
    SOURCE_URL = 'https://www.kaggle.com/unanimad/corona-virus-brazil'
    SOURCE_DESCRIPTION = 'CC0: Public Domain'
    SOURCE_ID = 'br_kaggle'

    def __init__(self):
        KaggleDataset.__init__(self,
             output_dir=get_overseas_dir() / 'br' / 'data',
             dataset='unanimad/corona-virus-brazil'
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings=br_region_mappings,
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_covid19())
        r.extend(self._get_covid19_cities())
        r.extend(self._get_covid19_macro())
        return r

    def _get_covid19(self):
        r = self.sdpf()

        # brazil_covid19.csv
        # date,region_child,state,cases,deaths
        # 2020-02-26,Sudeste,São Paulo,1,0
        # 2020-02-27,Sudeste,São Paulo,1,0
        # 2020-02-28,Sudeste,São Paulo,1,0

        with self.get_file('brazil_covid19.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Brazil',
                    region_child='br-'+item['state'],
                    datatype=DataTypes.TOTAL,
                    value=int(float(item['cases'])),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='Brazil',
                    region_child='br-'+item['state'],
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(int(item['deaths'])),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

        return r

    def _get_covid19_cities(self):
        r = self.sdpf()

        # brazil_covid19_cities.csv
        # date,state,name,code,cases,deaths
        # 2020-03-28,Acre,Rio Branco,120040,25,0
        # 2020-03-28,Alagoas,Maceió,270430,13,0
        # 2020-03-28,Alagoas,Porto Real do Colégio,270750,1,0

        with self.get_file('brazil_covid19_cities.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(
                    region_schema=Schemas.BR_CITY,
                    region_parent='BR-'+item['state'].upper(),
                    region_child=item['name'],
                    datatype=DataTypes.TOTAL,
                    value=int(float(item['cases'])),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

                r.append(
                    region_schema=Schemas.BR_CITY,
                    region_parent='BR-'+item['state'].upper(),
                    region_child=item['name'],
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['deaths']),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

        return r

    def _get_covid19_macro(self):
        r = self.sdpf()

        # brazil_covid19_macro.csv
        # date,country,week,cases,deaths,recovered,monitoring
        # 2020-02-26,Brazil,9,1,0,0,0
        # 2020-02-27,Brazil,9,1,0,0,0
        # 2020-02-28,Brazil,9,1,0,0,0

        with self.get_file('brazil_covid19_macro.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_child='Brazil',
                    datatype=DataTypes.TOTAL,
                    value=int(float(item['cases'])),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

                if item['deaths']:
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Brazil',
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(float(item['deaths'])),
                        source_url=self.SOURCE_URL,
                        date_updated=date
                    )

                if item['recovered']:
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Brazil',
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(float(item['recovered'])),
                        source_url=self.SOURCE_URL,
                        date_updated=date
                    )

                if item['recovered'] and item['deaths']:
                    r.append(
                        region_schema=Schemas.ADMIN_0,
                        region_child='Brazil',
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(float(item['cases'])) -
                              int(float(item['recovered'])) -
                              int(float(item['deaths'])),
                        source_url=self.SOURCE_URL,
                        date_updated=date
                    )

        return r


if __name__ == '__main__':
    inst = BRData()
    datapoints = inst.get_datapoints()
    inst.sdpf.print_mappings()
    #pprint(datapoints)
