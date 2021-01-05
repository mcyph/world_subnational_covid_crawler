import io
import json
import time
import random
import _thread
import cherrypy
import datetime
import mimetypes
from shlex import quote
from os import listdir, system
from jinja2 import Environment, FileSystemLoader
from cherrypy import _json
from _thread import start_new_thread

# MONKEY PATCH: Reduce cherrpy json file output
_json._encode = json.JSONEncoder(separators=(',', ':')).iterencode

env = Environment(loader=FileSystemLoader('./templates'))

from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.SQLiteDataRevision import SQLiteDataRevision
from covid_db.SQLiteDataRevisions import SQLiteDataRevisions
from _utility.get_package_dir import get_package_dir
from covid_db.datatypes import date_fns
from covid_db.output_compressor.output_revision_datapoints_to_zip import output_revision_datapoints_to_zip
from _utility.normalize_locality_name import normalize_locality_name


OUTPUT_DIR = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'output'
OUTPUT_GRAPHS_DIR = get_package_dir() / 'world_subnational_covid_crawler' / 'output_graphs' / 'output'
UPDATE_SCRIPT_PATH = get_package_dir() / 'output_data.py'
UPDATE_CASE_LOCS_PATH = get_package_dir() / 'case_locations' / 'update_spreadsheet.py'
mimetypes.types_map['.tsv'] = 'text/tab-separated-values'


class App(object):
    def __init__(self):
        self.revisions = SQLiteDataRevisions()
        _thread.start_new_thread(self.loop, ())

    def loop(self):
        powerbi_run_1st = False
        powerbi_run_2nd = False
        powerbi_run_3rd = False

        while True:
            # Run once every around every three hours
            # (an hour is 3600 seconds)
            time.sleep(random.randint(9000, 11000))

            dt = datetime.datetime.now()

            if dt.hour >= 7 and dt.hour <= 22:
                # Run between 7am and 10pm only

                if dt.hour >= 12 and dt.hour < 14 and not powerbi_run_1st:
                    # Run powerbi once only between 12pm and 2pm
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_CASE_LOCS_PATH))}',))
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_SCRIPT_PATH))} --run-infrequent-jobs',))
                    powerbi_run_1st = True
                    powerbi_run_2nd = False
                    powerbi_run_3rd = False
                elif dt.hour >= 15 and dt.hour < 17 and not powerbi_run_2nd:
                    # Run powerbi once only between 3pm and 5pm
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_CASE_LOCS_PATH))}',))
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_SCRIPT_PATH))} --run-infrequent-jobs',))
                    powerbi_run_1st = False
                    powerbi_run_2nd = True
                    powerbi_run_3rd = False
                elif dt.hour >= 17 and dt.hour < 19 and not powerbi_run_3rd:
                    # Run powerbi once only between 5pm and 7pm
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_CASE_LOCS_PATH))}',))
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_SCRIPT_PATH))} --run-infrequent-jobs',))
                    powerbi_run_1st = False
                    powerbi_run_2nd = False
                    powerbi_run_3rd = True
                else:
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_CASE_LOCS_PATH))}',))
                    start_new_thread(system, (f'python3 {quote(str(UPDATE_SCRIPT_PATH))}',))

    #=============================================================#
    #                            Index                            #
    #=============================================================#

    @cherrypy.expose
    def index(self):
        t = env.get_template('index.html')
        return t.render(
            revisions=self.revisions.get_revisions()
        )

    @cherrypy.expose
    def most_recent_changes(self):
        """
        TODO: Go thru each version from the
        last 48 hours, and output any changes
        """
        revisions = self.revisions.get_revisions()[:15]
        insts = [
            SQLiteDataRevision(period, subperiod_id)
            for period, subperiod_id, _ in revisions
        ]

        changes_by_revision = []
        for x, i_inst in enumerate(insts):
            if x == len(insts)-1:
                break

            changes_by_revision.append((
                revisions[x][0],
                revisions[x][1],
                revisions[x][2],
                self.revisions.get_changed(i_inst, insts[x+1])
            ))

        return env.get_template('most_recent_changes.html').render(
            changes_by_revision=changes_by_revision
        )

    @cherrypy.expose
    def most_recent_graphs(self):
        return env.get_template('most_recent_graphs.html').render(
            graphs=sorted([
                i for i in listdir(OUTPUT_GRAPHS_DIR)
                if i.endswith('.png')
            ])
        )

    #=============================================================#
    #                   View Specific Revision                    #
    #=============================================================#

    @cherrypy.expose
    def revision(self, rev_date, rev_subid):
        inst = SQLiteDataRevision(rev_date, rev_subid)

        try:
            status_list = sorted(
                list(inst.get_status_dict().items())
            )
        except FileNotFoundError:
            status_list = []

        return env.get_template('revision/revision.html').render(
            status_list=status_list,
            rev_date=rev_date,  # ESCAPE!
            rev_subid=rev_subid,  # ESCAPE!
            revision_time_string=inst.get_revision_time_string(),
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
            source_ids=inst.get_source_ids(),
            date_fns=date_fns,
        )

    @cherrypy.expose
    def view_log(self, rev_date, rev_subid):
        return env.get_template('revision/view_log.html').render(
            FIXME
        )

    @cherrypy.expose
    def get_data_as_table(self, rev_date, rev_subid, source_id):
        inst = SQLiteDataRevision(rev_date, rev_subid)

        datapoints = inst.get_datapoints_by_source_id(source_id)
        datapoints.sort(key=lambda i: (
            i.date_updated,
            i.region_schema,
            i.region_parent,
            i.region_child,
            i.agerange
        ))

        return env.get_template('revision/get_data_as_table.html').render(
            rev_date=rev_date,  # ESCAPE!
            rev_subid=rev_subid,  # ESCAPE!
            datapoints=datapoints,
            revision_time_string=inst.get_revision_time_string(),
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
            zip=zip,
            date_fns=date_fns,
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_json_data(self, rev_date, rev_subid, source_id):
        return SQLiteDataRevision(rev_date, rev_subid).get_datapoints()

    @cherrypy.expose
    def get_tsv_data(self, rev_date, rev_subid, source_id):
        rev_subid = int(rev_subid)
        inst = SQLiteDataRevision(rev_date, rev_subid)
        data = inst.get_tsv_data(source_id)

        cherrypy.response.headers['Content-Disposition'] = \
            'attachment; filename="covid_%s.tsv"' % source_id
        cherrypy.response.headers['Content-Type'] = 'text/csv'
        return data

    @cherrypy.expose
    def statistics(self, rev_date, rev_subid):
        inst = SQLiteDataRevision(rev_date, rev_subid)
        statistics_datapoints = []

        for from_date in (
            date_fns.apply_timedelta(rev_date, days=-0),
            date_fns.apply_timedelta(rev_date, days=-1),
            date_fns.apply_timedelta(rev_date, days=-2),
            date_fns.apply_timedelta(rev_date, days=-3),
            date_fns.apply_timedelta(rev_date, days=-4)
        ):
            print("**FROM DATE:", from_date)

            statistics_datapoints.append((
                from_date,
                inst.get_combined_values(
                    (
                        (Schemas.ADMIN_1, DataTypes.TOTAL, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.NEW, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.STATUS_DEATHS, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.STATUS_DEATHS_NEW, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.STATUS_RECOVERED, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.STATUS_RECOVERED_NEW, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.TESTS_TOTAL, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_CONFIRMED, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_COMMUNITY, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_INTERSTATE, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.STATUS_HOSPITALIZED, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.STATUS_ICU, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.TOTAL_FEMALE, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.TOTAL_MALE, 'AU'),
                    ),
                    from_date=from_date
                )
            ))

        return env.get_template('revision/statistics.html').render(
            rev_date=rev_date,
            rev_date_slash_format=rev_date,  # HACK!
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            statistics_datapoints=statistics_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
            date_fns=date_fns,
        )

    @cherrypy.expose
    def source_of_infection(self, rev_date, rev_subid):
        inst = SQLiteDataRevision(rev_date, rev_subid)
        statistics_datapoints = []

        for from_date in (
            date_fns.apply_timedelta(rev_date, days=-0),
            date_fns.apply_timedelta(rev_date, days=-1),
            date_fns.apply_timedelta(rev_date, days=-2),
            date_fns.apply_timedelta(rev_date, days=-3),
            date_fns.apply_timedelta(rev_date, days=-4)
        ):
            print("**FROM DATE:", from_date)

            statistics_datapoints.append((
                from_date,
                inst.get_combined_values(
                    (
                        (Schemas.ADMIN_1, DataTypes.SOURCE_OVERSEAS, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_CONFIRMED, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_COMMUNITY, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_INTERSTATE, 'AU'),
                        (Schemas.ADMIN_1, DataTypes.SOURCE_UNDER_INVESTIGATION, 'AU'),
                    ),
                    from_date=from_date
                )
            ))

        return env.get_template('revision/source_of_infection.html').render(
            rev_date=rev_date,
            rev_date_slash_format=rev_date,
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            statistics_datapoints=statistics_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
            date_fns=date_fns,
        )

    @cherrypy.expose
    def gender_age(self, rev_date, rev_subid):
        inst = SQLiteDataRevision(rev_date, rev_subid)
        gender_age_datapoints = [i for i in inst.get_combined_values_by_datatype(
            Schemas.ADMIN_1,
            (
                DataTypes.TOTAL_FEMALE,
                DataTypes.TOTAL_MALE,
                DataTypes.TOTAL,
            ),
            region_parent='AU'
        ) if i['agerange']]

        return env.get_template('revision/gender_age.html').render(
            rev_date=rev_date,
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            gender_age_datapoints=gender_age_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
            date_fns=date_fns,
        )

    @cherrypy.expose
    def local_area_case(self, rev_date, rev_subid):
        inst = SQLiteDataRevision(rev_date, rev_subid)

        out = []
        for region_schema in (
            Schemas.LGA,
            Schemas.SA3,
            Schemas.HHS,
            Schemas.LHD,
            Schemas.THS,
            Schemas.POSTCODE
        ):
            local_area_case_datapoints = inst.get_combined_values_by_datatype(
                region_schema,
                (
                    # TODO: What about by LGA (QLD only, other
                    #  LGA in DataTypes.CASES_BY_REGION) and LHA (NSW)
                    DataTypes.TOTAL,
                    DataTypes.STATUS_ACTIVE,
                    DataTypes.STATUS_RECOVERED,
                    DataTypes.STATUS_DEATHS,
                )
            )
            out.extend(local_area_case_datapoints)

        return env.get_template('revision/local_area_case.html').render(
            rev_date=rev_date,
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            local_area_case_datapoints=out,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
            date_fns=date_fns,
        )

    @cherrypy.expose
    def regionsTimeSeries(self, rev_date=None, rev_subid=None):
        zip_buffer = io.BytesIO()
        output_revision_datapoints_to_zip(zip_buffer, rev_date, rev_subid)

        cherrypy.response.headers['Content-Disposition'] = \
            'attachment; filename="covid_time_series_data.zip"'
        cherrypy.response.headers['Content-Type'] = 'application/zip'
        return zip_buffer.getvalue()

    def __get_time_series(self, inst,
                          region_schema, region_parent, region_child,
                          datatypes,
                          date_ids_dict):
        """
        Returns {
            'sub_headers': (sub_headers corresponding to each value idx),
            'data': [[region_child, agerange, [[date_updated_id, value 1, value 2...]], ...]
        }
        """

        out = []
        max_date = None

        for (region_child, agerange), date_updated_dict in sorted(inst.get_time_series(
            datatypes, region_schema, region_parent, region_child
        ).items()):

            values = []
            for date_updated, datapoints in sorted(
                date_updated_dict.items(), reverse=True
            ):
                if max_date is None or date_updated > max_date:
                    max_date = date_updated

                if not date_updated in date_ids_dict:
                    # Store the date as an ID to allow saving space
                    date_ids_dict[date_updated] = len(date_ids_dict)
                date_updated_id = date_ids_dict[date_updated]

                i_value = [date_updated_id]
                for datatype in datatypes:
                    found = None
                    for datapoint in datapoints:
                        if datapoint.datatype == datatype:
                            found = datapoint

                    if found:
                        i_value.append(found.value)
                    else:
                        i_value.append('')

                # Don't store values past the end,
                # if they aren't available!
                while i_value[-1] == '':
                    del i_value[-1]
                values.append(i_value)

            normalized_region_child = normalize_locality_name(region_child)
            out.append([
                normalized_region_child,
                agerange,
                values
            ])

        return max_date, {
            'sub_headers': [i.value for i in datatypes],
            'data': out
        }


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config={
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 6006,
            #'environment': 'production',
        },
        '/': {},
    })
