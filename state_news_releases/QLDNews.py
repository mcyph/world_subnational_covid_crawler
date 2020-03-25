from pyquery import PyQuery as pq
from re import compile, MULTILINE, DOTALL
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class QLDNews(StateNewsBase):
    STATE_NAME = 'qld'
    LISTING_URL = 'https://www.qld.gov.au/health/conditions/' \
                  'health-alerts/coronavirus-covid-19/current-status'
    LISTING_HREF_SELECTOR = '#qg-primary-content a'

    # Updates for regions is at
    # https://www.health.qld.gov.au/news-events/doh-media-releases/releases/queensland-novel-coronavirus-covid-19-update9
    #

    def _infer_missing_info(self, dates_dict):
        # TODO: QLD health now only provides a tally, but previously
        #  gave number of new cases by region. It makes sense to
        #  derive this info as needed.
        pass

    def _get_date(self, href, html):
        pass

    def _get_total_cases(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        compile(
            # Total number changed from being enclosed in a <strong>
            # tag to a <b> tag, so changed to be as broad as NSW
            # <strong>Total</strong></td>
            # <td headers="table59454r1c2"><b>37,334‬</b></td>
            r'<td[^>]*?>(?:<[^</>]+>)?Total(?:</[^<>]+>)?</td>'
            r'[^<]*?<td[^>]*?>.*?([0-9,]+).*?</td>',
            MULTILINE | DOTALL
        )

    def _get_total_cases_by_region(self, href, html):
        pass

    def _get_total_new_cases_by_region(self, href, html):
        # TODO: QLD only provided new cases for a few days
        # it might pay to do a tally of some kind!
        pass

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass

