import hashlib
import datetime
from json import loads, dumps


CACHE_PERIOD_NONE = 0
CACHE_PERIOD_HOURLY = 1
CACHE_PERIOD_HALF_DAILY = 2
CACHE_PERIOD_DAILY = 3


class URLArchiver:
    def __init__(self):
        pass

    def _get_filename_for_url(self, url, ext, period=None):
        hash_md5 = hashlib.md5()
        hash_md5.update(url)

        if period is not None:
            period = '.'+period
        else:
            period = ''

        return f'{hash_md5.digest().encode("base64")}' \
               f'{period}' \
               f'.{ext}'

    def _get_for_period(self, period=None, t=None):
        if t is None:
            t = datetime.datetime.now()

        if period == CACHE_PERIOD_NONE:
            return None
        elif period == CACHE_PERIOD_HOURLY:
            # YYYY-MM-DD HH
            return t.strftime('%YYYY-%MM-%DD %HH')
        elif period == CACHE_PERIOD_DAILY:
            # YYYY-MM-DD
            return t.strftime('%YYYY-%MM-%DD')
        elif period == CACHE_PERIOD_HALF_DAILY:
            # YYYY-MM-DD [AM/PM]
            return t.strftime('%YYYY-%MM-%DD %p')
        else:
            raise Exception("Unknown cache period type:", period)

    def get_image_file_path(self, url,
                            format=None,
                            cache_period=None):
        if format is None:
            format = url.split('.')[-1]

    def get_text(self, url,
                 cache_period=CACHE_PERIOD_NONE,
                 period_value=None):
        pass


    def get_newer_than(self):
        FIXME

    def get_older_than(self):
        FIXME
