from re import compile, IGNORECASE
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class TasNews(StateNewsBase):
    STATE_NAME = 'tas'
    LISTING_URL = 'https://www.dhhs.tas.gov.au/news/2020'
    LISTING_HREF_SELECTOR = 'table.dhhs a'

    def _get_date(self, url, html):
        pass

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, url, html):
        return self._extract_number_using_regex(
            compile(
                'confirmed ([0-9,]+) more cases of coronavirus',
                IGNORECASE
            ),
            html
        )

    def _get_total_cases(self, url, html):
        return self._extract_number_using_regex(
            compile(
                'tally to ([0-9,]+)'
            ),
            html
        )

    def _get_total_cases_tested(self, url, html):
        compile('([0-9,]+)[^0-9]*?'
                '(?:coronavirus tests had been completed|'
                   'tests[^0-9]*?complete)')

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    # What about age breakdown??
    # e.g. Two of the cases are aged in their 70s. One is aged in
    # their 60s, one in their 50s, one in their 30s, and one is
    # in their 20s.

    def _get_new_male_female_breakdown(self, url, html):
        # 'Four of the cases are women; two are men'
        men = self._extract_number_using_regex(
            compile('([0-9,]+)[^0-9.,]* men', IGNORECASE),
            html
        )
        women = self._extract_number_using_regex(
            compile('([0-9,]+)[^0-9.,]* women', IGNORECASE),
            html
        )
        if men is not None and women is not None:
            return (men, women)
        return None

    def _get_total_male_female_breakdown(self, url, html):
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_total_new_cases_by_region(self, url, html):
        # Three of the cases are from Northern Tasmania, two are
        # from Southern Tasmania and one case is from the North West.
        pass

    def _get_total_cases_by_region(self, url, html):
        pass

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        # Two of the cases have recently been on cruise ships.
        # One case is a close contact of a previously confirmed
        # case, and three have recently travelled to Tasmania
        # from overseas.
        pass

    def _get_total_source_of_infection(self, url, html):
        pass

