import csv
from os import listdir
from os.path import getctime, expanduser
import cherrypy
import datetime
import mimetypes
from glob import glob
from cherrypy import tools
from cherrypy.lib.static import serve_file
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('./templates'))


OUTPUT_DIR = expanduser('~/dev/covid_19_au_grab/state_news_releases/output')
OUTPUT_GRAPHS_DIR = expanduser('~/dev/covid_19_au_grab/output_graphs')
mimetypes.types_map['.tsv'] = 'text/tab-separated-values'


class App(object):
    def __init__(self):
        pass

    #=============================================================#
    #                       Utility Functions                     #
    #=============================================================#

    def __check_period(self, path):
        assert not '..' in path
        assert not '/' in path
        assert not '\\' in path

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

        def sortable_date(i):
            dd, mm, yyyy = i.split('/')
            return str(9999-int(yyyy)) + '_' + str(99-int(mm)) + '_' + str(99-int(dd))

        out.sort(key=lambda x: (
            sortable_date(x['date_updated']),
            x['state_name'],
            x['datatype'],
            x['name']
        ))

        return out

    def __get_revisions(self):
        # Return [[rev_date, rev_subid, rev_time], ...]
        r = []
        for fnam in listdir(OUTPUT_DIR):
            rev_date, rev_subid = fnam[:-4].split('-')
            rev_time = getctime(f'{OUTPUT_DIR}/{fnam}')
            r.append((rev_date, rev_subid, rev_time))
        return r

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

        today = datetime.datetime.now() \
                        .strftime(FIXME)
        yesterday = (
            datetime.datetime.now() -
            datetime.timedelta(days=1)
        ).strftime(FIXME)

        data = []
        for subdir in sorted(listdir(OUTPUT_DIR), reverse=True):
            if (
                subdir.startswith(today+'-') or
                subdir.startswith(yesterday+'-')
            ):
                data.append(self.__read_csv(*subdir.split('-')))

        out = []
        for x, i_data in enumerate(data):
            if x == len(data)-1:
                break
            out.append(self.__get_diffs(i_data, data[x+1]))

        return env.get_template('most_recent_changes.html').render(
            changes=out
        )

    def __get_diffs(self, data_1, data_2):
        # This could be done much more efficiently..
        set_1 = set()
        set_2 = set()

        for datapoint in data_1:
            set_1.add(datapoint.values())  #  MAKE SURE THIS IS ORDERED!!

        for datapoint in data_2:
            set_2.add(datapoint.values())

        deleted = []
        for datapoint in data_1:
            if datapoint.values() not in set_2:
                deleted.append(datapoint)

        added = []
        for datapoint in data_2:
            if datapoint.values() not in set_1:
                added.append(datapoint)

        return added, deleted

    @cherrypy.expose
    def most_recent_graphs(self):
        return env.get_template('most_recent_graphs.html').render()

    #=============================================================#
    #                   View Specific Revision                    #
    #=============================================================#

    @cherrypy.expose
    def revision(self, rev_date, rev_subid):
        return env.get_template('revision/revision.html').render(
            rev_date=rev_date,  # ESCAPE!
            rev_subid=rev_subid,  # ESCAPE!
            rev_time=None # FIXME
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
            rev_time=None,  # FIXME
            datapoints=datapoints
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
    def get_output_table(self):
        pass


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config={
        'global': {
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
