import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1,
    DT_TOTAL
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)

# These provide histories:
# https://docs.google.com/spreadsheets/d/1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw/edit#gid=2052139453
# https://docs.google.com/spreadsheets/d/1sgiz8x71QyIVJZQguYtG9n6xBEKdM4fXuDs_d8zKOmY/htmlview

# Getting automatically from
# https://docs.google.com/spreadsheet/ccc?key=1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw&gid=2052139453&output=csv
# Total Kasus,Aceh,Bali,Banten,Babel,Bengkulu,DIY,Jakarta,Jambi,Jabar,Jateng,Jatim,Kalbar,Kaltim,Kalteng,Kalsel,Kaltara,Kep Riau,NTB,Sumsel,Sumbar,Sulut,Sumut,Sultra,Sulsel,Sulteng,Lampung,Riau,Malut,Maluku,Papbar,Papua,Sulbar,NTT,Gorontalo,?
# 18-Mar,0,1,17,0,0,3,158,0,24,8,8,2,1,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0
# 19-Mar,0,1,27,0,0,5,210,0,26,12,9,2,3,0,0,0,3,0,0,0,1,2,3,2,0,1,2,0,0,0,0,0,0,0,0
# 20-Mar,0,4,37,0,0,4,215,0,41,12,15,2,10,2,0,0,4,0,0,0,1,2,3,2,0,1,1,0,0,0,0,0,0,0,13
# 21-Mar,0,3,43,0,0,5,267,0,55,14,26,2,9,2,0,0,4,0,0,0,1,2,3,2,0,1,1,0,0,0,0,0,0,0,10
# 22-Mar,0,3,47,0,0,5,307,0,59,15,41,2,9,2,1,0,4,0,0,0,1,2,3,2,0,1,1,0,1,0,2,0,0,0,6
# 23-Mar,0,6,56,0,0,5,353,1,59,15,41,2,11,2,1,0,5,0,0,0,1,2,3,2,0,1,1,1,1,0,2,0,0,0,8

# https://docs.google.com/spreadsheet/ccc?key=1sgiz8x71QyIVJZQguYtG9n6xBEKdM4fXuDs_d8zKOmY&gid=83750310&output=csv
# ,,14-May,,Selisih dengan hari sebelumnya,,Historical,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# Kode Provinsi BPS,Provinsi,Kasus Kumulatif,% Provinsi,,,20-Mar,21-Mar,22-Mar,23-Mar,24-Mar,25-Mar,26-Mar,27-Mar,28-Mar,29-Mar,30-Mar,31-Mar,1-Apr,2-Apr,3-Apr,4-Apr,5-Apr,6-Apr,7-Apr,8-Apr,9-Apr,10-Apr,11-Apr,12-Apr,13-Apr,14-Apr,15-Apr,16-Apr,17-Apr,18-Apr,19-Apr,20-Apr,21-Apr,22-Apr,23-Apr,24-Apr,25-Apr,26-Apr,27-Apr,28-Apr,29-Apr,30-Apr,1-May,2-May,3-May,4-May,5-May,6-May,7-May,8-May,9-May,10-May,11-May,12-May,13-May,14-May
# 11,Aceh,17,0.1%,0,,0,0,0,0,0,0,1,4,5,5,5,5,5,5,5,5,5,5,5,6,5,5,5,5,5,5,5,5,5,6,7,7,7,7,7,8,9,9,9,9,9,10,11,11,12,12,12,17,17,17,17,17,17,17,17,17
# 12,Sumatera Utara,200,1.3%,2,,2,2,2,2,7,8,8,8,8,8,13,20,22,22,22,25,25,26,26,59,59,59,59,65,67,72,78,79,79,79,81,83,84,93,95,96,105,111,111,111,114,117,117,117,123,129,130,141,142,157,179,179,196,198,200,202
# 13,Sumatera Barat,339,2.2%,20,,0,0,0,0,0,0,3,5,5,5,8,8,8,8,8,8,8,18,18,18,18,31,31,44,45,48,55,55,62,71,72,74,76,81,86,96,97,102,121,144,145,148,172,182,195,203,221,238,252,270,286,299,299,319,339,371


class IDGoogleDocsData(URLBase):
    SOURCE_URL = 'https://kawalcovid19.id/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'id_kawalcovid19'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'id' / 'data',
             urls_dict={
                 'provinces_1.csv': URL(
                     'https://docs.google.com/spreadsheet/ccc?'
                     'key=1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw&gid=2052139453&output=csv',
                     static_file=False
                 ),
                 'provinces_2.csv': URL(
                     'https://docs.google.com/spreadsheet/ccc?'
                     'key=1sgiz8x71QyIVJZQguYtG9n6xBEKdM4fXuDs_d8zKOmY&gid=83750310&output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_provinces_1())
        #r.extend(self._get_provinces_2())
        return r

    def _get_provinces_1(self):
        r = []

        f = self.get_file('provinces_1.csv',
                          include_revision=True)
        for item in csv.DictReader(f):
            if not item['Total Kasus'].strip():
                break
            date = self.convert_date(item['Total Kasus']+'-20')

            for province in list(item.keys())[1:]:
                value = item[province].replace(',', '')
                province = province.strip()

                if not province or not value:
                    continue
                elif province == '?':
                    province = 'Unknown'

                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent='Indonesia',
                    region_child=province,
                    datatype=DT_TOTAL,
                    value=int(value),
                    date_updated=date,
                    source_url='https://docs.google.com/spreadsheets/d/1ma1T9hWbec1pXlwZ89WakRk-OfVUQZsOCFl4FwZxzVw/edit'
                ))
        return r

    def _get_provinces_2(self):
        r = []

        return r

if __name__ == '__main__':
    from pprint import pprint
    pprint(IDGoogleDocsData().get_datapoints())
