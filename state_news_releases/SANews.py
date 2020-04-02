from re import compile
from pyquery import PyQuery as pq

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, bothlistingandstat, singledaystat
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES, DT_CASES_TESTED, \
    DT_DEATHS, DT_ICU, DT_SOURCE_OF_INFECTION, \
    DT_AGE, DT_AGE_MALE, DT_AGE_FEMALE
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint


class SANews(StateNewsBase):
    STATE_NAME = 'sa'
    LISTING_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/'  \
                  'SA+Health+Internet/About+us/News+and+media/all+media+releases/'
    LISTING_HREF_SELECTOR = '.news a'
    # SA actually has two URLS - the below and 'https://www.sa.gov.au/covid-19/
    #                                          latest-updates/daily-update/current' - SHOULD SUPPORT BOTH!!
    STATS_BY_REGION_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/' \
                          'sa+health+internet/health+topics/health+topics+a+-+z/covid+2019/' \
                          'latest+updates/' \
                          'confirmed+and+suspected+cases+of+covid-19+in+south+australia'

    def _get_date(self, href, html):
        if href == self.STATS_BY_REGION_URL:
            # Latest statistics – as of 4pm, 1 April 2020
            date = pq(html)(':contains("Latest statistics")').text().split(',')[-1].strip()
        else:
            date = pq(pq(html)('div.middle-column div.wysiwyg p')[0]) \
                               .text().strip().split(', ')[-1]

        try:
            # e.g. Monday, 30 March 2020
            return self._extract_date_using_format(date)
        except:
            # e.g. Sunday 22 March 2020
            return self._extract_date_using_format(date.partition(' ')[-1])

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        pass

    @bothlistingandstat
    def _get_total_cases(self, href, html):
        if href == self.STATS_BY_REGION_URL:
            tr = pq(html)('tr:contains("Confirmed cases")')[0]
            cc = int(pq(tr[1]).text().strip())
            if cc is not None:
                return DataPoint(
                    name='Confirmed cases',
                    datatype=DT_CASES,
                    value=cc,
                    date_updated=self._get_date(href, html),
                    source_url=href,
                    text_match=None
                )
            return None
        else:
            return None  # TODO!!! ===================================================================================

    def _get_total_cases_tested(self, href, html):
        # This is only a rough value - is currently displayed as "> (value)"!
        return self._extract_number_using_regex(
            compile(r'(?:undertaken (?:almost|more than) )?([0-9,]+)(?: COVID-19)? tests'),
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

    @singledaystat
    def _get_total_age_breakdown(self, href, html):
        """
        Age Group	Female	Male	Total
        0-9	0	3	3
        10-19	6	4	10
        20-29	31	30	61
        30-39	25	20	45
        40-49	16	21	37
        50-59	40	37	77
        60-69	34	48	82
        70-79	22	24	46
        80-89	2	4	6
        90-100	0	0	0
        >100	0	0	0
        Grand Total	176	191	367
        """

        r = []
        print("URL:", href)
        print(html)
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
            '90-100',
            '>100'
        ):
            tds = pq(table)('tr:contains("%s")' % age_group)
            if not tds:
                continue

            tds = tds[0]
            if len(tds) < 4:
                # Earliest didn't have male/female breakdown
                male = None
                female = None
                total = int(pq(tds[1]).text())
            else:
                female = int(pq(tds[1]).text())
                male = int(pq(tds[2]).text())
                total = int(pq(tds[3]).text())

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

    @singledaystat
    def _get_total_male_female_breakdown(self, url, html):
        # We need the "Grand Total
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

    @singledaystat
    def _get_total_source_of_infection(self, url, html):
        """
        Source 	Cases
        Overseas acquired 252
        Locally acquired (close contact of a confirmed case) 78
        Locally acquired (Interstate travel) 7
        Locally acquired (contact not identified) 3
        Under investigation 27
        TOTAL 367
        """
        r = []

        for k in (
            'Overseas acquired',
            'Locally acquired (close contact of a confirmed case)',
            'Locally acquired (Interstate travel)',
            'Locally acquired (contact not identified)',
            'Under investigation'
        ):
            tr = pq(html)('tr:contains("%s")' % k)
            if not tr:
                continue

            tr = tr[0]
            c_icu = int(pq(tr[1]).text().strip())

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

    @singledaystat
    def _get_total_dhr(self, href, html):
        r = []
        print(href)
        tr = pq(html)('tr:contains("Cases in ICU")')[0]
        c_icu = int(pq(tr[1]).text().strip())
        print(c_icu)

        if c_icu is not None:
            r.append(DataPoint(
                name=None,
                datatype=DT_ICU,
                value=c_icu,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match=None
            ))

        tr = pq(html)('tr:contains("Total deaths reported")')[0]
        t_d = int(pq(tr[1]).text().strip())
        if t_d is not None:
            r.append(DataPoint(
                name=None,
                datatype=DT_DEATHS,
                value=t_d,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match=None
            ))
        return r


if __name__ == '__main__':
    from pprint import pprint
    sn = SANews()
    pprint(sn.get_data())
