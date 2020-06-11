import json


class TimeSeriesSource:
    def __init__(self, name, desc):

        # Name/description of the source itself
        # (e.g. "OECD economic statistics" or something)
        self.name = name
        self.desc = desc

        # A dict from {group: [key, ...], ...}
        # Each key must be in a specific group.
        # For example, the group might be "Occupation"
        # and keys be "Managers (%)" or "Professionals (%)"
        self.key_groups = {}

        #self._possible_keys = set([
        #    v for k, v in key_groups.items()
        #])
        self._time_series_keys = {}

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False

    def __getitem__(self, item):
        return self._time_series_keys[item]

    def keys(self):
        return self._time_series_keys.keys()

    def append(self, inst):
        self._time_series_keys[inst.key] = inst

    def get_json(self):
        """
        returns -> {
            "region_ids": {}, // for schema/parent/child together
            "time_series_ids": {},
            "metadata": {
                "region_schema": {
                    "region_parent":
                        {...optional metadata...}
                }
            },
            "key_groups": {
                group_key: [key, ...],
                ...
            },
            "data": {
                "region_schema": {
                    "region_parent": {
                        "region_child": []]
                            "time_series_key": {
                                "datetype": (value)
                            }
                        }
                    }
                }
            }
        }
        """

        r = {
            'region_ids': {},
            'time_series_ids': {},
            'metadata': {},
            'key_groups': self.key_groups,
            'data': {}
        }

        def get_id(s):
            if not s in r['region_ids']:
                r['region_ids'][s] = str(len(r['region_ids']))
            return r['region_ids'][s]

        def get_time_series_id(s):
            if not s in r['time_series_ids']:
                r['time_series_ids'][s] = str(len(r['time_series_ids']))
            return r['time_series_ids'][s]

        for key, inst in self._time_series_keys.items():
            key_id = get_id(key)

            for schema_key, schema_dict in inst.get_datapoints_dict().items():
                schema_key_id = get_id(schema_key)

                for parent_key, parent_dict in schema_dict.items():
                    parent_key_id = get_id(parent_key)

                    for child_key, child_tsk in parent_dict.items():
                        child_key_id = get_id(child_key)
                        print(schema_key, parent_key, child_key, child_tsk)

                        out = []
                        for tsk in sorted(child_tsk.values(),
                                          key=lambda datapoint: str(datapoint[0].date),
                                          reverse=True):
                            # Make a flat list in pairs to reduce
                            # unnecessary [] characters
                            if len(tsk) != 1:
                                print("WARNING - datapoints have more than one value for date:", tsk)

                            tsk = tsk[0]
                            out.append(int(get_time_series_id(str(tsk.date))))
                            out.append(tsk.value)

                        r['data'].setdefault(key_id, {}) \
                                 .setdefault(schema_key_id, {}) \
                                 .setdefault(parent_key_id, {}) \
                                 .setdefault(child_key_id, out)

        r['region_ids'] = {
            v: k for k, v in r['region_ids'].items()
        }
        r['time_series_ids'] = {
            v: k for k, v in r['time_series_ids'].items()
        }

        return json.dumps(r)
