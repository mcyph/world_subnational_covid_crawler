from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_19_au_grab.state_news_releases.StateNewsBase import (
    StateNewsBase, singledaystat
)
from covid_19_au_grab.datatypes.constants import (
    DT_TOTAL, DT_NEW,
    DT_NEW_MALE, DT_NEW_FEMALE,
    DT_TOTAL_FEMALE, DT_TOTAL_MALE,
    DT_TESTS_TOTAL,
    DT_SOURCE_OVERSEAS, DT_SOURCE_CRUISE_SHIP,
    DT_SOURCE_INTERSTATE, DT_SOURCE_UNDER_INVESTIGATION,
    DT_SOURCE_CONFIRMED, DT_SOURCE_COMMUNITY,
    DT_STATUS_RECOVERED, DT_STATUS_HOSPITALIZED,
    DT_STATUS_DEATHS
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.state_news_releases.act.act_powerbi import (
    get_powerbi_data
)
from covid_19_au_grab.word_to_number import (
    word_to_number
)


class ACTNews(StateNewsBase):
    STATE_NAME = 'act'
    SOURCE_ISO_3166_2 = 'AU-ACT'
    SOURCE_ID = 'au_act'
    SOURCE_URL = 'https://www.covid19.act.gov.au'
    SOURCE_DESCRIPTION = ''

    LISTING_URL = (
        # There's only 2 pages for now, so will hardcode
        # MUST BE UPDATED!!! ===========================================================================================
        'https://www.covid19.act.gov.au/updates',  # 7 April the COVID-19 update is tagged "case updates" but isn't in the topics listing..
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

    def get_data(self):
        r = get_powerbi_data()
        r.extend(StateNewsBase.get_data(self))
        return r

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, href, html):
        # TODO: UPDATE ME and make me work with confirmed case info!!! ====================================
        c_html = word_to_number(html) \
            .replace('<b>', '<strong>') \
            .replace('</b>', '</strong>')

        return self._extract_number_using_regex(
            (
                compile(r'total to\s?(?:<strong>)?\s?([0-9,]+)'),
                compile(r'total is(?: now| still)?\s?(?:<strong>)?\s?([0-9,]+)'),
                # the "-" negative lookbehind is to prevent "COVID-19" matching
                compile(r'confirmed cases\s?[^0-9.,]+(?:<strong>)?\s?(?<!-)([0-9,]+)'),
                compile(r'total remains at\s?(?:<strong>)?\s?([0-9,]+)')
            ),
            c_html,
            datatype=DT_TOTAL,
            source_url=href,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases_tested(self, href, html):
        # TODO: UPDATE ME and make me work with confirmed case info!!! ====================================
        c_html = word_to_number(html) \
            .replace('<b>', '<strong>') \
            .replace('</b>', '</strong>')

        du = self._get_date(href, html)
        neg_cases = self._extract_number_using_regex(
            (
                compile(
                    r'number of negative tests in the ACT '
                    r'is now\s?(?:<strong>)?\s?(?:more than )?([0-9,]+)'
                ),
                compile(r'There have been\s?(?:<strong>)?\s?([0-9,]+)\s?(?:</strong>)?\s?negative'),
                compile(r'<p>Number of negative tests</p></td><td><p>(?:<strong>)?([0-9,]+)'),
                compile(r'tested negative is now\s?(?:<strong>)?\s?([0-9,]+)')
            ),
            c_html,
            datatype=DT_TESTS_TOTAL,
            source_url=href,
            date_updated=du
        )
        pos_cases = self._get_total_cases(href, html)

        if neg_cases is not None and pos_cases is not None:
            # TODO: ADD negative/positive tests as separate values? =======================================================
            return DataPoint(
                datatype=neg_cases.datatype,
                value=neg_cases.value + pos_cases.value,
                date_updated=du,
                source_url=neg_cases.source_url,
                text_match=(
                    neg_cases.text_match,
                    pos_cases.text_match
                )
            )
        return None

    def _get_total_new_cases(self, href, html):
        c_html = word_to_number(html) \
            .replace('<b>', '<strong>') \
            .replace('</b>', '</strong>')

        return self._extract_number_using_regex(
            compile(
                r'([0-9,]+)\s?(?:</strong>)?\)?\s?new (?:confirmed|cases?)'
            ),
            c_html,
            datatype=DT_NEW,
            date_updated=self._get_date(href, html),
            source_url=href
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
        )
        if not table:
            return  # WARNING!!! =======================================================================================

        du = self._get_date(href, html)
        table = table[0]
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
                datatype=DT_TOTAL,
                agerange=k,
                value=v,
                date_updated=du,
                source_url=href
            ))
        return r

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, href, html):
        c_html = word_to_number(html) \
            .replace('<b>', '<strong>') \
            .replace('</b>', '</strong>')

        # WARNING: Can have multiple entries per article =============================================================
        # (early reports, anyway)
        # 'a male in his ([0-9]+)\'?s'
        # 'a female in her ([0-9]+)\'?s'
        # e.g. https://www.covid19.act.gov.au/news-articles/fifth-and-sixth-cases-of-covid-19-confirmed-in-act

        c_html = '\n'.join([
            i for i in c_html.split('.')
            if 'new case' in i
        ])
        du = self._get_date(href, html)

        r = []
        male = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)?\s?(?:</strong>)?\s?[^0-9.]*?(?<!fe)male(?:s)?'),
            c_html,
            source_url=href,
            datatype=DT_NEW_MALE,
            date_updated=du
        )
        if male:
            r.append(male)

        female = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)?\s?(?:</strong>)?\s?[^0-9.]*?female(?:s)?'),
            c_html,
            datatype=DT_NEW_FEMALE,
            source_url=href,
            date_updated=du
        )
        if female:
            r.append(female)
        return r

    #@singledaystat
    def _get_total_male_female_breakdown(self, href, html):
        # https://www.covid19.act.gov.au/updates/confirmed-case-information
        # Only at stats by region_child URL!!!
        # Well, they had it for one day at the reports, but..)

        # ADDITION: This looks to only support the reports(?)
        # should the stats by region_child URL be supported(!?) ============================================================

        c_html = word_to_number(html)
        du = self._get_date(href, html)

        male = self._extract_number_using_regex(
            compile(
                '<p[^>]*><strong>By sex</strong></p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Male</p></td><td[^>]*><p[^>]*>([0-9,]+)</p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Female</p></td><td[^>]*><p[^>]*>(?:[0-9,]+)</p>',
                IGNORECASE
            ),
            c_html,
            datatype=DT_TOTAL_FEMALE,
            source_url=href,
            date_updated=du
        )
        female = self._extract_number_using_regex(
            compile(
                '<p[^>]*><strong[^>]*>By sex</strong></p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Male</p></td><td[^>]*><p[^>]*>(?:[0-9,]+)</p></td></tr>'
                '<tr[^>]*><td[^>]*><p[^>]*>Female</p></td><td[^>]*><p[^>]*>([0-9,]+)</p>',
                IGNORECASE
            ),
            c_html,
            datatype=DT_TOTAL_MALE,
            source_url=href,
            date_updated=du
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

        # Normalise it with other states
        act_norm_map = {
            'Overseas acquired': DT_SOURCE_OVERSEAS,
            'Cruise ship acquired': DT_SOURCE_CRUISE_SHIP,
            'Interstate acquired': DT_SOURCE_INTERSTATE,
            'Contact of a confirmed ACT case': DT_SOURCE_CONFIRMED,
            'Unknown or local transmission': DT_SOURCE_COMMUNITY,
            'Under investigation': DT_SOURCE_UNDER_INVESTIGATION,
        }
        du = self._get_date(url, html)

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
                        datatype=act_norm_map[k.replace('_', ' ')],
                        value=int(v.replace(',', '')),
                        date_updated=du,
                        source_url=url
                    ))

        return r or None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        # recovered/lives lost also at
        # https://www.covid19.act.gov.au/updates/confirmed-case-information  ===========================================

        c_html = word_to_number(html) \
            .replace('<b>', '<strong>') \
            .replace('</b>', '</strong>')
        du = self._get_date(href, html)
        
        patients = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)?\s?(?:</strong>)?\s?COVID-19 patients'),
            c_html,
            datatype=DT_STATUS_HOSPITALIZED,
            source_url=href,
            date_updated=du
        )
        recovered = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)?\s?(?:</strong>)?\s?cases have(?: now)? recovered'),
            c_html,
            datatype=DT_STATUS_RECOVERED,
            source_url=href,
            date_updated=du
        )
        deaths = self._extract_number_using_regex(
            compile(r'([0-9,]+)\)?\s?(?:</strong>)?\s?deaths\.'),
            c_html,
            datatype=DT_STATUS_DEATHS,
            source_url=href,
            date_updated=du
        )

        r = []
        if patients:
            r.append(patients)
        if recovered:
            r.append(recovered)
        if deaths:
            r.append(deaths)
        return r or None


if __name__ == '__main__':
    from pprint import pprint
    an = ACTNews()
    pprint(an.get_data())
