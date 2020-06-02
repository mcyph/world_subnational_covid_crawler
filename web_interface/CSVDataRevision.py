import csv
import json
import datetime
from pytz import timezone
from os.path import getctime
from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.datatypes.constants import \
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
            x['region_parent'],
            x['datatype'],
            x['agerange'],
            x['region_child']
        )

    def __generic_sort_key(self, x):
        """
        Sort only by state, datatype and name, ignoring date
        """
        # print(x)
        return (
            x['region_parent'],
            x['datatype'],
            x['agerange'],
            x['region_child']
        )

    #=============================================================#
    #                       Get DataPoints                        #
    #=============================================================#

    def get_combined_values_by_datatype(self, region_schema, datatypes, 
                                        from_date=None,
                                        region_parent=None, region_child=None):
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
        if isinstance(region_schema, int):
            region_schema = schema_to_name(region_schema)

        def to_datetime(dt):
            return datetime.datetime.strptime(dt, '%d/%m/%Y')

        combined = {}
        for datatype in datatypes:
            if isinstance(datatype, int):
                datatype = constant_to_name(datatype)

            for datapoint in self.get_combined_value(region_schema, datatype,
                                                     from_date=from_date,
                                                     region_parent=region_parent,
                                                     region_child=region_child):

                if datapoint['agerange'] and datapoint['region_child']:
                    k = f"{datapoint['agerange']} {datapoint['region_child']}"
                elif datapoint['agerange']:
                    k = datapoint['agerange'] or ''
                else:
                    k = datapoint['region_child'] or ''

                i_combined = combined.setdefault(datapoint['region_parent'], {}) \
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
                i_combined['region_child'] = datapoint['region_child']
                i_combined['region_parent'] = datapoint['region_parent']
                i_combined['region_schema'] = datapoint['region_schema']

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
        e.g. if filters (a list of ((region_schema, datatype, region_parent/None), ...) is (
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
        for region_schema, datatype, region_parent in filters:
            if isinstance(region_schema, int):
                region_schema = schema_to_name(region_schema)
            if isinstance(datatype, int):
                datatype = constant_to_name(datatype)

            for datapoint in self.get_combined_value(region_schema, datatype, region_parent,
                                                     from_date=from_date):

                i_combined = combined.setdefault(
                    (datapoint['region_parent'], datapoint['region_child']), {}
                )

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
                #if datapoint['region_child']:
                #    k = f"{k} ({datapoint['region_child']})"

                i_combined['region_parent'] = datapoint['region_parent']
                i_combined['region_child'] = datapoint['region_child']
                i_combined['agerange'] = datapoint['agerange']
                i_combined['region_schema'] = datapoint['region_schema']

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
    def get_combined_value(self, region_schema, datatype,
                           region_parent=None, region_child=None,
                           from_date=None):
        """
        Filter `datapoints` to have only `datatype` (e.g. "DT_PATIENT_STATUS"),
        and optionally only have `name` (e.g. "Recovered" or "None" as a string)

        Returns only the most recent value (optionally from `from_date`)
        """
        if not hasattr(self, '_datapoints_dict'):
            self.__create_datapoints_dict()

        if isinstance(region_schema, int):
            region_schema = schema_to_name(region_schema)
        if isinstance(datatype, int):
            datatype = constant_to_name(datatype)

        def date_greater_than_or_equal(x, y):
            #print(x, y)

            dd1, mm1, yyyy1 = x.split('/')
            x = (int(yyyy1), int(mm1), int(dd1))

            dd2, mm2, yyyy2 = y.split('/')
            y = (int(yyyy2), int(mm2), int(dd2))

            return x >= y

        if region_child is not None:
            datapoints = self._datapoints_dict3.get((region_parent, region_child, region_schema, datatype), [])
        elif region_parent is not None:
            datapoints = self._datapoints_dict2.get((region_parent, region_schema, datatype), [])
        else:
            datapoints = self._datapoints_dict.get((region_schema, datatype), [])

        if not datapoints:
            print(f"WARNING: not found for {region_parent}, {region_schema}, {datatype}")

        r = {}
        for datapoint in datapoints:
            if from_date is not None and not date_greater_than_or_equal(
                from_date, datapoint['date_updated']
            ):
                continue

            # Note we're restricting to only `datatype` already,
            # so no need to include it in the key
            unique_k = (
                datapoint['region_parent'],
                datapoint['agerange'],
                datapoint['region_child']
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
        d3 = {}
        for datapoint in self._datapoints[:]:
            d.setdefault((datapoint['region_schema'], datapoint['datatype']), []).append(datapoint)
            d2.setdefault((datapoint['region_parent'], datapoint['region_schema'], datapoint['datatype']), []).append(datapoint)
            d3.setdefault((datapoint['region_parent'], datapoint['region_child'], datapoint['region_schema'], datapoint['datatype']), []).append(datapoint)
        self._datapoints_dict = d
        self._datapoints_dict2 = d2
        self._datapoints_dict3 = d3


if __name__ == '__main__':
    from pprint import pprint
    inst = CSVDataRevision('2020_05_01', 4)

    for day in range(1, 30):
        print(day)

        if False:
            pprint([
                i for i in inst.get_combined_values_by_datatype(
                    region_schema='lga',
                    datatypes=('total', 'source_overseas', 'tests_total'),
                    from_date=f'{day}/04/2020',
                    region_parent='nsw'
                ) if i['region_child'] == 'Penrith'
            ])
        elif True:
            pprint([
                (i['total (Penrith)'], i['total (Penrith) date_updated'])
                for i in inst.get_combined_values(
                    [['lga', 'total', 'nsw']],
                    from_date=f'{day}/04/2020'
                )
            ])
