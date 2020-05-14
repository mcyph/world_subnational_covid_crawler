import csv
from json import loads
from datetime import datetime
from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_19_au_grab.state_news_releases.StateNewsBase import (
    StateNewsBase, singledaystat
)
from covid_19_au_grab.state_news_releases.constants import (
    SCHEMA_LGA, SCHEMA_THS,
    DT_TOTAL, DT_NEW, DT_TESTS_TOTAL,
    DT_TOTAL_FEMALE, DT_TOTAL_MALE,
    DT_STATUS_ACTIVE, DT_STATUS_RECOVERED, DT_STATUS_DEATHS,
    DT_STATUS_ICU, DT_STATUS_HOSPITALIZED
)
from covid_19_au_grab.state_news_releases.DataPoint import (
    DataPoint
)
from covid_19_au_grab.word_to_number import (
    word_to_number
)
from covid_19_au_grab.get_package_dir import (
    get_package_dir
)

TAS_BY_LGA = get_package_dir() / 'state_news_releases' / 'tas' / 'tas_by_lga.json'
TAS_BY_THS = get_package_dir() / 'state_news_releases' / 'tas' / 'tas_by_ths.tsv'


class TasNews(StateNewsBase):
    STATE_NAME = 'tas'
    LISTING_URL = (
        'https://www.dhhs.tas.gov.au/news/2020',
        'https://www.coronavirus.tas.gov.au/',
        'https://coronavirus.tas.gov.au/media-releases',
        'https://coronavirus.tas.gov.au/media-releases?result_85500_result_page=2',
        'https://coronavirus.tas.gov.au/media-releases?result_85500_result_page=3',
        'https://coronavirus.tas.gov.au/media-releases?result_85500_result_page=4',
    )
    LISTING_HREF_SELECTOR = 'table.dhhs a, ' \
                            '#pills-Media_Releases .card-rows .card a'
    STATS_BY_REGION_URL = 'https://coronavirus.tas.gov.au/facts/' \
                          'cases-and-testing-updates'

    def get_data(self):
        r = []

        # Add manually entered data by THS and LGA
        with open(TAS_BY_LGA, 'r', encoding='utf-8') as f:
            for date, date_dict in loads(f.read()).items():
                for _, region, total in date_dict['data']:
                    r.append(DataPoint(
                        schema=SCHEMA_LGA,
                        datatype=DT_TOTAL,
                        region=region,
                        value=total,
                        date_updated=date,
                        source_url=date_dict['source_url']
                    ))

        with open(TAS_BY_THS, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')

            for date_dict in reader:
                dd, mm, yyyy = date_dict['Date'].split('/')
                dt = datetime(day=int(dd), month=int(mm), year=int(yyyy)).strftime('%Y_%m_%d')

                for region in (
                    'North-West', 'North', 'South',
                ):
                    r.append(DataPoint(
                        schema=SCHEMA_THS,
                        datatype=DT_STATUS_ACTIVE,
                        region=region,
                        value=date_dict[f'{region} Active'],
                        date_updated=dt,
                        source_url='Peter Gutweins Facebook Page'
                    ))
                    r.append(DataPoint(
                        schema=SCHEMA_THS,
                        datatype=DT_STATUS_RECOVERED,
                        region=region,
                        value=int(date_dict[f'{region} Recovered']),
                        date_updated=dt,
                        source_url='Peter Gutweins Facebook Page'
                    ))
                    r.append(DataPoint(
                        schema=SCHEMA_THS,
                        datatype=DT_TOTAL,
                        region=region,
                        value=int(date_dict[f'{region} Active'])+
                              int(date_dict[f'{region} Recovered']),
                        date_updated=dt,
                        source_url='Peter Gutweins Facebook Page'
                    ))

        r.extend(StateNewsBase.get_data(self))
        return r

    def _get_date(self, url, html):
        # Format 12 March 2020
        # but sometimes it's an h2 or h3, it's
        # probably entered manually each time
        print(url)

        try:
            # cases and testing updates page
            date = pq(pq(html)('.page-content h4')[0]).text().split(',')[-1].strip()
            return self._extract_date_using_format(date)
        except (ValueError, IndexError):
            pass

        for selector in (
            '#main-banner h2',
            '#main-content div h2:first-child',
            '#main-content div h3:first-child',
            '#main-content div h4:first-child',
            '#main-content div:first-child p:first-child strong:first-child',
            '.page-content.col.order-xl-1.order-sm-2',
        ):
            try:
                date = pq(pq(html)(selector)[0]) \
                    .text() \
                    .strip() \
                    .split('\n')[0] \
                    .split('Update')[-1] \
                    .split('update')[-1] \
                    .strip()

                try:
                    try:
                        return self._extract_date_using_format(date)
                    except ValueError:
                        return self._extract_date_using_format(
                            date, format='%B %d, %Y'
                        )
                except ValueError:
                    return self._extract_date_using_format(
                        date, format='%d %b %Y'
                    )
            except (IndexError, ValueError):
                pass

        raise Exception("TAS Couldn't find date for URL:", url)

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, url, html):
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile(
                    'confirmed ([0-9,]+)[^0-9.]* cases? of coronavirus',
                    IGNORECASE
                ),
                compile(
                    '([0-9,]+) new cases of (?:coronavirus|COVID-19) confirmed',
                    IGNORECASE
                )
            ),
            c_html,
            datatype=DT_NEW,
            source_url=url,
            date_updated=self._get_date(url, html)
        )

    def _get_total_cases(self, url, html):
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile(
                    'tally to ([0-9,]+)'
                ),
                compile(
                    r"brings the State(?:’|&rsquo;|')s total to ([0-9,]+)",
                    IGNORECASE
                ),
                compile(
                    'total remains at ([0-9,]+)'
                )
            ),
            c_html,
            datatype=DT_TOTAL,
            source_url=url,
            date_updated=self._get_date(url, html)
        )

    def _get_total_cases_tested(self, url, html):
        c_html = word_to_number(html)

        r = self._extract_number_using_regex(
            (
                compile(
                    '([0-9,]+) (?:more )?(?:coronavirus )?(?:covid-19 )?'
                    'tests (?:have|had) been completed',  # [^0-9]*?complete
                    IGNORECASE
                ),
                compile(
                    'conducted ([0-9,]+) tests',
                    IGNORECASE
                ),
                #compile(
                #    '([0-9,]+)[^0-9<>]*? test',
                #    IGNORECASE
                #)
            ),
            c_html,
            source_url=url,
            datatype=DT_TESTS_TOTAL,
            date_updated=self._get_date(url, html)
        )
        return r

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

    # What about age breakdown??
    # e.g. Two of the cases are aged in their 70s. One is aged in
    # their 60s, one in their 50s, one in their 30s, and one is
    # in their 20s.

    def _get_new_male_female_breakdown(self, url, html):
        # 'Four of the cases are women; two are men'
        c_html = word_to_number(html)

        men = self._extract_number_using_regex(
            compile('([0-9,]+)[^0-9.,]* men', IGNORECASE),
            c_html,
            source_url=url,
            datatype=DT_TOTAL_MALE,
            date_updated=self._get_date(url, html)
        )
        women = self._extract_number_using_regex(
            compile('([0-9,]+)[^0-9.,]* women', IGNORECASE),
            c_html,
            source_url=url,
            datatype=DT_TOTAL_FEMALE,
            date_updated=self._get_date(url, html)
        )
        if men is not None or women is not None:
            r = []
            if men:
                r.append(men)
            if women:
                r.append(women)
            return r
        return None

    def _get_total_male_female_breakdown(self, url, html):
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, url, html):
        # Three of the cases are from Northern Tasmania, two are
        # from Southern Tasmania and one case is from the North West.
        pass

    def _get_total_cases_by_region(self, url, html):
        table = self._pq_contains(
            html, 'table', 'Local Government Area',
            ignore_case=True
        )

        r = []
        if table:
            for region, lga, num_cases in table[0][1]:
                r.append(DataPoint(
                    schema=SCHEMA_LGA,
                    region=pq(lga).text().strip(),
                    datatype=DT_TOTAL,
                    value=int(pq(num_cases).text().replace(',', '').strip()),
                    date_updated=self._get_date(url, html),
                    source_url=url
                ))
        return r

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        # Two of the cases have recently been on cruise ships.
        # One case is a close contact of a previously confirmed
        # case, and three have recently travelled to Tasmania
        # from overseas.
        pass

    def _get_total_source_of_infection(self, url, html):
        pass

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    @singledaystat
    def _get_total_dhr(self, href, html):
        r = []

        cases_map = {
            'New cases in past 24 hours': DT_NEW,
            'Total cases': DT_TOTAL,
            'Active': DT_STATUS_ACTIVE,
            'Recovered': DT_STATUS_RECOVERED,
            'Deaths': DT_STATUS_DEATHS,
        }

        cases_table = self._pq_contains(
            html, 'table', 'Cases in Tasmania',
            ignore_case=True
        )[0]

        for heading, value in cases_table[1]:
            heading = pq(heading).text().replace('*', '').strip().split('(')[0].strip()
            value = pq(value).text().replace('*', '').replace(',', '').strip()

            datatype = cases_map[heading]
            if datatype is None:
                continue

            r.append(DataPoint(
                datatype=datatype,
                value=int(value),
                date_updated=self._get_date(href, html),
                source_url=href
            ))

        tests_table = self._pq_contains(
            html, 'tr', 'Total laboratory tests',
            ignore_case=True
        )[0]

        r.append(DataPoint(
            datatype=DT_TESTS_TOTAL,
            value=int(pq(tests_table[1]).text().replace('*', '').replace(',', '').strip()),
            date_updated=self._get_date(href, html),
            source_url=href
        ))

        c_html = word_to_number(html)
        icu = self._extract_number_using_regex(
            compile(r'includes ([0-9,]+) hospital inpatients', IGNORECASE),
            c_html,
            datatype=DT_STATUS_HOSPITALIZED,
            source_url=href,
            date_updated=self._get_date(href, html)
        )
        if icu:
            r.append(icu)

        hospitalized = self._extract_number_using_regex(
            compile(r'\(([0-9,]+) in ICU\)', IGNORECASE),
            c_html,
            datatype=DT_STATUS_ICU,
            source_url=href,
            date_updated=self._get_date(href, html)
        )
        if hospitalized:
            r.append(hospitalized)

        return r


if __name__ == '__main__':
    from pprint import pprint
    tn = TasNews()
    pprint(tn.get_data())

