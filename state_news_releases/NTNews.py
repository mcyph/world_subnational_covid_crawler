from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class NTNews(StateNewsBase):
    STATE_NAME = ''
    LISTING_URL = ''
    LISTING_HREF_SELECTOR = ''

    def _get_total_cases(self, href, html):
        pass

    def _get_date(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        pass

    def _get_total_cases_by_region(self, href, html):
        pass

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass