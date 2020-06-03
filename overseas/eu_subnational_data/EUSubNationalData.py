# https://data.humdata.org/dataset/europe-covid-19-subnational-cases

import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0, SCHEMA_ADMIN_1,
    DT_TOTAL,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)

# https://proxy.hxlstandard.org/data/e2bb4b/download/jrc-covid-19-regions-hxl.csv
#
# Date,iso3,CountryName,Region,lat,lon,CumulativePositive,
# CumulativeDeceased,CumulativeRecovered,CurrentlyPositive,
# Hospitalized,IntensiveCare,EUcountry,EUCPMcountry
#
# #date,#country+code+iso3,#country+name,#adm1+name,#geo+lat,#geo+lon,
# #affected+positive+total,#affected+dead+total,#affected+recovered+total,
# #affected+positive,#affected+hospitalized,#affected+intensive_care,
# #indicator+eu,#indicator+eucpm
#
# 2020-01-24,FRA,France,Île-de-France,48.709229,2.503473,2,0,0,2,2,0,TRUE,TRUE
# 2020-01-24,FRA,France,Nouvelle-Aquitaine,45.479897,0.410462,1,0,0,1,1,0,TRUE,TRUE
# 2020-01-25,FRA,France,Île-de-France,48.709229,2.503473,2,0,0,2,2,0,TRUE,TRUE
# 2020-01-25,FRA,France,Nouvelle-Aquitaine,45.479897,0.410462,1,0,0,1,1,0,TRUE,TRUE


class EUSubNationalData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/europe-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'eu_subnational'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'eu_subnational' / 'data',
             urls_dict={
                 'jrc-covid-19-regions-hxl.csv':
                     URL('https://proxy.hxlstandard.org/data/e2bb4b/download/jrc-covid-19-regions-hxl.csv',
                         static_file=False),
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        with self.get_file('jrc-covid-19-regions-hxl.csv',
                           include_revision=True) as f:
            first_line = True

            for item in csv.DictReader(f):
                if first_line:
                    first_line = False
                    continue

                date = self.convert_date(item['Date'])
                country = {
                    'NOT SPECIFIED': 'Unknown',
                }.get(item['CountryName'], item['CountryName'])\
                    .replace('Russian Fed.', 'Russian Federation')\
                    .replace('Czech Republic', '')

                region_child = item['Region']

                if region_child == country:
                    region_child = country
                    country = None
                    schema = SCHEMA_ADMIN_0
                else:
                    schema = SCHEMA_ADMIN_1

                r.append(DataPoint(
                    region_schema=schema,
                    region_parent=country,
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=item['CumulativePositive'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=schema,
                    region_parent=country,
                    region_child=region_child,
                    datatype=DT_STATUS_DEATHS,
                    value=item['CumulativeDeceased'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=schema,
                    region_parent=country,
                    region_child=region_child,
                    datatype=DT_STATUS_RECOVERED,
                    value=item['CumulativeRecovered'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=schema,
                    region_parent=country,
                    region_child=region_child,
                    datatype=DT_STATUS_ACTIVE,
                    value=item['CurrentlyPositive'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=schema,
                    region_parent=country,
                    region_child=region_child,
                    datatype=DT_STATUS_HOSPITALIZED,
                    value=item['Hospitalized'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=schema,
                    region_parent=country,
                    region_child=region_child,
                    datatype=DT_STATUS_ICU,
                    value=item['IntensiveCare'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(EUSubNationalData().get_datapoints())
