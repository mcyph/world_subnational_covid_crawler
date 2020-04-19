from os.path import expanduser
import csv
from glob import glob
from covid_19_au_grab.other_data.abs_data.lga_to_state_and_name import \
    get_lga_to_state_and_name_dict


lga_dict = get_lga_to_state_and_name_dict()
BASE_PATH = expanduser('~/dev/covid_19_au_grab/other_data/abs_data/stats')


# "MEASURE","Data item","REGIONTYPE","Geography Level","LGA_2018","Region","FREQUENCY","Frequency","TIME","Time","Value","Flag Codes","Flags"
# "PRESCH_2","4 year olds enrolled in preschool or in a preschool program (no.)","LGA2018","Local Government Areas (2018)","10050","Albury (C)","A","Annual","2016","2016",580,,


def get_latest_abs_stats():
    r = {} # {(state, lga name, stat name): (year, value), ...}


    for path in glob(f'{BASE_PATH}/*.csv'):
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
                #print(row)
                lga_id = int(row.get('LGA_2018') or row['LGA_2011'])
                try:
                    state, lga_name = lga_dict[lga_id]
                except KeyError:
                    print("Warning: LGA ID not found", row)
                    continue

                stat_name = row.get('Data item') or row['Index Type']
                year = int(row['Time'])

                if '.' in row['Value']:
                    value = float(row['Value'])
                else:
                    value = int(row['Value'])

                if stat_name.endswith('(%)'):
                    if value >= 100.0:
                        print("PC VAL > 100: ", row)
                        value = 100.0   # WTF??!

                key = (state, lga_name, stat_name)
                if key in r and r[key][0] > year:
                    continue
                r[key] = (year, value)
    return r


def get_output_abs_json():
    r = {}
    sub_headers = []
    updated_dates = []

    for (state, lga_name, stat_name), (year, value) in get_latest_abs_stats().items():
        r.setdefault((state, lga_name), {})[stat_name] = value

    for (state, lga_name), stat_dict in r.items():
        # Get number of "Persons - 65-69 years (no.)",
        #  "Persons - 65-69 years (no.)",
        #  "Persons - 70-74 years (no.)",
        #  "Persons - 75-79 years (no.)",
        #  "Persons - 80-84 years (no.)",
        #  "Persons - 85 years and over (no.)"
        if 'Persons - 65-69 years (no.)' in stat_dict:
            t = (
                stat_dict['Persons - 65-69 years (no.)'] +
                stat_dict['Persons - 70-74 years (no.)'] +
                stat_dict['Persons - 75-79 years (no.)'] +
                stat_dict['Persons - 80-84 years (no.)'] +
                stat_dict['Persons - 85 and over (no.)']
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

            r.setdefault((state, lga_name), {})[stat_name] = \
                stat_dict[stat_name]


    data = []
    for (state, lga_name), stat_dict in r.items():
        #if 'Completed Year 12 or equivalent (%)' in stat_dict:
        #    print(stat_dict['Completed Year 12 or equivalent (%)'])

        data.append(
            [state, lga_name] + [
                stat_dict.get(stat_name)
                for stat_name
                in sub_headers
            ]
        )

    return {
        'updated_dates': updated_dates,
        'sub_headers': sub_headers,
        'data': data
    }


if __name__ == '__main__':
    import json
    from pprint import pprint

    output = get_output_abs_json()
    #pprint(output)

    with open('abs_stats.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(output))
