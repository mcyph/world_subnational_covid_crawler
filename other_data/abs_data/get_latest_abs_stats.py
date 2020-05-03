from os.path import expanduser
import csv
from glob import glob
from covid_19_au_grab.other_data.abs_data.lga_to_state_and_name import \
    get_lga_to_state_and_name_dict
from covid_19_au_grab.normalize_locality_name import \
    normalize_locality_name
from covid_19_au_grab.get_package_dir import get_package_dir


lga_dict = get_lga_to_state_and_name_dict()

BASE_PATH = get_package_dir() / 'other_data' / 'abs_data' / 'stats'
BASE_EXCEL_PATH = get_package_dir() / 'other_data' / 'abs_data' / 'excel_stats'


# "MEASURE","Data item","REGIONTYPE","Geography Level","LGA_2018","Region","FREQUENCY","Frequency","TIME","Time","Value","Flag Codes","Flags"
# "PRESCH_2","4 year olds enrolled in preschool or in a preschool program (no.)","LGA2018","Local Government Areas (2018)","10050","Albury (C)","A","Annual","2016","2016",580,,


def get_latest_abs_stats():
    """
    {
       measure initial:
           {(state, lga name, stat name): (year, value), ...},
       ...
    }
    """
    r = {}

    for path in glob(f'{BASE_PATH}/*.csv'):
        if not 'SEIFA' in path:
            # Better to use the excel reader for non-SEIFA stats!
            continue

        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['Value']:
                    continue

                # SEIFA data includes percentile, decile, ranks within area
                # I'm only going to get the national percentile values
                if 'Measure' in row and row['Measure'] != 'Rank within Australia - Percentile':
                    continue
                elif 'Measure' in row:
                    row['Index Type'] += ' (%)'

                # Map the LGA id to the state/locality name
                lga_id = int(row.get('LGA_2018') or row['LGA_2011'])
                try:
                    state, lga_name = lga_dict[lga_id]
                except KeyError:
                    print("Warning: LGA ID not found", row)
                    continue

                if True:
                    # This is often more useful, as it doesn't include ..council etc!!!
                    lga_name = (row.get('Region') or row['Local Government Areas - 2011']).split('(')[0].strip()
                    lga_name = normalize_locality_name(lga_name)

                stat_name = row.get('Data item') or row['Index Type']
                year = int(row['Time'])

                # Parse value to float if there's a decimal
                if '.' in row['Value']:
                    value = float(row['Value'])
                else:
                    value = int(row['Value'])

                # If it's a percentile value and it's
                # over 100%, there's something wrong!
                if stat_name.endswith('(%)'):
                    if value >= 100.0:
                        print("PC VAL > 100: ", row)
                        value = 100.0   # WTF??!

                MEASURE_key = (
                    row['MEASURE'].rpartition('_')[0]
                    if '_' in row['MEASURE']
                    else row['MEASURE']
                )
                if not MEASURE_key in r:
                    r[MEASURE_key] = {}

                key = (state, lga_name, stat_name)
                if key in r[MEASURE_key] and r[MEASURE_key][key][0] > year:
                    continue
                r[MEASURE_key][key] = (year, value)
    return r


def get_latest_excel_abs_stats():
    """
    {
       measure initial:
           {(state, lga name, stat name): (year, value), ...},
       ...
    }
    """
    r = {}

    for path in glob(f'{BASE_EXCEL_PATH}/*.csv'):
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
                # Map the LGA id to the state/locality name
                lga_id = int(row['Code'])
                try:
                    state, lga_name = lga_dict[lga_id]
                except KeyError:
                    print("Warning: LGA ID not found", row)
                    continue

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
                            value = 100.0   # WTF??!

                    if not header_name in r:
                        r[header_name] = {}

                    key = (state, lga_name, stat_name)
                    if key in r[header_name] and r[header_name][key][0] > year:
                        continue
                    r[header_name][key] = (year, value)
    return r


def get_output_abs_json(stats_dict, states, lga_names):
    r = {}
    sub_headers = []
    updated_dates = []

    for (state, lga_name, stat_name), (year, value) in stats_dict.items():
        r.setdefault((
            state.lower(),
            lga_name.lower().replace(' - ', '-')
        ), {})[stat_name] = value

    for (state, lga_name), stat_dict in r.items():
        # Get number of "Persons - 65-69 years (no.)",
        #  "Persons - 65-69 years (no.)",
        #  "Persons - 70-74 years (no.)",
        #  "Persons - 75-79 years (no.)",
        #  "Persons - 80-84 years (no.)",
        #  "Persons - 85 years and over (no.)"
        if 'Persons - 65-69 years (no.)' in stat_dict:
            print(stat_dict)
            t = (
                stat_dict.get('Persons - 65-69 years (no.)', 0) +
                stat_dict.get('Persons - 70-74 years (no.)', 0) +
                stat_dict.get('Persons - 75-79 years (no.)', 0) +
                stat_dict.get('Persons - 80-84 years (no.)', 0) +
                stat_dict.get('Persons - 85 and over (no.)', 0)
            )
            stat_dict['Persons - 65 years and over (%)'] = \
                (t / stat_dict['Persons - Total (no.)']) * 100.0

        for k, v in list(stat_dict.items()):
            if (
                (
                    k.endswith(' years (no.)') or
                    k.endswith(' years and over (no.)')
                )
                and k != 'Persons - 65 years and over (%)'
            ):
                # Convert "X-X years (no.)";
                # "80 years and over (no.)" stats into %
                # using "Persons - Total (no.)"
                if 'Persons - Total (no.)' in stat_dict:
                    percent = (v / stat_dict['Persons - Total (no.)'])*100.0
                    stat_dict[k.replace(' (no.)', ' (%)')] = percent
                #print("DELETING 2:", k)
                del stat_dict[k]

            #print(k)
            if (
                k.startswith('Number of Employee Jobs -') and
                k != 'Number of Employee Jobs - Total'
            ):
                # Convert Number of Employment Jobs - X into %
                # using Number of Employee Jobs - Total
                if 'Number of Employee Jobs - Total' in stat_dict:
                    percent = (v / stat_dict['Number of Employee Jobs - Total']) * 100.0
                    stat_dict[k + ' (%)'] = percent
                #print("DELETING:", k)
                del stat_dict[k]


    for (state, lga_name), stat_dict in r.items():
        for stat_name in stat_dict:
            if not stat_name in sub_headers:
                sub_headers.append(stat_name)
                updated_dates.append(2020)   # HACK!!!

            r.setdefault((state, lga_name), {})[stat_name] = stat_dict[stat_name]

    sub_headers.sort()

    data = []
    for (state, lga_name), stat_dict in r.items():
        if state.lower() in (#'tas', 'nt', 'sa',
                             'ot',):  # HACK - no use outputting if not displaying anyway!
            continue

        #if 'Completed Year 12 or equivalent (%)' in stat_dict:
        #    print(stat_dict['Completed Year 12 or equivalent (%)'])

        if not state in states:
            states.append(state)

        if not lga_name in states:
            lga_names.append(lga_name)

        data.append(
            [states.index(state), lga_names.index(lga_name)] + [
                stat_dict.get(stat_name, "")
                for stat_name
                in sub_headers
            ]
        )

    return {
        #'updated_dates': updated_dates,
        'sub_headers': sub_headers,
        'data': data
    }


if __name__ == '__main__':
    import json
    from pprint import pprint

    stats_dicts = get_latest_abs_stats()
    stats_dicts.update(get_latest_excel_abs_stats())

    states = []
    lga_names = []

    out = {}
    for MEASURE_key, value in stats_dicts.items():
        if MEASURE_key in (
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
        ):
            continue

        out[MEASURE_key] = get_output_abs_json(
            value, states, lga_names
        )
    #pprint(output)

    with open('abs_stats.json', 'w', encoding='utf-8') as f:
        out = {
            'states': states,
            'lga_names': lga_names,
            'data': out
        }
        out = json.dumps(
            json.loads(
                json.dumps(out),
                parse_float=lambda x: round(float(x), 1)
            ),
            separators=(',', ':')
        )
        f.write(out)
