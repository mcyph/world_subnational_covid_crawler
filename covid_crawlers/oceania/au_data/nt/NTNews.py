from re import compile
from pyquery import PyQuery as pq
from covid_crawlers.oceania.au_data.StateNewsBase import (
    StateNewsBase, singledaystat
)
from covid_db.datatypes.enums import Schemas, DataTypes


class NTNews(StateNewsBase):
    STATE_NAME = 'nt'

    SOURCE_ID = 'au_nt_press_releases'
    SOURCE_URL = 'https://coronavirus.nt.gov.au'
    SOURCE_DESCRIPTION = ''

    LISTING_URL = None
    LISTING_HREF_SELECTOR = None
    STATS_BY_REGION_URL = 'https://coronavirus.nt.gov.au/current-status'

    def _get_date(self, href, html):
        date = pq(self._pq_contains(
            html, 'p', 'Data last updated'
        )[0]).text()
        #print(date)

        date = ' '.join([
            # Remove 6:00pm/6:00PM times,
            # which can be at the start or end
            i.strip(':.') for i in date.split('updated')[1].split('\n')[0].split()
            if not ':' in i
               and not '.' in i.strip('.')
               and not 'pm' in i.lower()
        ])

        if not '2020' in date and not '2021' in date:
            date = date + ' 2020'  # YEAR HACK!!!! ========================

        return self._extract_date_using_format(date, format='%d %B %Y')

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
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-NT',
            datatype=DataTypes.TOTAL,
            source_url=href,
            date_updated=self._get_date(href, html)
        )

    @singledaystat
    def _get_total_cases_tested(self, href, html):
        return self._extract_number_using_regex(
            compile('([0-9,]+) tests conducted'),
            html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-NT',
            datatype=DataTypes.TESTS_TOTAL,
            source_url=href,
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
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-NT',
            datatype=DataTypes.STATUS_RECOVERED,
            source_url=href,
            date_updated=self._get_date(href, html)
        )
        return [recovered] if recovered else None


if __name__ == '__main__':
    from pprint import pprint
    nn = NTNews()
    pprint(nn.get_datapoints())
