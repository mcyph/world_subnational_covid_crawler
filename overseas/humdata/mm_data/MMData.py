# https://data.humdata.org/dataset/myanmar-coronavirus-covid-19-subnational-cases
# https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9GWlx9wsSxy253wGLjRqq79cQ1n4_X5N4dx6JemV7evq3DeGXSDdpnu4M9K4Rceujw3rt_CJRS5aD/pub?output=csv


# Objectidfieldname,Uniqueidfield Name,Uniqueidfield Issystemmaintained,Globalidfieldname,Geometrytype,Spatialreference Wkid,Spatialreference Latestwkid,Fields Name,Fields Type,Fields Alias,Fields Sqltype,Fields Domain,Fields Defaultvalue,Fields Length,Features Attributes No,Features Attributes Sr,Features Attributes Township,Features Attributes Case,Features Attributes Tested,Features Attributes Pui,Features Attributes M,Features Attributes F,Features Attributes Child,Features Attributes Adult,Features Attributes Confirmed,Features Attributes Death,Features Attributes Recovered,Features Attributes Latitude,Features Attributes Longitude,Features Attributes Fid
# FID,FID,true,,esriGeometryPoint,102100,3857,No,esriFieldTypeInteger,No,sqlTypeFloat,,,,4,Yangon Region,Insein Township,"3, 6, 34, 35, 36, 37, 38, 41, 54, 55, 56, 58, 59, 61, 72, 73, 84, 93, 94, 123, 127, 130, 141, 151,152, 153, 154, 157, 162, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 179",,,20,23,1,42,43,,14,16.901771,96.095959,4
# FID,FID,true,,esriGeometryPoint,102100,3857,SR,esriFieldTypeString,SR,sqlTypeNVarchar,,,256,14,Yangon Region,Mayangone Township,"24, 43, 44, 45, 62, 69, 70, 86, 98, 105, 108, 131, 160, 178, 180",,,5,10,1,15,15,1,9,16.86619,96.142611,14
# FID,FID,true,,esriGeometryPoint,102100,3857,Township,esriFieldTypeString,Township,sqlTypeNVarchar,,,256,13,Yangon Region,South Okkalapa Township,"47, 48, 49, 50, 51, 52, 89, 90, 91, 102, 128, 148, 149",,,9,4,1,13,13,1,5,16.846249,96.179859,13


import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class MMData(URLBase):
    SOURCE_URL = ''
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / '' / '',
            urls_dict={
                '': URL(
                    '',
                    static_file=False
                )
            }
        )
        self.update()

    def get_datapoints(self):
        r = []

        f = self.get_file('',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date'])

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MMData().get_datapoints())
