import csv
import datetime
import numpy as np
from os import listdir
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
from matplotlib.font_manager import FontProperties
from covid_19_au_grab._utility.get_package_dir import get_package_dir


OUTPUT_CSV_DIR = (
    get_package_dir() / 'state_news_releases' / 'output'
)
GRAPH_OUTPUT_DIR = (
    get_package_dir() / 'output_graphs' / 'output'
)


def read_csv(region_schema,
             datatype,
             agerange_filter=None,
             region_filter=None,
             value_filter=None,
             state_filter=None):

    if state_filter and not isinstance(state_filter, (list, tuple)):
        state_filter = (state_filter,)

    r = {}

    # Get the newest, based on binary sort order
    # (year->month->day->revision id)
    fnam = list(sorted(
        [
            i for i in listdir(OUTPUT_CSV_DIR)
            if i.endswith('.tsv')
        ],
        key=lambda k: (
            k.split('-')[0],
            int(k.split('-')[1].split('.')[0]
        ))
    ))[-1]

    with open(OUTPUT_CSV_DIR / fnam, 'r',
              encoding='utf-8', errors='replace') as f:

        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            print(row)
            if region_schema != row['region_schema']:
                continue
            if row['datatype'] != datatype:
                continue
            if state_filter and row['region_parent'] not in state_filter:
                continue
            if value_filter and not value_filter(row['value']):
                continue

            if agerange_filter and not agerange_filter(row['agerange']):
                print("IGNORE:", row)
                continue
            elif not agerange_filter and row['agerange']:
                # Only include by agerange if explicit!!
                continue

            if region_filter and not region_filter(row['region_child']):
                print("IGNORE:", row)
                continue

            key = row['region_parent']
            if row['region_child']:
                key = f'{key} {row["region_child"]}'
            if row['agerange']:
                key = f'{key} {row["agerange"]}'

            r.setdefault(key, []).append((
                datetime.datetime.strptime(
                    row['date_updated'], '%d/%m/%Y'
                ),
                int(row['value'])
            ))

    for k, v in r.items():
        v.sort()
    return r


COLORS = [
    'blue',
    'orange',
    'green',
    'red',
    'purple',
    'brown',
    'pink',
    'gray',
    'cyan',
    'yellow'
]
STYLES = [
    '-',
    '--',
    '-.',
    ':'
]
MARKERS = [
    'o',
    'P',
    '.',
    'X'
]


def output_graph(datatype,
                 region_schema='statewide',
                 agerange_filter=None,
                 region_filter=None,
                 value_filter=None,
                 state_filter=None,
                 append_to_name=None):

    if isinstance(state_filter, str):
        state_filter = (state_filter,)

    plt.figure(figsize=(10, 8), dpi=80)
    max_y = 0

    for x, (k, v) in enumerate(read_csv(
        region_schema, datatype, agerange_filter, region_filter, value_filter, state_filter
    ).items()):
        print(k)
        X = np.array([i[0] for i in v])
        Y = [i[1] for i in v]

        for i in Y:
            if max_y < i:
                max_y = i

        plt.plot(
            X, Y,
            color=COLORS[x % len(COLORS)],
            label=k,
            marker=MARKERS[x // len(COLORS)],
            linestyle=STYLES[x // len(COLORS)]
        )

    y_label = (
        f'%s (%s)' % (datatype, ','.join(state_filter))
        if state_filter
        else datatype
    )
    y_label = (
        f'%s (%s)' % (y_label, append_to_name)
        if append_to_name
        else y_label
    )

    fontP = FontProperties()
    fontP.set_size('small')

    ax = plt.gca()
    formatter = mdates.DateFormatter("%d/%m")
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(formatter)

    plt.xlabel('Date')
    plt.ylabel(y_label)

    if max_y > 50 and datatype != 'new' and False:
        plt.yscale('log')
        for axis in [ax.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
            formatter = axis.get_major_formatter()
            axis.set_minor_formatter(formatter)

    plt.legend(prop=fontP)
    plt.grid()
    #plt.show()

    plt.savefig(GRAPH_OUTPUT_DIR / f'{y_label}.png')
    plt.clf()


def output_graphs():
    # Output basic numbers
    output_graph('total', 'statewide')
    output_graph('new', 'statewide')
    output_graph('tests_total', 'statewide')

    # Output age distribution graphs
    output_graph('total_male', state_filter='vic')
    output_graph('total_female', state_filter='vic')
    output_graph('total_male', state_filter='nsw')
    output_graph('total_female', state_filter='nsw')
    output_graph('total_male', state_filter='sa')
    output_graph('total_female', state_filter='sa')
    output_graph('total', state_filter='act')
    output_graph('total_male', state_filter='qld')
    output_graph('total_female', state_filter='qld')
    output_graph('total', state_filter='qld')

    # Output "by region_child" graphs
    output_graph('total', 'lga',
                 state_filter='vic',
                 region_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('total', 'lga',
                 state_filter='vic',
                 region_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('total', 'lga',
                 state_filter='nsw',
                 region_filter=lambda p: p[0].lower() < 'f',
                 append_to_name='a-e')
    output_graph('total', 'lga',
                 state_filter='nsw',
                 region_filter=lambda p: 'f' <= p[0].lower() < 'p',
                 append_to_name='f-o')
    output_graph('total', 'lga',
                 state_filter='nsw',
                 region_filter=lambda p: p[0].lower() >= 'p',
                 append_to_name='p-z')
    output_graph('total', 'lga',
                 state_filter='wa',
                 region_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('total', 'lga',
                 state_filter='wa',
                 region_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('total', 'lga',
                 state_filter='sa',
                 region_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('total', 'lga',
                 state_filter='sa',
                 region_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('status_active', 'lga',
                 state_filter='sa',
                 region_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('status_active', 'lga',
                 state_filter='sa',
                 region_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('total', 'lga',
                 state_filter='qld',
                 region_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('total', 'lga',
                 state_filter='qld',
                 region_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('source_overseas', 'lga',
                 state_filter='qld',
                 region_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('source_overseas', 'lga',
                 state_filter='qld',
                 region_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('total', 'lha', state_filter='nsw')  # LGA??
    output_graph('total', 'hhs', state_filter='qld')
    output_graph('status_active', 'hhs', state_filter='qld')
    output_graph('status_deaths', 'hhs', state_filter='qld')
    output_graph('status_recovered', 'hhs', state_filter='qld')
    output_graph('new', 'hhs', state_filter='qld')
    output_graph('new', 'lga', state_filter='wa')

    # TODO: Add source of infection
    #output_graph('DataTypes.SOURCE_OF_INFECTION')
    #output_graph('DataTypes.SOURCE_OF_INFECTION', state_filter='sa')
    #output_graph('DataTypes.SOURCE_OF_INFECTION', state_filter='vic')
    #output_graph('DataTypes.SOURCE_OF_INFECTION', state_filter='nsw')
    #output_graph('DataTypes.SOURCE_OF_INFECTION', state_filter='act')
    #output_graph('DataTypes.SOURCE_OF_INFECTION', state_filter='qld')

    # TODO: Add patient status
    #output_graph('DataTypes.PATIENT_STATUS', state_filter='sa')
    #output_graph('DataTypes.PATIENT_STATUS', state_filter='vic')
    #output_graph('DataTypes.PATIENT_STATUS', state_filter='act')
    #output_graph('DataTypes.PATIENT_STATUS', state_filter='nsw')
    #output_graph('DataTypes.PATIENT_STATUS', state_filter='wa')
    #output_graph('DataTypes.PATIENT_STATUS', state_filter='qld')


if __name__ == '__main__':
    output_graphs()
    #output_graph('total', state_filter='qld', region_filter=lambda x: x == 'Darling Downs', append_to_name='TEST')
