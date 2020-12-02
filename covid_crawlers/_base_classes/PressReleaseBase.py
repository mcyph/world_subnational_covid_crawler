from os import makedirs
from os.path import exists, dirname
from urllib.request import urlretrieve
from pyquery import PyQuery as pq

from covid_19_au_grab.covid_crawlers._base_classes.GlobalBase import GlobalBase
from covid_19_au_grab._utility.URLArchiver import URLArchiver


class PressReleaseBase(GlobalBase):
    def __init__(self, output_dir, urls_dict, url_selector, encoding='utf-8'):
        GlobalBase.__init__(self, output_dir)
        self.listings_url_dict = urls_dict
        self.url_selector = url_selector
        self.encoding = encoding
        self.pr_dir = self.output_dir / 'pr'

        if not exists(self.pr_dir):
            makedirs(self.pr_dir)
        self.url_archiver = URLArchiver(self.pr_dir)

    def update(self, force=False):
        for fnam, url in self.listings_url_dict.items():
            revision_dir = self.get_today_revision_dir()
            path = revision_dir / fnam

            if not exists(dirname(path)):
                makedirs(dirname(path))

            if not exists(path) or force:
                urlretrieve(url, path)

            with open(path, encoding='utf-8') as f:
                print(path)
                for a_elm in pq(f.read())(self.url_selector):
                    url = pq(a_elm).attr('href')
                    html = self.url_archiver.get_url_data(
                        url, period=self._get_date
                    )

    def iter_press_releases(self):
        for fnam, url in self.listings_url_dict.items():
            revision_dir = self.get_today_revision_dir()
            path = revision_dir / fnam

            with open(path, encoding='utf-8') as f:
                print(path)
                for a_elm in pq(f.read())(self.url_selector):
                    url = pq(a_elm).attr('href')
                    html = self.url_archiver.get_url_data(
                        url, period=self._get_date
                    )
                    date = self._get_date(url, html)
                    yield url, date, html
