# https://www.gov.ie/en/service/0039bc-view-the-covid-19-coronavirus-dashboard-showing-the-latest-stats-and/
# https://data.gov.ie/dataset?q=covid&sort=score+desc%2C+metadata_created+desc

import csv
from os import listdir

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.covid_db.datatypes.DatapointMerger import DataPointMerger


class IEData(URLBase):
    SOURCE_URL = 'https://data.gov.ie/dataset?q=covid&sort=score+desc%2C+metadata_created+desc'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ie_open_data'

    def __init__(self):
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 'ie' / 'data',
             urls_dict={
                 # Points for each county w/stats
                 'county_data.csv': URL('http://opendata-geohive.hub.arcgis.com/datasets/4779c505c43c40da9101ce53f34bb923_0.csv?outSR={%22latestWkid%22:3857,%22wkid%22:102100}',
                                         static_file=False),
                 # Country-wide stats (age distribution etc)
                 'country_data.csv': URL('http://opendata-geohive.hub.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv?outSR={%22latestWkid%22:3857,%22wkid%22:102100}',
                                          static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_county_data())
        return r

    def _get_county_data(self):
        # ORIGID	CountyName	PopulationCensus16	IGEasting	IGNorthing	Lat	Long	UniqueGeographicIdentifier	ConfirmedCovidCases	PopulationProportionCovidCases	ConfirmedCovidDeaths	ConfirmedCovidRecovered	x	y	FID	TimeStampDate
        # 	Carlow	56932	278661	163444	52.7168	-6.8367	http://data.geohive.ie/resource/county/2ae19629-143d-13a3-e055-000000000001	175	307.384247874657			-6.8367	52.7168	194903	2020/07/01 00:00:00+00
        # 	Cavan	76176	246380	304501	53.9878	-7.2937	http://data.geohive.ie/resource/county/2ae19629-1448-13a3-e055-000000000001	862	1131.5900021004			-7.2937	53.9878	194904	2020/07/01 00:00:00+00
        # 	Clare	118817	133493	182732	52.8917	-8.9889	http://data.geohive.ie/resource/county/2ae19629-1450-13a3-e055-000000000001	368	309.719989563783			-8.9889	52.8917	194905	2020/07/01 00:00:00+00

        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            r = self.sdpf()
            path = f'{base_dir}/{date}/county_data.csv'

            with open(path, 'r', encoding='utf-8') as f:
                for item in csv.DictReader(f):
                    date = self.convert_date(
                        item['TimeStampDate'].split()[0]
                    )

                    for datatype, value in (
                        (DataTypes.TOTAL, int(item['ConfirmedCovidCases'])),
                        (DataTypes.STATUS_DEATHS, int(item['ConfirmedCovidDeaths'] or 0)),
                        (DataTypes.STATUS_RECOVERED, int(item['ConfirmedCovidRecovered'] or 0)),
                        (DataTypes.STATUS_ACTIVE, int(item['ConfirmedCovidCases'] or 0) -
                                           int(item['ConfirmedCovidDeaths'] or 0) -
                                           int(item['ConfirmedCovidRecovered'] or 0))
                    ):
                        r.append(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='IE',
                            region_child=item['CountyName'],
                            datatype=datatype,
                            value=value,
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

            out.extend(r)
        return out

    def _get_country_data(self):
        r = []

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(IEData().get_datapoints())
