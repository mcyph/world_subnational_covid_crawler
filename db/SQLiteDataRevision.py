import csv
import json
import datetime
from io import StringIO
from pytz import timezone
from os.path import getctime
from covid_19_au_grab.get_package_dir import get_output_dir, get_package_dir
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.db.DataPointsDB import DataPointsDB
from covid_19_au_grab.datatypes.datapoints_thinned_out import \
    datapoints_thinned_out


OUTPUT_DIR = get_output_dir() / 'output'


def needsdatapoints(fn):
    def newfn(self, *args, **kw):
        if self._datapoints_db is None:
            self._read_sqlite()
        return fn(self, *args, **kw)
    return newfn


class SQLiteDataRevision:
    def __init__(self, period, subperiod_id, datapoints_db=None):
        self.__check_period(period)
        subperiod_id = int(subperiod_id)
        self.period = period
        self.subperiod_id = subperiod_id
        self._datapoints_db = datapoints_db

    def _read_sqlite(self):
        self._datapoints_db = DataPointsDB(
            OUTPUT_DIR / f'{self.period}-{self.subperiod_id}.sqlite'
        )

    def get_status_dict(self, ):
        with open(OUTPUT_DIR / f'{self.period}-{self.subperiod_id}.json',
                  'r', encoding='utf-8', errors='replace') as f:
            return json.loads(f.read())['status']
    
    @needsdatapoints
    def __getitem__(self, item):
        return self._datapoints_db[item]

    @needsdatapoints
    def __iter__(self):
        for i in self._datapoints_db:
            yield i

    @needsdatapoints
    def __len__(self):
        return len(self._datapoints_db)

    @needsdatapoints
    def get_datapoints(self):
        return self._datapoints_db[:]

    @needsdatapoints
    def get_updated_dates(self, region_schema, region_parent, region_child):
        return [i.date_updated for i in self._datapoints_db.select_many(
            region_schema=region_schema,
            region_parent=region_parent,
            region_child=region_child
        )]

    @needsdatapoints
    def get_time_series(self, datatypes,
                        region_schema,
                        region_parent,
                        region_child):

        datatypes = [i.value for i in datatypes]
        datapoints = self._datapoints_db.select_many(
            region_schema=['= ?', [region_schema]],
            region_parent=['= ?', [region_parent]] if region_parent else None,
            region_child=['= ?', [region_child]] if region_child else None,
            datatype=[f"IN ({','.join('?' for _ in datatypes)})", datatypes],

            source_id=['!= ?', ['us_nytimes']],  # HACK!
        )

        r = {}
        for datapoint in datapoints:
            r.setdefault(
                (datapoint.region_child, datapoint.agerange), {}
            ).setdefault(
                datapoint.date_updated, []
            ).append(datapoint)
        return r

    @needsdatapoints
    def get_source_ids(self):
        return self._datapoints_db.get_source_ids()

    @needsdatapoints
    def get_datapoints_by_source_id(self, source_id):
        return self._datapoints_db.get_datapoints_by_source_id(source_id)

    @needsdatapoints
    def get_region_schemas(self):
        return self._datapoints_db.get_region_schemas()

    @needsdatapoints
    def get_datatypes_by_region_schema(self, region_schema):
        return self._datapoints_db.get_datatypes_by_region_schema(region_schema)

    @needsdatapoints
    def get_region_parents(self, region_schema):
        return self._datapoints_db.get_region_parents(region_schema)

    #=============================================================#
    #                       Utility Functions                     #
    #=============================================================#

    def __check_period(self, path):
        assert not '..' in path
        assert not '/' in path
        assert not '\\' in path

        dd, mm, yyyy = path.split('_')
        int(yyyy), int(mm), int(dd)

    def get_revision_time_string(self):
        rev_time = getctime(OUTPUT_DIR / f'{self.period}-{self.subperiod_id}.sqlite')
        dt = str(datetime.datetime.fromtimestamp(rev_time) \
                 .astimezone(timezone('Australia/Melbourne'))).split('.')[0]
        return dt

    def __date_updated_sort_key(self, x):
        """
        Sort so that the most recent dates come first,
        then sort by state, datatype and name
        """
        def sortable_date(i):
            yyyy, mm, dd = i.split('_')
            return (
                str(9999 - int(yyyy)) + '_' +
                str(99 - int(mm)) + '_' +
                str(99 - int(dd))
            )

        return (
            sortable_date(x.date_updated),
            x.region_parent,
            x.region_child,
            x.datatype,
            x.agerange,
            x.region_child
        )

    def __generic_sort_key(self, x):
        """
        Sort only by state, datatype and name, ignoring date
        """
        return (
            x.region_parent,
            x.region_child,
            x.datatype,
            x.agerange,
            x.region_child
        )

    def get_tsv_data(self, source_id, thin_out=True):
        datapoints = self.get_datapoints_by_source_id(source_id)

        datapoints.sort(
            key=lambda i: i.date_updated,
            reverse=True
        )

        assert datapoints

        if thin_out:
            datapoints = datapoints_thinned_out(datapoints)

        datapoints.sort(key=lambda i: (
            i.date_updated,
            i.region_schema,
            i.region_parent,
            i.region_child,
            i.agerange
        ))

        csvfile = StringIO()
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([i for i in datapoints[0]._fields])

        for datapoint in datapoints:
            row = []
            for key, value in zip(datapoint._fields, datapoint):
                if key == 'region_schema':
                    row.append(value.value)
                elif key == 'datatype':
                    row.append(value.value)
                else:
                    row.append(value)
            writer.writerow(row)

        csvfile.seek(0)
        return csvfile.read()

    #=============================================================#
    #                       Get DataPoints                        #
    #=============================================================#

    def get_combined_values_by_datatype(self, region_schema, datatypes, 
                                        from_date=None,
                                        region_parent=None, region_child=None):
        """
        Returns as a combined dict,
        e.g. if datatypes a list of ((datatype, name/None), ...) is (
            "DataTypes.AGE",
            "DataTypes.AGE_FEMALE",
        )
        it will output as [{
            'name': (e.g.) '70+',
            'date_updated': ...,
            'DataTypes.AGE': ...,
            'DataTypes.AGE_FEMALE': ...
        }, ...]
        """
        if region_parent:
            region_parent = region_parent.lower()
        if region_child:
            region_child = region_child.lower()

        combined = {}
        for datatype in datatypes:
            for datapoint in self.get_combined_value(region_schema, datatype,
                                                     from_date=from_date,
                                                     region_parent=region_parent,
                                                     region_child=region_child):

                if datapoint.agerange and datapoint.region_child:
                    k = f"{datapoint.agerange} {datapoint.region_child}"
                elif datapoint.agerange:
                    k = datapoint.agerange or ''
                else:
                    k = datapoint.region_child or ''

                i_combined = combined.setdefault(datapoint.region_parent, {}) \
                                     .setdefault(k, {})

                if (
                    not 'date_updated' in i_combined or
                    datapoint.date_updated < i_combined['date_updated']
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint.date_updated
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%Y_%m_%d')

                i_combined['agerange'] = datapoint.agerange
                i_combined['region_child'] = datapoint.region_child
                i_combined['region_parent'] = datapoint.region_parent
                i_combined['region_schema'] = datapoint.region_schema

                if not datatype.value in i_combined:
                    i_combined[datatype.value] = datapoint.value
                    i_combined[f'{datatype.value} date_updated'] = datapoint.date_updated
                    i_combined[f'{datatype.value} source_url'] = datapoint.source_url

        out = []
        for i_combined in combined.values():
            for add_me in i_combined.values():
                out.append(add_me)
        return out

    def get_combined_values(self, filters, from_date=None):
        """
        Returns as a combined dict,
        e.g. if filters (a list of ((region_schema, datatype, region_parent/None), ...) is (
            (DataTypes.PATIENT_STATUS, "Recovered"),
            (DataTypes.PATIENT_STATUS, "ICU")
        )
        it will output as [{
            'date_updated': ...,
            'DataTypes.PATIENT_STATUS (Recovered)': ...,
            'DataTypes.PATIENT_STATUS (ICU)': ...
        }, ...]
        """

        combined = {}
        for region_schema, datatype, region_parent in filters:
            if region_parent:
                region_parent = region_parent.lower()

            for datapoint in self.get_combined_value(region_schema,
                                                     datatype,
                                                     region_parent,
                                                     from_date=from_date):

                i_combined = combined.setdefault(
                    (datapoint.region_parent, datapoint.region_child), {}
                )

                if (
                    not 'date_updated' in i_combined or
                    datapoint.date_updated < i_combined['date_updated']
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint.date_updated
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%Y_%m_%d')

                k = datatype
                if datapoint.agerange:
                    k = f"{k} ({datapoint.agerange})"
                #if datapoint['region_child']:
                #    k = f"{k} ({datapoint['region_child']})"

                i_combined['region_parent'] = datapoint.region_parent
                i_combined['region_child'] = datapoint.region_child
                i_combined['agerange'] = datapoint.agerange
                i_combined['region_schema'] = datapoint.region_schema

                if not k in i_combined:
                    i_combined[k] = datapoint.value
                    i_combined[f'{k} date_updated'] = datapoint.date_updated
                    i_combined[f'{k} source_url'] = datapoint.source_url
                    i_combined[f'{k} text_match'] = datapoint.text_match or ''

        out = []
        for i_combined in combined.values():
            out.append(i_combined)
        return out
    
    @needsdatapoints
    def get_combined_value(self, region_schema, datatype,
                           region_parent=None, region_child=None,
                           from_date=None):
        """
        Filter `datapoints` to have only `datatype` (e.g. "DataTypes.PATIENT_STATUS"),
        and optionally only have `name` (e.g. "Recovered" or "None" as a string)

        Returns only the most recent value (optionally from `from_date`)
        """

        if region_child: region_child = region_child.lower()
        if region_parent: region_parent = region_parent.lower()

        datapoints = self._datapoints_db.select_many(
            region_schema=['= ?', [region_schema]] if region_schema is not None else None,
            region_parent=['= ?', [region_parent]] if region_parent is not None else None,
            region_child=['= ?', [region_child]] if region_child is not None else None,
            date_updated=['<= ?', [from_date]] if from_date is not None else None,
            datatype=['= ?', [datatype]] if datatype is not None else None,
            order_by='date_updated DESC',
            add_source_url=True
        )

        if not datapoints:
            print(f"WARNING: not found for {region_parent}, {region_schema}, {datatype}")

        r = {}
        for datapoint in datapoints:
            # Note we're restricting to only `datatype` already,
            # so no need to include it in the key
            unique_k = (
                datapoint.region_parent,
                datapoint.agerange,
                datapoint.region_child
            )
            if unique_k in r:
                continue
            r[unique_k] = datapoint

        r = list(r.values())
        r.sort(key=self.__generic_sort_key)
        return r


if __name__ == '__main__':
    from pprint import pprint
    inst = SQLiteDataRevision('2020_05_01', 4)

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
