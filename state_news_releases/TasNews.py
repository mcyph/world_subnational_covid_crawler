from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class TasNews(StateNewsBase):
    STATE_NAME = 'tas'
    LISTING_URL = 'https://www.dhhs.tas.gov.au/news/2020'
    LISTING_HREF_SELECTOR = 'table.dhhs a'

    def _get_total_cases(self, href, html):
        pass

    def _get_date(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        compile('([0-9,]+)[^0-9]*?(?:coronavirus tests had been completed|tests[^0-9]*?complete)')

    def _get_total_cases_by_region(self, href, html):
        pass

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass

