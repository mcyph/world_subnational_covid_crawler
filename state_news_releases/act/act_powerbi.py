from os.path import exists
from datetime import datetime

from covid_19_au_grab.datatypes.constants import (
    SCHEMA_SA3,
    DT_TOTAL, DT_TOTAL_FEMALE, DT_TOTAL_MALE,
    DT_SOURCE_COMMUNITY, DT_SOURCE_CONFIRMED, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_INTERSTATE, DT_SOURCE_OVERSEAS, DT_SOURCE_UNDER_INVESTIGATION,
    DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
)
from covid_19_au_grab.state_news_releases.act.ACTPowerBI import (
    ACTPowerBI, get_globals
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.PowerBIDataReader import (
    PowerBIDataReader
)


class _ACTPowerBI(PowerBIDataReader):
    def __init__(self, base_path, source_url):
        self.base_path = base_path
        self.source_url = source_url
        PowerBIDataReader.__init__(self, base_path, get_globals())

    def get_powerbi_data(self):
        r = []
        for updated_date, rev_id, response_dict in self._iter_all_dates():
            subdir = f'{self.base_path}/{updated_date}-{rev_id}'
            # Use a fallback only if can't get from the source
            # TODO: Get the date from the actual data!!! =============================

            # Only use most revision if there isn't
            # a newer revision ID for a given day!
            next_id = rev_id + 1
            next_subdir = f'{self.base_path}/{updated_date}-{next_id}'
            if exists(next_subdir):
                print(f"ACTPowerBI ignoring {subdir}")
                continue

            i_updated_date = self._get_updated_date(updated_date, response_dict)
            if i_updated_date is not None:
                updated_date = i_updated_date

            #print(updated_date)
            r.extend(self._get_age_groups_data(updated_date, response_dict))
            r.extend(self._get_confirmed_cases_data(updated_date, response_dict))
            r.extend(self._get_deaths_data(updated_date, response_dict))
            r.extend(self._get_gender_balance_data(updated_date, response_dict))
            r.extend(self._get_infection_source_data(updated_date, response_dict))
            r.extend(self._get_new_cases_data(updated_date, response_dict))
            r.extend(self._get_recovered_data(updated_date, response_dict))
            r.extend(self._get_regions_data(updated_date, response_dict))
        return r

    def _to_int(self, i):
        if not isinstance(i, str):
            return i
        return int(i.rstrip('L'))

    def _get_updated_date(self, updated_date, response_dict):
        print(updated_date)
        ts = response_dict['updated_date'][1]
        ts = ts['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']

        if ts < 1000:
            # FIXME!! ==================================================================================================
            return None
        else:
            return datetime.fromtimestamp(ts/1000).strftime('%Y_%m_%d')

    def _get_age_groups_data(self, updated_date, response_dict):
        r = []

        data = response_dict['age_groups'][1]
        agd = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']
        m_f_column_details = data['result']['data']['dsr']['DS'][0]['SH'][0]['DM1']
        assert m_f_column_details[0]['G1'] in ('Female', 'Females')
        assert m_f_column_details[1]['G1'] in ('Male', 'Males')

        for age in agd:
            print(age)

            X = age['X']

            if len(X) > 0:
                # Note that previous value simply means the very last value seen
                # That means that if female/not stated is 67 and the following
                # male stat is also 67 it'll be elided with an R-repeat val
                female = X[0].get(
                    'M0', previous_value if X[0].get('R') else 0
                )
                previous_value = female
            else:
                female = 0

            if len(X) > 1:
                male = X[1].get(
                    'M0', previous_value if X[1].get('R') else 0
                )  # "R" clearly means "Repeat"
                previous_value = male
            else:
                male = 0

            female = self._to_int(female)
            male = self._to_int(male)

            r.append(DataPoint(
                datatype=DT_TOTAL_MALE,
                agerange=age['G0'].replace('–', '-'),
                value=male,
                date_updated=updated_date,
                source_url=self.source_url
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL_FEMALE,
                agerange=age['G0'].replace('–', '-'),
                value=female,
                date_updated=updated_date,
                source_url=self.source_url
            ))
            r.append(DataPoint(
                datatype=DT_TOTAL,
                agerange=age['G0'].replace('–', '-'),
                value=female + male,
                date_updated=updated_date,
                source_url=self.source_url
            ))

        return r

    def _get_deaths_data(self, updated_date, response_dict):
        r = []
        data = response_dict['deaths'][1]

        value = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        r.append(DataPoint(
            datatype=DT_STATUS_DEATHS,
            value=int(value),
            date_updated=updated_date,
            source_url=self.source_url
        ))
        return r

    def _get_confirmed_cases_data(self, updated_date, response_dict):
        r = []

        data = response_dict['confirmed_cases'][1]
        value = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        r.append(DataPoint(
            datatype=DT_TOTAL,
            value=int(value),
            date_updated=updated_date,
            source_url=self.source_url
        ))
        return r

    def _get_gender_balance_data(self, updated_date, response_dict):
        r = []
        try:
            data = response_dict['gender_balance'][1]
        except KeyError:
            return [] # WARNING!!! ==================================================================================

        # WARNING: This sometimes has another query before it!!! =======================================================
        try:
            m_f = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

            assert m_f[0]['C'][0] in ('Males', 'Male')
            assert m_f[1]['C'][0] in ('Females', 'Female')
        except:
            m_f = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

            assert m_f[0]['C'][0] in ('Males', 'Male')
            assert m_f[1]['C'][0] in ('Females', 'Female')

        male = m_f[0]['C'][1]
        try:
            female = m_f[1]['C'][1]
        except IndexError:
            assert m_f[1]['R']
            female = male

        r.append(DataPoint(
            datatype=DT_TOTAL_MALE,
            value=self._to_int(male),
            date_updated=updated_date,
            source_url=self.source_url
        ))
        r.append(DataPoint(
            datatype=DT_TOTAL_FEMALE,
            value=self._to_int(female),
            date_updated=updated_date,
            source_url=self.source_url
        ))
        return r

    def _get_infection_source_data(self, updated_date, response_dict):
        # TODO: SHOULD THIS ONLY USE THE MOST RECENT VALUES?? ================================================================================
        data = response_dict['infection_source_time_series']

        act_norm_map = {
            'Overseas acquired': DT_SOURCE_OVERSEAS,
            'Cruise ship acquired': DT_SOURCE_CRUISE_SHIP,
            'Locally acquired - interstate': DT_SOURCE_INTERSTATE,
            'Locally acquired - contact of a confirmed ACT case': DT_SOURCE_CONFIRMED,
            'Unknown or local transmission': DT_SOURCE_COMMUNITY,
            'Locally acquired unknown source': DT_SOURCE_COMMUNITY,
            'Under investigation': DT_SOURCE_UNDER_INVESTIGATION
        }

        # "Locally acquired - contact of a confirmed ACT case"
        # "Locally acquired - interstate"
        # "Overseas acquired"
        # "Under investigation"

        print(data)

        tally = {}
        keys = [
            x['G1'] for x in
            data[1]['result']['data']['dsr']['DS'][0]['SH'][0]['DM1']
        ]
        for key in keys:
            tally[key] = 0

        r = []
        for item in data[1]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            timestamp = item['G0']  # e.g. 1585958400000

            xx = 0
            for sub_item in item['X']:
                #print(sub_item)
                if len(sub_item.keys()) == 1 and list(sub_item.keys())[0] == 'S':
                    continue
                xx = sub_item.get('I', xx)

                if sub_item.get('R'):
                    value = previous_value
                else:
                    value = sub_item['M0']

                value = self._to_int(value)
                tally[keys[xx]] += value
                previous_value = value
                xx += 1

            i_date_updated = datetime.fromtimestamp(timestamp/1000) \
                                     .strftime('%Y_%m_%d')

            if updated_date == i_date_updated:
                for xx, (key, value) in enumerate(tally.items()):
                    r.append(DataPoint(
                        datatype=act_norm_map[key],
                        value=value,
                        date_updated=i_date_updated,
                        source_url=self.source_url
                    ))
        return r

    def _get_new_cases_data(self, updated_date, response_dict):
        r = []
        return r

    def _get_recovered_data(self, updated_date, response_dict):
        r = []
        data = response_dict['recovered'][1]

        recovered = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        r.append(DataPoint(
            datatype=DT_STATUS_RECOVERED,
            value=self._to_int(recovered),
            date_updated=updated_date,
            source_url=self.source_url
        ))
        return r

    def _get_regions_data(self, updated_date, response_dict):
        r = []

        data = response_dict['regions_exact'][1]
        rd = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

        for region_child in rd:
            #print(region_child)
            if isinstance(region_child['C'][0], int):
                # {'C': [1], 'Ø': 1}
                # (what is this for???)
                continue

            if region_child.get('R'):
                value = previous_value
            else:
                value = region_child['C'][1]

            name = region_child['C'][0].split('(')[0].strip()
            if name == 'East Canberra':
                name = 'Canberra East'
            if name in ('Uriara', 'Uriarra'):
                name = 'Urriarra - Namadgi'

            r.append(DataPoint(
                region_schema=SCHEMA_SA3,
                datatype=DT_TOTAL,
                region_child=name,
                value=self._to_int(value),
                date_updated=updated_date,
                source_url=self.source_url
            ))
            previous_value = value
        return r


def get_powerbi_data():
    apb = _ACTPowerBI(
        ACTPowerBI.PATH_PREFIX,
        ACTPowerBI.POWERBI_URL
    )
    return apb.get_powerbi_data()


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_powerbi_data())
