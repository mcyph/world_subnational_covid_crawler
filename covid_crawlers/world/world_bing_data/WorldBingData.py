import csv

from _utility.get_package_dir import get_overseas_dir
from covid_crawlers.world.world_bing_data.world_bing_mappings import world_bing_mappings
from covid_crawlers._base_classes.GithubRepo import GithubRepo
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes


class WorldBingData(GithubRepo):
    SOURCE_ID = 'world_bing'
    SOURCE_URL = 'https://github.com/microsoft/Bing-COVID-19-Data'
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'world_bing' / 'Bing-COVID-19-Data',
                            github_url='https://github.com/microsoft/Bing-COVID-19-Data')

        self.sdpf = StrictDataPointsFactory(
            region_mappings=world_bing_mappings,
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_daily_reports_us())
        return r

    def _get_daily_reports_us(self):
        r = self.sdpf()

        # ID,Updated,Confirmed,ConfirmedChange,Deaths,DeathsChange,Recovered,RecoveredChange,Latitude,Longitude,ISO2,ISO3,Country_Region,AdminRegion1,AdminRegion2
        # 338995,01/21/2020,262,,0,,,,,,,,Worldwide,,
        # 338996,01/22/2020,313,51,0,0,,,,,,,Worldwide,,
        # 338997,01/23/2020,578,265,0,0,,,,,,,Worldwide,,
        # 338998,01/24/2020,841,263,0,0,,,,,,,Worldwide,,
        # 338999,01/25/2020,1320,479,0,0,,,,,,,Worldwide,,
        # 339000,01/26/2020,2014,694,0,0,,,,,,,Worldwide,,
        # 339001,01/27/2020,2798,784,0,0,,,,,,,Worldwide,,
        warning_printed = set()

        with open(self.get_path_in_dir(f'data/Bing-COVID19-Data.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                #print(item)
                if not item['Updated']:
                    continue  # WARNING!!
                date = self.convert_date(item['Updated'], formats=('%m/%d/%Y',))

                if item['AdminRegion2'] and item['ISO2'] != 'US':
                    if item['Country_Region'] == 'India':
                        region_schema = Schemas.IN_DISTRICT
                        region_parent = item['AdminRegion1']
                        region_child = item['AdminRegion2']
                    elif item['Country_Region'] == 'Costa Rica':
                        region_schema = Schemas.CR_CANTON
                        region_parent = item['AdminRegion1']
                        region_child = item['AdminRegion2']
                    else:
                        if (item['Country_Region'], item['AdminRegion1'], item['AdminRegion2']) in warning_printed:
                            continue
                        warning_printed.add((item['Country_Region'], item['AdminRegion1'], item['AdminRegion2']))
                        print("WARNING, IGNORING:", item)
                        continue  # HACK!!! =====================================================================================
                elif item['ISO2'] == 'US':
                    # Will use other sources for the US
                    continue

                elif item['AdminRegion1']:
                    region_schema = Schemas.ADMIN_1
                    region_parent = item['ISO2']
                    region_child = item['AdminRegion1']

                    if region_parent == 'PT':
                        # TODO: Support the more limited Portugal regions!!! ===========================================
                        continue
                else:
                    region_schema = Schemas.ADMIN_0
                    region_parent = None
                    region_child = item['Country_Region']

                r.append(
                    region_schema=region_schema,
                    region_parent=region_parent,
                    region_child=region_child,
                    datatype=DataTypes.TOTAL,
                    value=int(item['Confirmed']),
                    date_updated=date,
                    source_url='Bing'
                )
                #if region_schema == Schemas.ADMIN_1 and r[-1].region_child.upper() == 'US-TX':
                #    print(r[-1])

                if item['ConfirmedChange']:
                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.NEW,
                        value=int(item['ConfirmedChange']),
                        date_updated=date,
                        source_url='Bing'
                    )

                if item['Deaths']:
                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(item['Deaths']),
                        date_updated=date,
                        source_url='Bing'
                    )

                if item['Recovered']:
                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=int(item['Recovered']),
                        date_updated=date,
                        source_url='Bing'
                    )
                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(item['Confirmed']) -
                              int(item['Deaths'] or '0') -
                              int(item['Recovered']),
                        date_updated=date,
                        source_url='Bing'
                    )

        return r


if __name__ == '__main__':
    inst = WorldBingData()
    datapoints = inst.get_datapoints()
    #pprint(WorldBingData().get_datapoints())
    inst.sdpf.print_mappings()
