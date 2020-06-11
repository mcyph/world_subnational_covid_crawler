# Plain-old integer
DT_INTEGER = 0
# Plain-old floating point
DT_FLOATING_POINT = 1
# Float with limited decimal points and %
DT_PERCENT = 2
# Float with scaling like the miles/km indicator at Google Maps
DT_PER_100k = 3


class TimeSeriesKey:
    def __init__(self, key_group, key, datatype, desc=None):
        self.key_group = key_group
        self.key = key
        self.desc = desc
        self.datatype = datatype
        self.datapoints = {}

    def __delitem__(self, item):
        del self.datapoints[item[0]][item[1]][item[2]][item[3]]

    def __getitem__(self, item):
        return self.datapoints[item[0]][item[1]][item[2]][item[3]]

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False

    def pop(self, item):
        r = self[item]
        del self[item]
        return r

    def get_datapoints_dict(self):
        return self.datapoints

    def iter_by_schema(self):
        for schema, schema_dict in self.datapoints.items():
            yield schema, schema_dict

    def iter_by_parent(self):
        for schema, schema_dict in self.datapoints.items():
            for region_parent, region_parent_dict in schema_dict.items():
                yield schema, region_parent, region_parent_dict

    def iter_by_child(self):
        for schema, schema_dict in self.datapoints.items():
            for region_parent, region_parent_dict in schema_dict.items():
                for region_child, region_child_dict in region_parent_dict.items():
                    yield schema, region_parent, region_child, region_child_dict

    def append(self, datapoint):
        """

        """
        self.datapoints.setdefault(datapoint.region_schema, {}) \
                       .setdefault(datapoint.region_parent, {}) \
                       .setdefault(datapoint.region_child, {}) \
                       .setdefault(str(datapoint.date), []) \
                       .append(datapoint)
