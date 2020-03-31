from re import compile
from pyquery import PyQuery as pq

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint


class ACTNews(StateNewsBase):
    STATE_NAME = 'act'
    LISTING_URL = (
        # There's only 2 pages for now, so will hardcode
        # MUST BE UPDATED!!! ===========================================================================================
        'https://www.covid19.act.gov.au/topics?queries_topic_query=0002',
        'https://www.covid19.act.gov.au/topics?queries_topic_query=0002'
            '&result_1504801_result_page=2',
    )
    LISTING_HREF_SELECTOR = '.card .card-content .card--title a'

    def _get_date(self, href, html):
        date = pq(html)('.article-body--date p').text().strip()
        return self._extract_date_using_format(date)

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile(r'total to ([0-9,]+)'),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        ) or self._extract_number_using_regex(
            compile(r'confirmed cases in the ACT is now ([0-9,]+)'),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases_tested(self, href, html):
        neg_cases = self._extract_number_using_regex(
            compile('There have been ([0-9,]+) negative'),
            html,
            source_url=href,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(href, html)
        ) or self._extract_number_using_regex(
            compile(r'tested negative is now ([0-9,]+)'),
            html,
            source_url=href,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(href, html)
        )
        pos_cases = self._get_total_cases(href, html)

        if neg_cases is not None and pos_cases is not None:
            return DataPoint(
                datatype=neg_cases.datatype,
                value=neg_cases.value + pos_cases.value,
                date_updated=neg_cases.date_updated,
                source_url=neg_cases.source_url,
                text_match=(
                    neg_cases.text_match,
                    pos_cases.text_match
                )
            )
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


if __name__ == '__main__':
    from pprint import pprint
    an = ACTNews()
    pprint(an.get_data())
