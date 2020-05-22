import csv
import json

from covid_19_au_grab.state_news_releases.overseas.KaggleDataset import (
    KaggleDataset
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_KR_PROVINCE,
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

# https://www.kaggle.com/kimjihoo/coronavirusdataset
# https://github.com/jihoo-kim/Data-Science-for-COVID-19
# Kaggle is kept up-to-date more often


class KRData(KaggleDataset):
    SOURCE_URL = 'https://www.kaggle.com/kimjihoo/coronavirusdataset'
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        KaggleDataset.__init__(self,
             output_dir=get_overseas_dir() / 'ko' / 'data',
             dataset='kimjihoo/coronavirusdataset'
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_patient_info())
        r.extend(self._get_time_province())
        r.extend(self._get_time_age())
        r.extend(self._get_time_gender())
        r.extend(self._get_time())
        return r

    def _get_patient_info(self):
        # TODO: get age/gender/source of infection info by region_child!!
        #
        # PatientInfo.csv
        # patient_id,global_num,sex,birth_year,age,country,province,city,disease,infection_case,infection_order,infected_by,contact_number,symptom_onset_date,confirmed_date,released_date,deceased_date,state
        # 1000000001,2,male,1964,50s,Korea,Seoul,Gangseo-gu,,overseas inflow,1,,75,2020-01-22,2020-01-23,2020-02-05,,released
        # 1000000002,5,male,1987,30s,Korea,Seoul,Jungnang-gu,,overseas inflow,1,,31,,2020-01-30,2020-03-02,,released
        # 1000000003,6,male,1964,50s,Korea,Seoul,Jongno-gu,,contact with patient,2,2002000001,17,,2020-01-30,2020-02-19,,released
        #
        r = []

        return r

    def _get_time_province(self):
        r = []

        # TimeProvince.csv
        # date,time,province,confirmed,released,deceased
        # 2020-01-20,16,Seoul,0,0,0
        # 2020-01-20,16,Busan,0,0,0
        # 2020-01-20,16,Daegu,0,0,0

        with self.get_file('TimeProvince.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    region_schema=SCHEMA_KR_PROVINCE,
                    region_child=item['province'],
                    datatype=DT_TOTAL,
                    value=item['confirmed'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                #r.append(DataPoint(
                #    region_schema=SCHEMA_KR_PROVINCE,
                #    region_child=item['province'],
                #    datatype=DT_RELEASED,
                #    value=item['released'],
                #    date_updated=date,
                #    source_url=self.SOURCE_URL
                #))
                r.append(DataPoint(
                    region_schema=SCHEMA_KR_PROVINCE,
                    region_child=item['province'],
                    datatype=DT_STATUS_DEATHS,
                    value=item['deceased'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r

    def _get_time_age(self):
        r = []

        # TimeAge.csv
        # date,time,age,confirmed,deceased
        # 2020-03-02,0,0s,32,0
        # 2020-03-02,0,10s,169,0
        # 2020-03-02,0,20s,1235,0

        with self.get_file('TimeAge.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])
                agerange = int(item['age'].rstrip('s'))
                agerange = f'{agerange}-{agerange+9}'

                r.append(DataPoint(
                    datatype=DT_TOTAL,
                    agerange=agerange,
                    value=item['confirmed'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                #r.append(DataPoint(
                #    datatype=DT_STATUS_DEATHS_XXXX,
                #    agerange=agerange,
                #    value=item['confirmed'],
                #    date_updated=date,
                #    source_url=self.SOURCE_URL
                #))

        return r

    def _get_time_gender(self):
        r = []

        # TimeGender.csv
        # date,time,sex,confirmed,deceased
        # 2020-03-02,0,male,1591,13
        # 2020-03-02,0,female,2621,9
        # 2020-03-03,0,male,1810,16

        with self.get_file('TimeGender.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                if item['sex'] == 'male':
                    datatype = DT_TOTAL_MALE
                elif item['sex'] == 'female':
                    datatype = DT_TOTAL_FEMALE
                else:
                    raise Exception(datatype)

                r.append(DataPoint(
                    datatype=datatype,
                    value=item['confirmed'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                #r.append(DataPoint(
                #    datatype=DT_STATUS_DEATHS_XXXX,
                #    value=item['deceased'],
                #    date_updated=date,
                #    source_url=self.SOURCE_URL
                #))

        return r

    def _get_time(self):
        r = []

        # Time.csv
        # date,time,test,negative,confirmed,released,deceased
        # 2020-01-20,16,1,0,1,0,0
        # 2020-01-21,16,1,0,1,0,0
        # 2020-01-22,16,4,3,1,0,0

        with self.get_file('Time.csv',
                           include_revision=True) as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['date'])

                r.append(DataPoint(
                    datatype=DT_STATUS_DEATHS,
                    value=item['deceased'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_DEATHS,
                    value=item['deceased'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    datatype=DT_STATUS_DEATHS,
                    value=item['deceased'],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(KRData().get_datapoints())
