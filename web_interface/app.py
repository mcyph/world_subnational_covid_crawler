import csv
import json
import time
import random
import _thread
import cherrypy
import datetime
import mimetypes
from shlex import quote
from os import listdir, system
from os.path import getctime, expanduser
from cherrypy.lib.static import serve_file
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('./templates'))

from covid_19_au_grab.normalize_locality_name import \
    normalize_locality_name
from covid_19_au_grab.web_interface.CSVDataRevision import \
    CSVDataRevision
from covid_19_au_grab.web_interface.CSVDataRevisions import \
    CSVDataRevisions


OUTPUT_DIR = expanduser('~/dev/covid_19_au_grab/state_news_releases/output')
OUTPUT_GRAPHS_DIR = expanduser('~/dev/covid_19_au_grab/output_graphs')
UPDATE_SCRIPT_PATH = expanduser('~/dev/covid_19_au_grab/state_news_releases/output_data_from_news.py')
mimetypes.types_map['.tsv'] = 'text/tab-separated-values'


class App(object):
    def __init__(self):
        self.revisions = CSVDataRevisions()
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
                    system(f'python3 {quote(UPDATE_SCRIPT_PATH)} --update-powerbi')
                    powerbi_run_1st = True
                    powerbi_run_2nd = False
                elif dt.hour >= 17 and dt.hour < 19 and not powerbi_run_2nd:
                    # Run powerbi once only between 5pm and 7pm
                    system(f'python3 {quote(UPDATE_SCRIPT_PATH)} --update-powerbi')
                    powerbi_run_1st = False
                    powerbi_run_2nd = True
                else:
                    system(f'python3 {quote(UPDATE_SCRIPT_PATH)}')

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
            CSVDataRevision(period, subperiod_id)
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
        inst = CSVDataRevision(rev_date, rev_subid)

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
        )

    @cherrypy.expose
    def view_log(self, rev_date, rev_subid):
        return env.get_template('revision/view_log.html').render(
            FIXME
        )

    @cherrypy.expose
    def get_data_as_table(self, rev_date, rev_subid):
        inst = CSVDataRevision(rev_date, rev_subid)

        return env.get_template('revision/get_data_as_table.html').render(
            rev_date=rev_date,  # ESCAPE!
            rev_subid=rev_subid,  # ESCAPE!
            datapoints=inst.get_datapoints(),
            revision_time_string=inst.get_revision_time_string(),
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_json_data(self, rev_date, rev_subid):
        return CSVDataRevision(rev_date, rev_subid).get_datapoints()

    @cherrypy.expose
    def get_tsv_data(self, rev_date, rev_subid):
        rev_subid = int(rev_subid)
        return serve_file(
            f'{OUTPUT_DIR}/{rev_date}-{rev_subid}.tsv',
            "application/x-download", "attachment"
        )

    @cherrypy.expose
    def statistics(self, rev_date, rev_subid):
        inst = CSVDataRevision(rev_date, rev_subid)
        statistics_datapoints = []
        rev_date_parsed = datetime.datetime.strptime(rev_date, '%Y_%m_%d')

        for from_date in (
            (rev_date_parsed - datetime.timedelta(days=0)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=2)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=3)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=4)).strftime('%d/%m/%Y')
        ):
            print("**FROM DATE:", from_date)

            statistics_datapoints.append((
                from_date,
                inst.get_combined_values(
                    (
                        ('DT_CASES', 'None'),
                        ('DT_NEW_CASES', 'None'),
                        ('DT_PATIENT_STATUS', 'Deaths'),
                        #('DT_PATIENT_STATUS', 'New Deaths'),
                        ('DT_PATIENT_STATUS', 'Recovered'),
                        #('DT_PATIENT_STATUS', 'New Recovered'),
                        ('DT_CASES_TESTED', 'None'),
                        ('DT_SOURCE_OF_INFECTION', 'Locally acquired - contact of a confirmed case'),
                        ('DT_SOURCE_OF_INFECTION', 'Locally acquired - contact not identified'),
                        ('DT_SOURCE_OF_INFECTION', 'Interstate acquired'),
                        ('DT_PATIENT_STATUS', 'Hospitalized'),
                        ('DT_PATIENT_STATUS', 'ICU'),
                    ),
                    from_date=from_date
                )
            ))

        return env.get_template('revision/statistics.html').render(
            rev_date=rev_date,
            rev_date_slash_format=datetime.datetime.strptime(rev_date, '%Y_%m_%d').strftime('%d/%m/%Y'),
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            statistics_datapoints=statistics_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    def source_of_infection(self, rev_date, rev_subid):
        inst = CSVDataRevision(rev_date, rev_subid)
        statistics_datapoints = []
        rev_date_parsed = datetime.datetime.strptime(rev_date, '%Y_%m_%d')

        for from_date in (
            (rev_date_parsed - datetime.timedelta(days=0)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=2)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=3)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=4)).strftime('%d/%m/%Y')
        ):
            print("**FROM DATE:", from_date)

            statistics_datapoints.append((
                from_date,
                inst.get_combined_values(
                    (
                        ('DT_SOURCE_OF_INFECTION', 'Overseas acquired'),
                        ('DT_SOURCE_OF_INFECTION', 'Locally acquired - contact of a confirmed case'),
                        ('DT_SOURCE_OF_INFECTION', 'Locally acquired - contact not identified'),
                        ('DT_SOURCE_OF_INFECTION', 'Interstate acquired'),
                        ('DT_SOURCE_OF_INFECTION', 'Under investigation'),
                    ),
                    from_date=from_date
                )
            ))

        return env.get_template('revision/source_of_infection.html').render(
            rev_date=rev_date,
            rev_date_slash_format=datetime.datetime.strptime(rev_date, '%Y_%m_%d').strftime('%d/%m/%Y'),
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            statistics_datapoints=statistics_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    def gender_age(self, rev_date, rev_subid):
        inst = CSVDataRevision(rev_date, rev_subid)
        gender_age_datapoints = inst.get_combined_values_by_datatype(
            (
                'DT_AGE_FEMALE',
                'DT_AGE_MALE',
                'DT_AGE',
            )
        )
        return env.get_template('revision/gender_age.html').render(
            rev_date=rev_date,
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            gender_age_datapoints=gender_age_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    def local_area_case(self, rev_date, rev_subid):
        inst = CSVDataRevision(rev_date, rev_subid)
        local_area_case_datapoints = inst.get_combined_values_by_datatype(
            (
                # TODO: What about by LGA (QLD only, other LGA in DT_CASES_BY_REGION) and LHA (NSW)
                'DT_CASES_BY_REGION',
                'DT_CASES_BY_REGION_ACTIVE',
                'DT_CASES_BY_REGION_RECOVERED',
                'DT_CASES_BY_REGION_DEATHS',
            )
        )
        return env.get_template('revision/local_area_case.html').render(
            rev_date=rev_date,
            rev_subid=rev_subid,
            int=int,
            revision_time_string=inst.get_revision_time_string(),
            local_area_case_datapoints=local_area_case_datapoints,
            not_most_recent_warning=self.revisions.get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def regionsTimeSeriesAutogen(self, rev_date=None, rev_subid=None):
        if rev_date is None:
            # Output the last successful run if
            # rev_date/rev_subid not supplied
            for rev_date, rev_subid, dt in self.revisions.get_revisions():
                inst = CSVDataRevision(rev_date, rev_subid)
                status_dict = inst.get_status_dict()

                if all(status_dict[k][0] == 'OK' for k in status_dict):
                    break
        else:
            inst = CSVDataRevision(rev_date, rev_subid)

        from_dates = [i['date_updated'] for i in inst]

        out = []
        added = set()

        for from_date in from_dates:
            if from_date in added:
                continue
            added.add(from_date)

            print(from_date)
            local_area_case_datapoints = inst.get_combined_values_by_datatype(
                (
                    'DT_CASES_BY_REGION',
                    'DT_CASES_BY_REGION_ACTIVE',
                    'DT_CASES_BY_REGION_RECOVERED',
                    'DT_CASES_BY_REGION_DEATHS',
                ),
                from_date=from_date
            )

            out.extend(
                [(
                    i['date_updated'],
                    i['state_name'].lower(),
                    normalize_locality_name(i['name']),
                    i['DT_CASES_BY_REGION'],
                    i.get('DT_CASES_BY_REGION_ACTIVE', ''),
                    i.get('DT_CASES_BY_REGION_RECOVERED', ''),
                    i.get('DT_CASES_BY_REGION_DEATHS', '')
                ) for i in local_area_case_datapoints
                  if i['date_updated'] == from_date]
            )

        out_new = {}
        for date_updated, state_name, lga_name, cbr, cbr_a, cbr_r, cbr_d in out:
            out_new.setdefault((state_name, lga_name), []).append(
                [date_updated, cbr, cbr_a, cbr_r, cbr_d]
            )

        out_new_list = []
        for (state_name, lga_name), values in out_new.items():
            out_new_list.append([state_name, lga_name, values])

        return {
            'sub_headers': ['total', 'active', 'recovered', 'deaths'],
            'data': out_new_list
        }


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config={
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 5005,
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
