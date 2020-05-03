import csv
import json
import datetime
from pytz import timezone
from os.path import getctime
from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.state_news_releases.constants import \
    schema_to_name, constant_to_name


OUTPUT_DIR = get_package_dir() / 'state_news_releases' / 'output'


def needsdatapoints(fn):
    def newfn(self, *args, **kw):
        if self._datapoints is None:
            self._read_csv()
        return fn(self, *args, **kw)
    return newfn


class CSVDataRevision:
    def __init__(self, period, subperiod_id):
        self.__check_period(period)
        subperiod_id = int(subperiod_id)
        self.period = period
        self.subperiod_id = subperiod_id
        self._datapoints = None # self.__read_csv()
    
    def _read_csv(self):
        self._datapoints = self.__read_csv()
    
    @needsdatapoints
    def __getitem__(self, item):
        return self._datapoints[item]

    @needsdatapoints
    def __iter__(self):
        for i in self._datapoints:
            yield i

    @needsdatapoints
    def __len__(self):
        return len(self._datapoints)

    @needsdatapoints
    def get_datapoints(self):
        return self._datapoints[:]

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
            x['agerange'],
            x['region']
        )

    def __generic_sort_key(self, x):
        """
        Sort only by state, datatype and name, ignoring date
        """
        # print(x)
        return (
            x['state_name'],
            x['datatype'],
            x['agerange'],
            x['region']
        )

    #=============================================================#
    #                       Get DataPoints                        #
    #=============================================================#

    def get_combined_values_by_datatype(self, schema, datatypes, 
                                        from_date=None, state_name=None):
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
        if isinstance(schema, int):
            schema = schema_to_name(schema)[7:].lower()

        def to_datetime(dt):
            return datetime.datetime.strptime(dt, '%d/%m/%Y')

        combined = {}
        for datatype in datatypes:
            if isinstance(datatype, int):
                datatype = constant_to_name(datatype)[3:].lower()

            for datapoint in self.get_combined_value(schema, datatype,
                                                     from_date=from_date,
                                                     state_name=state_name):

                if datapoint['agerange'] and datapoint['region']:
                    k = f"{datapoint['agerange']} {datapoint['region']}"
                elif datapoint['agerange']:
                    k = datapoint['agerange'] or ''
                else:
                    k = datapoint['region'] or ''

                i_combined = combined.setdefault(datapoint['state_name'], {}) \
                                     .setdefault(k, {})

                if (
                    not 'date_updated' in i_combined or
                    to_datetime(datapoint['date_updated']) <
                        to_datetime(i_combined['date_updated'])
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint['date_updated']
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%d/%m/%Y')

                i_combined['agerange'] = datapoint['agerange']
                i_combined['region'] = datapoint['region']
                i_combined['state_name'] = datapoint['state_name']
                i_combined['schema'] = datapoint['schema']

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
        e.g. if filters (a list of ((schema, datatype, state_name/None), ...) is (
            (DT_PATIENT_STATUS, "Recovered"),
            (DT_PATIENT_STATUS, "ICU")
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
        for schema, datatype, state_name in filters:
            if isinstance(schema, int):
                schema = schema_to_name(schema)[7:].lower()
            if isinstance(datatype, int):
                datatype = constant_to_name(datatype)[3:].lower()

            for datapoint in self.get_combined_value(schema, datatype, state_name,
                                                     from_date=from_date):

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

                k = datatype
                if datapoint['agerange']:
                    k = f"{k} ({datapoint['agerange']})"
                if datapoint['region']:
                    k = f"{k} ({datapoint['region']})"

                i_combined['state_name'] = datapoint['state_name']
                i_combined['region'] = datapoint['region']
                i_combined['agerange'] = datapoint['agerange']
                i_combined['schema'] = datapoint['schema']

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
    
    @needsdatapoints
    def get_combined_value(self, schema, datatype, state_name=None, from_date=None):
        """
        Filter `datapoints` to have only `datatype` (e.g. "DT_PATIENT_STATUS"),
        and optionally only have `name` (e.g. "Recovered" or "None" as a string)

        Returns only the most recent value (optionally from `from_date`)
        """
        if not hasattr(self, '_datapoints_dict'):
            self.__create_datapoints_dict()

        if isinstance(schema, int):
            schema = schema_to_name(schema)[7:].lower()
        if isinstance(datatype, int):
            datatype = constant_to_name(datatype)[3:].lower()

        def date_greater_than_or_equal(x, y):
            #print(x, y)

            dd1, mm1, yyyy1 = x.split('/')
            x = (int(yyyy1), int(mm1), int(dd1))

            dd2, mm2, yyyy2 = y.split('/')
            y = (int(yyyy2), int(mm2), int(dd2))

            return x >= y

        if state_name is not None:
            datapoints = self._datapoints_dict2.get((state_name, schema, datatype), [])
        else:
            datapoints = self._datapoints_dict.get((schema, datatype), [])

        if not datapoints:
            print(f"WARNING: not found for {state_name}, {schema}, {datatype}")

        r = {}
        for datapoint in datapoints:
            if from_date is not None and not date_greater_than_or_equal(
                from_date, datapoint['date_updated']
            ):
                continue

            # Note we're restricting to only `datatype` already,
            # so no need to include it in the key
            unique_k = (
                datapoint['state_name'],
                datapoint['agerange'],
                datapoint['region']
            )
            if unique_k in r:
                assert date_greater_than_or_equal(
                    r[unique_k]['date_updated'],
                    datapoint['date_updated']
                )
                continue
            r[unique_k] = datapoint

        r = list(r.values())
        r.sort(key=self.__generic_sort_key)
        return r

    def __create_datapoints_dict(self):
        d = {}
        d2 = {}
        for datapoint in self._datapoints[:]:
            d.setdefault((datapoint['schema'], datapoint['datatype']), []).append(datapoint)
            d2.setdefault((datapoint['state_name'], datapoint['schema'], datapoint['datatype']), []).append(datapoint)
        self._datapoints_dict = d
        self._datapoints_dict2 = d2


if __name__ == '__main__':
    from pprint import pprint
    inst = CSVDataRevision('2020_05_01', 4)

    for day in range(1, 30):
        print(day)

        if False:
            pprint([
                i for i in inst.get_combined_values_by_datatype(
                    schema='lga',
                    datatypes=('total', 'source_overseas', 'tests_total'),
                    from_date=f'{day}/04/2020',
                    state_name='nsw'
                ) if i['region'] == 'Penrith'
            ])
        elif True:
            pprint([
                (i['total (Penrith)'], i['total (Penrith) date_updated'])
                for i in inst.get_combined_values(
                    [['lga', 'total', 'nsw']],
                    from_date=f'{day}/04/2020'
                )
            ])
