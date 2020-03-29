from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class ACTNews(StateNewsBase):
    # FIXME: THIS GRABBER IS ONLY A SINGLE PAGE - IT REALLY NEEDS TO BREAK IT UP!!! ==================================

    STATE_NAME = 'act'
    LISTING_URL = []#'https://www.health.act.gov.au/about-our-health-system/'  \
                  #'novel-coronavirus-covid-19'
    LISTING_HREF_SELECTOR = '.latestnewsinner a'

    def get_data(self):
        def get_until(elm, selector):
            L = []
            for i in elm:
                if pq(i).is_(selector):
                    break
                L.append(i)
            return pq(L)

        url = 'https://www.health.act.gov.au/about-our-health-system/' \
              'novel-coronavirus-covid-19/latest-news'
        html = pq(url=url)

        for h3 in html('.timelinemain h3'):
            elms_in_h3 = get_until(h3.next_all(), 'h3')

            date = self._get_date(
                FIXME, pq(h3).html() + pq(elms_in_h3)
            )

            FIXME

    def _get_date(self, href, html):
        text = pq(html)('h3').text().strip()
        date_str = text.partition(' ')[-1].split('-')[0].strip()
        return self._extract_date_using_format(date_str, '%d %B')

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile(r'total to ([0-9,]+)'),
            html
        ) or self._extract_number_using_regex(
            compile(r'confirmed cases in the ACT is now ([0-9,]+)'),
            html
        )

    def _get_total_cases_tested(self, href, html):
        neg = self._extract_number_using_regex(
            compile('There have been ([0-9,]+) negative'),
            html
        ) or self._extract_number_using_regex(
            compile(r'tested negative is now ([0-9,]+)'),
            html
        )
        pos = self._get_total_cases(href, html)

        if neg is not None and pos is not None:
            return neg + pos
        return None

    def _get_total_new_cases(self, href, html):
        return self._extract_number_using_regex(
            compile(r'([0-9,]+) new confirmed cases'), html
        )

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, href, html):
        pass

    def _get_total_male_female_breakdown(self, href, html):
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, href, html):
        pass

    def _get_total_cases_by_region(self, href, html):
        # There's still a "likely source" (as of 25-march)
        # but not sure it's worth adding e.g. interstate
        # or international values
        pass

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    def _get_total_source_of_infection(self, url, html):
        pass

