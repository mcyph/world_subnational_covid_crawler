import json
import datetime
from os import listdir
from collections import Counter

from _utility.cache_by_date import cache_by_date
from covid_db.datatypes.DatapointMerger import DataPointMerger
from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir

division_map = dict([i.split('\t')[::-1] for i in """
BD-A	Barishal
BD-A	Barisal
BD-B	Chattogram
BD-B	Chittagong
BD-C	Dhaka
BD-D	Khulna
BD-H	Mymensingh
BD-E	Rajshahi
BD-F	Rangpur
BD-G	Sylhet
""".strip().split('\n')])

place_map = dict([i.split('\t')[::-1] for i in """
BD-01	Bandarban
BD-02	Barguna
BD-03	Bogura
BD-03	Bogra
BD-04	Brahmanbaria
BD-04	Brahamanbaria
BD-04	B. Baria
BD-05	Bagerhat
BD-06	Barishal
BD-06	Barisal
BD-07	Bhola
BD-08	Cumilla
BD-08	Comilla
BD-09	Chandpur
BD-10	Chattogram
BD-10	Chittagong
BD-11	Cox’s bazar
BD-11	Cox’s Bazar
BD-11	Cox's Bazar
BD-12	Chuadanga
BD-13	Dhaka
BD-14	Dinajpur
BD-15	Faridpur
BD-16	Feni
BD-17	Gopalganj
BD-18	Gazipur
BD-19	Gaibandha
BD-20	Hobiganj
BD-20	Habiganj
BD-21	Jamalpur
BD-22	Jessore
BD-22	Jashore
BD-23	Jhenaidah
BD-24	Joypurhat
BD-25	Jhalakathi
BD-25	Jhalokathi
BD-25	Jhalokati
BD-26	Kishoreganj
BD-27	Khulna
BD-28	Kurigram
BD-29	Khagrachhari
BD-29	Khagrachari
BD-30	Kushtia
BD-31	Laksmipur
BD-31	Lakshmipur
BD-32	Lalmonirhat
BD-33	Manikganj
BD-34	Mymensingh
BD-35	Munshiganj
BD-35	Munshigonj
BD-36	Madaripur
BD-37	Magura
BD-38	Moulvibazar
BD-38	Moulovi Bazar
BD-38	Maulvibazar
BD-39	Meherpur
BD-40	Narayanganj
BD-41	Netrokona
BD-41	Netrakona
BD-42	Narsingdi
BD-42	Narshingdi
BD-43	Narail
BD-44	Natore
BD-45	Chapai Nawabganj
BD-45	Chapainawabganj
BD-45	Nawabganj
BD-46	Nilphamari
BD-47	Noakhali
BD-48	Naogaon
BD-49	Pabna
BD-50	Pirojpur
BD-51	Patuakhali
BD-51	Potuakhali
BD-52	Panchagarh
BD-52	Panchagar
BD-53	Rajbari
BD-54	Rajshahi
BD-55	Rangpur
BD-56	Rangmati
BD-56	Rangamati
BD-57	Sherpur
BD-58	Satkhira
BD-59	Sirajganj
BD-60	Sylhet
BD-61	Sunamganj
BD-62	Shariatpur
BD-63	Tangail
BD-64	Thakurgaon
""".strip().split('\n')])


class BDData(URLBase):
    SOURCE_URL = 'https://iedcr.gov.bd/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'bd_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'bd' / 'data',
            urls_dict={
                'data.json': URL('https://services3.arcgis.com/nIl76MjbPamkQiu8/arcgis/rest/services/corona_time_tracker_bd/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&maxRecordCountFactor=4&orderByFields=cases%20DESC&outSR=102100&resultOffset=0&resultRecordCount=8000&cacheHint=true&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A1.0583354500042312%2C%22extent%22%3A%7B%22xmin%22%3A9826271.639862971%2C%22ymin%22%3A2441939.9806026146%2C%22xmax%22%3A10265220.533389015%2C%22ymax%22%3A3040170.8239516346%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D%7D',
                                 static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'bd', 'bd-h'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        dpm = DataPointMerger()
        for date in self.iter_nonempty_dirs(self.output_dir):
            r.extend(self._get_recovered_sum(date, dpm))
        return r

    @cache_by_date(source_id=SOURCE_ID)
    def _get_recovered_sum(self, date, dpm):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        # {"date":1589220000000,"division":"Rajshahi","district":"Joypurhat","city":"Joypurhat",
        # "population":1017277,"cases":55,"recovered":null,"death":null,"geo_code":5038,
        # "lat":25.102372,"long":89.021208,"adjusted_cases":54.06590339,"labels":"Joypurhat(55)",
        # "ObjectId":1266},"geometry":{"x":78920,"y":143477}},
        # {"attributes":{"date":1589392800000,"division":"Rajshahi","district":"Joypurhat",
        # "city":"Joypurhat","population":1017277,"cases":55,"recovered":null,"death":null,
        # "geo_code":5038,"lat":25.102372,"long":89.021208,"adjusted_cases":54.06590339,
        # "labels":"Joypurhat(55)","ObjectId":1332},"geometry":{"x":78920,"y":143477}}

        path = f'{base_dir}/{date}/data.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
        except UnicodeDecodeError:
            import brotli
            with open(path, 'rb') as f:
                data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

        by_total = Counter()
        by_recovered = Counter()
        by_active = Counter()
        by_death = Counter()

        for feature in data['features']:
            #print(feature)
            attributes = feature['attributes']
            date = datetime.datetime \
                .fromtimestamp(attributes['date']/1000.0) \
                .strftime('%Y_%m_%d')
            district = place_map[attributes['district']]
            admin_1 = division_map[attributes['division']]

            r.append(
                region_schema=Schemas.BD_DISTRICT,
                region_parent=admin_1,
                region_child=district,
                datatype=DataTypes.TOTAL,
                value=int(attributes['cases']),
                date_updated=date,
                source_url=self.SOURCE_URL
            )
            by_total[date, admin_1] += int(attributes['cases'])

            if attributes['recovered'] is not None:
                r.append(
                    region_schema=Schemas.BD_DISTRICT,
                    region_parent=admin_1,
                    region_child=district,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(attributes['recovered']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.BD_DISTRICT,
                    region_parent=admin_1,
                    region_child=district,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(attributes['cases']) -
                          int(attributes['death'] or 0) -
                          int(attributes['recovered']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                by_recovered[date, admin_1] += int(attributes['recovered'])
                by_active[date, admin_1] += int(r[-1].value)

            if attributes['death'] is not None:
                r.append(
                    region_schema=Schemas.BD_DISTRICT,
                    region_parent=admin_1,
                    region_child=district,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(attributes['death']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                by_death[date, admin_1] += int(attributes['death'])

        for (date, admin_1), value in by_total.items():
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='BD',
                region_child=admin_1,
                datatype=DataTypes.TOTAL,
                value=value,
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        for (date, admin_1), value in by_death.items():
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='BD',
                region_child=admin_1,
                datatype=DataTypes.STATUS_DEATHS,
                value=value,
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        for (date, admin_1), value in by_recovered.items():
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='BD',
                region_child=admin_1,
                datatype=DataTypes.STATUS_RECOVERED,
                value=value,
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        for (date, admin_1), value in by_active.items():
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='BD',
                region_child=admin_1,
                datatype=DataTypes.STATUS_ACTIVE,
                value=value,
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return dpm.extend(r)


if __name__ == '__main__':
    from pprint import pprint
    pprint(BDData().get_datapoints())
