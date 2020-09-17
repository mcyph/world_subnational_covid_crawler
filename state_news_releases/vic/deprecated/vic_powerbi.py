from datetime import datetime
from os.path import exists

from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.state_news_releases.PowerBIDataReader import (
    PowerBIDataReader
)
from covid_19_au_grab.state_news_releases.vic.deprecated.VicPowerBI import (
    VicPowerBI, get_globals
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.get_package_dir import (
    get_data_dir
)


BASE_PATH = get_data_dir() / 'vic' / 'powerbi'
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
        previously_active_regions = set()
        previously_active_regions_postcode = set()

        for updated_date, rev_id, response_dict in sorted(list(self._iter_all_dates())):
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
                print("Specific date found for:", subdir, updated_date)
            except (KeyError, ValueError, AttributeError): # FIXME!!!! ==============================================================================
                print(f"SPECIFIC DATE NOT AVAILABLE FOR: {updated_date}")

                if updated_date > '2020_05_15':
                    raise

            try:
                active_updated_date = self._get_active_updated_date(response_dict)
            except (KeyError, ValueError, AttributeError):
                active_updated_date = updated_date
                print(f"ACTIVE SPECIFIC DATE NOT AVAILABLE FOR: {updated_date}")

                if updated_date > '2020_06_15':
                    raise

            if active_updated_date != updated_date:
                print("****ACTIVE != TOTAL DATE:", active_updated_date, updated_date)

            # DISABLED, as this data is also in the Tableau data, and doesn't completely align!! ===============================
            #r.extend(self._get_age_data(updated_date, response_dict))
            r.extend(self._get_source_of_infection(updated_date, response_dict))

            self.totals_dict = {}
            r.extend(self._get_regions(updated_date, response_dict))
            r.extend(self._get_active_regions(
                active_updated_date, response_dict, previously_active_regions
            ))

            if updated_date >= '2020_08_10':
                self.totals_dict_postcode = {}
                r.extend(self._get_regions_postcode(updated_date, response_dict))
                r.extend(self._get_active_regions_postcode(
                    active_updated_date, response_dict, previously_active_regions_postcode
                ))

        return r

    #============================================================================#
    #                             Get updated date                               #
    #============================================================================#

    def _get_updated_date(self, response_dict):
        # Try to get updated date from source, if possible
        # "M0": "08/04/2020 - 12:03:00 PM"
        data = response_dict['total_updated_date'][1]

        updated_str = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        updated_date = datetime.strptime(
            updated_str.split('-')[0].strip(), '%d/%m/%Y'
        ).strftime('%Y_%m_%d')
        return updated_date

    def _get_active_updated_date(self, response_dict):
        """
        The active updated date may not always be the same as the totals date
        """
        try:
            data = response_dict['active_updated_date'][1]
        except KeyError:
            data = response_dict['total_updated_date'][1]

        updated_str = data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0'][0]['M0']
        updated_date = datetime.strptime(
            updated_str.split('-')[0].strip(), '%d/%m/%Y'
        ).strftime('%Y_%m_%d')
        return updated_date

    #============================================================================#
    #                             Data by postcode                               #
    #============================================================================#

    def _get_regions_postcode(self, updated_date, response_dict):
        output = []
        data = response_dict['regions_postcode'][1]
        previous_value = None

        for region_child in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            value, previous_value = self.process_powerbi_value(region_child, previous_value, data)
            if value[0] is None:
                continue

            region_string = value[0].split('(')[0].strip().strip('s')
            output.append(DataPoint(
                region_schema=Schemas.POSTCODE,
                region_parent='au-vic',
                region_child=region_string,
                datatype=DataTypes.TOTAL,
                value=value[1],
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
            previous_value = value
            # print(output[-1])

            self.totals_dict_postcode[region_string] = value[1]

        return output

    def _get_active_regions_postcode(self, updated_date, response_dict,
                                     previously_active_regions):
        if updated_date < '2020_05_07':
            # There wasn't this info before this date!
            return []

        output = []
        data = response_dict['regions_active_postcode'][1]

        previous_value = None
        currently_active_regions = set()

        for region_child in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            value, previous_value = self.process_powerbi_value(region_child, previous_value, data)
            if value[0] is None:
                continue

            # Add active info
            region_string = value[0].split('(')[0].strip().strip('s')
            previously_active_regions.add(region_string)
            currently_active_regions.add(region_string)

            output.append(DataPoint(
                region_schema=Schemas.POSTCODE,
                region_parent='au-vic',
                region_child=region_string,
                datatype=DataTypes.STATUS_ACTIVE,
                value=value[1],
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))

            if region_string in self.totals_dict_postcode:
                # Add recovered info if total available
                output.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='au-vic',
                    region_child=region_string,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=self.totals_dict_postcode[region_string] - value[1],
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

            previous_value = value
            # print(output[-1])

        for region_child in previously_active_regions - currently_active_regions:
            # Make sure previous "active" values which are
            # no longer being reported are reset to 0!
            output.append(DataPoint(
                region_schema=Schemas.POSTCODE,
                region_parent='au-vic',
                region_child=region_child,
                datatype=DataTypes.STATUS_ACTIVE,
                value=0,
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))

            if region_child in self.totals_dict_postcode:
                # Add recovered info if total available
                output.append(DataPoint(
                    region_schema=Schemas.POSTCODE,
                    region_parent='au-vic',
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=self.totals_dict_postcode[region_child],
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

        return output

    #============================================================================#
    #                                Data by LGA                                 #
    #============================================================================#

    def _get_regions(self, updated_date, response_dict):
        output = []
        data = response_dict['regions'][1]
        previous_value = None

        for region_child in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            value, previous_value = self.process_powerbi_value(region_child, previous_value, data)
            if value[0] is None:
                continue

            region_string = value[0].split('(')[0].strip()
            output.append(DataPoint(
                region_schema=Schemas.LGA,
                region_child=region_string,
                datatype=DataTypes.TOTAL,
                value=value[1],
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
            previous_value = value
            # print(output[-1])

            self.totals_dict[region_string] = value[1]

        return output

    def _get_active_regions(self, updated_date, response_dict,
                            previously_active_regions):
        if updated_date < '2020_05_07':
            # There wasn't this info before this date!
            return []

        output = []
        data = response_dict['regions_active'][1]

        previous_value = None
        currently_active_regions = set()

        for region_child in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            value, previous_value = self.process_powerbi_value(region_child, previous_value, data)
            if value[0] is None:
                continue

            # Add active info
            region_string = value[0].split('(')[0].strip()
            previously_active_regions.add(region_string)
            currently_active_regions.add(region_string)

            output.append(DataPoint(
                region_schema=Schemas.LGA,
                region_child=region_string,
                datatype=DataTypes.STATUS_ACTIVE,
                value=value[1],
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))

            if region_string in self.totals_dict:
                # Add recovered info if total available
                output.append(DataPoint(
                    region_schema=Schemas.LGA,
                    region_child=region_string,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=self.totals_dict[region_string]-value[1],
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

            previous_value = value
            # print(output[-1])

        for region_child in previously_active_regions-currently_active_regions:
            # Make sure previous "active" values which are
            # no longer being reported are reset to 0!
            output.append(DataPoint(
                region_schema=Schemas.LGA,
                region_child=region_child,
                datatype=DataTypes.STATUS_ACTIVE,
                value=0,
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))

            if region_child in self.totals_dict:
                # Add recovered info if total available
                output.append(DataPoint(
                    region_schema=Schemas.LGA,
                    region_child=region_child,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=self.totals_dict[region_child],
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

        return output

    #============================================================================#
    #                               Age breakdown                                #
    #============================================================================#

    def _get_age_data(self, updated_date, response_dict):
        output = []
        DataTypes.TOTAL_NOTSTATED = 999999999 # HACK!
        data = response_dict['age_data'][1]

        cols = data['result']['data']['dsr']['DS'][0]['SH'][0]['DM1']
        cols = [i['G1'].rstrip('s') for i in cols]
        #print("COLS:", cols)

        gender_mapping = {
            '': DataTypes.TOTAL_NOTSTATED,
            'Female': DataTypes.TOTAL_FEMALE,
            'Male': DataTypes.TOTAL_MALE,
            'Not stated': DataTypes.TOTAL_NOTSTATED,
            'Other': DataTypes.TOTAL_NOTSTATED
        }
        age_mapping = {
            'Other': 'Unknown',
            'Unknown': 'Unknown',
            '00-04': '0-9',
            '05-09': '0-9',
            '10-14': '10-19',
            '15-19': '10-19',
            '20-24': '20-29',
            '25-29': '20-29',
            '30-34': '30-39',
            '35-39': '30-39',
            '40-44': '40-49',
            '45-49': '40-49',
            '50-54': '50-59',
            '55-59': '50-59',
            '60-64': '60-69',
            '65-69': '60-69',
            '70-74': '70-79',
            '75-79': '70-79',
            '80-84': '80-84',
            '85+': '85+',
        }

        col_mapping = []
        for col in cols:
            col_mapping.append(gender_mapping[col])
        #print(col_mapping)

        assert DataTypes.TOTAL_MALE in col_mapping
        assert DataTypes.TOTAL_FEMALE in col_mapping

        totals = {}
        female = {}
        male = {}

        for age in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            X = age['X']
            vals_dict = {}
            if not X:
                continue
            #print(X)

            i = 0
            X_i = 0
            while i < len(X):
                if X[i].get('I'):
                    # "jump to column index"
                    X_i = X[i]['I']
                
                if len(X) > 0:
                    # Note that previous value simply means the very last value seen
                    # That means that if female/not stated is 67 and the following
                    # male stat is also 67 it'll be elided with an R-repeat val
                    value_1 = X[i].get(
                        'M0', previous_value if X[i].get('R') else 0
                    )
                    previous_value = value_1
                else:
                    value_1 = 0

                # Make it so that if there's a blank column and a
                # "not specified" column they're both added together
                # into the total
                vals_dict[col_mapping[X_i]] = (
                    vals_dict.get(col_mapping[X_i], 0) + value_1
                )
                X_i += 1
                i += 1

            # Convert from e.g. "10-14" or "15-19" to "10-19"
            agerange = age_mapping[age['G0'].replace('–', '-')]

            if DataTypes.TOTAL_MALE in vals_dict:
                male.setdefault(agerange, 0)
                male[agerange] += vals_dict[DataTypes.TOTAL_MALE]

            if DataTypes.TOTAL_FEMALE in vals_dict:
                female.setdefault(agerange, 0)
                female[agerange] += vals_dict[DataTypes.TOTAL_FEMALE]

            # TODO: support "not stated" separately!!! ====================================================
            general_age = (
                vals_dict.get(DataTypes.TOTAL_MALE, 0) +
                vals_dict.get(DataTypes.TOTAL_FEMALE, 0) +
                vals_dict.get(DataTypes.TOTAL_NOTSTATED, 0)
            )
            totals.setdefault(agerange, 0)
            totals[agerange] += general_age

        for datatype, values in (
            (DataTypes.TOTAL_MALE, male),
            (DataTypes.TOTAL_FEMALE, female),
            (DataTypes.TOTAL, totals)
        ):
            for agerange, value in values.items():
                output.append(DataPoint(
                    datatype=datatype,
                    agerange=agerange,
                    value=value,
                    date_updated=updated_date,
                    source_url=SOURCE_URL
                ))

        return output

    #============================================================================#
    #                             Source of infection                            #
    #============================================================================#

    def _get_source_of_infection(self, updated_date, response_dict):
        # * Overseas acquired
        # * Cruise ship acquired (included in overseas acquired)
        # * Interstate acquired
        # * Locally acquired - contact of a confirmed case
        # * Locally acquired - contact not identified
        # * Under investigation

        # Normalise it with other states
        vic_norm_map = {
            'Travel overseas': DataTypes.SOURCE_OVERSEAS,
            'Contact with a confirmed case': DataTypes.SOURCE_CONFIRMED,
            'Acquired in Australia, unknown source': DataTypes.SOURCE_COMMUNITY,
            'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION
        }

        output = []
        data = response_dict['source_of_infection'][1]
        added = set()

        for source in data['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
            output.append(DataPoint(
                datatype=vic_norm_map[source['C'][0]],
                value=source['C'][1],
                date_updated=updated_date,
                source_url=SOURCE_URL
            ))
            added.add(vic_norm_map[source['C'][0]])

        for datatype in vic_norm_map.values():
            if datatype in added:
                continue

            # Sometimes "under investigation" isn't provided,
            # but probably can assume at 0 for these days
            output.append(DataPoint(
                datatype=datatype,
                value=0,
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
    __r = get_powerbi_data()
    for i in __r:
        if i.datatype in (DataTypes.SOURCE_OVERSEAS,):
            print(i)
    #pprint(__r)
