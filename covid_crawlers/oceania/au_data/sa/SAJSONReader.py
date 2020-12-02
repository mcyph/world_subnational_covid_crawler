import json
import datetime

from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DataPoint import DataPoint
from _utility.URLArchiver import URLArchiver
from covid_db.datatypes.DatapointMerger import DataPointMerger


class SAJSONReader:
    SOURCE_ID = 'au_sa_dash'
    SOURCE_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/' \
                  'public+content/sa+health+internet/conditions/' \
                  'infectious+diseases/covid+2019/covid-19+dashboard'
    SOURCE_DESCRIPTION = ''

    def get_datapoints(self):
        ua = URLArchiver(f'sa/dashboard')

        i_r = DataPointMerger()
        for period in ua.iter_periods():
            for subperiod_id, subdir in ua.iter_paths_for_period(period):
                path = ua.get_path(subdir)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                i_r.extend(self._get_from_json(data))
        return i_r

    def _get_from_json(self, data):
        # Additional time series data is also available:
        # 'laboratory_char'
        # 'newcase_sa_char'
        # travellers/expiations/compliance not currently used

        def parse_date(s):
            return datetime.datetime.strptime(
                ' '.join(s.split()[-3:]), '%d %B %Y'
            ).strftime('%Y_%m_%d')

        r = []
        base_data_date = parse_date(data['hp_date'])

        r.append(DataPoint(
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-SA',
            datatype=DataTypes.NEW,
            value=int(data['newcase_sa']),
            date_updated=base_data_date,
            source_url=self.SOURCE_URL,
            source_id=self.SOURCE_ID
        ))
        r.append(DataPoint(
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-SA',
            datatype=DataTypes.TOTAL,
            value=int(data['todaycase_sa']),
            date_updated=base_data_date,
            source_url=self.SOURCE_URL,
            source_id=self.SOURCE_ID
        ))
        r.append(DataPoint(
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-SA',
            datatype=DataTypes.STATUS_ICU,
            value=int(data['icu_sa']),
            date_updated=base_data_date,
            source_url=self.SOURCE_URL,
            source_id=self.SOURCE_ID
        ))
        r.append(DataPoint(
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-SA',
            datatype=DataTypes.STATUS_DEATHS,
            value=int(data['deaths_sa']),
            date_updated=base_data_date,
            source_url=self.SOURCE_URL,
            source_id=self.SOURCE_ID
        ))
        r.append(DataPoint(
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-SA',
            datatype=DataTypes.STATUS_RECOVERED,
            value=int(data['recovered_sa']),
            date_updated=base_data_date,
            source_url=self.SOURCE_URL,
            source_id=self.SOURCE_ID
        ))

        for agerange, value in zip(
            data['age_char']['field_order'],
            data['age_char']['data']
        ):
            agerange = agerange.replace(' - ', '-')
            r.append(DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-SA',
                datatype=DataTypes.TOTAL,
                agerange=agerange,
                value=int(value),
                date_updated=parse_date(data['age_char']['datetime']),
                source_url=self.SOURCE_URL,
                source_id=self.SOURCE_ID
            ))

        for gender, value in zip(
            data['gender_char']['field_order'],
            data['gender_char']['data']
        ):
            datatype = {
                'male': DataTypes.TOTAL_MALE,
                'female': DataTypes.TOTAL_FEMALE
            }[gender.lower()]

            r.append(DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-SA',
                datatype=datatype,
                value=int(value),
                date_updated=parse_date(data['gender_char']['datetime']),
                source_url=self.SOURCE_URL,
                source_id=self.SOURCE_ID
            ))

        for source, value in zip(
            data['infection_char']['field_order'],
            data['infection_char']['data']
        ):
            datatype = {
                'overseas acquired': DataTypes.SOURCE_OVERSEAS,
                'contact confirmed': DataTypes.SOURCE_CONFIRMED,
                'interstate travel': DataTypes.SOURCE_INTERSTATE,
                'under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION,
                'locally acquired': DataTypes.SOURCE_COMMUNITY,
                'close contact': DataTypes.SOURCE_CONFIRMED,
                'locally acquired (contact unknown)': DataTypes.SOURCE_COMMUNITY,
                'interstate acquired': DataTypes.SOURCE_INTERSTATE,
                'under investigation (in quarantine)': DataTypes.SOURCE_UNDER_INVESTIGATION,
            }[source.lower()]

            r.append(DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-SA',
                datatype=datatype,
                value=int(value),
                date_updated=parse_date(data['infection_char']['datetime']),
                source_url=self.SOURCE_URL,
                source_id=self.SOURCE_ID
            ))
        return r


if __name__ == '__main__':
    from pprint import pprint
    dp = SAJSONReader().get_datapoints()
    pprint(dp)
