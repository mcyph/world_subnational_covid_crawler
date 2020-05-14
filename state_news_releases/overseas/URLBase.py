from os import makedirs
from os.path import exists, dirname
from collections import namedtuple
from urllib.request import urlretrieve

from covid_19_au_grab.state_news_releases.overseas.GlobalBase import \
    GlobalBase


URL = namedtuple('URL', [
    'url', 'static_file'
])


class URLBase(GlobalBase):
    def __init__(self, output_dir, urls_dict):
        GlobalBase.__init__(self, output_dir)
        self.urls_dict = urls_dict

    def update(self, force=False):
        for fnam, url in self.urls_dict.items():
            assert isinstance(url, URL)

            if url.static_file:
                path = self.output_dir / 'static' / fnam
            else:
                revision_dir = self.get_current_revision_dir()
                path = revision_dir / fnam

            if not exists(dirname(path)):
                makedirs(dirname(path))

            if not exists(path) or force:
                urlretrieve(url.url, path)
