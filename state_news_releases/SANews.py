from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class SANews(StateNewsBase):
    STATE_NAME = 'sa'
    LISTING_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/'  \
                  'SA+Health+Internet/About+us/News+and+media/all+media+releases/'
    LISTING_HREF_SELECTOR = '.news a'

    def _get_total_cases(self, href, html):
        pass

    def _get_date(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        # This is only a rough value - is currently displayed as "> (value)"!
        compile(r'(?:undertaken more than )?([0-9,]+) tests')

    def _get_total_cases_by_region(self, href, html):
        pass

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass

