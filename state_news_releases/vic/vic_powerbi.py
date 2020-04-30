from datetime import datetime
from os.path import expanduser, exists

from covid_19_au_grab.state_news_releases.DataPoint import \
    DataPoint
from covid_19_au_grab.state_news_releases.constants import \
    SCHEMA_LGA, \
    DT_CASES_TOTAL, DT_CASES_TOTAL_FEMALE, DT_CASES_TOTAL_MALE, \
    DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_COMMUNITY, \
    DT_SOURCE_CONFIRMED, DT_SOURCE_OVERSEAS
from covid_19_au_grab.state_news_releases.PowerBIDataReader import \
    PowerBIDataReader
from covid_19_au_grab.state_news_releases.vic.VicPowerBI import \
    VicPowerBI, get_globals


BASE_PATH = expanduser('~/dev/covid_19_data/vic/powerbi')
SOURCE_URL = 'https://app.powerbi.com/view?r=' \
             'eyJrIjoiODBmMmE3NWQtZWNlNC00OWRkLTk1NjYtM' \
             'jM2YTY1MjI2NzdjIiwidCI6ImMwZTA2MDFmLTBmYW' \
             'MtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9'


class _VicPowerBI(PowerBIDataReader):
    def __init__(self, base_path, source_url):
        self.base_path = base_path
        self.source_url = source_url
        PowerBIDataReader.__init__(self, base_path, get_globals())

    def get_powerbi_data(self):
        # Use a fallback only if can't get from the source

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
                print(f"VicPowerBI ignoring {subdir}")
                continue

            try:
                updated_date = self._get_updated_date(response_dict)
            except (KeyError, ValueError):
                pass
            r.extend(self._get_regions(updated_date, response_dict))
            r.extend(self._get_age_data(updated_date, response_dict))
            r.extend(self._get_source_of_infection(updated_date, response_dict))
        return r

    def _get_updated_date(self, response_dict):
        # Try to get updated date from source, if possible
        # "M0": "08/04/2020 - 12:03:00 PM"
        data = response_dict['unknown_please_categorize_5'][1]  #  ??? ====================================================================
        updated_str = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        updated_date = datetime.strptime(
            updated_str.split('-')[0].strip(), '%d/%m/%Y'
        ).strftime('%Y_%m_%d')
        print("Vic updated date supplied:", updated_date)
        return updated_date

    def _get_regions(self, updated_date, response_dict):
        output = []
        try:
            data = response_dict['regions'][1]
        except KeyError:
            data = response_dict['regions_2'][1]

        for region in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            # print(region)

            if region.get('R'):
                value = previous_value
            else:
                value = region['C'][1]

            output.append(DataPoint(
                schema=SCHEMA_LGA,
                datatype=DT_CASES_TOTAL,
                region=region['C'][0].split('(')[0].strip(),
                value=value,
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
            previous_value = value
            # print(output[-1])

        return output

    def _get_age_data(self, updated_date, response_dict):
        output = []
        data = response_dict['age_data'][1]

        cols = data['result']['data']['dsr']['DS'][0]['SH'][0]['DM1']
        cols = [i['G1'].rstrip('s') for i in cols]
        #print("COLS:", cols)

        for age in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            #print(age)
            X = age['X']

            if len(X) > 0:
                # Note that previous value simply means the very last value seen
                # That means that if female/not stated is 67 and the following
                # male stat is also 67 it'll be elided with an R-repeat val
                value_1 = X[0].get(
                    'M0', previous_value if X[0].get('R') else 0
                )
                previous_value = value_1
            else:
                value_1 = 0

            if len(X) > 1:
                value_2 = X[1].get(
                    'M0', previous_value if X[1].get('R') else 0
                )  # "R" clearly means "Repeat"
                previous_value = value_2
            else:
                value_2 = 0

            if len(X) > 2:
                not_stated = X[2].get(
                    'M0', previous_value if X[2].get('R') else 0
                )
                previous_value = not_stated
            else:
                not_stated = 0

            assert cols[0] in ('Male', 'Female')
            assert cols[1] in ('Male', 'Female')

            output.append(DataPoint(
                datatype=DT_CASES_TOTAL_MALE if cols[0] == 'Male' else DT_CASES_TOTAL_FEMALE,
                agerange=age['G0'].replace('–', '-'),
                value=value_1,
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
            output.append(DataPoint(
                datatype=DT_CASES_TOTAL_FEMALE if cols[1] == 'Female' else DT_CASES_TOTAL_MALE,
                agerange=age['G0'].replace('–', '-'),
                value=value_2,
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
            # TODO: support "not stated" separately!!! ====================================================
            general_age = (
                value_1 + value_2 + not_stated
            )

            output.append(DataPoint(
                datatype=DT_CASES_TOTAL,
                agerange=age['G0'].replace('–', '-'),
                value=general_age,
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))

        return output

    def _get_source_of_infection(self, updated_date, response_dict):
        # * Overseas acquired
        # * Cruise ship acquired (included in overseas acquired)
        # * Interstate acquired
        # * Locally acquired - contact of a confirmed case
        # * Locally acquired - contact not identified
        # * Under investigation

        # Normalise it with other states
        vic_norm_map = {
            'Travel overseas': DT_SOURCE_OVERSEAS,
            'Contact with a confirmed case': DT_SOURCE_CONFIRMED,
            'Acquired in Australia, unknown source': DT_SOURCE_COMMUNITY,
            'Under investigation': DT_SOURCE_UNDER_INVESTIGATION
        }

        output = []
        try:
            try:
                data = response_dict['source_of_infection'][1]
            except KeyError:
                data = response_dict['source_of_infection_2'][1]
        except KeyError:
            data = response_dict['source_of_infection_3'][1]

        for source in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            output.append(DataPoint(
                datatype=vic_norm_map[source['C'][0]],
                value=source['C'][1],
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
        return output


def get_powerbi_data():
    apb = _VicPowerBI(
        VicPowerBI.PATH_PREFIX,
        VicPowerBI.POWERBI_URL
    )
    return apb.get_powerbi_data()


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_powerbi_data())
