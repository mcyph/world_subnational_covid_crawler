from collections import Counter
from covid_19_au_grab.datatypes.datapoints_thinned_out import \
    datapoints_thinned_out
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes


class TimeSeriesDataPoints:
    def __init__(self, region_schema):
        self.region_schema = region_schema
        self.region_schema_str = Schemas(region_schema)

        self.by_region = {}
        self.datatype_counter = Counter()
        self.date_counter = Counter()

    def add_datapoint(self, datapoint):
        """

        """

        # TODO: Support different values for different source IDs!
        assert datapoint.region_schema == self.region_schema

        self.by_region.setdefault(datapoint.region_parent, {}) \
                      .setdefault(datapoint.region_child, {}) \
                      .setdefault(datapoint.agerange, {}) \
                      .setdefault(datapoint.datatype, {}) \
                      [datapoint.date_updated] = datapoint

        self.datatype_counter[datapoint.datatype] += 1
        self.date_counter[datapoint.date_updated] += 1

    def get_compressed_data(self, thin_out=True):
        """

        """
        r = {}
        updated_dates = {}

        date_ids_map = self.__get_from_to_ids(self.date_counter)
        process_datatypes_in_order = [
            v for k, v in sorted(self.__get_to_from_ids(self.datatype_counter).items())
        ]

        for region_parent, region_parent_dict in self.by_region.items():
            region_parent_out = []

            for region_child, region_child_dict in region_parent_dict.items():
                for agerange, agerange_dict in region_child_dict.items():

                    all_dates = set()
                    datapoints_by_datatype = {}
                    region_child_out = [region_child, agerange or '', []]

                    for datatype, datatype_dict in agerange_dict.items():
                        datapoints = sorted(
                            datatype_dict.values(),
                            key=lambda i: i.date_updated,
                            reverse=True
                        )
                        if thin_out:
                            datapoints = datapoints_thinned_out(datapoints)

                        datapoints_by_datatype[datatype] = {
                            datapoint.date_updated: datapoint
                            for datapoint in datapoints
                        }

                        for datapoint in datapoints:
                            # Update the updated dates value to be the highest
                            # Note if a source has multiple parts+only one is updated,
                            # it'll be the most recent of the two, even if the other data is old
                            # but difficult to deal with every case
                            cur_updated_date = updated_dates.setdefault(self.region_schema_str, {}) \
                                                            .setdefault(region_parent)
                            if not cur_updated_date or datapoint.date_updated > cur_updated_date:
                                updated_dates[self.region_schema_str][region_parent] = datapoint.date_updated

                            all_dates.add(datapoint.date_updated)

                    for i_date in sorted(all_dates, reverse=True):
                        # [["bd-a","",[[0,45,
                        # First number is a date id, and the rest are the values
                        append_me = [date_ids_map[i_date]]

                        for datatype in process_datatypes_in_order:
                            a = datapoints_by_datatype.get(datatype, {}) \
                                                      .get(i_date)
                            append_me.append(
                                a.value if a is not None else ''
                            )

                        # Don't add if on the end+no value to save space
                        while len(append_me) > 0 and append_me[-1] == '':
                            del append_me[-1]

                        region_child_out[-1].append(append_me)
                    region_parent_out.append(region_child_out)

            assert not region_parent in r, region_parent
            r[region_parent] = {
                'data': region_parent_out
            }

        return {
            'time_series_data': r,
            'date_ids': self.__get_to_from_ids(self.date_counter),
            'updated_dates': updated_dates,
            'sub_headers': [
                datatype.value for id, datatype in
                sorted(self.__get_to_from_ids(self.datatype_counter).items())
            ],
        }

    def __get_from_to_ids(self, counter):
        """

        """
        r = {}
        for x, (k, v) in enumerate(counter.most_common()):
            r[k] = x
        return r

    def __get_to_from_ids(self, counter):
        """

        """
        r = {}
        for x, (k, v) in enumerate(counter.most_common()):
            r[x] = k
        return r
