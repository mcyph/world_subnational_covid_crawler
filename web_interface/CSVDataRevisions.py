import datetime
from os import listdir
from pytz import timezone
from os.path import getctime
from covid_19_au_grab.get_package_dir import get_package_dir


OUTPUT_DIR = get_package_dir() / 'state_news_releases' / 'output'


class CSVDataRevisions:
    def get_not_most_recent_warning(self, period, subperiod_id):
        i_period, i_subperiod_id, i_dt = self.get_revisions()[0]

        if i_period != period or int(i_subperiod_id) != int(subperiod_id):
            return (
                '<div style="font-size: 1.2em; font-weight: bold; color: red">'
                f'WARNING: This is an outdated revision. '
                f'You can find the newest '
                f'<a href="/revision?rev_date={i_period}&rev_subid={i_subperiod_id}">here</a>.'
                '</div>'
            )
        return ''

    def get_revisions(self):
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

    def get_changed(self, current, previous):
        # Get a diff between current and previous datapoints
        current_dict = {}
        previous_dict = {}
        previous_dict_by_name = {}

        keys = (
            'schema',
            'state_name',
            'datatype',
            'agerange',
            'region',
            'value',
        )

        for datapoint in current.get_datapoints():
            unique_key = tuple([datapoint[k] for k in keys])
            if unique_key in current_dict:
                continue
            current_dict[unique_key] = datapoint

        for datapoint in previous.get_datapoints():
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

