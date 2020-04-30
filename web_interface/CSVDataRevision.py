import csv
import json
import datetime
from pytz import timezone
from os.path import getctime
from covid_19_au_grab.get_package_dir import get_package_dir


OUTPUT_DIR = get_package_dir() / 'state_news_releases' / 'output'


class CSVDataRevision:
    def __init__(self, period, subperiod_id):
        self.__check_period(period)
        subperiod_id = int(subperiod_id)
        self.period = period
        self.subperiod_id = subperiod_id
        self.__datapoints = self.__read_csv()

    def __getitem__(self, item):
        return self.__datapoints[item]

    def __iter__(self):
        for i in self.__datapoints:
            yield i

    def __len__(self):
        return len(self.__datapoints)

    def get_datapoints(self):
        return self.__datapoints[:]

    #=============================================================#
    #                       Utility Functions                     #
    #=============================================================#

    def __check_period(self, path):
        assert not '..' in path
        assert not '/' in path
        assert not '\\' in path

        dd, mm, yyyy = path.split('_')
        int(yyyy), int(mm), int(dd)

    def __read_csv(self):
        out = []
        with open(OUTPUT_DIR / f'{self.period}-{self.subperiod_id}.tsv',
                  'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                out.append(row)

        out.sort(key=self.__date_updated_sort_key)
        return out

    def get_status_dict(self, ):
        with open(OUTPUT_DIR / f'{self.period}-{self.subperiod_id}.json',
                  'r', encoding='utf-8', errors='replace') as f:
            return json.loads(f.read())['status']

    def get_revision_time_string(self):
        rev_time = getctime(OUTPUT_DIR / f'{self.period}-{self.subperiod_id}.tsv')
        dt = str(datetime.datetime.fromtimestamp(rev_time) \
                 .astimezone(timezone('Australia/Melbourne'))).split('.')[0]
        return dt

    def __date_updated_sort_key(self, x):
        """
        Sort so that the most recent dates come first,
        then sort by state, datatype and name
        """

        def sortable_date(i):
            dd, mm, yyyy = i.split('/')
            return (
                str(9999 - int(yyyy)) + '_' +
                str(99 - int(mm)) + '_' +
                str(99 - int(dd))
            )

        return (
            sortable_date(x['date_updated']),
            x['state_name'],
            x['datatype'],
            x['name']
        )

    def __generic_sort_key(self, x):
        """
        Sort only by state, datatype and name, ignoring date
        """
        # print(x)
        return (
            x['state_name'],
            x['datatype'],
            x['name']
        )

    #=============================================================#
    #                       Get DataPoints                        #
    #=============================================================#

    def get_combined_values_by_datatype(self, datatypes, from_date=None):
        """
        Returns as a combined dict,
        e.g. if datatypes a list of ((datatype, name/None), ...) is (
            "DT_AGE",
            "DT_AGE_FEMALE",
        )
        it will output as [{
            'name': (e.g.) '70+',
            'date_updated': ...,
            'DT_AGE': ...,
            'DT_AGE_FEMALE': ...
        }, ...]
        """
        def to_datetime(dt):
            return datetime.datetime.strptime(dt, '%d/%m/%Y')

        combined = {}
        for datatype in datatypes:
            for datapoint in self.get_combined_value(datatype, from_date=from_date):

                i_combined = combined.setdefault(datapoint['state_name'], {}) \
                                     .setdefault(datapoint['name'], {})

                if (
                    not 'date_updated' in i_combined or
                    to_datetime(datapoint['date_updated']) <
                        to_datetime(i_combined['date_updated'])
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint['date_updated']
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%d/%m/%Y')

                i_combined['name'] = datapoint['name']
                i_combined['state_name'] = datapoint['state_name']

                if not datatype in i_combined:
                    i_combined[datatype] = datapoint['value']
                    i_combined[f'{datatype} date_updated'] = datapoint['date_updated']
                    i_combined[f'{datatype} source_url'] = datapoint['source_url']

        out = []
        for i_combined in combined.values():
            for add_me in i_combined.values():
                out.append(add_me)
        return out

    def get_combined_values(self, filters, from_date=None):
        """
        Returns as a combined dict,
        e.g. if filters (a list of ((datatype, name/None), ...) is (
            ("DT_PATIENT_STATUS", "Recovered"),
            ("DT_PATIENT_STATUS", "ICU")
        )
        it will output as [{
            'date_updated': ...,
            'DT_PATIENT_STATUS (Recovered)': ...,
            'DT_PATIENT_STATUS (ICU)': ...
        }, ...]
        """
        def to_datetime(dt):
            return datetime.datetime.strptime(dt, '%d/%m/%Y')

        combined = {}
        for datatype, name in filters:
            for datapoint in self.get_combined_value(datatype, name, from_date=from_date):

                i_combined = combined.setdefault(datapoint['state_name'], {})

                if (
                    not 'date_updated' in i_combined or
                    to_datetime(datapoint['date_updated']) <
                        to_datetime(i_combined['date_updated'])
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint['date_updated']
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%d/%m/%Y')

                k = (
                    f'{datatype} ({datapoint["name"]})'
                    if datapoint["name"] != 'None'
                    else datatype
                )

                i_combined['state_name'] = datapoint['state_name']

                if not k in i_combined:
                    i_combined[k] = datapoint['value']
                    i_combined[f'{k} date_updated'] = datapoint['date_updated']
                    i_combined[f'{k} source_url'] = datapoint['source_url']
                    i_combined[f'{k} text_match'] = (
                        datapoint['text_match']
                        if datapoint['text_match'] != "'None'"
                        else ''
                    )

        out = []
        for i_combined in combined.values():
            out.append(i_combined)
        return out

    def get_combined_value(self, datatype, name=None, from_date=None):
        """
        Filter `datapoints` to have only `datatype` (e.g. "DT_PATIENT_STATUS"),
        and optionally only have `name` (e.g. "Recovered" or "None" as a string)

        Returns only the most recent value (optionally from `from_date`)
        """

        def date_greater_than(x, y):
            #print(x, y)

            dd1, mm1, yyyy1 = x.split('/')
            x = (int(yyyy1), int(mm1), int(dd1))

            dd2, mm2, yyyy2 = y.split('/')
            y = (int(yyyy2), int(mm2), int(dd2))

            return x >= y

        r = {}
        for datapoint in self.__datapoints[:]:
            if datapoint['datatype'] != datatype:
                continue
            elif name is not None and datapoint['name'] != name:
                continue
            elif from_date is not None and not date_greater_than(
                from_date, datapoint['date_updated']
            ):
                continue

            # Note we're restricting to only `datatype` already,
            # so no need to include it in the key
            unique_k = (
                datapoint['state_name'],
                datapoint['name']
            )
            if unique_k in r:
                assert date_greater_than(
                    r[unique_k]['date_updated'],
                    datapoint['date_updated']
                )
                continue
            r[unique_k] = datapoint

        r = list(r.values())
        r.sort(key=self.__generic_sort_key)
        return r
