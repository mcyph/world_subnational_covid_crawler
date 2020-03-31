from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class SANews(StateNewsBase):
    STATE_NAME = 'sa'
    LISTING_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/'  \
                  'SA+Health+Internet/About+us/News+and+media/all+media+releases/'
    LISTING_HREF_SELECTOR = '.news a'

    def _get_date(self, href, html):
        return self._extract_date_using_format(
            # e.g. Monday, 30 March 2020
            pq(html)('div.middle-column div.wysiwyg p') \
                .text().strip().split(', ')[-1]
        )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        pass

    def _get_total_cases(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        # This is only a rough value - is currently displayed as "> (value)"!
        return self._extract_number_using_regex(
            compile(r'(?:undertaken more than )?([0-9,]+) tests'),
            html
        )

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, url, html):
        pass


    def _get_total_male_female_breakdown(self, url, html):
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, href, html):
        pass

    def _get_total_cases_by_region(self, href, html):
        pass

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    def _get_total_source_of_infection(self, url, html):
        pass

