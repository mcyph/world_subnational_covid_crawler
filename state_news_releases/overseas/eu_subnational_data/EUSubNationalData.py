# https://data.humdata.org/dataset/europe-covid-19-subnational-cases

import csv
import json

from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_EU,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TOTAL, DT_TESTS_TOTAL, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_INTERSTATE, DT_SOURCE_CONFIRMED,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_DOMESTIC
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
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
                country = item['CountryName']
                region = item['Region']

                r.append(DataPoint(
                    statename=country,
                    schema=SCHEMA_EU,
                    region=region,
                    datatype=DT_TOTAL,
                    value=item['CumulativePositive'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    statename=country,
                    schema=SCHEMA_EU,
                    region=region,
                    datatype=DT_STATUS_DEATHS,
                    value=item['CumulativeDeceased'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    statename=country,
                    schema=SCHEMA_EU,
                    region=region,
                    datatype=DT_STATUS_RECOVERED,
                    value=item['CumulativeRecovered'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    statename=country,
                    schema=SCHEMA_EU,
                    region=region,
                    datatype=DT_STATUS_ACTIVE,
                    value=item['CurrentlyPositive'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    statename=country,
                    schema=SCHEMA_EU,
                    region=region,
                    datatype=DT_STATUS_HOSPITALIZED,
                    value=item['Hospitalized'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    statename=country,
                    schema=SCHEMA_EU,
                    region=region,
                    datatype=DT_STATUS_ICU,
                    value=item['IntensiveCare'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(EUSubNationalData().get_datapoints())
