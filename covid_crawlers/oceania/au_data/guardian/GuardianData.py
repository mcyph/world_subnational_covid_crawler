# https://docs.google.com/spreadsheets/d/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE/edit#gid=0
# https://docs.google.com/spreadsheets/d/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE/edit#gid=1437767505
# https://docs.google.com/spreadsheets/d/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE/edit#gid=167406050

from datetime import datetime
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_crawlers.oceania.au_data.CacheBase import CacheBase

URL_TEMPLATE = 'https://docs.google.com/spreadsheet/ccc?key=%(long_id)s&gid=%(short_id)s&output=csv'

STATE_LATEST_STATS_URL = URL_TEMPLATE % {'long_id': '1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE', 'short_id': '0'}
STATE_STATS_HISTORY_URL = URL_TEMPLATE % {'long_id': '1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE', 'short_id': '1437767505'}
STATE_DEATHS_URL = URL_TEMPLATE % {'long_id': '1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE', 'short_id': '167406050'}


class GuardianData(CacheBase):
    STATE_NAME = 'au'

    SOURCE_URL = 'https://docs.google.com/spreadsheets/d/1q5gdePANXci8enuiS4oHUJxcxC13d6bjMRSicakychE/edit#gid=0'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'au_guardian'

    def __init__(self):
        CacheBase.__init__(self)
        self.sdpf = StrictDataPointsFactory(
            region_mappings={},
            mode=MODE_STRICT
        )
        self.update()

    def update(self):
        dir_ = self._get_new_dir()

        self.download_to(dir_ / 'latest_stats.csv', STATE_LATEST_STATS_URL)
        self.download_to(dir_ / 'stats_history.csv', STATE_STATS_HISTORY_URL)
        self.download_to(dir_ / 'deaths.csv', STATE_DEATHS_URL)

    def get_datapoints(self):
        r = []
        r.extend(self._get_stats_history())
        return r

    def _get_stats_history(self):
        # State	Date	Time	Cumulative case count	Cumulative deaths
        # Tests conducted (negative)	Tests conducted (total)
        # Hospitalisations (count)	Intensive care (count)
        # Ventilator usage (count)	Recovered (cumulative)
        # Update Source	Notes
        # SA	23/01/2020		0			6					SA Health website
        # NSW	25/01/2020		3								NSW Health media release

        r = self.sdpf()
        data = self.get_csv('stats_history.csv')

        for item in data:
            state = 'AU-%s' % item['State']
            date = datetime.strptime(item['Date'], '%d/%m/%Y')

            for k, v in item.items():
                if v == '-':
                    item[k] = ''

            d = {}
            if item['Cumulative case count']:
                d[DataTypes.TOTAL] = item['Cumulative case count']
            if item['Cumulative deaths']:
                d[DataTypes.STATUS_DEATHS] = item['Cumulative deaths']
            if item['Tests conducted (negative)']:
                d[DataTypes.TESTS_NEGATIVE] = item['Tests conducted (negative)']
            if item['Tests conducted (total)']:
                d[DataTypes.TESTS_TOTAL] = item['Tests conducted (total)']
            if item['Hospitalisations (count)']:
                d[DataTypes.STATUS_HOSPITALIZED] = item['Hospitalisations (count)']
            if item['Intensive care (count)']:
                d[DataTypes.STATUS_ICU] = item['Intensive care (count)']
            if item['Ventilator usage (count)']:
                d[DataTypes.STATUS_ICU_VENTILATORS] = item['Ventilator usage (count)']
            if item['Recovered (cumulative)']:
                d[DataTypes.STATUS_RECOVERED] = item['Recovered (cumulative)']
                if DataTypes.TOTAL in d:
                    d[DataTypes.STATUS_ACTIVE] = \
                        str(int(d[DataTypes.TOTAL].replace(',', '')) -
                            int(d[DataTypes.STATUS_RECOVERED].replace(',', '')))

            for datatype, value in d.items():
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='AU',
                    region_child=state,

                    datatype=datatype,
                    value=int(value.replace(',', '')),
                    date_updated=date.strftime('%Y_%m_%d')
                )
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(GuardianData().get_datapoints())
