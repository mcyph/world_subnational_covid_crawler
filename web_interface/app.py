import csv
import json
import time
import random
import _thread
import cherrypy
import datetime
import mimetypes
from shlex import quote
from io import StringIO
from os import listdir, system
from cherrypy.lib.static import serve_file
from jinja2 import Environment, FileSystemLoader
from cherrypy import _json

# MONKEY PATCH: Reduce cherrpy json file output
_json._encode = json.JSONEncoder(separators=(',', ':'),
                                 ensure_ascii=False).iterencode

env = Environment(loader=FileSystemLoader('./templates'))

from covid_19_au_grab.normalize_locality_name import \
    normalize_locality_name
#from covid_19_au_grab.web_interface.CSVDataRevision import \
#    CSVDataRevision
#from covid_19_au_grab.web_interface.CSVDataRevisions import \
#    CSVDataRevisions

from covid_19_au_grab.db.SQLiteDataRevision import \
    SQLiteDataRevision
from covid_19_au_grab.db.SQLiteDataRevisions import \
    SQLiteDataRevisions

from covid_19_au_grab.datatypes.constants import (
    constant_to_name, schema_to_name,
    SCHEMA_ADMIN_1, SCHEMA_POSTCODE, SCHEMA_LGA,
    SCHEMA_HHS, SCHEMA_LHD, SCHEMA_SA3, SCHEMA_THS,
    DT_TOTAL, DT_TOTAL_FEMALE, DT_TOTAL_MALE,
    DT_STATUS_DEATHS_NEW, DT_STATUS_RECOVERED_NEW,
    DT_NEW, DT_TESTS_TOTAL,
    DT_STATUS_ACTIVE, DT_STATUS_RECOVERED,
    DT_STATUS_ICU, DT_STATUS_HOSPITALIZED,
    DT_STATUS_ICU_VENTILATORS, DT_STATUS_DEATHS,
    DT_STATUS_UNKNOWN,
    DT_SOURCE_COMMUNITY, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_CONFIRMED, DT_SOURCE_OVERSEAS,
    DT_SOURCE_INTERSTATE
)
from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.datatypes import date_fns


OUTPUT_DIR = get_package_dir() / 'state_news_releases' / 'output'
OUTPUT_GRAPHS_DIR = get_package_dir() / 'covid_19_au_grab' / 'output_graphs' / 'output'
UPDATE_SCRIPT_PATH = get_package_dir() / 'output_data.py'
mimetypes.types_map['.tsv'] = 'text/tab-separated-values'


class App(object):
    def __init__(self):
        self.revisions = SQLiteDataRevisions()
        _thread.start_new_thread(self.loop, ())

    def loop(self):
        powerbi_run_1st = False
        powerbi_run_2nd = False

        while True:
            # Run once every around every hour and a half
            # (an hour is 3600 seconds)
            time.sleep(random.randint(4000, 5000))

            dt = datetime.datetime.now()

            if dt.hour >= 7 and dt.hour <= 22:
                # Run between 7am and 10pm only

                if dt.hour >= 12 and dt.hour < 14 and not powerbi_run_1st:
                    # Run powerbi once only between 12pm and 2pm
                    system(f'python3 {quote(str(UPDATE_SCRIPT_PATH))} --run-infrequent-jobs')
                    powerbi_run_1st = True
                    powerbi_run_2nd = False
                elif dt.hour >= 17 and dt.hour < 19 and not powerbi_run_2nd:
                    # Run powerbi once only between 5pm and 7pm
                    system(f'python3 {quote(str(UPDATE_SCRIPT_PATH))} --run-infrequent-jobs')
                    powerbi_run_1st = False
                    powerbi_run_2nd = True
                else:
                    system(f'python3 {quote(str(UPDATE_SCRIPT_PATH))}')

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
            schema_to_name=schema_to_name,
            constant_to_name=constant_to_name,
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
        datapoints = inst.get_datapoints_by_source_id(source_id)
        assert datapoints
        datapoints.sort(key=lambda i: (
            i.date_updated,
            i.region_schema,
            i.region_parent,
            i.region_child,
            i.agerange
        ))

        csvfile = StringIO()
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([i for i in datapoints[0]._fields])

        for datapoint in datapoints:
            row = []
            for key, value in zip(datapoint._fields, datapoint):
                row.append(value)
            writer.writerow(row)

        cherrypy.response.headers['Content-Disposition'] = \
            'attachment; filename="covid_%s.tsv"' % source_id
        cherrypy.response.headers['Content-Type'] = 'text/csv'
        csvfile.seek(0)
        return csvfile.read()


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
                        (SCHEMA_ADMIN_1, DT_TOTAL, 'AU'),
                        (SCHEMA_ADMIN_1, DT_NEW, 'AU'),
                        (SCHEMA_ADMIN_1, DT_STATUS_DEATHS, 'AU'),
                        (SCHEMA_ADMIN_1, DT_STATUS_DEATHS_NEW, 'AU'),
                        (SCHEMA_ADMIN_1, DT_STATUS_RECOVERED, 'AU'),
                        (SCHEMA_ADMIN_1, DT_STATUS_RECOVERED_NEW, 'AU'),
                        (SCHEMA_ADMIN_1, DT_TESTS_TOTAL, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_CONFIRMED, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_COMMUNITY, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_INTERSTATE, 'AU'),
                        (SCHEMA_ADMIN_1, DT_STATUS_HOSPITALIZED, 'AU'),
                        (SCHEMA_ADMIN_1, DT_STATUS_ICU, 'AU'),
                        (SCHEMA_ADMIN_1, DT_TOTAL_FEMALE, 'AU'),
                        (SCHEMA_ADMIN_1, DT_TOTAL_MALE, 'AU'),
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
                        (SCHEMA_ADMIN_1, DT_SOURCE_OVERSEAS, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_CONFIRMED, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_COMMUNITY, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_INTERSTATE, 'AU'),
                        (SCHEMA_ADMIN_1, DT_SOURCE_UNDER_INVESTIGATION, 'AU'),
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
            SCHEMA_ADMIN_1,
            (
                DT_TOTAL_FEMALE,
                DT_TOTAL_MALE,
                DT_TOTAL,
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
            SCHEMA_LGA,
            SCHEMA_SA3,
            SCHEMA_HHS,
            SCHEMA_LHD,
            SCHEMA_THS,
            SCHEMA_POSTCODE
        ):
            local_area_case_datapoints = inst.get_combined_values_by_datatype(
                region_schema,
                (
                    # TODO: What about by LGA (QLD only, other
                    #  LGA in DT_CASES_BY_REGION) and LHA (NSW)
                    DT_TOTAL,
                    DT_STATUS_ACTIVE,
                    DT_STATUS_RECOVERED,
                    DT_STATUS_DEATHS,
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
            schema_to_name=schema_to_name,
            date_fns=date_fns,
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def regionsTimeSeries(self, rev_date=None, rev_subid=None,
                          compat_mode=True):

        if rev_date is None:
            # Output the last successful run if
            # rev_date/rev_subid not supplied
            for rev_date, rev_subid, dt in self.revisions.get_revisions():
                inst = SQLiteDataRevision(rev_date, rev_subid)
                status_dict = inst.get_status_dict()

                if all(status_dict[k][0] == 'OK' for k in status_dict):
                    break
        else:
            inst = SQLiteDataRevision(rev_date, rev_subid)

        r = {}
        date_ids_dict = {}
        max_dates = {}

        schema_list = (
            (SCHEMA_ADMIN_1, 'AU', 'AU-ACT', (
                DT_TOTAL,
                DT_TESTS_TOTAL,

                DT_STATUS_RECOVERED,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_HOSPITALIZED,

                DT_SOURCE_OVERSEAS,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-NSW', (
                DT_TOTAL,
                DT_TESTS_TOTAL,

                DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED,
                #DT_STATUS_UNKNOWN,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_ICU_VENTILATORS,
                DT_STATUS_HOSPITALIZED,

                DT_SOURCE_OVERSEAS,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-NT', (
                DT_TOTAL,
                DT_TESTS_TOTAL,
                DT_STATUS_ICU,
                DT_STATUS_DEATHS,
                DT_STATUS_RECOVERED,
                DT_STATUS_HOSPITALIZED,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-QLD', (
                DT_TOTAL,
                DT_TESTS_TOTAL,

                DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_HOSPITALIZED,

                DT_SOURCE_OVERSEAS,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-SA', (
                DT_TOTAL,
                DT_TESTS_TOTAL,

                DT_STATUS_RECOVERED,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_HOSPITALIZED,

                DT_SOURCE_OVERSEAS,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-TAS', (
                DT_TOTAL,
                DT_TESTS_TOTAL,
                DT_STATUS_RECOVERED,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_HOSPITALIZED,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-VIC', (
                DT_TOTAL,
                DT_TESTS_TOTAL,

                #DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED,
                #DT_STATUS_UNKNOWN,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_HOSPITALIZED,

                DT_SOURCE_OVERSEAS,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            (SCHEMA_ADMIN_1, 'AU', 'AU-WA', (
                DT_TOTAL,
                DT_TESTS_TOTAL,

                DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED,
                DT_STATUS_UNKNOWN,
                DT_STATUS_DEATHS,
                DT_STATUS_ICU,
                DT_STATUS_HOSPITALIZED,

                DT_SOURCE_OVERSEAS,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),

            (SCHEMA_LGA, 'AU-NSW', None, (
                DT_TOTAL,
                DT_STATUS_ACTIVE,
                DT_STATUS_DEATHS,
                DT_STATUS_RECOVERED,
                DT_TESTS_TOTAL,
                DT_SOURCE_OVERSEAS,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            # Won't use LGA for totals, as don't have a long history
            (SCHEMA_LGA, 'AU-QLD', None, (
                #DT_TOTAL,
                DT_SOURCE_OVERSEAS,
                DT_SOURCE_CONFIRMED,
                DT_SOURCE_COMMUNITY,
                DT_SOURCE_INTERSTATE,
                DT_SOURCE_UNDER_INVESTIGATION,
            )),
            # Won't use SA for now, at least till can increase the accuracy
            (SCHEMA_LGA, 'AU-SA', None, (
                DT_TOTAL,
                DT_STATUS_ACTIVE,
            )),
            #(SCHEMA_LGA, 'AU-TAS', None, (DT_TOTAL,
            #                     )),
            (SCHEMA_LGA, 'AU-VIC', None, (
                DT_TOTAL,
                DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED,
            )),
            (SCHEMA_LGA, 'AU-WA', None, (
                DT_TOTAL,
            )),

            # NSW by postcode is possible, debating whether
            # to leave it as a non-goal for now:
            # * would require zooming in further
            # * would take orders of magnitude more time to download
            # * data comes in later each day than website
            #(SCHEMA_POSTCODE, 'AU-NSW', None, (DT_TOTAL,
            #                          DT_STATUS_ACTIVE,
            #                          DT_STATUS_DEATHS,
            #                          DT_STATUS_RECOVERED,
            #                          DT_TESTS_TOTAL,
            #                          DT_SOURCE_OVERSEAS,
            #                          DT_SOURCE_COMMUNITY,
            #                          DT_SOURCE_CONFIRMED,
            #                          DT_SOURCE_INTERSTATE,
            #                          DT_SOURCE_UNDER_INVESTIGATION
            #                          )),

            (SCHEMA_SA3, 'AU-ACT', None, (
                DT_TOTAL,
            )),
            # LHD is used for Active/Recovered values
            # It's also available by postcode on the NSW gov's site
            #(SCHEMA_LHD, 'AU-NSW', (DT_STATUS_ACTIVE,
            #                     DT_STATUS_DEATHS,
            #                     DT_STATUS_RECOVERED)),
            (SCHEMA_THS, 'AU-TAS', None, (
                DT_TOTAL,
                DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED
            )),
            (SCHEMA_HHS, 'AU-QLD', None, (
                DT_TOTAL,
                DT_STATUS_ACTIVE,
                DT_STATUS_RECOVERED,
                DT_STATUS_DEATHS
            )),
        )

        for region_schema, region_parent, region_child, datatypes in schema_list:
            schema_name = schema_to_name(region_schema)

            if compat_mode:
                if schema_name == 'admin_1':
                    schema_name = 'statewide'  # Back-compat HACK! ==========================================================
                    i_region_parent = region_child.split('-')[-1].lower()
                else:
                    i_region_parent = region_parent.split('-')[-1].lower()
            else:
                i_region_parent = region_parent

            schema_key = f'{i_region_parent}:{schema_name}'
            i_max_date, r[schema_key] = self.__get_time_series(
                inst,
                region_schema, region_parent, region_child,
                datatypes,
                date_ids_dict
            )
            if max_dates.get(schema_key) is None or i_max_date > max_dates[schema_key]:
                max_dates[schema_key] = i_max_date

        print("** MAX_DATE:", max_dates)
        return {
            'date_ids': {
                # Back-compat: convert to DD/MM/YYYY format!
                date_id: date_fns.to_slash_format(date_string)
                for (date_string, date_id)
                in date_ids_dict.items()
            },
            'time_series_data': r,
            'updated_dates': {
                k: v for k, v in max_dates.items() if v
            }
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def regionsTimeSeries2(self, rev_date=None, rev_subid=None):
        r = {}
        date_ids_dict = {}
        max_dates = {}

        inst = SQLiteDataRevision(rev_date, rev_subid)

        for region_schema in inst.get_region_schemas():
            datatypes = inst.get_datatypes_by_region_schema(region_schema)
            datatypes.sort()  # HACK: Really should sort based on largest number to allow for compression!
            print("DATATYPES:", datatypes, region_schema)

            for region_parent in inst.get_region_parents(region_schema):
                i_max_date, datapoints = self.__get_time_series(
                    inst, region_schema, region_parent, None,
                    datatypes, date_ids_dict
                )
                print(region_schema, region_parent, datatypes, len(datapoints))

                region_schema_str = schema_to_name(region_schema)
                r.setdefault(region_schema_str, {})[region_parent] = datapoints
                if (
                    max_dates.setdefault(region_schema_str, {}).get(region_parent, None) is None or
                    i_max_date > max_dates[region_schema_str][region_parent]
                ):
                    max_dates[region_schema_str][region_parent] = i_max_date

        return {
            'date_ids': date_ids_dict,
            'time_series_data': r,
            'updated_dates': max_dates
        }

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
            for date_updated, datapoints in sorted(date_updated_dict.items(), reverse=True):

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
            'sub_headers': [constant_to_name(i) for i in datatypes],
            'data': out
        }


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config={
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 6006,
            #'environment': 'production',
        },
        '/': {

        },
        '/graphs': {
            'tools.staticdir.root': OUTPUT_GRAPHS_DIR,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': ""
        },
        '/raw_data': {
            'tools.staticdir.root': OUTPUT_DIR,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': ""
        }
    })
