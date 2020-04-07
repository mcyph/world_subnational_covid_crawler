from re import compile, IGNORECASE
from pyquery import PyQuery as pq

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, singledaystat
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES, DT_NEW_CASES, \
    DT_NEW_MALE, DT_NEW_FEMALE, \
    DT_FEMALE, DT_MALE, \
    DT_SOURCE_OF_INFECTION, \
    DT_PATIENT_STATUS, \
    DT_AGE
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
        # TODO: UPDATE ME and make me work with confirmed case info!!! ====================================
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile(r'total to ([0-9,]+)'),
                compile(r'confirmed cases [^0-9.]+([0-9,]+)'),
                compile(r'total remains at (?:<strong>)?([0-9,]+)(?:</strong>)?')
            ),
            c_html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases_tested(self, href, html):
        # TODO: UPDATE ME and make me work with confirmed case info!!! ====================================
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
                r'([0-9,]+)\)? new (?:confirmed|cases?)'
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
        table = self._pq_contains(
            html, 'table', 'By age group',
            ignore_case=True
        )[0]
        tbody = pq(table)('tbody')[0]
        tr = tbody[1]
        ages = [
            int(i.replace(',', '').strip())
            for i in pq(tr).text().split('\n')
        ]
        ages = {
            '0-29': ages[0],
            '30-39': ages[1],
            '40-49': ages[2],
            '50-59': ages[3],
            '60-69': ages[4],
            '70+': ages[5]
        }
        r = []
        for k, v in ages.items():
            r.append(DataPoint(
                name=k,
                datatype=DT_AGE,
                value=v,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match=None  # HACK!
            ))
        return r

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

    #@singledaystat
    def _get_total_male_female_breakdown(self, href, html):
        # https://www.covid19.act.gov.au/updates/confirmed-case-information
        # Only at stats by region URL!!!
        # Well, they had it for one day at the reports, but..)

        # ADDITION: This looks to only support the reports(?)
        # should the stats by region URL be supported(!?) ============================================================

        c_html = word_to_number(html)

        male = self._extract_number_using_regex(
            compile(
                '<p[^>]*><strong>By sex</strong></p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Male</p></td><td[^>]*><p[^>]*>([0-9,]+)</p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Female</p></td><td[^>]*><p[^>]*>(?:[0-9,]+)</p>',
                IGNORECASE
            ),
            c_html,
            source_url=href,
            datatype=DT_FEMALE,
            date_updated=self._get_date(href, html)
        )
        female = self._extract_number_using_regex(
            compile(
                '<p[^>]*><strong[^>]*>By sex</strong></p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Male</p></td><td[^>]*><p[^>]*>(?:[0-9,]+)</p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Female</p></td><td[^>]*><p[^>]*>([0-9,]+)</p>',
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
        pass

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    #@singledaystat
    def _get_total_source_of_infection(self, url, html):
        # NOTE: there are also stats at
        # https://www.covid19.act.gov.au/updates/confirmed-case-information
        # but they're in a different format -
        # not sure it's worth supporting them

        r = []
        for re_text in (
            r'<tr[^>]*><td[^>]*><p[^>]*>Overseas acquired</p></td>'
                r'<td[^>]*><p[^>]*>(?P<Overseas_acquired>[0-9,]+)</p></td></tr>',
            # Cruise ship-acquired was only added around 6 April
            r'<tr[^>]*><td[^>]*><p[^>]*>Cruise ship acquired</p></td>'
                r'<td[^>]*><p[^>]*>(?P<Cruise_ship_acquired>[0-9,]+) of the [0-9,]+</p></td></tr>',
            r'<tr[^>]*><td[^>]*><p[^>]*>Interstate acquired</p></td>'
                r'<td[^>]*><p[^>]*>(?P<Interstate_acquired>[0-9,]+)</p></td></tr>',
            r'<tr[^>]*><td[^>]*><p[^>]*>Contact of a confirmed ACT case</p></td>'
                r'<td[^>]*><p[^>]*>(?P<Contact_of_a_confirmed_ACT_case>[0-9,]+)</p></td></tr>',
            r'<tr[^>]*><td[^>]*><p[^>]*>Unknown / local transmission</p></td>'
                r'<td[^>]*><p[^>]*>(?P<Unknown_or_local_transmission>[0-9,]+)</p></td></tr>',
            r'<tr[^>]*><td[^>]*><p[^>]*>Under investigation</p></td>'
                r'<td[^>]*><p[^>]*>(?P<Under_investigation>[0-9,]+)</p></td></tr>'
        ):
            re_soi = compile(re_text, IGNORECASE)

            match = re_soi.search(html)
            if match:
                gd = match.groupdict()

                for k, v in gd.items():
                    if v is None:
                        continue

                    r.append(DataPoint(
                        name=k.replace('_', ' '),
                        datatype=DT_SOURCE_OF_INFECTION,
                        value=int(v.replace(',', '')),
                        date_updated=self._get_date(url, html),
                        source_url=url,
                        text_match=None  # HACK!
                    ))

        return r or None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        # recovered/lives lost also at
        # https://www.covid19.act.gov.au/updates/confirmed-case-information  ===========================================

        c_html = word_to_number(html)
        patients = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)? COVID-19 patients'),
            c_html,
            name='Hospitalized',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
            date_updated=self._get_date(href, html)
        )
        recovered = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)? cases have recovered'),
            c_html,
            name='Recovered',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
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
