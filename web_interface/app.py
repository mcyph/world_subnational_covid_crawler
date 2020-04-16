import csv
import json
import time
import random
import _thread
import cherrypy
import datetime
import mimetypes
from shlex import quote
from pytz import timezone
from os import listdir, system
from os.path import getctime, expanduser
from cherrypy.lib.static import serve_file
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('./templates'))


OUTPUT_DIR = expanduser('~/dev/covid_19_au_grab/state_news_releases/output')
OUTPUT_GRAPHS_DIR = expanduser('~/dev/covid_19_au_grab/output_graphs')
UPDATE_SCRIPT_PATH = expanduser('~/dev/covid_19_au_grab/state_news_releases/output_data_from_news.py')
mimetypes.types_map['.tsv'] = 'text/tab-separated-values'


class App(object):
    def __init__(self):
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
    #                       Utility Functions                     #
    #=============================================================#

    def __check_period(self, path):
        assert not '..' in path
        assert not '/' in path
        assert not '\\' in path

        dd, mm, yyyy = path.split('_')
        int(yyyy), int(mm), int(dd)

    def __read_csv(self, period, subperiod_id):
        self.__check_period(period)
        subperiod_id = int(subperiod_id)
        print(f'{period}-{subperiod_id}.tsv')

        out = []
        with open(f'../state_news_releases/output/{period}-{subperiod_id}.tsv',
                  'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                out.append(row)

        out.sort(key=self.__date_updated_sort_key)
        return out

    def __get_status_dict(self, period, subperiod_id):
        self.__check_period(period)
        subperiod_id = int(subperiod_id)

        with open(f'../state_news_releases/output/{period}-{subperiod_id}.json',
                  'r', encoding='utf-8', errors='replace') as f:
            return json.loads(f.read())['status']

    def __get_revisions(self):
        # Return [[rev_date, rev_subid, rev_time], ...]
        r = []

        for fnam in listdir(OUTPUT_DIR):
            if not fnam.endswith('.tsv'):
                continue
            rev_date, rev_subid = fnam[:-4].split('-')
            rev_time = getctime(f'{OUTPUT_DIR}/{fnam}')
            dt = str(datetime.datetime.fromtimestamp(rev_time) \
                .astimezone(timezone('Australia/Melbourne'))).split('.')[0]
            r.append((rev_date, int(rev_subid), dt))

        r.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))
        return r

    def __get_revision_time_string(self, period, subperiod_id):
        rev_time = getctime(f'{OUTPUT_DIR}/{period}-{subperiod_id}.tsv')
        dt = str(datetime.datetime.fromtimestamp(rev_time) \
                 .astimezone(timezone('Australia/Melbourne'))).split('.')[0]
        return dt

    def __date_updated_sort_key(self, x):
        """
        Sort so that the most recent dates come first,
        then sort by state, datatype and name
        """
        def sortable_date(i):
            dd, mm, yyyy = i.split('/')
            return (
                str(9999-int(yyyy)) + '_' +
                str(99-int(mm)) + '_' +
                str(99-int(dd))
            )

        return (
            sortable_date(x['date_updated']),
            x['state_name'],
            x['datatype'],
            x['name']
        )

    def __generic_sort_key(self, x):
        """
        Sort only by state, datatype and name, ignoring date
        """
        #print(x)
        return (
            x['state_name'],
            x['datatype'],
            x['name']
        )

    def __get_not_most_recent_warning(self, period, subperiod_id):
        i_period, i_subperiod_id, i_dt = self.__get_revisions()[0]

        if i_period != period or int(i_subperiod_id) != int(subperiod_id):
            return (
                '<div style="font-size: 1.2em; font-weight: bold; color: red">'
                    f'WARNING: This is an outdated revision. '
                    f'You can find the newest '
                    f'<a href="/revision?rev_date={i_period}&rev_subid={i_subperiod_id}">here</a>.'
                '</div>'
            )
        return ''

    #=============================================================#
    #                            Index                            #
    #=============================================================#

    @cherrypy.expose
    def index(self):
        t = env.get_template('index.html')
        return t.render(
            revisions=self.__get_revisions()
        )

    @cherrypy.expose
    def most_recent_changes(self):
        """
        TODO: Go thru each version from the
        last 48 hours, and output any changes
        """
        revisions = self.__get_revisions()[:15]
        data = [
            self.__read_csv(period, subperiod_id)
            for period, subperiod_id, _ in revisions
        ]

        changes_by_revision = []
        for x, i_data in enumerate(data):
            if x == len(data)-1:
                break

            changes_by_revision.append((
                revisions[x][0],
                revisions[x][1],
                revisions[x][2],
                self.__get_changed(i_data, data[x+1])
            ))

        return env.get_template('most_recent_changes.html').render(
            changes_by_revision=changes_by_revision
        )

    def __get_changed(self, current_datapoints, previous_datapoints):
        current_dict = {}
        previous_dict = {}
        previous_dict_by_name = {}

        keys = (
            'state_name',
            'datatype',
            'name',
            'value',
        )

        for datapoint in current_datapoints:
            unique_key = tuple([datapoint[k] for k in keys])
            if unique_key in current_dict:
                continue
            current_dict[unique_key] = datapoint

        for datapoint in previous_datapoints:
            unique_key = tuple([datapoint[k] for k in keys])
            previous_dict[unique_key] = None
            if unique_key[:-1] in previous_dict_by_name:
                continue
            previous_dict_by_name[unique_key[:-1]] = datapoint

        changed = []
        for unique_key in current_dict:
            if unique_key not in previous_dict:
                changed.append((
                    current_dict[unique_key],
                    previous_dict_by_name.get(unique_key[:-1])
                ))
        return changed

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
        try:
            status_list = sorted(list(self.__get_status_dict(rev_date, rev_subid).items()))
        except FileNotFoundError:
            status_list = []

        return env.get_template('revision/revision.html').render(
            status_list=status_list,
            rev_date=rev_date,  # ESCAPE!
            rev_subid=rev_subid,  # ESCAPE!
            revision_time_string=self.__get_revision_time_string(
                rev_date, rev_subid
            ),
            not_most_recent_warning=self.__get_not_most_recent_warning(
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
        datapoints = self.__read_csv(rev_date, rev_subid)

        return env.get_template('revision/get_data_as_table.html').render(
            rev_date=rev_date,  # ESCAPE!
            rev_subid=rev_subid,  # ESCAPE!
            datapoints=datapoints,
            revision_time_string=self.__get_revision_time_string(
                rev_date, rev_subid
            ),
            not_most_recent_warning=self.__get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_json_data(self, rev_date, rev_subid):
        # TODO: Validate period!! ===========================================================================
        return self.__read_csv(rev_date, int(rev_subid))

    @cherrypy.expose
    def get_tsv_data(self, rev_date, rev_subid):
        self.__check_period(rev_date)
        rev_subid = int(rev_subid)
        return serve_file(
            f'{OUTPUT_DIR}/{rev_date}-{rev_subid}.tsv',
            "application/x-download", "attachment"
        )

    @cherrypy.expose
    def statistics(self, rev_date, rev_subid):
        datapoints = self.__read_csv(rev_date, rev_subid)
        statistics_datapoints = []
        rev_date_parsed = datetime.datetime.strptime(rev_date, '%Y_%m_%d')

        for from_date in (
            None,
            (rev_date_parsed - datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=2)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=3)).strftime('%d/%m/%Y'),
            (rev_date_parsed - datetime.timedelta(days=4)).strftime('%d/%m/%Y')
        ):
            print("**FROM DATE:", from_date)

            statistics_datapoints.append((
                from_date, self.__get_combined_values(
                datapoints,
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
            )))

        return env.get_template('revision/statistics.html').render(
            rev_date=rev_date,
            rev_date_slash_format=datetime.datetime.strptime(rev_date, '%Y_%m_%d').strftime('%d/%m/%Y'),
            rev_subid=rev_subid,
            int=int,
            revision_time_string=self.__get_revision_time_string(
                rev_date, rev_subid
            ),
            statistics_datapoints=statistics_datapoints,
            not_most_recent_warning=self.__get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    def gender_age(self, rev_date, rev_subid):
        datapoints = self.__read_csv(rev_date, rev_subid)
        gender_age_datapoints = self.__get_combined_values_by_datatype(
            datapoints,
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
            revision_time_string=self.__get_revision_time_string(
                rev_date, rev_subid
            ),
            gender_age_datapoints=gender_age_datapoints,
            not_most_recent_warning=self.__get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    @cherrypy.expose
    def local_area_case(self, rev_date, rev_subid):
        datapoints = self.__read_csv(rev_date, rev_subid)
        local_area_case_datapoints = self.__get_combined_values_by_datatype(
            datapoints,
            (
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
            revision_time_string=self.__get_revision_time_string(
                rev_date, rev_subid
            ),
            local_area_case_datapoints=local_area_case_datapoints,
            not_most_recent_warning=self.__get_not_most_recent_warning(
                rev_date, rev_subid
            ),
        )

    def __get_combined_values_by_datatype(self,
                                          datapoints,
                                          datatypes,
                                          from_date=None):
        """
        Returns as a combined dict,
        e.g. if datatypes a list of ((datatype, name/None), ...) is (
            "DT_AGE",
            "DT_AGE_FEMALE",
        )
        it will output as [{
            'name': (e.g.) '70+',
            'date_updated': ...,
            'DT_AGE': ...,
            'DT_AGE_FEMALE': ...
        }, ...]
        """
        def to_datetime(dt):
            return datetime.datetime.strptime(dt, '%d/%m/%Y')

        combined = {}
        for datatype in datatypes:
            for datapoint in self.__get_combined_value(
                datapoints, datatype,
                from_date=from_date
            ):
                i_combined = combined.setdefault(datapoint['state_name'], {}) \
                                     .setdefault(datapoint['name'], {})

                if (
                    not 'date_updated' in i_combined or
                    to_datetime(datapoint['date_updated']) <
                        to_datetime(i_combined['date_updated'])
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint['date_updated']
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%d/%m/%Y')

                i_combined['name'] = datapoint['name']
                i_combined['state_name'] = datapoint['state_name']

                if not datatype in i_combined:
                    i_combined[datatype] = datapoint['value']
                    i_combined[f'{datatype} date_updated'] = datapoint['date_updated']
                    i_combined[f'{datatype} source_url'] = datapoint['source_url']

        out = []
        for i_combined in combined.values():
            for add_me in i_combined.values():
                out.append(add_me)
        return out

    def __get_combined_values(self, datapoints, filters,
                              from_date=None):
        """
        Returns as a combined dict,
        e.g. if filters (a list of ((datatype, name/None), ...) is (
            ("DT_PATIENT_STATUS", "Recovered"),
            ("DT_PATIENT_STATUS", "ICU")
        )
        it will output as [{
            'date_updated': ...,
            'DT_PATIENT_STATUS (Recovered)': ...,
            'DT_PATIENT_STATUS (ICU)': ...
        }, ...]
        """
        def to_datetime(dt):
            return datetime.datetime.strptime(dt, '%d/%m/%Y')

        combined = {}
        for datatype, name in filters:
            for datapoint in self.__get_combined_value(
                datapoints[:], datatype, name,
                from_date=from_date
            ):
                i_combined = combined.setdefault(datapoint['state_name'], {})

                if (
                    not 'date_updated' in i_combined or
                    to_datetime(datapoint['date_updated']) <
                        to_datetime(i_combined['date_updated'])
                ):
                    # Use the least recent date
                    i_combined['date_updated'] = datapoint['date_updated']
                    i_combined['date_today'] = datetime.datetime.now() \
                        .strftime('%d/%m/%Y')

                k = (
                    f'{datatype} ({datapoint["name"]})'
                    if datapoint["name"] != 'None'
                    else datatype
                )

                i_combined['state_name'] = datapoint['state_name']

                if not k in i_combined:
                    i_combined[k] = datapoint['value']
                    i_combined[f'{k} date_updated'] = datapoint['date_updated']
                    i_combined[f'{k} source_url'] = datapoint['source_url']
                    i_combined[f'{k} text_match'] = datapoint['text_match']

        out = []
        for i_combined in combined.values():
            out.append(i_combined)
        return out

    def __get_combined_value(self,
                             datapoints,
                             datatype,
                             name=None,
                             from_date=None):
        """
        Filter `datapoints` to have only `datatype` (e.g. "DT_PATIENT_STATUS"),
        and optionally only have `name` (e.g. "Recovered" or "None" as a string)

        Returns only the most recent value (optionally from `from_date`)
        """

        def date_greater_than(x, y):
            #print(x, y)

            dd1, mm1, yyyy1 = x.split('/')
            x = (int(yyyy1), int(mm1), int(dd1))

            dd2, mm2, yyyy2 = y.split('/')
            y = (int(yyyy2), int(mm2), int(dd2))

            return x >= y

        r = {}
        for datapoint in datapoints:
            if datapoint['datatype'] != datatype:
                continue
            elif name is not None and datapoint['name'] != name:
                continue
            elif from_date is not None and not date_greater_than(
                from_date, datapoint['date_updated']
            ):
                continue

            # Note we're restricting to only `datatype` already,
            # so no need to include it in the key
            unique_k = (
                datapoint['state_name'],
                datapoint['name']
            )
            if unique_k in r:
                assert date_greater_than(
                    r[unique_k]['date_updated'],
                    datapoint['date_updated']
                )
                continue
            r[unique_k] = datapoint

        r = list(r.values())
        r.sort(key=self.__generic_sort_key)
        return r


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
