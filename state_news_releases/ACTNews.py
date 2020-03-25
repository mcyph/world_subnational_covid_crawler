from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class ACTNews(StateNewsBase):
    STATE_NAME = 'act'
    LISTING_URL = 'https://www.health.act.gov.au/about-our-health-system/'  \
                  'novel-coronavirus-covid-19'
    LISTING_HREF_SELECTOR = '.latestnewsinner a'

    def _get_total_cases(self, href, html):
        pass

    def _get_date(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        (
            compile(r'tested negative is now ([0-9,]+)'),
            compile(r'confirmed cases in the ACT is now ([0-9,]+)')
        )

    def _get_total_new_cases(self, href, html):
        pass

    def _get_total_cases_by_region(self, href, html):
        pass

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass

