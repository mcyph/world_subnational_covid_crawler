from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_crawlers.oceania.au_data.StateNewsBase import StateNewsBase, singledaystat, bothlistingandstat
from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DataPoint import DataPoint
from _utility.word_to_number import word_to_number
from _utility.get_package_dir import get_package_dir

TAS_BY_LGA = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'tas' / 'tas_by_lga.json'
TAS_BY_THS = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'tas' / 'tas_by_ths.tsv'


class TasNews(StateNewsBase):
    STATE_NAME = 'tas'

    SOURCE_ID = 'au_tas_press_releases'
    SOURCE_URL = 'https://coronavirus.tas.gov.au'
    SOURCE_DESCRIPTION = ''

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

    def _get_date(self, url, html):
        # Format 12 March 2020
        # but sometimes it's an h2 or h3, it's
        # probably entered manually each time
        #print(url)

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
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            datatype=DataTypes.NEW,
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
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            datatype=DataTypes.TOTAL,
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
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            source_url=url,
            datatype=DataTypes.TESTS_TOTAL,
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
        return [] # HACK!!

        # 'Four of the cases are women; two are men'
        c_html = word_to_number(html)
        du = self._get_date(url, html)

        men = self._extract_number_using_regex(
            compile('([0-9,]+)[^0-9.,]* men', IGNORECASE),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            source_url=url,
            datatype=DataTypes.TOTAL_MALE,
            date_updated=du
        )
        women = self._extract_number_using_regex(
            compile('([0-9,]+)[^0-9.,]* women', IGNORECASE),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            source_url=url,
            datatype=DataTypes.TOTAL_FEMALE,
            date_updated=du
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

    @bothlistingandstat
    def _get_total_cases_by_region(self, url, html):
        if url == self.STATS_BY_REGION_URL:
            tables = self._pq_contains(
                html, 'table', 'LGA Region',
                ignore_case=True
            ) or []
            du = self._get_date(url, html)

            r = []
            for table in tables:
                for lga, num_cases in table[1]:
                    lga = pq(lga).text().strip()

                    if lga.lower() == 'total':
                        # This value is very often out of date!!! ====================================================
                        if False:
                            r.append(DataPoint(
                                region_schema=Schemas.THS,
                                region_parent='au-tas',
                                region_child=pq(table[0][0][0]).text().strip().split(' - ')[-1].strip(),
                                datatype=DataTypes.TOTAL,
                                value=int(pq(num_cases).text().replace(',', '').strip()),
                                date_updated=du,
                                source_url=url
                            ))
                    else:
                        r.append(DataPoint(
                            region_schema=Schemas.LGA,
                            region_parent='au-tas',
                            region_child=lga,
                            datatype=DataTypes.TOTAL,
                            value=int(pq(num_cases).text().replace(',', '').strip()),
                            date_updated=du,
                            source_url=url
                        ))
            return r

        else:
            table = self._pq_contains(
                html, 'table', 'Local Government Area',
                ignore_case=True
            )
            du = self._get_date(url, html)

            r = []
            if table:
                for region_child, lga, num_cases in table[0][1]:
                    r.append(DataPoint(
                        region_schema=Schemas.LGA,
                        region_parent='au-tas',
                        region_child=pq(lga).text().strip(),
                        datatype=DataTypes.TOTAL,
                        value=int(pq(num_cases).text().replace(',', '').strip()),
                        date_updated=du,
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
            'New cases in past 24 hours': DataTypes.NEW,
            'Total cases': DataTypes.TOTAL,
            'Active': DataTypes.STATUS_ACTIVE,
            'Recovered': DataTypes.STATUS_RECOVERED,
            'Deaths': DataTypes.STATUS_DEATHS,
        }

        cases_table = self._pq_contains(html, 'table', 'Cases in Tasmania', ignore_case=True)[0]
        du = self._get_date(href, html)

        for heading, value in cases_table[1]:
            heading = pq(heading).text().replace('*', '').strip().split('(')[0].strip()
            value = pq(value).text().replace('*', '').replace(',', '').replace('.', '').strip()

            datatype = cases_map[heading]
            if datatype is None:
                continue

            r.append(DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-TAS',
                datatype=datatype,
                value=int(value),
                date_updated=du,
                source_url=href
            ))

        tests_table = self._pq_contains(
            html, 'tr', 'Total laboratory tests',
            ignore_case=True
        )[0]

        r.append(DataPoint(
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            datatype=DataTypes.TESTS_TOTAL,
            value=int(pq(tests_table[1]).text().replace('*', '').replace(',', '').replace('.', '').strip()),
            date_updated=du,
            source_url=href
        ))

        c_html = word_to_number(html)
        icu = self._extract_number_using_regex(
            compile(r'includes ([0-9,]+) hospital inpatients', IGNORECASE),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            datatype=DataTypes.STATUS_HOSPITALIZED,
            source_url=href,
            date_updated=du
        )
        if icu:
            r.append(icu)

        hospitalized = self._extract_number_using_regex(
            compile(r'\(([0-9,]+) in ICU\)', IGNORECASE),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-TAS',
            datatype=DataTypes.STATUS_ICU,
            source_url=href,
            date_updated=du
        )
        if hospitalized:
            r.append(hospitalized)

        return r


if __name__ == '__main__':
    from pprint import pprint
    tn = TasNews()
    pprint(tn.get_datapoints())
