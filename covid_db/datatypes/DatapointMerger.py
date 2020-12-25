import re
import json
import snappy
import hashlib
from _utility.get_package_dir import get_cache_dir
from covid_db.datatypes.DataPoint import _DataPoint


DATE_RE = re.compile('[0-9]{4}_[0-9]{2}_[0-9]{2}(-[0-9]*)?')


class DataPointMerger(list):
    def __init__(self, source_id=None):
        list.__init__(self)
        self.__added = set()
        self.source_id = source_id
        self.__after_date = None

        if source_id:
            self.__restore_state()

    #==========================================================#
    # List append/extend methods
    #==========================================================#

    def extend(self, datapoints):
        r = []
        for datapoint in datapoints:
            i = self.append(datapoint)
            if i is not None:
                r.append(i)
        return r

    def append(self, datapoint, also_append_to=None):
        unique_key = (
            datapoint.region_schema,
            datapoint.region_parent,
            datapoint.region_child,
            datapoint.date_updated,
            datapoint.datatype,
            datapoint.agerange,
            datapoint.source_id
        )
        if not unique_key in self.__added:
            self.__added.add(unique_key)
            list.append(self, datapoint)
            if also_append_to is not None:
                also_append_to.append(datapoint)
            return datapoint
        return None

    #==========================================================#
    # Save/restore state (to conserve resources)
    #==========================================================#

    def iter_unprocessed_dates(self, dates):
        self.__max_date = max(dates)

        if self.__after_date is None:
            r = sorted(dates)
        else:
            r = sorted([i for i in dates if i > self.__after_date])
        return r

    def __restore_state(self):
        cache_path = self.__get_state_path()

        if not cache_path.parent.exists():
            cache_path.parent.mkdir()

        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                data = json.loads(snappy.decompress(f.read()))
                data['datapoints'] = [_DataPoint(*i) for i in data['datapoints']]
                self.__after_date = data['last_date']
                self.extend(data['datapoints'])

    def save_state(self):
        assert self.source_id, \
            "Source ID must be specified to allow saving state!"

        cache_path = self.__get_state_path()
        json_data = json.dumps({
            'last_date': self.__max_date,
            'datapoints': [tuple(i) for i in self]
        }).encode('utf-8')
        json_data = snappy.compress(json_data)

        with open(cache_path, 'wb') as f:
            f.write(json_data)

    def __get_state_path(self):
        return get_cache_dir() / self.source_id / '_merge_cache.json'
