from pyquery import PyQuery as pq
from re import compile, MULTILINE, DOTALL, IGNORECASE

from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_NEW_CASES, DT_CASES, \
    DT_AGE, DT_AGE_MALE, DT_AGE_FEMALE, \
    DT_ICU, DT_ICU_VENTILATORS, DT_HOSPITALIZED, DT_DEATHS, \
    DT_SOURCE_OF_INFECTION
from covid_19_au_grab.word_to_number import word_to_number


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
        return self._extract_number_using_regex(
            compile(
                'additional ([0-9,]+) cases',
                IGNORECASE
            ),
            html,
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases(self, href, html):
        return self._extract_number_using_regex(
            compile(
                '([0-9,]+) COVID-19 cases',
                IGNORECASE
            ),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )

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
    #                      Age Breakdown                         #
    #============================================================#

    def _get_new_age_breakdown(self, href, html):
        pass

    def _get_total_age_breakdown(self, href, html):
        r = []
        table = pq(html, parser='html')(
            'table:contains("Age Group")'
        ) or pq(html, parser='html')(
            'table:contains("Age group")'
        )
        if not table:
            return None
        table = table[0]

        for age_group in (
            '0-9',
            '10-19',
            '20-29',
            '30-39',
            '40-49',
            '50-59',
            '60-69',
            '70-79',
            '80-89',
            '90-100'
        ):
            tds = pq(table)('tr:contains("%s")' % age_group)
            if not tds:
                continue
            tds = tds[0]

            female = int(pq(tds[1]).text().strip() or 0)
            male = int(pq(tds[2]).text().strip() or 0)
            total = int(pq(tds[3]).text().replace(' ', '').strip() or 0)

            for datatype, value in (
                (DT_AGE_FEMALE, female),
                (DT_AGE_MALE, male),
                (DT_AGE, total)
            ):
                if value is None:
                    continue
                r.append(DataPoint(
                    name=age_group,
                    datatype=datatype,
                    value=value,
                    date_updated=self._get_date(href, html),
                    source_url=href,
                    text_match=None
                ))
        return r

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
        r = []

        c_html = html.replace('  ', ' ').replace('\u200b', '')  # HACK!
        c_html = pq(c_html)('table:contains("Source")')

        for k in (
            'Overseas acquired',
            'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Locally acquired – contact not identified',
            'Under investigation',
            'Epi link (contact of confirmed case)',
            'Unknown',
        ):
            # TODO: MAKE WORD WITH ALL THE CASES!!
            # not sure why this doesn't always work! ==================================================================
            tr = pq(c_html)('tr:contains("%s")' % k)
            if not tr:
                continue

            tr = tr[0]
            c_icu = int(pq(tr[1]).text().replace(',', '').strip())

            r.append(DataPoint(
                name=k,
                datatype=DT_SOURCE_OF_INFECTION,
                value=c_icu,
                date_updated=self._get_date(url, html),
                source_url=url,
                text_match=None
            ))
        return r or None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        r = []
        c_html = word_to_number(html)

        recovered = self._extract_number_using_regex(
            compile(
                '([0-9,]+) COVID-19 cases being treated by NSW Health',
                IGNORECASE
            ),
            c_html,
            source_url=href,
            datatype=DT_HOSPITALIZED,
            date_updated=self._get_date(href, html)
        )
        if recovered:
            r.append(recovered)

        icu = self._extract_number_using_regex(
            compile(
                '([0-9,]+) cases in our Intensive Care Units',
                IGNORECASE
            ),
            c_html,
            source_url=href,
            datatype=DT_ICU,
            date_updated=self._get_date(href, html)
        )
        if icu:
            r.append(icu)

        ventilators = self._extract_number_using_regex(
            compile(
                '([0-9,]+) cases in our Intensive Care Units',
                IGNORECASE
            ),
            c_html,
            source_url=href,
            datatype=DT_ICU_VENTILATORS,
            date_updated=self._get_date(href, html)
        )
        if ventilators:
            r.append(ventilators)

        deaths = self._extract_number_using_regex(
            compile(
                '([0-9,]+) deaths in NSW',
                MULTILINE | DOTALL
            ),
            c_html,
            source_url=href,
            datatype=DT_DEATHS,
            date_updated=self._get_date(href, html)
        )
        if deaths:
            r.append(deaths)
        return r


if __name__ == '__main__':
    from pprint import pprint
    nn = NSWNews()
    pprint(nn.get_data())
