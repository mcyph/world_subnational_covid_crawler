class DataPointMerger(list):
    def __init__(self):
        list.__init__(self)
        self.__added = set()

    def extend(self, datapoints):
        for datapoint in datapoints:
            self.append(datapoint)

    def append(self, datapoint):
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
