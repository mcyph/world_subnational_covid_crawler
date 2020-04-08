from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, singledaystat
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES, DT_CASES_TESTED, DT_PATIENT_STATUS


class NTNews(StateNewsBase):
    STATE_NAME = 'nt'
    LISTING_URL = None
    LISTING_HREF_SELECTOR = None
    STATS_BY_REGION_URL = 'https://coronavirus.nt.gov.au/current-status'

    def _get_date(self, href, html):
        date = self._pq_contains(
            html, 'p', 'Data last updated'
        ).text()
        print(date)
        return self._extract_date_using_format(
            date.split('updated')[-1].split(':')[-1].strip().strip('.').partition(' ')[-1]+' 2020',  # YEAR HACK!!!! ========================
            format='%d %B %Y'
        )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        pass

    @singledaystat
    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile('([0-9,]+) confirmed cases'),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )

    @singledaystat
    def _get_total_cases_tested(self, href, html):
        return self._extract_number_using_regex(
            compile('([0-9,]+) tests conducted'),
            html,
            source_url=href,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(href, html)
        )

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

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    @singledaystat
    def _get_total_dhr(self, href, html):
        recovered = self._extract_number_using_regex(
            compile('([0-9,]+) people recovered'),
            html,
            name='Recovered',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
            date_updated=self._get_date(href, html)
        )
        return [recovered] if recovered else None


if __name__ == '__main__':
    from pprint import pprint
    nn = NTNews()
    pprint(nn.get_data())
