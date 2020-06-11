from collections import Counter

from covid_19_au_grab.datatypes.constants import (
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

    DT_CONFIRMED, DT_CONFIRMED_NEW,
    DT_PROBABLE, DT_PROBABLE_NEW
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes import (
    date_fns
)


class DerivedData:
    def __init__(self, datapoints_db):
        self.datapoints_db = datapoints_db

    def add_derived(self):
        for source_id in self.datapoints_db.get_source_ids():
            self.add_derived_for_source(source_id)

    def add_derived_for_source(self, source_id):
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

            (DT_CONFIRMED, DT_CONFIRMED_NEW),
            (DT_PROBABLE, DT_PROBABLE_NEW),
        ):
            self.add_new_datapoints_from_total(
                source_id, new_datatype, total_datatype
            )

        self.add_gender_balance_from_breakdown(source_id)
        #self.add_rate_of_change(region_schema)

    def add_new_datapoints_from_total(
            self, source_id, new_datatype, total_datatype
        ):
        print("Adding new datapoints from totals:", source_id)

        new_datapoints = self.datapoints_db.select_many(
            source_id=['=?', [source_id]],
            datatype=['=?', [new_datatype]]
        )
        total_datapoints = self.datapoints_db.select_many(
            source_id=['=?', [source_id]],
            datatype=['=?', [total_datatype]]
        )

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
                datatype=new_datatype,
                agerange=total_datapoint.agerange,
                value=total_datapoint.value -
                      total_datapoint_pd.value,
                source_url='DERIVED'
            ))

        self.datapoints_db.extend(
            source_id, append_datapoints, is_derived=True
        )

    def add_gender_balance_from_breakdown(self, source_id):
        print("Adding gender balance from breakdown:", source_id)
        append_datapoints = []

        for datatype in (DT_TOTAL_MALE, DT_TOTAL_FEMALE):
            has_total = {}
            age_breakdowns = Counter()

            datapoints = self.datapoints_db.select_many(
                source_id=['=?', [source_id]],
                datatype=['=?', [datatype]]
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
            source_id, append_datapoints, is_derived=True
        )


if __name__ == '__main__':
    from covid_19_au_grab.db.SQLiteDataRevisions import SQLiteDataRevisions
    from covid_19_au_grab.db.DataPointsDB import DataPointsDB
    from covid_19_au_grab.get_package_dir import get_output_dir

    OUTPUT_DIR = get_output_dir() / 'output'

    sdr = SQLiteDataRevisions()
    most_recent_revision = sdr.get_revisions()[0]
    period = most_recent_revision[0]
    subperiod_id = most_recent_revision[1]
    path = OUTPUT_DIR / f'{period}-{subperiod_id}.sqlite'

    dpdb = DataPointsDB(path)
    DerivedData(dpdb).add_derived()
    dpdb.close()
