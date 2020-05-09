import json
import glob
import datetime
from os import listdir
from os.path import dirname, exists

from covid_19_au_grab.URLArchiver import (
    URLArchiver
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_LGA,
    DT_TOTAL_FEMALE, DT_TOTAL_MALE,
    DT_TESTS_TOTAL, DT_TOTAL, DT_NEW,
    DT_STATUS_DEATHS, DT_STATUS_RECOVERED,
    DT_STATUS_HOSPITALIZED,
    DT_STATUS_ACTIVE
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.get_package_dir import (
    get_data_dir
)


SOURCE_URL = 'https://experience.arcgis.com/experience/359bca83a1264e3fb8d3b6f0a028d768'


def get_wa_dash_datapoints():
    inst = WARegionsProcess()
    r = []
    r.extend(inst.get_new_datapoints())
    r.extend(inst.get_old_datapoints())
    return r


class WARegionsProcess:
    def get_old_datapoints(self):
        r = []
        wa_custom_map_ua = URLArchiver(f'wa/custom_map')

        for period in wa_custom_map_ua.iter_periods():
            for subperiod_id, subdir in wa_custom_map_ua.iter_paths_for_period(period):
                if exists(
                    f'wa/custom_map/'+subdir.rpartition('-')[0]+f'-{subperiod_id + 1}'
                ):
                    # Only add the most recent revision!
                    continue

                for path in glob.glob(dirname(wa_custom_map_ua.get_path(subdir))+'/*'):
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        json_text = f.read()

                    data = json.loads(json_text)
                    cbr = self.get_regions_data(subdir.split('-')[0], data)
                    if cbr:
                        r.extend(cbr)
        return r

    def get_new_datapoints(self):
        r = []
        dir_ = get_data_dir() / 'wa' / 'custom_dash'

        for subdir in listdir(dir_):
            period = subdir.split('-')[0]
            next_id = int(subdir.split('-')[-1])+1

            if exists(f'{dir_}/{period}-{next_id}'):
                # Don't use if there's a newer version!
                continue

            for fn, fnam_prefix in (
                (self.get_regions_data, 'regions'),
                (self.get_source_of_infection, 'infection_source'),
                (self.get_other_stats, 'other_stats'),
                (self.get_mf_balance, 'mf_balance'),
                (self.get_age_balance, 'age_balance')
            ):
                path = f'{dir_}/{subdir}/{fnam_prefix}.json'
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    data = json.loads(f.read())
                r.extend(fn(period, data))

        return r

    def get_regions_data(self, period, data):
        r = []
        for feature_dict in data['features']:
            """
            {
                "attributes":{
                    "OBJECTID":145,
                    "LGA_CODE19":"50080",
                    "LGA_NAME19":"Albany (C)",
                    "AREASQKM19":4310.8905,
                    "Metro_WACHS":"WACHS",
                    "Pop65_plus":7781,
                    "Pop_total_18":37826,
                    "Confirmed_cases":6,
                    "Classification":"6 - 10",
                    "Shape__Area":6399054898.15234,
                    "Shape__Length":910942.011045383,
                    "LGA_Name_Full":"City of Albany  "
                }, ...
            }
            """

            attributes = feature_dict['attributes']
            if attributes.get('exceedslimit'):
                continue
            elif len(attributes) == 1:
                continue

            if 'Confirmed_cases' in feature_dict:
                value = attributes['Confirmed_cases']
            else:
                try:
                    value = int(attributes['PopUpLabel'])
                except (ValueError, KeyError, TypeError):
                    cls = attributes['Classification'].strip()
                    if cls == 'No case':
                        continue
                    elif ' - ' in cls:
                        from_num, to_num = cls.split(' - ')
                        from_num = int(from_num)
                        to_num = int(to_num)
                        value = (from_num + to_num) // 2
                    else:
                        try:
                            value = int(cls.strip('+'))
                        except ValueError:
                            import traceback
                            traceback.print_exc()
                            continue  # WARNING!!! ============================================================================

            num = DataPoint(
                schema=SCHEMA_LGA,
                datatype=DT_TOTAL,
                region=attributes['LGA_NAME19'].split('(')[0].strip(),
                value=value,
                date_updated=period,
                source_url='https://experience.arcgis.com/experience/359bca83a1264e3fb8d3b6f0a028d768'
            )
            r.append(num)
        return r

    def __get_date(self, ts):
        dt = datetime.datetime.fromtimestamp(ts/1000)
        return dt.strftime("%Y_%m_%d")

    def get_source_of_infection(self, period, data):
        r = []
        for feature in data['features']:
            attribute = feature['attributes']
            dt = self.__get_date(attribute['Date'])

            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['Total_Confirmed'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            # WARNING: Cruise ships isn't included in overseas here!
            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['Oversea_Travel']+
                      attribute['Cruise_Ships'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['Cruise_Ships'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['Close_Contact'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['Unknown'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['Interstate'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            #r.append(DataPoint(
            #    datatype=DT_TOTAL,
            #    value=attribute['Pending'],
            #    date_updated=dt,
            #    source_url=SOURCE_URL
            #))
            r.append(DataPoint(
                datatype=DT_TESTS_TOTAL,
                value=attribute['Total_Confirmed']+
                      attribute['Negative_results'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
        return r

    def get_other_stats(self, period, data):
        r = []
        for feature in data['features']:
            attribute = feature['attributes']
            dt = self.__get_date(attribute['date'])
            
            r.append(DataPoint(
                datatype=DT_NEW,
                value=attribute['new_cases'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL,
                value=attribute['total_cases'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_STATUS_RECOVERED,
                value=attribute['total_recovered'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_STATUS_DEATHS,
                value=attribute['total_death'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_STATUS_ACTIVE,
                value=attribute['existing_cases'],
                date_updated=dt,
                source_url=SOURCE_URL
            ))
            #r.append(DataPoint(
            #    datatype=DT_TESTS_TOTAL,
            #    value=attribute['total_ruledout'],
            #    date_updated=dt,
            #    source_url=SOURCE_URL
            #))
            r.append(DataPoint(
                datatype=DT_STATUS_HOSPITALIZED,
                value=attribute['total_hospitalised'] or 0,
                date_updated=dt,
                source_url=SOURCE_URL
            ))
        return r

    def get_mf_balance(self, period, data):
        r = []
        for feature in data['features']:
            attribute = feature['attributes']
            r.append(DataPoint(
                datatype=DT_TOTAL_MALE,
                value=attribute['Male'],
                date_updated=period,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL_FEMALE,
                value=attribute['Female'],
                date_updated=period,
                source_url=SOURCE_URL
            ))
        return r

    def get_age_balance(self, period, data):
        r = []
        for feature in data['features']:
            attribute = feature['attributes']
            r.append(DataPoint(
                datatype=DT_TOTAL,
                agerange=attribute['Age_Group'],
                value=attribute['Total'],
                date_updated=period,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL_MALE,
                agerange=attribute['Age_Group'],
                value=attribute['Male'],
                date_updated=period,
                source_url=SOURCE_URL
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL_FEMALE,
                agerange=attribute['Age_Group'],
                value=attribute['Female'],
                date_updated=period,
                source_url=SOURCE_URL
            ))
        return r


null = true = false = 0
{"objectIdFieldName":"FID",
 "uniqueIdField":{"name":"FID","isSystemMaintained":true},
 "globalIdFieldName":"",
 "fields":[{"name":"Date","type":"esriFieldTypeDate","alias":"Date","sqlType":"sqlTypeTimestamp2","length":8,"domain":null,"defaultValue":null},
           {"name":"Total_Confirmed","type":"esriFieldTypeInteger","alias":"Total_Confirmed","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Oversea_Travel","type":"esriFieldTypeInteger","alias":"Overseas_Travel","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Cruise_Ships","type":"esriFieldTypeInteger","alias":"Cruise_Ships","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Close_Contact","type":"esriFieldTypeInteger","alias":"Close_Contact","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Unknown","type":"esriFieldTypeInteger","alias":"Unknown","sqlType":"sqlTypeFloat","domain":null,"defaultValue":null},
           {"name":"Interstate","type":"esriFieldTypeInteger","alias":"Interstate","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Pending","type":"esriFieldTypeInteger","alias":"Pending","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Recovered","type":"esriFieldTypeInteger","alias":"Recovered","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Negative_results","type":"esriFieldTypeInteger","alias":"Negative_results","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"FID","type":"esriFieldTypeOID","alias":"FID","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null}],
 "features":[{"attributes":{"Date":1583020800000,
                            "Total_Confirmed":2,
                            "Oversea_Travel":0,
                            "Cruise_Ships":2,
                            "Close_Contact":0,
                            "Unknown":0,
                            "Interstate":0,
                            "Pending":0,
                            "Recovered":0,
                            "Negative_results":594,
                            "FID":1}},
             {"attributes":{"Date":1583107200000,"Total_Confirmed":2,"Oversea_Travel":0,"Cruise_Ships":2,"Close_Contact":0,"Unknown":0,"Interstate":0,"Pending":0,"Recovered":0,"Negative_results":682,"FID":2}},
             ]}
URL_SOURCE_OF_INFECTION = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/Epidemic_curve_date_new_view_layer/FeatureServer/0/query?f=json&where=Total_Confirmed%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&outSR=102100&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'

{"objectIdFieldName":"OBJECTID",
 "uniqueIdField":{"name":"OBJECTID","isSystemMaintained":true},
 "globalIdFieldName":"GlobalID",
 "fields":[{"name":"OBJECTID","type":"esriFieldTypeOID","alias":"OBJECTID","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"date","type":"esriFieldTypeDate","alias":"date","sqlType":"sqlTypeOther","length":8,"domain":null,"defaultValue":null},
           {"name":"new_cases","type":"esriFieldTypeInteger","alias":"new_cases","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"total_cases","type":"esriFieldTypeInteger","alias":"total_cases","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"total_recovered","type":"esriFieldTypeInteger","alias":"total_recovered","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"total_death","type":"esriFieldTypeInteger","alias":"total_death","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"existing_cases","type":"esriFieldTypeInteger","alias":"existing_cases","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"total_ruledout","type":"esriFieldTypeDouble","alias":"total_ruledout","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"total_hospitalised","type":"esriFieldTypeInteger","alias":"total_hospitalised","sqlType":"sqlTypeOther","domain":null,"defaultValue":null},
           {"name":"GlobalID","type":"esriFieldTypeGlobalID","alias":"GlobalID","sqlType":"sqlTypeOther","length":38,"domain":null},
           {"name":"CreationDate","type":"esriFieldTypeDate","alias":"CreationDate","sqlType":"sqlTypeOther","length":8,"domain":null,"defaultValue":null},
           {"name":"Creator","type":"esriFieldTypeString","alias":"Creator","sqlType":"sqlTypeOther","length":128,"domain":null,"defaultValue":null},
           {"name":"EditDate","type":"esriFieldTypeDate","alias":"EditDate","sqlType":"sqlTypeOther","length":8,"domain":null,"defaultValue":null},
           {"name":"Editor","type":"esriFieldTypeString","alias":"Editor","sqlType":"sqlTypeOther","length":128,"domain":null,"defaultValue":null}],
 "features":[{"attributes":{"OBJECTID":1,
                            "date":1582243200000,
                            "new_cases":1,
                            "total_cases":1,
                            "total_recovered":0,
                            "total_death":0,
                            "existing_cases":1,
                            "total_ruledout":204,
                            "total_hospitalised":0,
                            "GlobalID":"2d271dcd-e3b3-4ddc-a751-e9864d03d766",
                            "CreationDate":1586412449426,
                            "Creator":"ting.lin_DoHWA",
                            "EditDate":1586576652796,
                            "Editor":"DoHArcGIS"}},
             {"attributes":{"OBJECTID":2,
                            "date":1582329600000,
                            "new_cases":0,
                            "total_cases":1,
                            "total_recovered":0,
                            "total_death":0,
                            "existing_cases":1,
                            "total_ruledout":246,"total_hospitalised":0,"GlobalID":"e832bdee-9f70-4e3d-8386-871347ffe763","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":3,"date":1582416000000,"new_cases":0,"total_cases":1,"total_recovered":0,"total_death":0,"existing_cases":1,"total_ruledout":256,"total_hospitalised":0,"GlobalID":"e4830152-3f32-46cf-a48a-9355963c72a8","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":4,"date":1582502400000,"new_cases":0,"total_cases":1,"total_recovered":0,"total_death":0,"existing_cases":1,"total_ruledout":289,"total_hospitalised":0,"GlobalID":"96fe1c47-4bd7-4a1d-9d64-16007b956c97","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":5,"date":1582588800000,"new_cases":0,"total_cases":1,"total_recovered":0,"total_death":0,"existing_cases":1,"total_ruledout":325,"total_hospitalised":0,"GlobalID":"2da5d773-8ca5-4aa0-9252-4aea33741c67","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":6,"date":1582675200000,"new_cases":0,"total_cases":1,"total_recovered":0,"total_death":0,"existing_cases":1,"total_ruledout":398,"total_hospitalised":0,"GlobalID":"2e86379d-c98a-4f26-977f-831d3e039828","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":7,"date":1582761600000,"new_cases":0,"total_cases":1,"total_recovered":0,"total_death":0,"existing_cases":1,"total_ruledout":453,"total_hospitalised":0,"GlobalID":"76f9927d-703b-44fb-bddb-8802db0ec232","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":8,"date":1582848000000,"new_cases":1,"total_cases":2,"total_recovered":0,"total_death":0,"existing_cases":2,"total_ruledout":511,"total_hospitalised":1,"GlobalID":"6a704093-a2e6-436e-83bd-6fdc3c113e6c","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":9,"date":1582934400000,"new_cases":0,"total_cases":2,"total_recovered":0,"total_death":0,"existing_cases":2,"total_ruledout":566,"total_hospitalised":1,"GlobalID":"7bfd25bd-1c29-4088-8829-139730cb5a38","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":10,"date":1583020800000,"new_cases":0,"total_cases":2,"total_recovered":0,"total_death":1,"existing_cases":2,"total_ruledout":594,"total_hospitalised":1,"GlobalID":"3fa25ec7-8808-46fa-b025-1a371efac807","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":11,"date":1583107200000,"new_cases":0,"total_cases":2,"total_recovered":0,"total_death":1,"existing_cases":2,"total_ruledout":682,"total_hospitalised":1,"GlobalID":"6f270149-a2cb-4581-ad7a-7e7a58115d67","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":12,"date":1583193600000,"new_cases":0,"total_cases":2,"total_recovered":0,"total_death":1,"existing_cases":2,"total_ruledout":713,"total_hospitalised":1,"GlobalID":"42277a9e-c837-4c43-a714-4ff56a49589a","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":13,"date":1583280000000,"new_cases":0,"total_cases":2,"total_recovered":0,"total_death":1,"existing_cases":2,"total_ruledout":733,"total_hospitalised":1,"GlobalID":"0ceeb40e-dbc0-419e-96ec-6c02f98f8407","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":14,"date":1583366400000,"new_cases":1,"total_cases":2,"total_recovered":0,"total_death":1,"existing_cases":3,"total_ruledout":973,"total_hospitalised":1,"GlobalID":"4f6a321a-4a66-4c99-9f04-899ef88d8f48","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":15,"date":1583452800000,"new_cases":0,"total_cases":3,"total_recovered":0,"total_death":1,"existing_cases":3,"total_ruledout":1110,"total_hospitalised":1,"GlobalID":"ff7bedf7-0569-4430-9797-31edaf8f0b2d","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":16,"date":1583539200000,"new_cases":0,"total_cases":3,"total_recovered":0,"total_death":1,"existing_cases":3,"total_ruledout":1454,"total_hospitalised":1,"GlobalID":"54948aea-a505-4d4a-9a11-8e1a34702587","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":17,"date":1583625600000,"new_cases":1,"total_cases":4,"total_recovered":1,"total_death":1,"existing_cases":3,"total_ruledout":1665,"total_hospitalised":0,"GlobalID":"8f86f0a7-d79e-422f-a9bf-b8c419f25f74","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":18,"date":1583712000000,"new_cases":2,"total_cases":6,"total_recovered":1,"total_death":1,"existing_cases":4,"total_ruledout":1796,"total_hospitalised":0,"GlobalID":"4060e5c3-720a-4aaa-8ffa-7d627dce40e1","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":19,"date":1583798400000,"new_cases":0,"total_cases":6,"total_recovered":1,"total_death":1,"existing_cases":4,"total_ruledout":1874,"total_hospitalised":0,"GlobalID":"888e9911-3f75-4b4e-8f42-d9847a3b6d8d","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":20,"date":1583884800000,"new_cases":3,"total_cases":9,"total_recovered":1,"total_death":1,"existing_cases":7,"total_ruledout":2014,"total_hospitalised":0,"GlobalID":"cc84acca-dc38-4ac5-9562-31f72200e3e2","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":21,"date":1583971200000,"new_cases":0,"total_cases":9,"total_recovered":1,"total_death":1,"existing_cases":7,"total_ruledout":2188,"total_hospitalised":0,"GlobalID":"9a691305-25da-47fb-8a07-d8d8c77976bd","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":22,"date":1584057600000,"new_cases":5,"total_cases":14,"total_recovered":1,"total_death":1,"existing_cases":12,"total_ruledout":3788,"total_hospitalised":0,"GlobalID":"30cb4555-02cd-4502-81b9-df54b3206396","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":23,"date":1584144000000,"new_cases":3,"total_cases":17,"total_recovered":1,"total_death":1,"existing_cases":15,"total_ruledout":4806,"total_hospitalised":0,"GlobalID":"9c34f316-bee2-4142-90e3-a910f15868a0","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":24,"date":1584230400000,"new_cases":0,"total_cases":17,"total_recovered":1,"total_death":1,"existing_cases":15,"total_ruledout":5424,"total_hospitalised":0,"GlobalID":"46fb23c4-1314-4a1c-9326-9b736a9098d0","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":25,"date":1584316800000,"new_cases":10,"total_cases":28,"total_recovered":1,"total_death":1,"existing_cases":26,"total_ruledout":5878,"total_hospitalised":1,"GlobalID":"ee716266-d62d-42f6-9bf1-695085daddf1","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":26,"date":1584403200000,"new_cases":3,"total_cases":31,"total_recovered":1,"total_death":1,"existing_cases":29,"total_ruledout":6582,"total_hospitalised":1,"GlobalID":"289503fa-11b3-4ef6-bfb7-5b5bab8d35cc","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":27,"date":1584489600000,"new_cases":4,"total_cases":35,"total_recovered":1,"total_death":1,"existing_cases":33,"total_ruledout":7039,"total_hospitalised":1,"GlobalID":"27bab848-ea21-42be-b336-655ef7193313","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":28,"date":1584576000000,"new_cases":17,"total_cases":52,"total_recovered":1,"total_death":1,"existing_cases":50,"total_ruledout":7596,"total_hospitalised":1,"GlobalID":"765b75e7-df1c-4cd7-a4ba-435de375bbf4","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":29,"date":1584662400000,"new_cases":12,"total_cases":64,"total_recovered":1,"total_death":1,"existing_cases":62,"total_ruledout":8539,"total_hospitalised":3,"GlobalID":"4aec1585-305f-43d1-af1c-34d4e28d8c1c","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":30,"date":1584748800000,"new_cases":26,"total_cases":90,"total_recovered":1,"total_death":1,"existing_cases":88,"total_ruledout":9130,"total_hospitalised":4,"GlobalID":"0f96986d-8814-4b9a-bc54-e76512e99a83","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":31,"date":1584835200000,"new_cases":30,"total_cases":120,"total_recovered":1,"total_death":1,"existing_cases":118,"total_ruledout":9498,"total_hospitalised":4,"GlobalID":"1690c28c-b597-4f67-a65c-4ed6ec099be1","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":32,"date":1584921600000,"new_cases":20,"total_cases":140,"total_recovered":1,"total_death":1,"existing_cases":138,"total_ruledout":9998,"total_hospitalised":7,"GlobalID":"ca351d0e-6c88-4cab-8343-6c03e00ee930","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":33,"date":1585008000000,"new_cases":35,"total_cases":175,"total_recovered":6,"total_death":1,"existing_cases":168,"total_ruledout":10353,"total_hospitalised":11,"GlobalID":"e982155d-cac7-4fe0-8dd9-215a5a213202","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":34,"date":1585094400000,"new_cases":30,"total_cases":205,"total_recovered":6,"total_death":1,"existing_cases":198,"total_ruledout":10783,"total_hospitalised":11,"GlobalID":"210f8361-022b-4601-962c-2365cafefbca","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":35,"date":1585180800000,"new_cases":27,"total_cases":232,"total_recovered":6,"total_death":1,"existing_cases":225,"total_ruledout":10783,"total_hospitalised":15,"GlobalID":"a4400c1e-a168-413f-9746-259908e64a0f","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":36,"date":1585267200000,"new_cases":23,"total_cases":255,"total_recovered":23,"total_death":2,"existing_cases":230,"total_ruledout":11288,"total_hospitalised":15,"GlobalID":"d1b3b591-e7b8-41f4-ba68-4302b4946e27","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":37,"date":1585353600000,"new_cases":23,"total_cases":278,"total_recovered":28,"total_death":2,"existing_cases":253,"total_ruledout":12693,"total_hospitalised":15,"GlobalID":"e5f1a5fe-6730-4dc3-822d-885f313d2b1d","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":38,"date":1585440000000,"new_cases":33,"total_cases":311,"total_recovered":28,"total_death":2,"existing_cases":286,"total_ruledout":13337,"total_hospitalised":18,"GlobalID":"c0af6d88-8f13-4212-914b-f99ceaa242d3","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":39,"date":1585526400000,"new_cases":44,"total_cases":355,"total_recovered":41,"total_death":2,"existing_cases":330,"total_ruledout":13833,"total_hospitalised":29,"GlobalID":"b3206615-ffc3-4be0-a391-2d038f578a22","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":40,"date":1585612800000,"new_cases":9,"total_cases":364,"total_recovered":41,"total_death":2,"existing_cases":339,"total_ruledout":13833,"total_hospitalised":29,"GlobalID":"6fa22df3-91e7-4084-bc32-fb1307c1a1c8","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":42,"date":1585699200000,"new_cases":28,"total_cases":392,"total_recovered":64,"total_death":2,"existing_cases":326,"total_ruledout":15130,"total_hospitalised":null,"GlobalID":"0db39e47-1b7d-40bf-bfac-f5e696a41eed","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":43,"date":1585785600000,"new_cases":8,"total_cases":400,"total_recovered":92,"total_death":2,"existing_cases":306,"total_ruledout":15790,"total_hospitalised":null,"GlobalID":"2eb95c58-d5d6-4c91-857f-f404ac4ff1a2","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":44,"date":1585872000000,"new_cases":22,"total_cases":422,"total_recovered":92,"total_death":3,"existing_cases":327,"total_ruledout":16022,"total_hospitalised":null,"GlobalID":"5c74099f-3cda-4dda-9bd1-1201283090ab","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":45,"date":1585958400000,"new_cases":14,"total_cases":436,"total_recovered":92,"total_death":3,"existing_cases":341,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"09fa50ab-782f-405e-a29d-94f36fa1b436","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":46,"date":1586044800000,"new_cases":17,"total_cases":453,"total_recovered":148,"total_death":3,"existing_cases":302,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"7353d2d4-2e99-43a9-91e8-57da803ab881","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":47,"date":1586131200000,"new_cases":7,"total_cases":460,"total_recovered":162,"total_death":4,"existing_cases":294,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"b689785b-7663-41ad-a79d-12268b76f78e","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":48,"date":1586217600000,"new_cases":10,"total_cases":470,"total_recovered":170,"total_death":6,"existing_cases":284,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"f9c62cb8-1818-469b-b093-15ad281dea49","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":49,"date":1586304000000,"new_cases":11,"total_cases":481,"total_recovered":170,"total_death":6,"existing_cases":305,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"faa733fe-7b3c-4394-8a1d-aecad2260ae6","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":50,"date":1586390400000,"new_cases":14,"total_cases":495,"total_recovered":187,"total_death":6,"existing_cases":302,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"d50ce52c-d946-4158-9a7d-c53af3fa6988","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":51,"date":1586476800000,"new_cases":11,"total_cases":506,"total_recovered":203,"total_death":6,"existing_cases":297,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"c6e7d140-955b-420f-a5c9-af9825a4f013","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":52,"date":1586563200000,"new_cases":8,"total_cases":514,"total_recovered":216,"total_death":6,"existing_cases":292,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"01bffd97-126d-4a79-8900-3b3d417f964b","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586576652796,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":53,"date":1586649600000,"new_cases":3,"total_cases":517,"total_recovered":239,"total_death":6,"existing_cases":272,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"75cf98cf-ab1b-4c71-888a-57a15e5920cc","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586668040871,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":54,"date":1586736000000,"new_cases":6,"total_cases":523,"total_recovered":251,"total_death":6,"existing_cases":266,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"996374c4-b08c-4871-8f5a-20f347d7e9f0","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586750921247,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":55,"date":1586822400000,"new_cases":4,"total_cases":527,"total_recovered":296,"total_death":6,"existing_cases":225,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"1bc902f8-dcee-4b22-9605-14b595e588e0","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586828651346,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":56,"date":1586908800000,"new_cases":5,"total_cases":532,"total_recovered":338,"total_death":6,"existing_cases":194,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"062a23b5-360e-495a-b94c-e1090d2db6cc","CreationDate":1586412449426,"Creator":"ting.lin_DoHWA","EditDate":1586923825362,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":58,"date":1586995200000,"new_cases":3,"total_cases":535,"total_recovered":340,"total_death":6,"existing_cases":189,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"b0fafca6-2bbd-4f90-a1ec-90d03ea451ab","CreationDate":1587005796746,"Creator":"ting.lin_DoHWA","EditDate":1587005870884,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":59,"date":1587081600000,"new_cases":6,"total_cases":541,"total_recovered":376,"total_death":7,"existing_cases":165,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"a8a5232e-0641-46be-8eb7-ba141a8391aa","CreationDate":1587096030414,"Creator":"ting.lin_DoHWA","EditDate":1587096053712,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":60,"date":1587168000000,"new_cases":3,"total_cases":544,"total_recovered":388,"total_death":7,"existing_cases":156,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"e2a699f0-8f61-4a61-94b9-3d086cdab710","CreationDate":1587184262701,"Creator":"ting.lin_DoHWA","EditDate":1587184301853,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":61,"date":1587254400000,"new_cases":1,"total_cases":545,"total_recovered":426,"total_death":7,"existing_cases":112,"total_ruledout":28343,"total_hospitalised":null,"GlobalID":"028c3551-c61d-42b0-a347-9832f602b7df","CreationDate":1587269147283,"Creator":"DoHArcGIS","EditDate":1587269410701,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":62,"date":1587340800000,"new_cases":0,"total_cases":545,"total_recovered":435,"total_death":7,"existing_cases":103,"total_ruledout":28924,"total_hospitalised":null,"GlobalID":"2199d6a6-30f7-4b78-952a-082aaa45b20a","CreationDate":1587269157151,"Creator":"DoHArcGIS","EditDate":1587522424224,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":63,"date":1587427200000,"new_cases":1,"total_cases":546,"total_recovered":443,"total_death":7,"existing_cases":96,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"50addbf6-7408-495a-96fd-a2bdbde9842d","CreationDate":1587269167752,"Creator":"DoHArcGIS","EditDate":1587522416803,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":64,"date":1587513600000,"new_cases":0,"total_cases":546,"total_recovered":451,"total_death":7,"existing_cases":88,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"df1b41e8-3451-400f-8a67-bc61b5e52350","CreationDate":1587269176096,"Creator":"DoHArcGIS","EditDate":1587522406050,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":65,"date":1587600000000,"new_cases":0,"total_cases":546,"total_recovered":458,"total_death":7,"existing_cases":81,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"b8ddaa89-ec3a-42d6-a9ef-96efbb4d387c","CreationDate":1587269184161,"Creator":"DoHArcGIS","EditDate":1587609514877,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":66,"date":1587686400000,"new_cases":2,"total_cases":548,"total_recovered":464,"total_death":7,"existing_cases":77,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"1cbbecb5-e6d8-4e9d-acbc-3c3000bf8b07","CreationDate":1587269194852,"Creator":"DoHArcGIS","EditDate":1587698709897,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":67,"date":1587772800000,"new_cases":1,"total_cases":549,"total_recovered":478,"total_death":8,"existing_cases":63,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"19143107-d8a7-46d8-85dc-aaefbb6a8242","CreationDate":1587269202465,"Creator":"DoHArcGIS","EditDate":1587787835520,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":68,"date":1587859200000,"new_cases":0,"total_cases":549,"total_recovered":486,"total_death":8,"existing_cases":55,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"d4f41a24-5aca-4562-b8df-054ad45d108d","CreationDate":1587269209272,"Creator":"DoHArcGIS","EditDate":1587868928340,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":69,"date":1587945600000,"new_cases":0,"total_cases":549,"total_recovered":486,"total_death":8,"existing_cases":55,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"4287eda7-4f9d-4104-8699-a0cc753e3cee","CreationDate":1587269215582,"Creator":"DoHArcGIS","EditDate":1587960949219,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":70,"date":1588032000000,"new_cases":1,"total_cases":550,"total_recovered":495,"total_death":8,"existing_cases":47,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"bab9788a-d2f8-49a3-aaf5-a132db4c696e","CreationDate":1587269222460,"Creator":"DoHArcGIS","EditDate":1588133004220,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":71,"date":1588118400000,"new_cases":1,"total_cases":551,"total_recovered":500,"total_death":8,"existing_cases":43,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"3eb0051b-f64a-4334-ba91-301b9ee102a6","CreationDate":1587269229696,"Creator":"DoHArcGIS","EditDate":1588132973544,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":72,"date":1588204800000,"new_cases":0,"total_cases":551,"total_recovered":507,"total_death":8,"existing_cases":36,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"e3202d46-b758-46d2-a58f-88bdb2997394","CreationDate":1587269236999,"Creator":"DoHArcGIS","EditDate":1588217154919,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":73,"date":1588291200000,"new_cases":0,"total_cases":551,"total_recovered":511,"total_death":8,"existing_cases":32,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"f79c774d-1d76-4698-a7de-1ffb110156ae","CreationDate":1587269246840,"Creator":"DoHArcGIS","EditDate":1588298341404,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":74,"date":1588377600000,"new_cases":0,"total_cases":551,"total_recovered":520,"total_death":8,"existing_cases":23,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"dcbb7b64-6613-4011-9b33-ba18775b16d8","CreationDate":1587269254127,"Creator":"DoHArcGIS","EditDate":1588402993262,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":75,"date":1588464000000,"new_cases":0,"total_cases":551,"total_recovered":523,"total_death":9,"existing_cases":19,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"3d8bd333-5baa-4254-934f-7f39d94e54aa","CreationDate":1587269262493,"Creator":"DoHArcGIS","EditDate":1588482599452,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":76,"date":1588550400000,"new_cases":0,"total_cases":551,"total_recovered":527,"total_death":9,"existing_cases":15,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"f3bc8361-7045-45db-ab43-5d38bd916727","CreationDate":1587269271430,"Creator":"DoHArcGIS","EditDate":1588559935694,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":77,"date":1588636800000,"new_cases":0,"total_cases":551,"total_recovered":528,"total_death":9,"existing_cases":14,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"767dded5-fd8e-4777-9e33-e115b95374e9","CreationDate":1587269279224,"Creator":"DoHArcGIS","EditDate":1588648957028,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":78,"date":1588723200000,"new_cases":0,"total_cases":551,"total_recovered":528,"total_death":9,"existing_cases":14,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"3f30c097-1c87-429b-9157-ca23672346e7","CreationDate":1587269285159,"Creator":"DoHArcGIS","EditDate":1588736433199,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":79,"date":1588809600000,"new_cases":0,"total_cases":551,"total_recovered":531,"total_death":9,"existing_cases":11,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"c67fb483-565e-4f15-a799-9867c1ba6e9c","CreationDate":1587269293622,"Creator":"DoHArcGIS","EditDate":1588818233288,"Editor":"DoHArcGIS"}},{"attributes":{"OBJECTID":80,"date":1588896000000,"new_cases":1,"total_cases":552,"total_recovered":534,"total_death":9,"existing_cases":9,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"8fbed08f-1f7d-461f-8cca-105bf5f74a32","CreationDate":1587269300019,"Creator":"DoHArcGIS","EditDate":1588913459095,"Editor":"ting.lin_DoHWA"}},{"attributes":{"OBJECTID":81,"date":1588982400000,"new_cases":0,"total_cases":552,"total_recovered":536,"total_death":9,"existing_cases":7,"total_ruledout":null,"total_hospitalised":null,"GlobalID":"05af311a-144c-43c3-9ce8-a779c9ec3ca7","CreationDate":1587269308082,"Creator":"DoHArcGIS","EditDate":1588990388049,"Editor":"ting.lin_DoHWA"}}]}
URL_OTHER_STATS = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/COVID19_Dashboard_Chart_ViewLayer/FeatureServer/0/query?f=json&where=new_cases%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=date%20asc&outSR=102100&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'

{"objectIdFieldName":"FID",
 "uniqueIdField":{"name":"FID","isSystemMaintained":true},
 "globalIdFieldName":"",
 "fields":[{"name":"Age_Group","type":"esriFieldTypeString","alias":"Age_Group","sqlType":"sqlTypeNVarchar","length":256,"domain":null,"defaultValue":null},
           {"name":"Male","type":"esriFieldTypeInteger","alias":"Male","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Female","type":"esriFieldTypeInteger","alias":"Female","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"Total","type":"esriFieldTypeInteger","alias":"Total","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
           {"name":"FID","type":"esriFieldTypeOID","alias":"FID","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null}],
 "features":[{"attributes":{"Age_Group":"Total","Male":303,"Female":249,"Total":552,"FID":10}}]}
URL_MF_BALANCE = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/Age_sex_total_COVID19_Chart_view_layer/FeatureServer/0/query?f=json&where=Age_Group%3D%27Total%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true'

{"objectIdFieldName":"FID",
 "uniqueIdField":{"name":"FID","isSystemMaintained":true},
 "globalIdFieldName":"",
 "fields":[
     {"name":"Age_Group","type":"esriFieldTypeString","alias":"Age_Group","sqlType":"sqlTypeNVarchar","length":256,"domain":null,"defaultValue":null},
     {"name":"Male","type":"esriFieldTypeInteger","alias":"Male","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
     {"name":"Female","type":"esriFieldTypeInteger","alias":"Female","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
     {"name":"Total","type":"esriFieldTypeInteger","alias":"Total","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null},
     {"name":"FID","type":"esriFieldTypeOID","alias":"FID","sqlType":"sqlTypeInteger","domain":null,"defaultValue":null}],
 "features":[
     {"attributes":{"Age_Group":"00-09","Male":3,"Female":4,"Total":7,"FID":1}},
     {"attributes":{"Age_Group":"10-19","Male":4,"Female":2,"Total":6,"FID":2}},
     {"attributes":{"Age_Group":"20-29","Male":48,"Female":47,"Total":95,"FID":3}},
     {"attributes":{"Age_Group":"30-39","Male":63,"Female":27,"Total":90,"FID":4}},
     {"attributes":{"Age_Group":"40-49","Male":34,"Female":21,"Total":55,"FID":5}},
     {"attributes":{"Age_Group":"50-59","Male":39,"Female":43,"Total":82,"FID":6}},
     {"attributes":{"Age_Group":"60-69","Male":52,"Female":58,"Total":110,"FID":7}},
     {"attributes":{"Age_Group":"70-79","Male":52,"Female":42,"Total":94,"FID":8}},
     {"attributes":{"Age_Group":"80+","Male":8,"Female":5,"Total":13,"FID":9}}]}
URL_AGE_BALANCE = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/services/Age_sex_total_COVID19_Chart_view_layer/FeatureServer/0/query?f=json&where=Age_Group%3C%3E%27Total%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_wa_dash_datapoints())
