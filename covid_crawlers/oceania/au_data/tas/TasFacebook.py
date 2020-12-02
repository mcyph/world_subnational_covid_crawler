import csv
from json import loads
from datetime import datetime

from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DataPoint import DataPoint
from _utility.get_package_dir import get_package_dir

TAS_BY_LGA = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'tas' / 'tas_by_lga.json'
TAS_BY_THS = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'tas' / 'tas_by_ths.tsv'


class TasFacebook:
    SOURCE_ID = 'au_tas_peter_gutwein_fb'
    SOURCE_URL = 'Peter Gutweins Facebook Page'
    SOURCE_DESCRIPTION = ''

    def get_datapoints(self):
        r = []

        # Add manually entered data by THS and LGA
        if False:
            with open(TAS_BY_LGA, 'r', encoding='utf-8') as f:
                for date, date_dict in loads(f.read()).items():
                    for _, region_child, total in date_dict['data']:
                        r.append(DataPoint(
                            region_schema=Schemas.LGA,
                            region_parent='au-tas',
                            region_child=region_child,
                            datatype=DataTypes.TOTAL,
                            value=total,
                            date_updated=date,
                            source_url=date_dict['source_url'],
                            source_id='au_tas_csv'
                        ))

        with open(TAS_BY_THS, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')

            for date_dict in reader:
                dd, mm, yyyy = date_dict['Date'].split('/')
                dt = datetime(day=int(dd), month=int(mm), year=int(yyyy)).strftime('%Y_%m_%d')

                for region_child in (
                        'North-West', 'North', 'South',
                ):
                    r.append(DataPoint(
                        region_schema=Schemas.THS,
                        region_parent='au-tas',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=date_dict[f'{region_child} Active'],
                        date_updated=dt,
                        source_url=self.SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))
                    r.append(DataPoint(
                        region_schema=Schemas.THS,
                        region_parent='au-tas',
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(date_dict[f'{region_child} Recovered']),
                        date_updated=dt,
                        source_url=self.SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))
                    r.append(DataPoint(
                        region_schema=Schemas.THS,
                        region_parent='au-tas',
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(date_dict[f'{region_child} Active']) +
                              int(date_dict[f'{region_child} Recovered']),
                        date_updated=dt,
                        source_url=self.SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))
        return r

if __name__ == '__main__':
    from pprint import pprint
    tn = TasFacebook()
    pprint(tn.get_datapoints())
