import json
from os import listdir
from os.path import exists
from datetime import datetime
from covid_19_au_grab.state_news_releases.constants import \
    DT_AGE_MALE, DT_AGE_FEMALE, DT_AGE, \
    DT_CASES_BY_REGION, \
    DT_PATIENT_STATUS, \
    DT_MALE, DT_FEMALE
from covid_19_au_grab.powerbi_grabber.ACTPowerBI import \
    ACTPowerBI, get_globals
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.state_news_releases.PowerBIDataReader import \
    PowerBIDataReader


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

            r.extend(self._get_age_groups_data(updated_date, response_dict))
            r.extend(self._get_confirmed_cases_data(updated_date, response_dict))
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

    def _get_age_groups_data(self, updated_date, response_dict):
        r = []
        try:
            try:
                try:
                    data = response_dict['age_groups'][1]
                except KeyError:
                    data = response_dict['age_groups_2'][1]
            except KeyError:
                data = response_dict['age_groups_3'][1]
        except KeyError:
            data = response_dict['age_groups_4'][1]

        agd = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

        m_f_column_details = data['result']['data']['dsr']['DS'][0]['SH'][0]['DM1']
        assert m_f_column_details[0]['G1'] in ('Female', 'Females')
        assert m_f_column_details[1]['G1'] in ('Male', 'Males')

        for age in agd:
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
                name=age['G0'].replace('–', '-'),
                datatype=DT_AGE_MALE,
                value=male,
                date_updated=updated_date,
                source_url=self.source_url,
                text_match=None
            ))
            r.append(DataPoint(
                name=age['G0'].replace('–', '-'),
                datatype=DT_AGE_FEMALE,
                value=female,
                date_updated=updated_date,
                source_url=self.source_url,
                text_match=None
            ))
            r.append(DataPoint(
                name=age['G0'].replace('–', '-'),
                datatype=DT_AGE,
                value=female + male,
                date_updated=updated_date,
                source_url=self.source_url,
                text_match=None
            ))

        return r

    def _get_confirmed_cases_data(self, updated_date, response_dict):
        r = []
        return r

    def _get_gender_balance_data(self, updated_date, response_dict):
        r = []
        try:
            try:
                data = response_dict['gender_balance'][1]
            except KeyError:
                data = response_dict['gender_balance_2'][1]
        except KeyError:
            data = response_dict['gender_balance_3'][1]

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
            name=None,
            datatype=DT_MALE,
            value=self._to_int(male),
            date_updated=updated_date,
            source_url=self.source_url,
            text_match=None
        ))
        r.append(DataPoint(
            name=None,
            datatype=DT_FEMALE,
            value=self._to_int(female),
            date_updated=updated_date,
            source_url=self.source_url,
            text_match=None
        ))
        return r

    def _get_infection_source_data(self, updated_date, response_dict):
        r = []
        data = response_dict['infection_source_time_series']
        #recovered = data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']

        #for time_dict in data:

        return r

    def _get_new_cases_data(self, updated_date, response_dict):
        r = []
        return r

    def _get_recovered_data(self, updated_date, response_dict):
        r = []
        try:
            data = response_dict['recovered'][1]
        except KeyError:
            data = response_dict['recovered_2'][1]

        recovered = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        r.append(DataPoint(
            name='Recovered',
            datatype=DT_PATIENT_STATUS,
            value=self._to_int(recovered),
            date_updated=updated_date,
            source_url=self.source_url,
            text_match=None
        ))
        return r

    def _get_regions_data(self, updated_date, response_dict):
        r = []
        data = response_dict['regions_exact'][1]
        rd = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

        for region in rd:
            print(region)
            if isinstance(region['C'][0], int):
                # {'C': [1], 'Ø': 1}
                # (what is this for???)
                continue

            if region.get('R'):
                value = previous_value
            else:
                value = region['C'][1]

            r.append(DataPoint(
                name=region['C'][0].split('(')[0].strip(),
                datatype=DT_CASES_BY_REGION,
                value=self._to_int(value),
                date_updated=updated_date,
                source_url=self.source_url,
                text_match=None
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
