from datetime import datetime
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_crawlers.oceania.au_data.CacheBase import CacheBase


class Covid19AUData(CacheBase):
    STATE_NAME = 'au'

    SOURCE_URL = 'https://covid-19-au.com'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'au_covid_19_au'

    def __init__(self):
        CacheBase.__init__(self)
        self.sdpf = StrictDataPointsFactory(
            region_mappings={},
            mode=MODE_STRICT
        )
        self.update()

    def update(self):
        dir_ = self._get_new_dir()

        self.download_to(
            dir_ / 'country.json',
            'https://raw.githubusercontent.com/covid-19-au/covid-19-au.github.io/dev/src/data/country.json'
        )
        self.download_to(
            dir_ / 'state.json',
            'https://raw.githubusercontent.com/covid-19-au/covid-19-au.github.io/dev/src/data/state.json'
        )

    def get_datapoints(self):
        r = []
        r.extend(self._get_country_data())
        r.extend(self._get_state_data())
        return r

    def _get_country_data(self):
        r = self.sdpf()
        data = self.get_json('country.json')

        for date, values in data.items():
            date = datetime.strptime(date, '%Y-%m-%d')
            d = self._unpack_values(values)

            for datatype, value in d.items():
                r.append(
                    region_schema=Schemas.ADMIN_0,
                    region_parent='',
                    region_child='AU',

                    datatype=datatype,
                    value=value,
                    date_updated=date.strftime('%Y_%m_%d')
                )

        return r

    def _get_state_data(self):
        r = self.sdpf()
        data = self.get_json('state.json')

        for date, state_dict in data.items():
            date = datetime.strptime(date, '%Y-%m-%d')

            for state, values in state_dict.items():
                d = self._unpack_values(values)

                for datatype, value in d.items():
                    r.append(
                        region_schema=Schemas.ADMIN_1,
                        region_parent='AU',
                        region_child='AU-%s' % state,

                        datatype=datatype,
                        value=value,
                        date_updated=date.strftime('%Y_%m_%d')
                    )

        return r

    def _unpack_values(self, values):
        d = {}

        if len(values) == 8:
            d[DataTypes.TOTAL], \
            d[DataTypes.STATUS_DEATHS], \
            d[DataTypes.STATUS_RECOVERED], \
            d[DataTypes.TESTS_TOTAL], \
            d[DataTypes.STATUS_ACTIVE], \
            d[DataTypes.STATUS_HOSPITALIZED], \
            d[DataTypes.STATUS_ICU], \
            d[DataTypes.STATUS_VACCINATED], = values
        elif len(values) == 7:
            d[DataTypes.TOTAL], \
            d[DataTypes.STATUS_DEATHS], \
            d[DataTypes.STATUS_RECOVERED], \
            d[DataTypes.TESTS_TOTAL], \
            d[DataTypes.STATUS_ACTIVE], \
            d[DataTypes.STATUS_HOSPITALIZED], \
            d[DataTypes.STATUS_ICU] = values
        elif len(values) == 6:
            d[DataTypes.TOTAL], \
            d[DataTypes.STATUS_DEATHS], \
            d[DataTypes.STATUS_RECOVERED], \
            d[DataTypes.TESTS_TOTAL], \
            d[DataTypes.STATUS_ACTIVE], \
            d[DataTypes.STATUS_HOSPITALIZED] = values
        elif len(values) == 5:
            d[DataTypes.TOTAL], \
            d[DataTypes.STATUS_DEATHS], \
            d[DataTypes.STATUS_RECOVERED], \
            d[DataTypes.TESTS_TOTAL], \
            d[DataTypes.STATUS_ACTIVE] = values
        elif len(values) == 4:
            d[DataTypes.TOTAL], \
            d[DataTypes.STATUS_DEATHS], \
            d[DataTypes.STATUS_RECOVERED], \
            d[DataTypes.TESTS_TOTAL] = values
        elif len(values) == 1:
            d[DataTypes.TOTAL], = values
        else:
            raise ValueError(values)

        return d


if __name__ == '__main__':
    from pprint import pprint
    pprint(Covid19AUData().get_datapoints())
