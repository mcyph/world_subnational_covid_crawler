# https://sbsgm.saglik.gov.tr/TR,66424/covid-19-situation-report-turkey.html
# https://www.aa.com.tr/tr/koronavirus/turkiyenin-il-il-kovid-19-vaka-haritasi/1788776
# https://cbskampus.maps.arcgis.com/apps/opsdashboard/index.html#/233c6c3e8a7144eb8153ca1636ea3f86

# Turkiye Test Sayisi
# Yogun Bakim Hasta Sayisi
# Entube Hasta Sayisi
# Turkey Deaths Toplam
# Toplam Test
# Gunluk Vaka Sayisi
# Gunluk Iyilesme
# iyilesme yuzde
# toplam test yuzde
# toplamyogun yuzde
# vefat yuzde
# gunluk pozitiftest

# Turkey Number of Tests *
# Intensive Care Patients *
# Entube Patients (ICU+ventilator?) *
# Turkey Deaths Total *
# Total Test *
# Number of Daily Cases *
# Daily Healing *
# percent improvement
# percent of total test
# percent intense
# percent of death
# daily positive test

import json
import datetime
from pyquery import PyQuery as pq
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir


class TRData(URLBase):
    SOURCE_URL = 'https://cbskampus.maps.arcgis.com/apps/opsdashboard/index.html#/233c6c3e8a7144eb8153ca1636ea3f86'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'tr_dash'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'tr' / 'data',
            urls_dict={
                'regions.json': URL('https://services5.arcgis.com/26ObnytmBZ58Wbj8/arcgis/rest/services/Kovid_19_TurkiyeIL/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=T_KesinVaka%20desc&resultOffset=0&resultRecordCount=81&resultType=standard&cacheHint=true',
                                    static_file=False),
                'other_stats.json': URL('https://services1.arcgis.com/5hM12kUbM5soE48F/arcgis/rest/services/Case_time_v4/FeatureServer/0/query?f=json&where=Turkey_Date%20BETWEEN%20timestamp%20%272019-12-31%2013%3A00%3A00%27%20AND%20CURRENT_TIMESTAMP&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Turkey_Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard',
                                        static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        # HACK THIS IS DISABLED AS DOESN'T SEEM TO BE UP-TO-DATE as of 17th July!! ==================================================
        r.extend(self._get_regions())
        #r.extend(self._get_other_stats())
        return r

    def _get_regions(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/regions.json'
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

            for feature in data['features']:
                attributes = feature['attributes']
                #print(feature)

                # Only confirmed and deaths are shown in the dashboard
                date = datetime.datetime.fromtimestamp(attributes['Tarih']/1000.0).strftime('%Y_%m_%d') # -> 2020_04_14??
                region = attributes['İL_ADı']
                total = attributes['toplam']  # I don't know what this value is(?) perhaps it's the total population of the region
                confirmed = attributes['T_KesinVaka']
                recovered = attributes['T_IyilesenVaka']
                deaths = attributes['T_OlenVaka']

                if confirmed is not None:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.TOTAL,
                        value=int(confirmed),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if recovered is not None and False:  # A lot of these values are 0(?)
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(recovered),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                if deaths is not None:
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='TR',
                        region_child=region,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(deaths),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

        return r

    def _get_other_stats(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/other_stats.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(TRData().get_datapoints())
