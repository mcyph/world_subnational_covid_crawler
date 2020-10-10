import csv
from os import listdir

from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.overseas.GithubRepo import GithubRepo
from covid_19_au_grab.get_package_dir import get_overseas_dir
from covid_19_au_grab.overseas.world.world_jhu_data.get_county_to_code_map import get_county_to_code_map
from covid_19_au_grab.datatypes.SchemaTypeInfo import get_schema_type_info
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_DEV, MODE_STRICT
from covid_19_au_grab.overseas.world.world_jhu_data.world_jhu_mappings import world_jhu_mappings


county_to_code_map = get_county_to_code_map()


class WorldJHUData(GithubRepo):
    SOURCE_ID = 'world_jhu'
    SOURCE_URL = 'https://github.com/CSSEGISandData/COVID-19'
    SOURCE_DESCRIPTION = ''

    def __init__(self, do_update=True):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'world_jhu' / 'COVID-19',
                            github_url='https://github.com/CSSEGISandData/COVID-19')
        self.spdf = StrictDataPointsFactory(
            region_mappings=world_jhu_mappings,
            mode=MODE_STRICT
        )
        if do_update:
            self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_daily_reports_us())
        r.extend(self._get_daily_reports_global())
        return r

    def _get_daily_reports_us(self):
        r = self.spdf()
        
        # Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate
        # Alabama,US,2020-05-21 02:32:54,32.3182,-86.9023,13052,522,,12530.0,1,266.1943206303658,164450,1493,3.999387067116151,84000001,USA,3353.9423864284136,11.438859944836041
        # Alaska,US,2020-05-21 02:32:54,61.3707,-152.4044,401,10,352,39.0,2,54.81549323691639,37045,,2.493765586034913,84000002,USA,5063.940017360518,
        # American Samoa,US,2020-05-21 02:32:54,-14.270999999999999,-170.132,0,0,,0.0,60,0.0,124,,,16,ASM,222.85724555633436,
        # Arizona,US,2020-05-21 02:32:54,33.7298,-111.4312,14906,747,3773,10386.0,4,204.78883847249455,165435,1792,5.011404803434859,84000004,USA,2272.8593514488884,12.022004561921374
        # Diamond Princess,US,2020-05-21 02:32:54,,,49,0,,49.0,88888,,,,0.0,84088888,USA,,

        for fnam in listdir(self.get_path_in_dir('csse_covid_19_data/'
                                                 'csse_covid_19_daily_reports_us')):
            if not fnam.endswith('.csv'):
                continue

            with open(self.get_path_in_dir(f'csse_covid_19_data/'
                                           f'csse_covid_19_daily_reports_us/{fnam}'),
                      'r', encoding='utf-8') as f:
                for item in csv.DictReader(f):
                    if not item['Last_Update']:
                        continue # WARNING!!

                    #print(item)
                    try:
                        date = self.convert_date(item['Last_Update'].split()[0])
                    except:
                        date = self.convert_date(item['Last_Update'].split()[0], formats=('%m/%d/%y',))

                    if item['Province_State']:
                        region_schema = Schemas.ADMIN_1
                        region_parent = item['Country_Region']
                        region_child = item['Province_State']
                    else:
                        region_schema = Schemas.ADMIN_0
                        region_parent = None
                        region_child = item['Country_Region']

                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.TOTAL,
                        value=int(float(item['Confirmed'])),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )
                    #if region_schema == Schemas.ADMIN_1 and r[-1].region_child.upper() == 'US-TX':
                    #    print(r[-1])

                    r.append(
                        region_schema=region_schema,
                        region_parent=region_parent,
                        region_child=region_child,
                        datatype=DataTypes.STATUS_DEATHS,
                        value=int(float(item['Deaths'])),
                        date_updated=date,
                        source_url=self.SOURCE_URL
                    )

                    if item['Recovered']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.STATUS_RECOVERED,
                            value=int(float(item['Recovered'])),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

                    if item['Active']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.STATUS_ACTIVE,
                            value=int(float(item['Active'])),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

                    if item['People_Tested']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.TESTS_TOTAL,
                            value=int(float(item['People_Tested'])),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

                    if item['People_Hospitalized']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.STATUS_HOSPITALIZED,
                            value=int(float(item['People_Hospitalized'])),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )
        
        return r

    def _get_daily_reports_global(self):
        r = self.spdf()
        printed = set()

        # FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key
        # 45001,Abbeville,South Carolina,US,2020-05-21 02:32:48,34.22333378,-82.46170658,36,0,0,36,"Abbeville, South Carolina, US"
        # 22001,Acadia,Louisiana,US,2020-05-21 02:32:48,30.2950649,-92.41419698,262,12,0,250,"Acadia, Louisiana, US"
        # 51001,Accomack,Virginia,US,2020-05-21 02:32:48,37.76707161,-75.63234615,709,11,0,698,"Accomack, Virginia, US"
        # 16001,Ada,Idaho,US,2020-05-21 02:32:48,43.4526575,-116.24155159999998,792,23,0,769,"Ada, Idaho, US"
        # 19001,Adair,Iowa,US,2020-05-21 02:32:48,41.33075609,-94.47105874,6,0,0,6,"Adair, Iowa, US"

        for fnam in sorted(listdir(self.get_path_in_dir(
            'csse_covid_19_data/csse_covid_19_daily_reports'
        ))):
            if not fnam.endswith('.csv'):
                continue

            with open(self.get_path_in_dir(f'csse_covid_19_data/'
                                           f'csse_covid_19_daily_reports/{fnam}'),
                      'r', encoding='utf-8-sig') as f:
                #print(fnam)
                for item in csv.DictReader(f):
                    if item.get('Province_State') in (
                        'Diamond Princess',
                        'Grand Princess',
                        'Guam',
                        'Northern Mariana Islands',
                        'Puerto Rico',
                        'Virgin Islands',
                        'American Samoa'
                    ):
                        continue  # HACK!
                    #print(item)

                    if 'Last Update' in item:
                        date = item['Last Update'].split('T')[0].split()[0]
                    else:
                        date = item['Last_Update'].split()[0]

                    try:
                        date = self.convert_date(date, formats=('%Y-%m-%d',))
                    except:
                        date = self.convert_date(date, formats=('%m/%d/%y', '%m/%d/%Y'))

                    if 'Province/State' in item:
                        province_state = item['Province/State'].strip('*')
                        country_region = item['Country/Region'].strip('*')
                    else:
                        province_state = item['Province_State'].strip('*')
                        country_region = item['Country_Region'].strip('*')

                    if item.get('Admin2'):
                        assert item['Country_Region'] == 'US', item['Country_Region']
                        region_schema = Schemas.US_COUNTY
                        region_parent = province_state
                        region_child = item['Admin2']
                    elif province_state:
                        assert not item.get('FIPS'), item['FIPS']
                        region_schema = Schemas.ADMIN_1
                        region_parent = country_region
                        region_child = province_state

                        if ', ' in region_child:
                            # e.g. 'Sonoma County, CA' in earlier versions
                            county, state_code = region_child.split(', ')
                            region_schema = Schemas.US_COUNTY
                            region_parent = 'US-'+state_code  # FIXME!! =====================================================
                            region_child = county
                    else:
                        region_schema = Schemas.ADMIN_0
                        region_parent = None
                        region_child = country_region

                    if region_parent:
                        region_parent = region_parent.strip('*').strip().replace('Mainland China', 'China')

                    if region_schema == Schemas.US_COUNTY:
                        # Convert US counties to FIPS codes
                        region_parent, region_child = get_schema_type_info(
                            region_schema
                        ).convert_parent_child(region_parent, region_child)

                        try:
                            region_child = county_to_code_map[region_parent.split('-')[-1], region_child.lower()]
                        except KeyError:
                            if (region_parent, region_child) in printed:
                                continue
                            printed.add((region_parent, region_child))
                            print(f'1111111,{region_child},{region_parent.split("-")[-1]}')
                            continue

                        if int(region_child) >= 1111111:
                            # HACK!!! =================================================================================================
                            continue

                        region_child = region_child[-3:]
                        assert len(region_child) == 3, region_child

                    if '(From' in region_child:
                        # HACK: Ignore e.g. 'Omaha, NE (From Diamond Princess)'
                        continue

                    # Normally it's ok to remove "oblast" in normalizations
                    # but "Kiev" and "Kiev Oblast" refer to different things here
                    if region_parent:
                        if region_parent.lower() == 'ukraine' and region_child.lower() == 'kiev':
                            region_parent = 'UA'
                            region_child = 'UA-30'
                        elif region_parent.lower() == 'ukraine' and region_child.lower() == 'kiev oblast':
                            region_parent = 'UA'
                            region_child = 'UA-32'

                    if item['Confirmed']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.TOTAL,
                            value=int(float(item['Confirmed'])),
                            date_updated=date,
                            source_url='JHU'  # HACK: JHU is larger than any of the other sources, so makes sense to reduce the source just for this file!
                        )
                        #if region_schema == Schemas.ADMIN_1 and r[-1].region_child.upper() == 'US-TX':
                        #    print(r[-1])
                        #    print(item)

                    if item['Deaths']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(float(item['Deaths'])),
                            date_updated=date,
                            source_url='JHU'
                        )

                    if item['Recovered']:
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.STATUS_RECOVERED,
                            value=int(float(item['Recovered'])),
                            date_updated=date,
                            source_url='JHU'
                        )

                    if item.get('Active'):
                        r.append(
                            region_schema=region_schema,
                            region_parent=region_parent,
                            region_child=region_child,
                            datatype=DataTypes.STATUS_ACTIVE,
                            value=int(float(item['Active'])),
                            date_updated=date,
                            source_url='JHU'
                        )

        return r


class WorldJHUDataAdmin0(WorldJHUData):
    SOURCE_ID = 'world_jhu_admin0'

    def __init__(self):
        WorldJHUData.__init__(self, do_update=True)

    def get_datapoints(self):
        r = []
        for i in WorldJHUData.get_datapoints(self):
            if i.region_schema == Schemas.ADMIN_0:
                r.append(i)
        return r


class WorldJHUDataAdmin1(WorldJHUData):
    SOURCE_ID = 'world_jhu_admin1'

    def __init__(self):
        WorldJHUData.__init__(self, do_update=False)

    def get_datapoints(self):
        r = []
        for i in WorldJHUData.get_datapoints(self):
            if i.region_schema == Schemas.ADMIN_1:
                r.append(i)
        return r


class WorldJHUDataAdmin2(WorldJHUData):
    SOURCE_ID = 'world_jhu_admin2'

    def __init__(self):
        WorldJHUData.__init__(self, do_update=False)

    def get_datapoints(self):
        r = []
        for i in WorldJHUData.get_datapoints(self):
            if i.region_schema in (Schemas.US_COUNTY,):
                r.append(i)
        return r


if __name__ == '__main__':
    WorldJHUData().get_datapoints()
    #pprint()
