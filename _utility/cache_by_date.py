import re
import json
import snappy
import hashlib
from _utility.get_package_dir import get_cache_dir
from covid_db.datatypes.DataPoint import _DataPoint


DATE_RE = re.compile('[0-9]{4}_[0-9]{2}_[0-9]{2}(-[0-9]*)?')


def cache_by_date(source_id):
    def new_fn(fn):
        def new_fn(self, arg, *args, **kw):
            try:
                date = arg.name
            except AttributeError:
                date = arg

            assert DATE_RE.match(date), date
            fnam = hashlib.md5((source_id + date).encode('utf-8')).hexdigest()
            cache_path = get_cache_dir() / source_id / f'{fnam}.json'

            if not cache_path.parent.exists():
                cache_path.parent.mkdir()

            if cache_path.exists():
                with open(cache_path, 'rb') as f:
                    datapoints = json.loads(snappy.decompress(f.read()))
                    return [_DataPoint(*i) for i in datapoints]
            else:
                datapoints = fn(self, date, *args, **kw)  # WARNING: args/kw aren't taken into account here!!
                json_data = json.dumps([tuple(i) for i in datapoints]).encode('utf-8')
                json_data = snappy.compress(json_data)

                with open(cache_path, 'wb') as f:
                    f.write(json_data)
                return datapoints

        return new_fn
    return new_fn
