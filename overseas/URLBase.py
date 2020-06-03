import ssl
import urllib
import certifi
from os import makedirs
from os.path import exists, dirname
from collections import namedtuple
from urllib.request import urlretrieve

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
#ssl._create_default_https_context = ssl._create_unverified_context

proxy = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy)
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0')]
urllib.request.install_opener(opener)


from covid_19_au_grab.overseas.GlobalBase import \
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
                revision_dir = self.get_today_revision_dir()
                path = revision_dir / fnam

            if not exists(dirname(path)):
                makedirs(dirname(path))

            if not exists(path) or force:
                urlretrieve(url.url, path)
