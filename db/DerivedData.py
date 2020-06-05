from collections import Counter

from covid_19_au_grab.datatypes.constants import (
    get_schemas,

    DT_TOTAL, DT_NEW,
    DT_TOTAL_MALE, DT_TOTAL_FEMALE,
    DT_TESTS_TOTAL, DT_TESTS_NEW,

    DT_STATUS_DEATHS, DT_STATUS_DEATHS_NEW,
    DT_STATUS_RECOVERED, DT_STATUS_RECOVERED_NEW,
    DT_STATUS_ACTIVE, DT_STATUS_ACTIVE_NEW,
    DT_STATUS_HOSPITALIZED, DT_STATUS_HOSPITALIZED_NEW,
    DT_STATUS_ICU, DT_STATUS_ICU_NEW,
    DT_STATUS_ICU_VENTILATORS, DT_STATUS_ICU_VENTILATORS_NEW,
    DT_STATUS_ICU_RUNNINGTOTAL, DT_STATUS_ICU_RUNNINGTOTAL_NEW,
    DT_STATUS_HOSPITALIZED_RUNNINGTOTAL, DT_STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW,
    DT_STATUS_ICU_VENTILATORS_RUNNINGTOTAL, DT_STATUS_ICU_VENTILATORS_RUNNINGTOTAL_NEW,

    DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_UNDER_INVESTIGATION_NEW,
    DT_SOURCE_OVERSEAS, DT_SOURCE_OVERSEAS_NEW,
    DT_SOURCE_CONFIRMED, DT_SOURCE_CONFIRMED_NEW,
    DT_SOURCE_COMMUNITY, DT_SOURCE_COMMUNITY_NEW,
    DT_SOURCE_DOMESTIC, DT_SOURCE_DOMESTIC_NEW,
    DT_SOURCE_CRUISE_SHIP, DT_SOURCE_CRUISE_SHIP_NEW,
    DT_SOURCE_INTERSTATE, DT_SOURCE_INTERSTATE_NEW,

    DT_CONFIRMED, DT_CONFIRMED_NEW,
    DT_PROBABLE, DT_PROBABLE_NEW,

    DT_TOTAL_PERCAPITA, DT_TOTAL_PERREGIONPC,
    DT_STATUS_ACTIVE_PERCAPITA, DT_STATUS_ACTIVE_PERREGIONPC,
    DT_STATUS_RECOVERED_PERCAPITA, DT_STATUS_RECOVERED_PERREGIONPC,
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes import (
    date_fns
)


class DerivedData:
    def __init__(self, datapoints_db, source_id):
        self.datapoints_db = datapoints_db
        self.source_id = source_id

    def add_derived(self):
        for region_schema in get_schemas():
            for total_datatype, new_datatype in (
                (DT_TOTAL, DT_NEW),
                (DT_TESTS_TOTAL, DT_TESTS_NEW),

                (DT_STATUS_DEATHS, DT_STATUS_DEATHS_NEW),
                (DT_STATUS_RECOVERED, DT_STATUS_RECOVERED_NEW),
                (DT_STATUS_ACTIVE, DT_STATUS_ACTIVE_NEW),
                (DT_STATUS_HOSPITALIZED, DT_STATUS_HOSPITALIZED_NEW),
                (DT_STATUS_ICU, DT_STATUS_ICU_NEW),
                (DT_STATUS_ICU_VENTILATORS, DT_STATUS_ICU_VENTILATORS_NEW),
                (DT_STATUS_ICU_RUNNINGTOTAL, DT_STATUS_ICU_RUNNINGTOTAL_NEW),
                (DT_STATUS_HOSPITALIZED_RUNNINGTOTAL, DT_STATUS_HOSPITALIZED_RUNNINGTOTAL_NEW),
                (DT_STATUS_ICU_VENTILATORS_RUNNINGTOTAL, DT_STATUS_ICU_VENTILATORS_RUNNINGTOTAL_NEW),

                (DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_UNDER_INVESTIGATION_NEW),
                (DT_SOURCE_OVERSEAS, DT_SOURCE_OVERSEAS_NEW),
                (DT_SOURCE_CONFIRMED, DT_SOURCE_CONFIRMED_NEW),
                (DT_SOURCE_COMMUNITY, DT_SOURCE_COMMUNITY_NEW),
                (DT_SOURCE_DOMESTIC, DT_SOURCE_DOMESTIC_NEW),
                (DT_SOURCE_CRUISE_SHIP, DT_SOURCE_CRUISE_SHIP_NEW),
                (DT_SOURCE_INTERSTATE, DT_SOURCE_INTERSTATE_NEW),

                (DT_CONFIRMED, DT_CONFIRMED_NEW),
                (DT_PROBABLE, DT_PROBABLE_NEW),
            ):
                new_datapoints = self.datapoints_db.select_many(
                    region_schema=region_schema,
                    datatype=new_datatype
                )
                total_datapoints = self.datapoints_db.select_many(
                    region_schema=region_schema,
                    datatype=total_datatype
                )
                self.add_new_datapoints_from_total(
                    new_datatype, total_datatype,
                    new_datapoints, total_datapoints
                )

    def add_new_datapoints_from_total(
            self, new_datatype, total_datatype,
            new_datapoints, total_datapoints
        ):
        n = {}
        t = {}

        for new_datapoint in new_datapoints:
            n[
                new_datapoint.date_updated,
                new_datapoint.region_schema,
                new_datapoint.region_parent,
                new_datapoint.region_child,
                new_datapoint.agerange
            ] = new_datapoint

        for total_datapoint in total_datapoints:
            t[
                total_datapoint.date_updated,
                total_datapoint.region_schema,
                total_datapoint.region_parent,
                total_datapoint.region_child,
                total_datapoint.agerange
            ] = total_datapoint

        append_datapoints = []
        for k, total_datapoint in t.items():
            if k in n:
                # Already have a new datapoint for this, so don't add!
                continue

            day_before = date_fns.apply_timedelta(
                total_datapoint.date_updated, days=-1
            )
            k_pd = (day_before,)+k[1:]  # previous day
            if not k_pd in t:
                continue
            total_datapoint_pd = t[k_pd]

            append_datapoints.append(DataPoint(
                region_schema=total_datapoint.region_schema,
                region_parent=total_datapoint.region_parent,
                region_child=total_datapoint.region_child,
                date_updated=total_datapoint.date_updated,
                datatype=total_datapoint.datatype,
                agerange=total_datapoint.agerange,
                value=total_datapoint.value -
                      total_datapoint_pd.value,
                source_url='DERIVED'
            ))

        self.datapoints_db.extend(
            append_datapoints, is_derived=True
        )

    def add_gender_balance_from_breakdown(self, region_schema):
        append_datapoints = []

        for datatype in (DT_TOTAL_MALE, DT_TOTAL_FEMALE):
            has_total = {}
            age_breakdowns = Counter()

            datapoints = self.datapoints_db.select_many(
                region_schema=region_schema,
                datatype=datatype
            )

            for datapoint in datapoints:
                if datapoint.agerange:
                    age_breakdowns[
                        datapoint.date_updated,
                        datapoint.region_schema,
                        datapoint.region_parent,
                        datapoint.region_child
                    ] += datapoint.value
                else:
                    has_total[
                        datapoint.date_updated,
                        datapoint.region_schema,
                        datapoint.region_parent,
                        datapoint.region_child
                    ] = True

        for (date_updated,
             region_schema,
             region_parent,
             region_child), value in age_breakdowns.items():

            append_datapoints.append(DataPoint(
                region_schema=region_schema,
                region_parent=region_parent,
                region_child=region_child,
                datatype=datatype,
                date_updated=date_updated,
                agerange=None,
                value=value,
                source_url='DERIVED'
            ))

        self.datapoints_db.extend(
            append_datapoints, is_derived=True
        )

    def add_other_datatypes_from_regions(
            self, other_datatype
        ):
        pass

    def add_rate_of_change(self):
        # https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
        pass
