from pprint import pprint
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.constants import SCHEMA_ADMIN_1, schema_to_name, name_to_schema
from covid_19_au_grab.geojson_data.LabelsToRegionChild import LabelsToRegionChild


MODE_DEV = 0
MODE_STRICT = 1

DUPE_TOLERANCE = 30


class StrictDataPointsFactory:
    def __init__(self, region_mappings=None, mode=MODE_DEV):
        """
        A factory for creating "strict datapoints", which are like lists
        which make sure there aren't duplicate datapoints for a given region
        on a given day.

        * In "dev" mode, this factory also registers the guessed "mappings"
          from the original source (e.g. "Victoria") to the ISO 3166-2 or
          other unique code (e.g. "au-vic")
        * In "strict" mode, this makes sure mappings exist, and raises an
          exception when it doesn't.
        """
        self.__mode = mode
        self.__region_mappings = (region_mappings or {}).copy()
        self.__ltrc = LabelsToRegionChild()

    def __call__(self, *args, **kwargs):
        return _StrictDataPoints(self, self.__mode, self.__region_mappings, self.__ltrc)

    def register_mapping(self,
                         from_schema, from_parent, from_child,
                         to_schema, to_parent, to_child):
        self.__region_mappings[from_schema, from_parent, from_child] = (
            to_schema, to_parent, to_child
        )

    def get_mappings(self):
        return self.__region_mappings.copy()

    def print_mappings(self):
        pprint(self.__region_mappings, width=160)


class _StrictDataPoints(list):
    def __init__(self, sdpf, mode, region_mappings, ltrc):
        """

        """
        list.__init__(self)

        self.__sdpf = sdpf
        self.__mode = mode
        self.__region_mappings = region_mappings
        self.__ltrc = ltrc

        # A way of registering whether a given kind
        # of datapoint has been registered
        self.__datapoints_added = {}
        self.__datapoint_indexes = {}
        self.__merged = set()

    def append(self,
               region_schema=SCHEMA_ADMIN_1,
               region_parent=None,
               region_child=None,

               date_updated=None,
               datatype=None,
               agerange=None,

               value=None,
               source_url=None,
               text_match=None):

        region_parent = (region_parent or '').lower()
        region_child = (region_child or '').lower()

        # Use any previously-defined mappings (if they exist)
        mapping_key = (
            schema_to_name(region_schema),
            (region_parent or '').lower(),
            (region_child or '').lower()
        )
        replace_index = None

        #print(mapping_key)
        if mapping_key in self.__region_mappings:
            mapping = self.__region_mappings[mapping_key]
            if mapping is None:
                # Explicitly set to ignore
                return None
            elif mapping[0] == 'MERGE':
                # Merge with an existing datapoint (if it exists)
                region_schema, region_parent, region_child = mapping[1:]
                region_schema = name_to_schema(region_schema)
                region_parent = region_parent.lower()
                region_child = region_child.lower()

                replace_index, r = self.__get_merged_datapoint(DataPoint(
                    region_schema=region_schema,
                    region_parent=region_parent,
                    region_child=region_child,

                    date_updated=date_updated,
                    datatype=datatype,
                    agerange=agerange,

                    value=value,
                    source_url=source_url,
                    text_match=text_match
                ))

                if replace_index is not None:
                    # Make sure merge only occurs once for a given date!
                    merged_key = (
                        mapping_key,
                        r.date_updated,
                        r.datatype,
                        r.agerange
                    )
                    assert not merged_key in self.__merged
                    self.__merged.add(merged_key)

            elif len(mapping) == 3:
                region_schema, region_parent, region_child = mapping
                region_schema = name_to_schema(region_schema)
                region_parent = region_parent.lower()
                region_child = region_child.lower()

                r = DataPoint(
                    region_schema=region_schema,
                    region_parent=region_parent,
                    region_child=region_child,

                    date_updated=date_updated,
                    datatype=datatype,
                    agerange=agerange,

                    value=value,
                    source_url=source_url,
                    text_match=text_match
                )
            else:
                raise Exception(mapping)

        else:
            r = DataPoint(
                region_schema=region_schema,
                region_parent=region_parent,
                region_child=region_child,

                date_updated=date_updated,
                datatype=datatype,
                agerange=agerange,

                value=value,
                source_url=source_url,
                text_match=text_match
            )

        if self.__mode == MODE_STRICT:
            # Make sure the region exists in GeoJSON
            if not self.__ltrc.region_child_in_geojson(
                region_schema, region_parent, region_child
            ):
                raise Exception("Region child not found in GeoJSON: %s %s %s %s" % (
                    r,
                    schema_to_name(region_schema),
                    region_parent.lower() if region_parent else '',
                    region_child.lower()
                ))

            # Make sure there aren't dupes on this day!
            unique_key = self.__get_unique_key(r)
            if (
                unique_key in self.__datapoints_added and
                abs(self.__datapoints_added[unique_key].value != r.value) > DUPE_TOLERANCE
            ):
                raise Exception("Datapoint already provided for this date: %s %s %s %s %s" % (
                    r,
                    self.__datapoints_added[unique_key],
                    schema_to_name(region_schema),
                    region_parent.lower() if region_parent else '',
                    region_child.lower()
                ))
            self.__datapoints_added[unique_key] = r

        else:
            self.__sdpf.register_mapping(
                schema_to_name(region_schema),
                region_parent.lower() if region_parent else '',
                region_child.lower(),

                schema_to_name(r.region_schema),
                r.region_parent.lower() if r.region_parent else '',
                r.region_child.lower()
            )

        if replace_index is None:
            # Append to the end if not merging one region with another
            self.__datapoint_indexes[self.__get_unique_key(r)] = len(r)
            list.append(self, r)
        else:
            # Much faster to replace than append!
            self[replace_index] = r

        return r

    def __get_merged_datapoint(self, datapoint):
        """
        Find+remove the previous datapoint (if it exists);
        return a new datapoint with both values added
        """
        unique_key = self.__get_unique_key(datapoint)

        if unique_key in self.__datapoint_indexes:
            replace_index = self.__datapoint_indexes[unique_key]
            i = self[replace_index]

            r = DataPoint(
                region_schema=datapoint.region_schema,
                region_parent=datapoint.region_parent,
                region_child=datapoint.region_child,

                date_updated=datapoint.date_updated,
                datatype=datapoint.datatype,
                agerange=datapoint.agerange,

                value=datapoint.value + i.value,
                source_url=datapoint.source_url or i.source_url,
                text_match=datapoint.text_match or i.text_match
            )
        else:
            replace_index = None
            r = datapoint

        return replace_index, r

    def __get_unique_key(self, datapoint):
        return (
            datapoint.region_schema,
            datapoint.region_parent,
            datapoint.region_child,
            datapoint.date_updated,
            datapoint.datatype,
            datapoint.agerange
        )

    def extend(self, datapoints):
        for datapoint in datapoints:
            self.append(**datapoint._todict())


if __name__ == '__main__':
    FIXME
