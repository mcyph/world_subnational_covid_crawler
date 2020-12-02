import requests
from os import makedirs
from os.path import exists, dirname
from collections import namedtuple
from covid_19_au_grab.covid_crawlers._base_classes.GlobalBase import GlobalBase


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
                r = requests.get(
                    url.url,
                    headers={
                        "USER-AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
                        "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "ACCEPT-LANGUAGE": "en-US,en;q=0.5",
                        "ACCEPT-ENCODING": "gzip, deflate", # , br
                        "CONNECTION": "keep-alive",
                        "REFERER": url.url,  # FIXME!
                        "UPGRADE-INSECURE-REQUESTS": "1",
                        "PRAGMA": "no-cache",
                        "CACHE-CONTROL": "no-cache",
                        "TE": "Trailers",
                        "COOKIE": "language=en; _ga=GA1.2.2016181909.1598484966; _gid=GA1.2.1748222623.1599205537; _gat_gtag_UA_125495940_3=1; mzcr-diseases-eu-cookies=1"  # For Yemen
                    },
                    verify=False
                )
                with open(path, 'wb') as f:
                    f.write(r.content)
