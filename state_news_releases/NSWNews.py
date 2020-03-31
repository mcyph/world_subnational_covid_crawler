from pyquery import PyQuery as pq
from re import compile, MULTILINE, DOTALL

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase
from covid_19_au_grab.state_news_releases.constants import DT_CASES_TESTED


class NSWNews(StateNewsBase):
    STATE_NAME = 'nsw'
    #LISTING_URL = 'https://www.health.nsw.gov.au/news/Pages/default.aspx'
    LISTING_URL = 'https://www.health.nsw.gov.au/news/pages/2020-nsw-health.aspx'
    LISTING_HREF_SELECTOR = '.dfwp-item a'
    STATS_BY_REGION_URL = 'https://www.health.nsw.gov.au/Infectious/' \
                          'diseases/Pages/covid-19-latest.aspx'

    def _get_date(self, href, html):
        return self._extract_date_using_format(
            pq(pq(html)('.newsdate')[0]).text().strip()
        )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        pass

    def _get_total_cases(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        return self._extract_number_using_regex(
            compile(
                # Total (including tested and excluded)
                r'<td[^>]*?>(?:<[^</>]+>)?Total(?:</[^<>]+>)?</td>'
                r'[^<]*?<td[^>]*>.*?([0-9,]+).*?</td>',
                MULTILINE | DOTALL
            ),
            html,
            source_url=href,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(href, html)
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
        """
        TODO: Use Tesseract to grab the data from
        https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-latest.aspx

        NOTE: This webpage *changes daily*!!!! --------
        """
        pass

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    def _get_total_source_of_infection(self, url, html):
        pass


if __name__ == '__main__':
    from pprint import pprint
    nn = NSWNews()
    pprint(nn.get_data())
