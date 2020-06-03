import csv
from os import listdir

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_US_COUNTY,
    SCHEMA_ADMIN_1, SCHEMA_ADMIN_0,
    DT_TOTAL, DT_TESTS_TOTAL, DT_STATUS_ACTIVE, DT_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class WorldBingData(GithubRepo):
    SOURCE_ID = 'world_bing'
    SOURCE_URL = 'https://github.com/microsoft/Bing-COVID-19-Data'
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'world_bing' / 'Bing-COVID-19-Data',
                            github_url='https://github.com/microsoft/Bing-COVID-19-Data')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_daily_reports_us())
        return r

    def _get_daily_reports_us(self):
        r = []

        # ID,Updated,Confirmed,ConfirmedChange,Deaths,DeathsChange,Recovered,RecoveredChange,Latitude,Longitude,ISO2,ISO3,Country_Region,AdminRegion1,AdminRegion2
        # 338995,01/21/2020,262,,0,,,,,,,,Worldwide,,
        # 338996,01/22/2020,313,51,0,0,,,,,,,Worldwide,,
        # 338997,01/23/2020,578,265,0,0,,,,,,,Worldwide,,
        # 338998,01/24/2020,841,263,0,0,,,,,,,Worldwide,,
        # 338999,01/25/2020,1320,479,0,0,,,,,,,Worldwide,,
        # 339000,01/26/2020,2014,694,0,0,,,,,,,Worldwide,,
        # 339001,01/27/2020,2798,784,0,0,,,,,,,Worldwide,,

        with open(self.get_path_in_dir(f'data/Bing-COVID19-Data.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                if not item['Updated']:
                    continue  # WARNING!!
                date = self.convert_date(item['Updated'], formats=('%m/%d/%Y',))

                if item['AdminRegion2'] and item['ISO2'] != 'US':
                    print("WARNING, IGNORING:", item)
                    continue  # HACK!!! =====================================================================================
                elif item['AdminRegion1']:
                    region_schema = SCHEMA_ADMIN_1
                    region_parent = item['ISO2']
                    region_child = item['AdminRegion1']
                else:
                    region_schema = SCHEMA_ADMIN_0
                    region_parent = None
                    region_child = item['Country_Region']

                r.append(DataPoint(
                    region_schema=region_schema,
                    region_parent=region_parent,
                    region_child=region_child,
                    datatype=DT_TOTAL,
                    value=int(item['Confirmed']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

                if item['ConfirmedChange']:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_NEW,
                        value=int(item['ConfirmedChange']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['Deaths']:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_DEATHS,
                        value=int(item['Deaths']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

                if item['Recovered']:
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_RECOVERED,
                        value=int(item['Recovered']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))
                    r.append(DataPoint(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DT_STATUS_ACTIVE,
                        value=int(item['Confirmed']) -
                              int(item['Deaths'] or '0') -
                              int(item['Recovered']),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    ))

        return r



if __name__ == '__main__':
    from pprint import pprint
    pprint(WorldBingData().get_datapoints())
