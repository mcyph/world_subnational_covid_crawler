from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class WANews(StateNewsBase):
    STATE_NAME = 'wa'
    LISTING_URL = 'https://ww2.health.wa.gov.au/News/' \
                  'Media-releases-listing-page'
    LISTING_HREF_SELECTOR = 'div.threeCol-accordian a'

    def _get_date(self, href, html):
        pass

    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile(r'total to ([0-9,]+)'),
            html
        )

    def _get_total_cases_tested(self, href, html):
        negative_cases = self._extract_number_using_regex(
            # Seems the WA website's wording can change day-to-day
            compile(r'([0-9]+[0-9,]*?)'
                    r'([^0-9]*?negative COVID-19 tests|'
                    r'[^0-9]*?tested negative|'
                    r'[^0-9]*?negative)'),
            html
        )
        positive_cases = self._get_total_cases(href, html)
        return negative_cases + positive_cases

    def _get_total_cases_by_region(self, href, html):
        # AFAIK, this information currently isn't
        # available in an easily readable format
        return None

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass
