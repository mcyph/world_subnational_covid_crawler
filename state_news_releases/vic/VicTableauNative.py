import csv
import json
import zipfile
import datetime
from os import listdir
from os.path import exists
from collections import Counter
from tableauhyperapi import HyperProcess, Connection, Telemetry

from covid_19_au_grab.overseas.URLBase import URL, URLBase
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import get_data_dir, get_package_dir
from covid_19_au_grab.geojson_data.LabelsToRegionChild import LabelsToRegionChild
from covid_19_au_grab.normalize_locality_name import normalize_locality_name
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


class VicTableauNative(URLBase):
    # https://public.tableau.com/profile/vicdhhs#!/
    SOURCE_URL = 'https://www.dhhs.vic.gov.au/coronavirus'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'vic_tableau_native'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_data_dir() / 'vic' / 'tableau_native',
             urls_dict={
                 'agegroup.json': URL('https://public.tableau.com/workbooks/Agegroup_15982346382420.twb',
                                      static_file=False),
                 'genderagegroup.json': URL('https://public.tableau.com/workbooks/GenderAgeGroup.twb',
                                            static_file=False),
                 'transmissions.json': URL('https://public.tableau.com/workbooks/Transmissions.twb',
                                           static_file=False),
                 'transmissions_over_time.json': URL('https://public.tableau.com/workbooks/Transmissionsovertime.twb',
                                                     static_file=False),
                 'active_cases.json': URL('https://public.tableau.com/workbooks/Activecases_15982341517530.twb',
                                          static_file=False),
                 'cases.json': URL('https://public.tableau.com/workbooks/Cases_15982342702770.twb',
                                   static_file=False),

                # TODO: Support healthcare workers graphs!
                 'hcw_source_infections.json': URL('https://public.tableau.com/workbooks/HCWSourceInfections.twb',
                                                   static_file=False),
                 'hcw_cases.json': URL('https://public.tableau.com/workbooks/HCWCases.twb',
                                       static_file=False),
            }
        )
        self.update()

    def get_datapoints(self):
        r = DataPointMerger()
        #return r

        for date in sorted(listdir(self.output_dir)):
            self.__unzip_date(date)

            # active_cases/Data/dash-transmission/vic-details-transmissions-pub-extract.hyper
            # cases/Data/dash-charts/vic_detailed_prep Extract_daily-pubextract.hyper
            r.extend(self.__get_genderagegroup_datapoints(date))
            r.extend(self.__get_transmissions_datapoints(date))
            r.extend(self.__get_transmissions_over_time_datapoints(date))

        return r

    def __get_genderagegroup_datapoints(self, date):
        r = []
        base_path = self.output_dir / date / 'genderagegroup'
        if not exists(str(base_path)+'.json'):
            return r

        # agegroup/Data/TableauTemp/TEMP_0cskvrs1awf0qi17eeuta10ngsof.hyper

        # Start Hyper
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            #  Connect to an existing .hyper file (CreateMode.NONE)
            with Connection(endpoint=hyper.endpoint,
                            database=base_path / 'Data/dash-gender/dpc-metrics-agegroup-gender-prep-pub-extract-h.hyper') as connection:
                keys = [
                    str(i.name).strip('"')
                    for i in connection.catalog.get_table_definition(
                        name=connection.catalog.get_table_names('Extract')[0]
                    ).columns
                ]

                out_map = {}
                with connection.execute_query('SELECT * FROM '+str(connection.catalog.get_table_names('Extract')[0])) as result:
                    for row in result:
                        map = dict(zip(keys, row))
                        date = datetime.date(
                            map['Date'].year, map['Date'].month, map['Date'].day
                        ).strftime('%Y_%m_%d')
                        #print(map)

                        if map['agegroup'].lower() == 'age unknown':
                            map['agegroup'] = 'unknown'

                        assert map['Sex'] in ('Male', 'Female', 'Not stated', 'Other'), map['Sex']
                        assert not map['Sex'] in out_map.setdefault(date, {}) \
                                                        .setdefault(map['agegroup'], {}), (map['Sex'], date)
                        out_map.setdefault(date, {}) \
                               .setdefault(map['agegroup'], {})[map['Sex']] = map

                male_cum = Counter()
                female_cum = Counter()
                both_cum = Counter()

                assert '2020_01_25' in out_map  # Make sure previous items haven't been trimmed!

                for date, agegroup_map in sorted(out_map.items()):
                    for agegroup, i_map in agegroup_map.items():
                        #print(agegroup, i_map)

                        # Make sure we don't add in totals for some other value if the format changes!
                        assert agegroup

                        if 'Male' in i_map:
                            male_cum[agegroup] += int(i_map['Male']['Cases'] or 0)
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                date_updated=date,
                                agerange=agegroup,
                                datatype=DataTypes.TOTAL_MALE,
                                value=male_cum[agegroup],  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                date_updated=date,
                                agerange=agegroup,
                                datatype=DataTypes.STATUS_ACTIVE_MALE,
                                value=int(i_map['Male']['Active_Cases'] or 0),  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))

                        if 'Female' in i_map:
                            female_cum[agegroup] += int(i_map['Female']['Cases'] or 0)
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                date_updated=date,
                                agerange=agegroup,
                                datatype=DataTypes.TOTAL_FEMALE,
                                value=female_cum[agegroup],  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                date_updated=date,
                                agerange=agegroup,
                                datatype=DataTypes.STATUS_ACTIVE_FEMALE,
                                value=int(i_map['Female']['Active_Cases'] or 0),  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))

                        total = 0
                        active = 0

                        if 'Male' in i_map:
                            total += int(i_map['Male']['Cases'] or 0)
                            active += int(i_map['Male']['Active_Cases'] or 0)

                        if 'Female' in i_map:
                            total += int(i_map['Female']['Cases'] or 0)
                            active += int(i_map['Female']['Active_Cases'] or 0)

                        if 'Other' in i_map:
                            total += int(i_map['Other']['Cases'] or 0)
                            active += int(i_map['Other']['Active_Cases'] or 0)

                        if 'Not stated' in i_map:
                            total += int(i_map['Not stated']['Cases'] or 0)
                            active += int(i_map['Not stated']['Active_Cases'] or 0)

                        both_cum[agegroup] += total

                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='au',
                            region_child='au-vic',
                            date_updated=date,
                            agerange=agegroup,
                            datatype=DataTypes.TOTAL,
                            value=both_cum[agegroup],
                            source_url=self.SOURCE_URL,
                            source_id=self.SOURCE_ID
                        ))
                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='au',
                            region_child='au-vic',
                            date_updated=date,
                            agerange=agegroup,
                            datatype=DataTypes.STATUS_ACTIVE,
                            value=active,
                            source_url=self.SOURCE_URL,
                            source_id=self.SOURCE_ID
                        ))

        return r

    def __get_transmissions_datapoints(self, date):
        r = []
        base_path = self.output_dir / date / 'transmissions'
        # Data/dash-charts/vic-details-transmissions-prep Extract.hyper

        # Start Hyper
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            #  Connect to an existing .hyper file (CreateMode.NONE)
            path = base_path / 'Data/dash-charts/vic-details-transmissions-prep Extract.hyper'
            if not path.exists():
                path = base_path / 'Data/dash-transmission/vic-details-transmissions-pub-extract.hyper'
            if not path.exists():
                path = base_path / 'Data/TableauTemp/'
                path = list(path.glob('*.hyper'))[0]

            #print("Opening:", path)

            with Connection(endpoint=hyper.endpoint,
                            database=path) as connection:
                sources = {
                    'Acquired in Australia, unknown source': DataTypes.SOURCE_COMMUNITY_ACTIVE,
                    'Contact with a confirmed case': DataTypes.SOURCE_CONFIRMED_ACTIVE,
                    'Travel overseas': DataTypes.SOURCE_OVERSEAS_ACTIVE,
                    'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION_ACTIVE,
                }
                #print(connection.catalog.get_table_names('Extract'))

                with connection.execute_query(
                        'SELECT * FROM ' + str(connection.catalog.get_table_names('Extract')[0])) as result:
                    for row in result:
                        #print(row)
                        if len(row) == 3:
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                agerange=None,
                                date_updated=datetime.date(row[-1].year, row[-1].month, row[-1].day).strftime(
                                    '%Y_%m_%d'),
                                datatype=sources[row[0]],
                                value=int(row[1] or 0),  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                        else:
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                agerange=None,
                                date_updated=datetime.date(row[-2].year, row[-2].month, row[-2].day).strftime('%Y_%m_%d'),
                                datatype=sources[row[0]],
                                value=int(row[1] or 0),  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))

        return r

    def __get_transmissions_over_time_datapoints(self, date):
        r = []
        base_path = self.output_dir / date / 'transmissions_over_time'
        # Data/dash-transmission/vic-details-transmissions-pub-extract-lv.hyper
        # Data/test-download/vic-details-transmissions-prep-xl-pub-extract.hyper

        # Start Hyper
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            #  Connect to an existing .hyper file (CreateMode.NONE)

            path = base_path / 'Data/dash-transmission/vic-details-transmissions-pub-extract-lv.hyper'
            if not path.exists():
                path = base_path / 'Data/dash-transmission/vic-details-transmissions-prep.hyper'
            if not path.exists():
                path = base_path / 'Data/dash-transmission/vic-details-transmissions-prep-xl-pub-extract.hyper'

            with Connection(endpoint=hyper.endpoint,
                            database=path) as connection:

                sources = {
                    'Acquired in Australia, unknown source': DataTypes.SOURCE_COMMUNITY_ACTIVE,
                    'Contact with a confirmed case': DataTypes.SOURCE_CONFIRMED_ACTIVE,
                    'Travel overseas': DataTypes.SOURCE_OVERSEAS_ACTIVE,
                    'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION_ACTIVE,
                }

                with connection.execute_query(
                        'SELECT * FROM ' + str(connection.catalog.get_table_names('Extract')[0])) as result:
                    for row in result:
                        #print(row)
                        if len(row) == 3:
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                agerange=None,
                                date_updated=datetime.date(row[-1].year, row[-1].month, row[-1].day).strftime(
                                    '%Y_%m_%d'),
                                datatype=sources[row[0]],
                                value=int(row[1] or 0),  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))
                        else:
                            r.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='au',
                                region_child='au-vic',
                                agerange=None,
                                date_updated=datetime.date(row[-2].year, row[-2].month, row[-2].day).strftime('%Y_%m_%d'),
                                datatype=sources[row[0]],
                                value=int(row[1] or 0),  # WARNING!!
                                source_url=self.SOURCE_URL,
                                source_id=self.SOURCE_ID
                            ))

        return r

    def __unzip_date(self, date):
        for zip_fnam in (
            'agegroup.json',
            'genderagegroup.json',
            'transmissions.json',
            'transmissions_over_time.json',
            'active_cases.json',
            'cases.json'
        ):
            path = self.output_dir / date / zip_fnam
            if exists(path) and not exists(str(path)[:-5]):
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(str(path)[:-5])


if __name__ == '__main__':
    from pprint import pprint
    datapoints = VicTableauNative().get_datapoints()
    pprint(datapoints)
