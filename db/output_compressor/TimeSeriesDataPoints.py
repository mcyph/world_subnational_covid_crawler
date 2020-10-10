from collections import Counter, defaultdict

from covid_19_au_grab.datatypes.enums import Schemas
from covid_19_au_grab.datatypes.datapoints_thinned_out import datapoints_thinned_out


class TimeSeriesDataPoints:
    def __init__(self, region_schema):
        self.region_schema = region_schema
        self.region_schema_str = Schemas(region_schema)

        self.by_region = {}
        self.datatype_counter = Counter()
        self.date_counter = Counter()
        self.source_ids = []

    def add_datapoint(self, datapoint):
        """
        Add a datapoint, assigning by region, age range, datatype, source id,
        and date updated.

        Note that if there are any datapoints of the same region/age range/datatype
        on the same date that they will be overwritten.
        """

        # TODO: Support different values for different source IDs!
        assert datapoint.region_schema == self.region_schema
        assert datapoint.source_id

        if not datapoint.source_id in self.source_ids:
            self.source_ids.append(datapoint.source_id)

        self.by_region.setdefault(datapoint.region_parent, {}) \
                      .setdefault(datapoint.region_child, {}) \
                      .setdefault(datapoint.agerange, {}) \
                      .setdefault(datapoint.datatype, {}) \
                      .setdefault(datapoint.source_id, {}) \
                      [datapoint.date_updated] = datapoint

        self.datatype_counter[datapoint.datatype] += 1
        self.date_counter[datapoint.date_updated] += 1

    def get_compressed_data(self, thin_out=True):
        """
        Get data which is compressed, saving download times
        """
        r = {}
        updated_dates = {}
        updated_dates_by_datatype = {}

        # Get a map from date -> number of datapoints
        date_ids_map = self.__get_from_to_ids(self.date_counter)

        # Put the datapoints in the order of most to least common of a certain datatype,
        # so we'll be more likely to elide blank values if they aren't given on a certain day
        process_datatypes_in_order = [
            v for k, v in sorted(self.__get_to_from_ids(self.datatype_counter).items())
        ]

        for region_parent, region_parent_dict in self.by_region.items():
            region_parent_out = {}

            for region_child, region_child_dict in region_parent_dict.items():
                for agerange, agerange_dict in region_child_dict.items():

                    # Assign datapoints by datatype
                    all_dates = defaultdict(lambda: set())
                    datapoints_by_datatype = {}

                    for datatype, datatype_dict in agerange_dict.items():
                        for source_id, source_id_dict in datatype_dict.items():
                            # The source id dict keys are dates in format YYYY_MM_DD
                            # They're only put into keys to remove dupes for each date,
                            # so we'll get the values (DataPoint instances) directly
                            # to allow thinning out datapoints for each source
                            datapoints = sorted(source_id_dict.values(),
                                                key=lambda x: x.date_updated, reverse=True)

                            if thin_out:
                                datapoints = datapoints_thinned_out(datapoints)

                            datapoints_by_datatype.setdefault(datatype, {}) \
                                                  .setdefault(source_id, {}).update({
                                datapoint.date_updated: datapoint
                                for datapoint in datapoints
                            })

                            for datapoint in datapoints:
                                # Update the updated dates value to be the highest
                                # Note if a source has multiple parts+only one is updated,
                                # it'll be the most recent of the two, even if the other data is old
                                # but difficult to deal with every case
                                cur_updated_date = updated_dates.setdefault(self.region_schema_str, {}) \
                                                                .setdefault(region_parent)
                                if not cur_updated_date or datapoint.date_updated > cur_updated_date:
                                    updated_dates[self.region_schema_str][region_parent] = datapoint.date_updated

                                cur_updated_date_by_datatype = updated_dates_by_datatype.setdefault(datapoint.datatype.value)
                                if not cur_updated_date_by_datatype or datapoint.date_updated > cur_updated_date_by_datatype:
                                    updated_dates_by_datatype[datapoint.datatype.value] = datapoint.date_updated

                                all_dates[source_id].add(datapoint.date_updated)

                    # Compress the data to save download times
                    # The format is: [["bd-a", "", [[0, 45, ...]], [...], ...]]
                    # First number is a date id, and the rest are the values
                    # Multiple sources' data are put in the order of self.source_ids
                    # after the date id

                    region_child_out = []

                    for source_id in self.source_ids:
                        source_item = []

                        for i_date in sorted(all_dates[source_id], reverse=True):
                            append_me = []
                            append_me.append(date_ids_map[i_date])

                            for datatype in process_datatypes_in_order:
                                a = datapoints_by_datatype.get(datatype, {}) \
                                                          .get(source_id, {}) \
                                                          .get(i_date)

                                value = a.value if a is not None else ''
                                if value == '':
                                    value = '1'

                                if value == '1' and isinstance(append_me[-1], str):
                                    # A poor man's RLE (Run Length Encoding)
                                    # https://en.wikipedia.org/wiki/Run-length_encoding
                                    # Strings with numbers in them indicate that many null values
                                    append_me[-1] = str(int(append_me[-1])+1)
                                else:
                                    append_me.append(value)

                            # Don't add if on the end+no value to save space
                            while isinstance(append_me[-1], str):
                                del append_me[-1]

                            source_item.append(append_me)

                        region_child_out.append(source_item)

                    key = f'{region_child}||{agerange}'
                    assert not key in region_parent_out, key
                    region_parent_out[key] = region_child_out

            assert not region_parent in r, region_parent
            r[region_parent] = {'data': region_parent_out}

        return {
            'time_series_data': r,
            'date_ids': self.__get_to_from_ids(self.date_counter),
            'updated_dates': updated_dates,
            'updated_dates_by_datatype': updated_dates_by_datatype,
            'source_ids': self.source_ids,
            'sub_headers': [
                datatype.value for id, datatype in
                sorted(self.__get_to_from_ids(self.datatype_counter).items())
            ],
        }

    def __get_from_to_ids(self, counter):
        """
        Get a dict which assigns IDs as values
        Lower IDs are given for for more frequent values
        """
        r = {}
        for x, (k, v) in enumerate(counter.most_common()):
            r[k] = x
        return r

    def __get_to_from_ids(self, counter):
        """
        Get a dict which assigns IDs as keys
        Lower IDs are given for for more frequent values
        """
        r = {}
        for x, (k, v) in enumerate(counter.most_common()):
            r[x] = k
        return r
