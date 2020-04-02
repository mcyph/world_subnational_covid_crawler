from pyquery import PyQuery as pq
from re import compile, MULTILINE, DOTALL

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, singledaystat
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_NEW_CASES, DT_CASES, \
    DT_CASES_BY_REGION, DT_NEW_CASES_BY_REGION
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint


class QLDNews(StateNewsBase):
    STATE_NAME = 'qld'
    LISTING_URL = 'https://www.health.qld.gov.au/' \
                  'news-events/doh-media-releases'
    LISTING_HREF_SELECTOR = '.presszebra div h3 a'
    STATS_BY_REGION_URL = 'https://www.qld.gov.au/health/conditions/' \
                          'health-alerts/coronavirus-covid-19/' \
                          'current-status/' \
                          'current-status-and-contact-tracing-alerts'

    def _infer_missing_info(self, dates_dict):
        # TODO: QLD health now only provides a tally, but previously
        #  gave number of new cases by region. It makes sense to
        #  derive this info as needed.
        pass

    def _get_date(self, href, html):
        return self._extract_date_using_format(
            # e.g. 24 March 2020
            pq(html)('div#content div h2').text().strip()
        )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile('state total to ([0-9,]+)'),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)

        ) or self._extract_number_using_regex(
            compile(
                # Total number changed from being enclosed in a <strong>
                # tag to a <b> tag, so changed to be as broad as NSW
                # <strong>Total</strong></td>
                # <td headers="table59454r1c2"><b>37,334‬</b></td>
                r'<td[^>]*?>(?:<[^</>]+>)?Total(?:</[^<>]+>)?</td>'
                r'[^<]*?<td[^>]*?>.*?([0-9,]+).*?</td>',
                MULTILINE | DOTALL
            ),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_new_cases(self, href, html):
        return self._extract_number_using_regex(
            compile('([0-9,]+) new cases'),
            html,
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        )

    @singledaystat
    def _get_total_cases_tested(self, href, html):
        # NOTE: This is actually a different page to the press releases!
        #  I needed to get some of these from web.archive.org.
        #  Some of the stats may be a day or more old,
        #  so will need to add the date of the stat as well(!)

        # Find the start of the # samples tested table
        th_regex = compile(
            '<th id="table[^"]+">[^<]*?As at ([^<]+)[^<]*?</th>[^<]*'
            '<th id="table[^"]+">[^<]*?(?:Samples|Patients) tested[^<]*?</th>',
            DOTALL | MULTILINE
        )
        match = th_regex.search(html)
        if not match:
            print("NOT INITIAL MATCH!")
            return None  # WARNING!!!

        # Get the date - it's in format "30 March 2020"
        date_updated = self._extract_date_using_format(
            match.group(1).strip()
        )
        slice_from = match.end(1)  # CHECK ME!
        html = html[slice_from:]

        # Get the # samples total
        value = self._extract_number_using_regex(
            compile(
                # Total number changed from being enclosed in a <strong>
                # tag to a <b> tag, so changed to be as broad as NSW
                # <strong>Total</strong></td>
                # <td headers="table59454r1c2"><b>37,334‬</b></td>
                r'<td[^>]*?>(?:<[^</>]+>)?Total(?:</[^<>]+>)?</td>'
                r'[^<]*?<td[^>]*?>.*?([0-9,]+).*?</td>',
                MULTILINE | DOTALL
            ),
            html,
            date_updated=date_updated,
            datatype=DT_CASES_TESTED,
            source_url=href
        )
        if not value:
            print("NOT SECOND MATCH!")
            return None  # WARNING!
        return value

    #============================================================#
    #                      Age Breakdown                         #
    #============================================================#

    def _get_new_age_breakdown(self, href, html):
        pass

    def _get_total_age_breakdown(self, href, html):
        pass

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
        table = pq(pq(html)('table.table.table-bordered.header-basic'))
        if not table:
            return None

        if not 'Total confirmed cases to date' in pq(table[0]).text():
            print("NOT TOTAL:", table.text())
            return None

        regions = []
        for tr in table('tr'):
            if 'total' in pq(tr).text().lower():
                continue

            for x, td in enumerate(pq(tr)('td')):
                if x == 0:
                    hhs_region = pq(td).text().strip()
                elif x == 1:
                    try:
                        value = int(pq(td).text().strip())
                        regions.append(DataPoint(
                            datatype=DT_CASES_BY_REGION,
                            name=hhs_region,
                            value=value,
                            date_updated=self._get_date(href, html),
                            source_url=href,
                            text_match=None
                        ))
                    except ValueError:
                        # WARNING!!!
                        pass
                else:
                    FIXME

        return regions

    def _get_new_cases_by_region(self, href, html):
        # TODO: QLD only provided new cases for a few days
        # it might pay to do a tally of some kind!
        ' New confirmed cases'

        table = pq(html)('table.table.table-bordered.header-basic')
        if not table:
            return None

        if not 'New confirmed cases' in pq(table[0]).text():
            return None

        regions = []
        for tr in table('tr'):
            text = pq(tr).text().lower()
            if 'total' in text or 'new confirmed' in text:
                continue

            for x, td in enumerate(pq(tr)('td')):
                if x == 0:
                    hhs_region = pq(td).text().strip()
                elif x == 1:
                    try:
                        value = int(pq(td).text().strip())
                        regions.append(DataPoint(
                            datatype=DT_NEW_CASES_BY_REGION,
                            name=hhs_region,
                            value=value,
                            date_updated=self._get_date(href, html),
                            source_url=href,
                            text_match=None
                        ))
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

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        pass


if __name__ == '__main__':
    from pprint import pprint
    qn = QLDNews()
    pprint(qn.get_data())
