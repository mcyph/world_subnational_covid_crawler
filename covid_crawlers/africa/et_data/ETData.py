import csv

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


class ETData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/' \
                 'ethiopia-coronavirus-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'et_ocha_humdata'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'et' / 'data',
             urls_dict={
                 'et_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/'
                     '1wpMiswWu5En3Ljoqv-N9gK_VQWU6xYA9NBAYzJ3aE2g/'
                     'export?format=csv&'
                     'id=1wpMiswWu5En3Ljoqv-N9gK_VQWU6xYA9NBAYzJ3aE2g',
                     static_file=False
                 )
             }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'et', 'snnpr'): ('admin_1', 'et', 'et-sn'),
                ('admin_1', 'et', 'sidama'): None,
                ('admin_1', 'et', 'benshangul gumuz'): ('admin_1', 'et', 'et-be'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = self.sdpf()

        # Date	admin1Name_en	admin1Pcode	Number of confirmed COVID-19	Number of reported deaths	Number of reported recoveries
        # #date	#adm1+name	#adm1+code	#affected+infected+confirmed	#affected+infected+dead	#affected+infected+recovered
        # 2020-05-13	Addis Ababa	ET14	172	3	47
        # 2020-05-13	Afar	ET02	20
        # 2020-05-13	Amhara	ET03	9		2
        # 2020-05-13	Dire Dawa	ET15	8		1
        # 2020-05-13	Oromia	ET04	17

        f = self.get_file('et_data.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue
            date = self.convert_date(item['Date'])
            region_child = {
                'Amhara': 'Amara',
                'Oromia': 'Oromiya',
                'Somali': 'Sumale',
                'SNNP': 'YeDebub Biheroch Bihereseboch na Hizboch',
            }.get(item['admin1Name_en'].strip(), item['admin1Name_en'].strip())

            if item['Number of confirmed COVID-19']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='et',
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(item['Number of confirmed COVID-19'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )
                
            if item['Number of reported deaths']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='et',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(item['Number of reported deaths'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

            if item['Number of reported recoveries']:
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='et',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(item['Number of reported recoveries'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='et',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(item['Number of confirmed COVID-19'].replace(',', '')) -
                          int(item['Number of reported recoveries'].replace(',', '')),
                    source_url=self.SOURCE_URL,
                    date_updated=date
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ETData().get_datapoints())
