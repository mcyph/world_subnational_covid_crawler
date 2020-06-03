import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_0,
    DT_TOTAL, DT_NEW,
    DT_STATUS_ACTIVE,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class VEData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/corona-virus-covid-19-cases-and-deaths-in-venezuela'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 've_ocha_venezuela_humdata'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / 've' / 'data',
             urls_dict={
                 'cases_deaths.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/2PACX-1vTT8ef-uVa5q_5kBYbVXeEpRCW8gOJHlWhHGrH8dQ704D64_yNaMMjvkzdgD9YweSBQ-GyqnGLLasvK/pub?gid=608241994&single=true&output=csv',
                     static_file=False
                 ),
                 'cases_by_age_gender.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/2PACX-1vTT8ef-uVa5q_5kBYbVXeEpRCW8gOJHlWhHGrH8dQ704D64_yNaMMjvkzdgD9YweSBQ-GyqnGLLasvK/pub?gid=1574343536&single=true&output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self.get_cases_deaths())
        r.extend(self.get_cases_by_age_gender())
        return r

    def get_cases_deaths(self):
        r = []

        # Date,Datets,Confirmed Count,Confirmed New,Recovered Count,Recovered New,Deaths Count,Deaths New,Active Count
        # #date,,#affected +infected +total,#affected +infected +new,#affected +recovered +total,#affected +confirmed +new,#affected +killed +total,#affected +killed +new,#affected +active
        # 2020-03-13,1584072000,2,2,,,,,2
        # 2020-03-14,1584158400,10,8,,,,,10
        # 2020-03-15,1584244800,17,7,,,,,17
        # 2020-03-16,1584331200,33,16,,,,,33
        # 2020-03-17,1584417600,36,3,,,,,36
        # 2020-03-18,1584504000,41,5,,,,,41

        f = self.get_file('cases_deaths.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            date = self.convert_date(item['Date'])

            if item['Confirmed Count']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Venezuela',
                    datatype=DT_TOTAL,
                    value=int(item['Confirmed Count']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))

            if item['Confirmed New']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Venezuela',
                    datatype=DT_NEW,
                    value=int(item['Confirmed New']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))

            if item['Recovered Count']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Venezuela',
                    datatype=DT_STATUS_RECOVERED,
                    value=int(item['Recovered Count']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))

            if item['Deaths Count']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Venezuela',
                    datatype=DT_STATUS_DEATHS,
                    value=int(item['Deaths Count']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))

            if item['Active Count']:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_0,
                    region_child='Venezuela',
                    datatype=DT_STATUS_ACTIVE,
                    value=int(item['Active Count']),
                    date_updated=date,
                    source_url=self.SOURCE_URL,
                ))

        return r

    def get_cases_by_age_gender(self):
        r = []

        # Confirmed Count,Confirmed Byagerange 0-9,Confirmed Byagerange 10-19,Confirmed Byagerange 20-29,Confirmed Byagerange 30-39,Confirmed Byagerange 40-49,Confirmed Byagerange 50-59,Confirmed Byagerange 60-69,Confirmed Byagerange 70-79,Confirmed Byagerange 80-89,Confirmed Byagerange 90-99,Confirmed Bygender Male,Confirmed Bygender Female
        # #affected +infected +total,#affected +infected +age_0_9,#affected +infected +age_10_19,#affected +infected +age_20_29,#affected +infected +age_30_39,#affected +infected +age_40_49,#affected +infected +age_50_59,#affected +infected +age_60_69,#affected +infected +age_70_79,#affected +infected +age_80_89,#affected +infected +age_90_99,#affected +infected +m,#affected +infected +f
        # 944,76,85,283,220,133,83,37,18,3,,513,431

        f = self.get_file('cases_by_age_gender.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            if first_item:
                first_item = False
                continue

            # TODO: Implement me!
            # Possibly not highest priority now, but would
            # be nice to save copies of this over time for later
            #date = self.convert_date(item['Date'])

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(VEData().get_datapoints())
