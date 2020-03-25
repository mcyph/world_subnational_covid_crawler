
from json import loads, dumps


CACHE_PERIOD_NONE = 0
CACHE_PERIOD_HOURLY = 1
CACHE_PERIOD_HALF_DAILY = 2
CACHE_PERIOD_DAILY = 3


class URLArchiver:
    def __init__(self):
        pass

    def _hash_for_filename(self, s, ext):
        pass

    def get_image_file_path(self, url,
                            format=None,
                            cache_period=None):

        if cache_period == CACHE_PERIOD_NONE:
            pass
        elif cache_period == CACHE_PERIOD_HOURLY:
            pass
        elif cache_period == CACHE_PERIOD_DAILY:
            pass
        elif cache_period == CACHE_PERIOD_HALF_DAILY:
            pass
        else:
            raise Exception("Unknown cache period type:", cache_period)

        if format is None:
            format = url.split('.')[-1]



    def get_text(self, url):
        pass


