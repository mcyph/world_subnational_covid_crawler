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
        'div#content div h2'

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile('state total to ([0-9,]+)'),
            html
        )

    def _get_total_cases_tested(self, href, html):
        return self._extract_number_using_regex(
            compile(
                # Total number changed from being enclosed in a <strong>
                # tag to a <b> tag, so changed to be as broad as NSW
                # <strong>Total</strong></td>
                # <td headers="table59454r1c2"><b>37,334‬</b></td>
                r'<td[^>]*?>(?:<[^</>]+>)?Total(?:</[^<>]+>)?</td>'
                r'[^<]*?<td[^>]*?>.*?([0-9,]+).*?</td>',
                MULTILINE | DOTALL
            ),
            html
        )

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_total_male_female_breakdown(self, url, html):
        pass

    def _get_new_male_female_breakdown(self, url, html):
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_total_cases_by_region(self, href, html):
        table = pq(pq('table.table.table-bordered.header-basic')[0])

        if not 'Total confirmed cases to date' in table.text():
            return None

        regions = {}
        for tr in table('tr'):
            if 'total' in pq(tr).text().lower():
                continue

            for x, td in enumerate(pq(tr)('td')):
                if x == 0:
                    hhs_region = td.text().strip()
                elif x == 1:
                    try:
                        value = int(td.text().strip())
                        regions[hhs_region] = value
                    except ValueError:
                        # WARNING!!!
                        pass
                else:
                    FIXME

        return regions

    def _get_total_new_cases_by_region(self, href, html):
        # TODO: QLD only provided new cases for a few days
        # it might pay to do a tally of some kind!
        ' New confirmed cases'

        table = pq(pq('table.table.table-bordered.header-basic')[0])

        if not 'New confirmed cases' in table.text():
            return None

        regions = {}
        for tr in table('tr'):
            text = pq(tr).text().lower()
            if 'total' in text or 'new confirmed' in text:
                continue

            for x, td in enumerate(pq(tr)('td')):
                if x == 0:
                    hhs_region = td.text().strip()
                elif x == 1:
                    try:
                        value = int(td.text().strip())
                        regions[hhs_region] = value
                    except ValueError:
                        # WARNING!!!
                        pass
                else:
                    FIXME

        return regions

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    def _get_total_source_of_infection(self, url, html):
        pass
