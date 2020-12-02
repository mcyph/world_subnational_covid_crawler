import csv
from glob import glob

from covid_19_au_grab.misc_data_scripts.other_data import UnderlayDataBase
from covid_19_au_grab.misc_data_scripts.other_data.TimeSeriesKey import \
    TimeSeriesKey, DataTypes.PERCENT, DataTypes.INTEGER, DataTypes.FLOATING_POINT
from covid_19_au_grab.misc_data_scripts.other_data import DataPoint
from covid_19_au_grab.misc_data_scripts.other_data import DateType
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes

from covid_19_au_grab.misc_data_scripts.other_data.abs_data.lga_to_state_and_name import \
    get_lga_to_state_and_name_dict
from covid_19_au_grab._utility.normalize_locality_name import \
    normalize_locality_name
from covid_19_au_grab._utility.get_package_dir import get_package_dir


lga_dict = get_lga_to_state_and_name_dict()


BASE_PATH = get_package_dir() / 'misc_data_scripts' / 'other_data' / 'abs_data' / 'stats'
BASE_EXCEL_PATH = get_package_dir() / 'misc_data_scripts' / 'other_data' / 'abs_data' / 'excel_stats'


class ExcelABSStats(UnderlayDataBase):
    IGNORE_KEYS = {
        'Age of Persons Born Overseas',
        'Business Entries',
        'Building Approvals',
        'Selected Government Pensions and Allowances',
        'Children Attending a Preschool Program',
        'Children Attending a Preschool Program (4 & 5 year olds)',
        'Children Enrolled in a Preschool Program (4 & 5 year olds)',
        'Age of Persons Born Overseas',
        'Religious Affiliation',
        'Religious Affiliation Persons Born Overseas',
        'Estimates of Personal Income',
        'Families by Type',
        'Gifts/donations reported by taxpayers',
        'Gross Capital Gains reported by taxpayers',
        'Number of Businesses',
        'Business Exits',
        'Dwelling Structure',
        'Registered Motor Vehicles',
    }

    OVER_65_KEYS = (
        'Persons - 65-69 years (no.)'
        'Persons - 70-74 years (no.)'
        'Persons - 75-79 years (no.)'
        'Persons - 80-84 years (no.)'
        'Persons - 85 and over (no.)'
    )

    def __init__(self):
        UnderlayDataBase.__init__(self,
            name='Australian Bureau of Statistics',
            desc='Statistics from the Australian Bureau of Statistics '
                 'under the Creative Commons BY-SA license',
        )

    def process_data(self):
        """
        {
           measure initial:
               {(state, lga name, stat name): (year, value), ...},
           ...
        }
        """
        for path in glob(f'{BASE_EXCEL_PATH}/*.csv'):
            self._process_csv_file(path)

    def get_time_series_source(self):
        for (state, lga_name), stat_dict in r.items():

            if 'Persons - 65-69 years (no.)' in stat_dict:
                # Get number of "Persons - 65-69 years (no.)",
                # deriving from other keys
                print(stat_dict)
                t = sum([stat_dict.get(k, 0) for k in self.OVER_65_KEYS])
                stat_dict['Persons - 65 years and over (%)'] = \
                    (t / stat_dict['Persons - Total (no.)']) * 100.0

            for k, v in list(stat_dict.items()):
                if (
                    (k.endswith(' years (no.)') or k.endswith(' years and over (no.)'))
                    and k != 'Persons - 65 years and over (%)'
                ):
                    # Convert "X-X years (no.)";
                    # "80 years and over (no.)" stats into %
                    # using "Persons - Total (no.)"
                    if 'Persons - Total (no.)' in stat_dict:
                        percent = (v / stat_dict['Persons - Total (no.)']) * 100.0
                        stat_dict[k.replace(' (no.)', ' (%)')] = percent
                    # print("DELETING 2:", k)
                    del stat_dict[k]

                # print(k)
                if (
                        k.startswith('Number of Employee Jobs -') and
                        k != 'Number of Employee Jobs - Total'
                ):
                    # Convert Number of Employment Jobs - X into %
                    # using Number of Employee Jobs - Total
                    if 'Number of Employee Jobs - Total' in stat_dict:
                        percent = (v / stat_dict['Number of Employee Jobs - Total']) * 100.0
                        stat_dict[k + ' (%)'] = percent
                    # print("DELETING:", k)
                    del stat_dict[k]

    def _process_csv_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            # The first row contains base header info
            first_header_row = []
            for i in f.readline().split(',')[3:]:
                if i.strip():
                    first_header_row.append(i)
                    previous = i
                else:
                    first_header_row.append(previous)
            del previous

            reader = csv.DictReader(f)
            for row in reader:
                self._process_row(first_header_row, row)

    def _process_row(self, first_header_row, row):
        # "MEASURE","Data item","REGIONTYPE","Geography Level","LGA_2018","Region","FREQUENCY","Frequency","TIME","Time","Value","Flag Codes","Flags"
        # "PRESCH_2","4 year olds enrolled in preschool or in a preschool program (no.)","LGA2018","Local Government Areas (2018)","10050","Albury (C)","A","Annual","2016","2016",580,,

        # Map the LGA id to the state/locality name
        lga_id = int(row['Code'])
        try:
            region_parent, lga_name = lga_dict[lga_id]
        except KeyError:
            print("Warning: LGA ID not found", row)
            return

        # This is often more useful, as it doesn't include ..council etc!!!
        lga_name = row['Label'].split('(')[0].strip()
        lga_name = normalize_locality_name(lga_name)

        for xx, (stat_name, value) in enumerate(list(row.items())[3:]):
            if value == '-':
                # Value not supplied
                continue

            header_name = first_header_row[xx].split(' - ')[0].strip()
            year = int(row['Year'])

            # Parse value to float if there's a decimal
            value = value.replace(',', '')
            if '.' in value:
                value = float(value)
            else:
                value = int(value)

            # If it's a percentile value and it's
            # over 100%, there's something wrong!
            if stat_name.endswith('(%)'):
                if value >= 100.0:
                    print("PC VAL > 100: ", row)
                    value = 100.0  # WTF??!
                datatype = DataTypes.PERCENT
            elif isinstance(value, float):
                datatype = DataTypes.FLOATING_POINT
            elif isinstance(value, int):
                datatype = DataTypes.INTEGER
            else:
                raise Exception()

            if not stat_name in self.time_series_source:
                self.time_series_source.append(TimeSeriesKey(
                    key_group=header_name,
                    key=stat_name,
                    datatype=datatype,
                    desc=None
                ))

            time_series_key = self.time_series_source[stat_name]
            time_series_key.append(DataPoint(
                date=DateType(year=year),
                region_schema=Schemas.LGA,
                region_parent=region_parent,
                region_child=lga_name,
                value=value
            ))


if __name__ == '__main__':
    inst = ExcelABSStats()
    #pprint(inst.get_encoded_data())

    with open('abs_out.json', 'w', encoding='utf-8') as f:
        f.write(inst.get_encoded_data_as_json(newest_only=True))
