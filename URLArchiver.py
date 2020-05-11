import re
import datetime
import unicodedata
from os import listdir, makedirs
from os.path import isfile, expanduser, exists, dirname
from urllib.request import urlretrieve, urlopen

from covid_19_au_grab.get_package_dir import get_data_dir


BASE_PATH = get_data_dir()


def slugify(value):
    """
    Function from Django, under the 3-clause BSD
    https://docs.djangoproject.com/en/3.0/ref/utils/

    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


class URLArchiver:
    def __init__(self, base_dir):
        self.base_dir = BASE_PATH / base_dir

    def get_path(self, subdir):
        dir_ = self.base_dir / subdir
        fnam = self._get_first_fnam_in_dir(dir_)
        path = dir_ / fnam
        return path

    def get_url_data(self, url, period=None, cache=True,
                     unicode_fix=True):
        """
        Download data from `url`, optionally

        :param url: the url to download
        :param period: either "YYYY_MM_DD" period-formatted string,
                       a function which returns a "YYYY_MM_DD" string
                           based on the url and the data at `url`,
                       or `None`
        :param cache: whether to use a cached copy.
                      when `False` and `period` is a function,
                          overwrite the cache item
                      when `False` and `period` is a string,
                          don't overwrite, but use a new subperiod id
                      when `True` and `period` is a function,
                          FIXME
                      when `True` and `period` is a string,
                          FIXME
        """
        def _unicode_fix(s):
            if unicode_fix:
                return self.unicode_fix(s)
            else:
                return s

        # I'm using YYYY_MM_DD-ID here, so
        #   that it binary sorts in
        #   year-month-day, then ID order
        if period is None:
            t = datetime.datetime.now()
            period = t.strftime('%Y_%m_%d')
        elif isinstance(period, datetime.datetime):
            period = period.strftime('%Y_%m_%d')

        if callable(period):
            # Provide support for getting the period
            # based on the content located at the url
            # by providing the content to the
            # user-supplied "obtain period" function.
            fnam = self._escape_url(url)
            found_path = None

            for subdir in listdir(self.base_dir):
                # The period(/date) of the content can't be
                # figured out until it's been downloaded.
                # If there's any file which corresponds to `url`
                # in any of the period subdirs, then we'll use it.
                check_path = f'{self.base_dir}/{subdir}/{fnam}'
                if exists(check_path) and cache:
                    with open(check_path, 'r',
                              encoding='utf-8',
                              errors='replace') as f:
                        return _unicode_fix(f.read())
                elif exists(check_path):
                    # If cache is disabled, overwrite regardless!
                    found_path = check_path
                    break

            with urlopen(url) as f:
                data = f.read().decode(
                    'utf-8', errors='replace'
                )

            if found_path:
                dir_ = dirname(found_path)
            else:
                period = period(url, data)
                subperiod_id = self._get_subperiod_id_for_url(period, url)
                dir_ = f'{self.base_dir}/{period}-{subperiod_id}'

            try:
                makedirs(dir_)
            except OSError:
                pass

            with open(f'{dir_}/{fnam}', 'w',
                      encoding='utf-8',
                      errors='replace') as f:
                f.write(data)
            return _unicode_fix(data)

        else:
            subperiod_id = self._get_subperiod_id_for_url(period, url)
            dir_ = f'{self.base_dir}/{period}-{subperiod_id}'

            try:
                makedirs(dir_)
            except OSError:
                pass

            try:
                if not cache:
                    # Always download if cache is disabled!
                    raise FileNotFoundError()
                fnam = self._get_first_fnam_in_dir(dir_)
            except FileNotFoundError:
                # Download if a cached version
                # for this URL can't be found
                fnam = self._escape_url(url)
                urlretrieve(url, f'{dir_}/{fnam}')

            with open(f'{dir_}/{fnam}', 'r',
                      encoding='utf-8',
                      errors='replace') as f:
                return _unicode_fix(f.read())

    def unicode_fix(self, s):
        # Replace no-break spaces with spaces
        s = s.replace('&nbsp;', ' ')
        # Replace zero-width spaces with nothing
        s = s.replace('&#8203;', '')
        s = s.replace('\u200B', '')
        s = re.sub(r'\s+', ' ', s, re.DOTALL)
        return s

    def iter_periods(self, newest_first=True):
        """
        Iterate through all the periods without the subperiod ID
        i.e. in YYYY_MM_DD format
        """
        for dir_ in sorted(listdir(self.base_dir),
                           reverse=newest_first):
            assert '-' in dir_
            yield dir_.split('-')[0]

    def iter_paths_for_period(self, period, newest_first=True):
        """
        Iterate through subperiods within a period.
        Yields the subperiod ID (which is 1+) and the subdirectory
        (which is in the [YYYY]_[MM]_[DD]-[subperiod ID] format)
        """
        out = []
        for dir_ in listdir(f"{self.base_dir}"):
            if dir_.split('-')[0] == period:
                subperiod_id = int(dir_.split('-')[-1])
                out.append((subperiod_id, dir_))
        out.sort(reverse=newest_first)
        return out

    def _get_subperiod_id_for_url(self, period, url=None):
        """
        TODO: Find the ID that corresponds to `url`
        by looking through all the current DD_MM_YYYY-ID
        directories, and seeing if there's a file which
        corresponds to `url`. If one doesn't

        if one doesn't
        """
        largest_id = 0
        escaped_url = self._escape_url(url)

        for subperiod_id, subdir in self.iter_paths_for_period(period):
            fnam = self._get_first_fnam_in_dir(f'{self.base_dir}/{subdir}')

            if fnam == escaped_url:
                print("FOUND:", subperiod_id)
                return subperiod_id
            if subperiod_id > largest_id:
                largest_id = subperiod_id

        return largest_id+1

    def _get_first_fnam_in_dir(self, dir_):
        for fnam in listdir(dir_):
            if isfile(f'{dir_}/{fnam}'):
                return fnam
        raise FileNotFoundError("No file found in directory:", dir_)

    def _escape_url(self, url):
        return slugify(url)[:250]


if __name__ == '__main__':
    ua = URLArchiver('act/listing')
    print(ua.get_url_data('https://www.covid19.act.gov.au/news-articles/covid-19-update-31-march'))

    ua = URLArchiver('qld/current_status')
    for i in ua.iter_periods():
        print(i)
        for j in ua.iter_paths_for_period(i):
            print(j)
