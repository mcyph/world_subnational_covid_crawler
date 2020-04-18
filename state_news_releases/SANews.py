import json
from os import listdir
from os.path import expanduser
from re import compile
from pyquery import PyQuery as pq

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, bothlistingandstat, singledaystat
from covid_19_au_grab.state_news_releases import constants
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES, DT_NEW_CASES, DT_CASES_TESTED, \
    DT_PATIENT_STATUS, DT_SOURCE_OF_INFECTION, \
    DT_AGE, DT_AGE_MALE, DT_AGE_FEMALE
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.word_to_number import word_to_number


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
        print("HREF:", href)

        if href == self.STATS_BY_REGION_URL:
            # Latest statistics – as of 4pm, 1 April 2020
            date = self._pq_contains(html, 'h2,h1,h3', 'Latest statistics',
                                     ignore_case=True).text().split(',')[-1].strip()
        else:
            try:
                # Fix for date at
                # http://emergencydepartments.sa.gov.au/wps/wcm/connect/public+content/
                # sa+health+internet/about+us/news+and+media/all+media+releases/
                # covid-19+update+17+april+2020
                return self._extract_date_using_format(
                    pq(html)('div.wysiwyg h1').text().split('Update')[-1].strip()
                )
            except (ValueError, IndexError):
                date = pq(pq(html)('div.middle-column div.wysiwyg p')[0]) \
                                   .text().strip().split(',')[-1].strip()

        try:
            # e.g. Monday, 30 March 2020
            return self._extract_date_using_format(date)
        except:
            # e.g. Sunday 22 March 2020
            return self._extract_date_using_format(date.partition(' ')[-1])

    def get_data(self):
        OUTPUT_DIR = expanduser('~/dev/covid_19_au_grab/sa_pdf_extract/output')

        r = []
        for fnam in listdir(OUTPUT_DIR):
            date = fnam.split('.')[0]

            with open(f'{OUTPUT_DIR}/{fnam}', 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for region, datatype, value in data:
                r.append(DataPoint(
                    name=region,
                    datatype=getattr(constants, datatype),
                    value=value,
                    date_updated=date,
                    source_url='https://www.sahealth.sa.gov.au/wps/wcm/connect/'
                               'public+content/sa+health+internet/health+topics/'
                               'health+topics+a+-+z/covid+2019/latest+updates/'
                               'confirmed+and+suspected+cases+of+covid-19+in+south+australia',
                    text_match=None,
                ))

        r.extend(StateNewsBase.get_data(self))
        return r

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        # FIXME!!!! ==================================================================================================
        'Eighteen people in South Australia have today tested positive'
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile('([0-9,]+) (?:people|person)[^0-9<.]+?(?:have|has)(?: today)? tested positive'),
                compile('([0-9,]+) new (?:people have|person has)(?: today)? tested positive'),
                compile('([0-9,]+) new cases of COVID-19'),
            ),
            c_html,
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        )

    @bothlistingandstat
    def _get_total_cases(self, href, html):
        if href == self.STATS_BY_REGION_URL:
            tr = self._pq_contains(html, 'tr', 'Confirmed cases',
                                   ignore_case=True)[0]
            cc = int(pq(tr[1]).text().strip())
            if cc is not None:
                return DataPoint(
                    name=None,
                    datatype=DT_CASES,
                    value=cc,
                    date_updated=self._get_date(href, html),
                    source_url=href,
                    text_match=None
                )
            return None
        else:
            # 'There have now been a total of 385 confirmed cases in South Australia'
            c_html = word_to_number(html)

            return self._extract_number_using_regex(
                compile('total of ([0-9,]+) confirmed'),
                c_html,
                source_url=href,
                datatype=DT_CASES,
                date_updated=self._get_date(href, html)
            )

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
        #print(html)
        table = self._pq_contains(
            html, 'table', 'Age Group',
            ignore_case=True
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
            tds = self._pq_contains(table, 'tr', age_group)
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

        # Normalise it with other states
        sa_norm_map = {
            'Overseas acquired':
                'Overseas acquired',
            'Locally acquired (Interstate travel)':
                'Interstate acquired',
            'Locally acquired (close contact of a confirmed case)':
                'Locally acquired - contact of a confirmed case',
            'Locally acquired (contact not identified)':
                'Locally acquired - contact not identified',
            'Under investigation':
                'Under investigation'
        }

        for k in (
            'Overseas acquired',
            'Locally acquired (close contact of a confirmed case)',
            'Locally acquired (Interstate travel)',
            'Locally acquired (contact not identified)',
            'Under investigation'
        ):
            tr = self._pq_contains(html, 'tr', k,
                                   ignore_case=True)
            if not tr:
                continue

            tr = tr[0]
            c_icu = int(pq(tr[1]).text().strip())

            r.append(DataPoint(
                name=sa_norm_map[k],
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
        # TODO: Also support updates!
        # e.g. https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/about+us/news+and+media/all+media+releases/covid-19+update+15+april+2020

        r = []
        print(href)
        tr = self._pq_contains(html, 'tr', 'Cases in ICU',
                               ignore_case=True)[0]
        c_icu = int(pq(tr[1]).text().strip())
        print(c_icu)

        if c_icu is not None:
            r.append(DataPoint(
                name='ICU',
                datatype=DT_PATIENT_STATUS,
                value=c_icu,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match=None
            ))

        tr = self._pq_contains(html, 'tr', 'Total deaths reported',
                               ignore_case=True)[0]
        t_d = int(pq(tr[1]).text().strip())
        if t_d is not None:
            r.append(DataPoint(
                name='Deaths',
                datatype=DT_PATIENT_STATUS,
                value=t_d,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match=None
            ))

        tr = self._pq_contains(html, 'tr', 'Cases cleared of COVID-19',
                               ignore_case=True)
        if tr:
            tr = tr[0]
            t_d = int(pq(tr[1]).text().strip())

            if t_d is not None:
                r.append(DataPoint(
                    name='Recovered',
                    datatype=DT_PATIENT_STATUS,
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
