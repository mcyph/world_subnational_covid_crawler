from math import log
from os.path import exists
from datetime import datetime

from covid_19_au_grab.datatypes.constants import (
    SCHEMA_ADMIN_1,
    DT_TOTAL, DT_TESTS_TOTAL,
    DT_STATUS_HOSPITALIZED,
    DT_STATUS_DEATHS,
    DT_STATUS_RECOVERED
)
from covid_19_au_grab.overseas.west_africa_data.WestAfricaPowerBI import (
    WestAfricaPowerBI, get_globals
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.PowerBIDataReader import (
    PowerBIDataReader
)


def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b


class _WestAfricaPowerBI(PowerBIDataReader):
    def __init__(self, base_path, source_url):
        self.base_path = base_path
        self.source_url = source_url
        PowerBIDataReader.__init__(self, base_path, get_globals())

    def get_powerbi_data(self):
        r = []
        for updated_date, rev_id, response_dict in self._iter_all_dates():
            subdir = f'{self.base_path}/{updated_date}-{rev_id}'

            # Only use most revision if there isn't
            # a newer revision ID for a given day!
            next_id = rev_id + 1
            next_subdir = f'{self.base_path}/{updated_date}-{next_id}'
            if exists(next_subdir):
                print(f"West Africa PowerBI ignoring {subdir}")
                continue

            r.extend(self._get_regions_data(updated_date, response_dict))
        return r

    def _to_int(self, i):
        if not isinstance(i, str):
            return i
        return int(i.rstrip('L'))

    def _get_updated_date(self, updated_date, response_dict):
        try:
            ts = response_dict['updated_date'][1]
        except KeyError:
            ts = response_dict['updated_date_2'][1]

        ts = ts['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']

        if ts < 1000:
            # FIXME!! ==================================================================================================
            return None
        else:
            return datetime.fromtimestamp(ts/1000).strftime('%Y_%m_%d')

    def _get_regions_data(self, updated_date, response_dict):
        r = []
        try:
            data = response_dict['country_data'][1]
        except KeyError:
            data = response_dict['country_data_2'][1]

        SOURCE_URL = 'https://app.powerbi.com/view?r=eyJrIjoiZTRkZDhmMDctM2NmZi00NjRkLTgzYzMtYzI1MDMzNWI3NTRhIiwidCI6IjBmOWUzNWRiLTU0NGYtNGY2MC1iZGNjLTVlYTQxNmU2ZGM3MCIsImMiOjh9'

        for region_dict in data['result']['data']['dsr']['DS'][0]['PH'][1]['DM1']:
            value = region_dict['C']

            if region_dict.get('Ø'):
                value.insert(region_dict['Ø']-1, None)

            if region_dict.get('R'):
                for bit in bits(region_dict['R']):
                    bit = int(log(bit, 2))
                    try:
                        value.insert(bit, previous_value[bit])
                    except IndexError:
                        value.insert(bit, None)

            if isinstance(value[0], int):
                value[0] = data['result']['data']['dsr']['DS'][0]['ValueDicts']['D0'][value[0]]

            if isinstance(value[1], int):
                value[1] = data['result']['data']['dsr']['DS'][0]['ValueDicts']['D1'][value[1]]

            previous_value = value
            while len(value) != 8:
                value.append(None)
            
            admin_0, admin_1, contacts, tests, \
            cases, recoveries, deaths, in_treatment = value

            if cases is not None:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent=admin_0,
                    region_child=admin_1,
                    datatype=DT_TOTAL,
                    value=int(cases),
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

            if tests is not None:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent=admin_0,
                    region_child=admin_1,
                    datatype=DT_TESTS_TOTAL,
                    value=int(tests),
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

            if recoveries is not None:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent=admin_0,
                    region_child=admin_1,
                    datatype=DT_STATUS_RECOVERED,
                    value=int(recoveries),
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

            if deaths is not None:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent=admin_0,
                    region_child=admin_1,
                    datatype=DT_STATUS_DEATHS,
                    value=int(deaths),
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

            if in_treatment is not None:
                r.append(DataPoint(
                    region_schema=SCHEMA_ADMIN_1,
                    region_parent=admin_0,
                    region_child=admin_1,
                    datatype=DT_STATUS_HOSPITALIZED,
                    value=int(in_treatment),
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

        return r


def get_powerbi_data():
    apb = _WestAfricaPowerBI(
        WestAfricaPowerBI.PATH_PREFIX,
        WestAfricaPowerBI.POWERBI_URL
    )
    return apb.get_powerbi_data()


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_powerbi_data())
