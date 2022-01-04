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
        items = {}

        with open(self.get_path_in_dir(f'data/Bing-COVID19-Data.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):

                if item['ISO2'].lower() in ('au', 'nz'):
                    # HACK: Disable recovered/active values for AU, as they aren't accurate!
                    item['Recovered'] = None

                if not item['Updated']:
                    continue  # WARNING!!
                date = self.convert_date(item['Updated'], formats=('%m/%d/%Y',))

                region_schema, region_parent, region_child = \
                    self.__get_region(item, warning_printed)
                if region_schema is None:
                    continue

                d = {}
                if item['Confirmed']:
                    d[DataTypes.TOTAL] = int(item['Confirmed'])
                #if item['ConfirmedChange']:
                #    d[DataTypes.NEW] = int(item['ConfirmedChange'])
                if item['Deaths']:
                    d[DataTypes.STATUS_DEATHS] = int(item['Deaths'])
                if item['Recovered']:
                    d[DataTypes.STATUS_RECOVERED] = int(item['Recovered'])

                # Only add if greater than previous values, as Bing has
                # quite a few problems with aggregators stopping working!
                unique_key = (region_schema, region_parent, region_child)
                if unique_key in items:
                    prev_dict = items[unique_key]
                    for k, v in list(d.items()):
                        if k in prev_dict and v < prev_dict[k]:
                            del d[k]

                for k, v in d.items():
                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=k,
                        value=v,
                        date_updated=date,
                        source_url='Bing'
                    )
                    items.setdefault(unique_key, {})[k] = v

                if DataTypes.TOTAL in d and \
                   DataTypes.STATUS_DEATHS in d and \
                   DataTypes.STATUS_RECOVERED in d:
                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=d[DataTypes.TOTAL] -
                              d[DataTypes.STATUS_DEATHS] -
                              d[DataTypes.STATUS_RECOVERED],
                        date_updated=date,
                        source_url='Bing'
                    )
        return r

    def __get_region(self, item, warning_printed):
        if item['AdminRegion2'] and item['ISO2'] != 'US':
            if item['Country_Region'] == 'India':
                region_schema = Schemas.IN_DISTRICT
                region_parent = item['AdminRegion1']
                region_child = item['AdminRegion2']
            elif item['Country_Region'] == 'Costa Rica':
                region_schema = Schemas.CR_CANTON
                region_parent = item['AdminRegion1']
                region_child = item['AdminRegion2']
            elif item['Country_Region'] == 'Germany':
                region_schema = Schemas.ADMIN_1
                region_parent = 'de'
                region_child = item['AdminRegion1']
            elif item['Country_Region'] == 'Czechia':
                region_schema = Schemas.ADMIN_1
                region_parent = 'cz'
                region_child = item['AdminRegion1']
            else:
                if (item['Country_Region'], item['AdminRegion1'], item['AdminRegion2']) in warning_printed:
                    return None, None, None
                warning_printed.add((item['Country_Region'], item['AdminRegion1'], item['AdminRegion2']))
                print("WARNING, IGNORING:", item)
                return None, None, None  # HACK!!! =====================================================================================
        elif item['ISO2'] == 'US':
            # Will use other sources for the US
            return None, None, None

        elif item['AdminRegion1']:
            region_schema = Schemas.ADMIN_1
            region_parent = item['ISO2']
            region_child = item['AdminRegion1']

            if region_parent == 'PT':
                # TODO: Support the more limited Portugal regions!!! ===========================================
                return None, None, None
        else:
            region_schema = Schemas.ADMIN_0
            region_parent = None
            region_child = item['Country_Region']

        if region_child == 'Negri Sembilan':
            region_child = 'Negeri Sembilan'

        return region_schema, region_parent, region_child


if __name__ == '__main__':
    inst = WorldBingData()
    datapoints = inst.get_datapoints()
    #pprint(WorldBingData().get_datapoints())
    inst.sdpf.print_mappings()
