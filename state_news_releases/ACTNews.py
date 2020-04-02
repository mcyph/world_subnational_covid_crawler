from re import compile, IGNORECASE
from pyquery import PyQuery as pq

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, singledaystat
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES, DT_NEW_CASES, \
    DT_NEW_MALE, DT_NEW_FEMALE, \
    DT_FEMALE, DT_MALE, \
    DT_SOURCE_OF_INFECTION, \
    DT_HOSPITALIZED, DT_RECOVERED
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.word_to_number import word_to_number


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
    STATS_BY_REGION_URL = 'https://www.covid19.act.gov.au/updates/' \
                          'confirmed-case-information'

    def _get_date(self, href, html):

        date = pq(html)('.article-body--date p').text().strip()

        if not date:
            date = pq(self._pq_contains(html, '.container', 'Last Updated:')[0]).text()
            date = date.split('</strong>')[-1].strip()
            # April 02 2020
            return self._extract_date_using_format(
                date.split(':')[-1].strip(), '%B %d %Y'
            )
        else:
            return self._extract_date_using_format(date)

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, href, html):
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile(r'total to ([0-9,]+)'),
                compile(r'confirmed cases [^0-9.]+([0-9,]+)')
            ),
            c_html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases_tested(self, href, html):
        c_html = word_to_number(html)

        neg_cases = self._extract_number_using_regex(
            (
                compile('There have been ([0-9,]+) negative'),
                compile('<p>Number of negative tests</p></td><td><p>([0-9,]+)</p>'),
                compile(r'tested negative is now ([0-9,]+)')
            ),
            c_html,
            source_url=href,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(href, html)
        )
        pos_cases = self._get_total_cases(href, html)

        if neg_cases is not None and pos_cases is not None:
            return DataPoint(
                name=None,
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
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            compile(
                r'([0-9,]+)\)? new confirmed'
            ),
            c_html,
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        )

    #============================================================#
    #                      Age Breakdown                         #
    #============================================================#

    def _get_new_age_breakdown(self, href, html):
        pass

    @singledaystat
    def _get_total_age_breakdown(self, href, html):
        if href != self.STATS_BY_REGION_URL:
            # Only at stats by region URL
            return None

        '<strong>By age group</strong></p></td><td><p><strong>Total</strong></p></td></tr><tr><td><p>0-29</p></td><td><p>5</p></td></tr><tr><td><p>30-39</p></td><td><p>7</p></td></tr><tr><td><p>40-49</p></td><td><p>8</p></td></tr><tr><td><p>50-59</p></td><td><p>6</p></td></tr><tr><td><p>60-69</p></td><td><p>8</p></td></tr><tr><td><p>70+</p></td><td><p>5</p>'

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, href, html):
        c_html = word_to_number(html)

        # WARNING: Can have multiple entries per article =============================================================
        # (early reports, anyway)
        # 'a male in his ([0-9]+)\'?s'
        # 'a female in her ([0-9]+)\'?s'
        # e.g. https://www.covid19.act.gov.au/news-articles/fifth-and-sixth-cases-of-covid-19-confirmed-in-act

        c_html = '\n'.join([
            i for i in c_html.split('.')
            if 'new case' in i
        ])

        r = []
        male = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)? [^0-9.]*?(?<!fe)male(?:s)?'),
            c_html,
            source_url=href,
            datatype=DT_NEW_MALE,
            date_updated=self._get_date(href, html)
        )
        if male:
            r.append(male)

        female = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)? [^0-9.]*?female(?:s)?'),
            c_html,
            source_url=href,
            datatype=DT_NEW_FEMALE,
            date_updated=self._get_date(href, html)
        )
        if female:
            r.append(female)
        return r

    @singledaystat
    def _get_total_male_female_breakdown(self, href, html):
        # https://www.covid19.act.gov.au/updates/confirmed-case-information
        # Only at stats by region URL!!!
        # Well, they had it for one day at the reports, but..)

        c_html = word_to_number(html)

        male = self._extract_number_using_regex(
            compile(
                '<p><strong>By sex</strong></p></td></tr>'
                '<tr><td><p>Male</p></td><td><p>([0-9,]+)</p></td></tr>'
                '<tr><td><p>Female</p></td><td><p>(?:[0-9,]+)</p>',
                IGNORECASE
            ),
            c_html,
            source_url=href,
            datatype=DT_FEMALE,
            date_updated=self._get_date(href, html)
        )
        female = self._extract_number_using_regex(
            compile(
                '<p><strong>By sex</strong></p></td></tr>'
                '<tr><td><p>Male</p></td><td><p>(?:[0-9,]+)</p></td></tr>'
                '<tr><td><p>Female</p></td><td><p>([0-9,]+)</p>',
                IGNORECASE
            ),
            c_html,
            source_url=href,
            datatype=DT_MALE,
            date_updated=self._get_date(href, html)
        )
        if male and female:
            return (male, female)
        elif male or female:
            return (male or female,)
        return None

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

    @singledaystat
    def _get_total_source_of_infection(self, url, html):
        # only source is at
        # https://www.covid19.act.gov.au/updates/confirmed-case-information

        re_soi = compile(
            r'<strong>By likely source of infection</strong></p></td>'
                r'<td><p><strong> Count</strong></p></td></tr>'
            r'<tr><td><p>Overseas acquired</p></td>'
                r'<td><p>(?P<Overseas_Acquired>[0-9,]+)</p></td></tr>'
            r'<tr><td><p>Interstate acquired</p></td>'
                r'<td><p>(?P<Interstate_Acquired>[0-9,]+)</p></td></tr>'
            r'<tr><td><p>Contact of a confirmed ACT case</p></td>'
                r'<td><p>(?P<Contact_of_a_Confirmed_ACT_Case>[0-9,]+)</p></td></tr>'
            r'<tr><td><p>Unknown / local transmission</p></td>'
                r'<td><p>(?P<Unknown_or_Local_Transmission>[0-9,]+)</p></td></tr>',
            IGNORECASE
        )

        match = re_soi.match(html)
        if match:
            r = []
            gd = match.groupdict()

            for k, v in gd.items():
                r.append(DataPoint(
                    name=k.replace('_', ' '),
                    datatype=DT_SOURCE_OF_INFECTION,
                    value=int(v.replace(',', '')),
                    date_updated=self._get_date(url, html),
                    source_url=url,
                    text_match=None  # HACK!
                ))
            return r
        return None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        # recovered/lives lost also at
        # https://www.covid19.act.gov.au/updates/confirmed-case-information

        c_html = word_to_number(html)
        patients = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)? COVID-19 patients'),
            c_html,
            source_url=href,
            datatype=DT_HOSPITALIZED,
            date_updated=self._get_date(href, html)
        )
        recovered = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)? cases have recovered'),
            c_html,
            source_url=href,
            datatype=DT_RECOVERED,
            date_updated=self._get_date(href, html)
        )

        r = []
        if patients:
            r.append(patients)
        if recovered:
            r.append(recovered)
        return r or None


if __name__ == '__main__':
    from pprint import pprint
    an = ACTNews()
    pprint(an.get_data())
