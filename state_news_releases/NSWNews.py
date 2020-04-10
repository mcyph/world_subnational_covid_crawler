from pyquery import PyQuery as pq
from re import compile, MULTILINE, DOTALL, IGNORECASE

from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, singledaystat, ALWAYS_DOWNLOAD_LISTING
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_NEW_CASES, DT_CASES, \
    DT_AGE, DT_AGE_MALE, DT_AGE_FEMALE, \
    DT_PATIENT_STATUS, \
    DT_SOURCE_OF_INFECTION, DT_CASES_BY_REGION, DT_CASES_BY_LHA
from covid_19_au_grab.word_to_number import word_to_number
from covid_19_au_grab.URLArchiver import URLArchiver


class NSWNews(StateNewsBase):
    STATE_NAME = 'nsw'
    #LISTING_URL = 'https://www.health.nsw.gov.au/news/Pages/default.aspx'
    LISTING_URL = 'https://www.health.nsw.gov.au/news/pages/2020-nsw-health.aspx'
    LISTING_HREF_SELECTOR = '.dfwp-item a'
    STATS_BY_REGION_URL = 'https://www.health.nsw.gov.au/Infectious/' \
                          'diseases/Pages/covid-19-latest.aspx'

    NSW_LHD_STATS_URL = 'https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-lhd.aspx'
    NSW_LGA_STATS_URL = 'https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-lga.aspx'

    def _get_date(self, href, html):
        try:
            return self._extract_date_using_format(
                pq(pq(html)('.newsdate')[0]).text().strip()
            )
        except:
            return self._extract_date_using_format(
                ' '.join(
                    pq(pq(html)('.lastupdated')[0])
                               .text()
                               .split(':')[-1]
                               .strip()
                               .split()[1:]
                )
            )

    def get_data(self):
        r = []

        for typ, url in (
            ('lhd', self.NSW_LHD_STATS_URL),
            ('lga', self.NSW_LGA_STATS_URL)
        ):
            ua = URLArchiver(f'{self.STATE_NAME}/{typ}')
            ua.get_url_data(
                url,
                cache=False if ALWAYS_DOWNLOAD_LISTING else True
            )

            for period in ua.iter_periods():
                for subperiod_id, subdir in ua.iter_paths_for_period(period):
                    path = ua.get_path(subdir)

                    with open(path, 'r',
                              encoding='utf-8',
                              errors='ignore') as f:
                        html = f.read()

                    cbr = self._get_total_cases_by_region(url, html)
                    if cbr:
                        r.extend(cbr)

        r.extend(StateNewsBase.get_data(self))
        return r

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile('([0-9,]+) additional cases of COVID-19'),
                compile(
                    'additional[^0-9.<]+(?:COVID-19[^0-9.<]+)?'
                    '(?:<strong>)?([0-9,]+)[^0-9.<]*(?:</strong>)?'
                    '[^0-9.<]+cases',
                    IGNORECASE
                )
            ),
            c_html.replace('\n', ' '),
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases(self, href, html):
        tr = self._pq_contains(
            html, 'tr', 'Confirmed cases',
            ignore_case=True
        )
        if not tr:
            return None
        tr = tr[0]

        return DataPoint(
            name=None,
            datatype=DT_CASES,
            value=int(pq(tr[1]).html().split('<')[0]
                                      .strip()
                                      .replace(',', '')
                                      .replace('*', '')),
            date_updated=self._get_date(href, html),
            source_url=href,
            text_match=None
        )

    def _get_total_cases_tested(self, href, html):
        return self._extract_number_using_regex(
            (
                compile(
                    # Total (including tested and excluded)
                    r'<td[^>]*?>(?:<[^</>]+>)?'
                        r'Total[^0-9<]+persons[^0-9<]+tested[^0-9<]*'
                        r'(?:</[^<>]+>)?</td>'
                    r'[^<]*?<td[^>]*>.*?([0-9,]+).*?</td>',
                    MULTILINE | DOTALL | IGNORECASE
                ),
                compile(
                    # Total (including tested and excluded)
                    r'<td[^>]*?>(?:<[^</>]+>)?Total(?:</[^<>]+>)?</td>'
                    r'[^<]*?<td[^>]*>.*?([0-9,]+).*?</td>',
                    MULTILINE | DOTALL
                )
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
        # TODO: TRANSITION TO https://data.nsw.gov.au/nsw-covid-19-data !! =============================================

        if '20200316_02.aspx' in href:
            # HACK: The very first entry was in a different format with percentages
            #  Maybe I could fix this later, but not sure it's worth it
            return None

        r = []
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
            '90-100'
        ):
            tds = self._pq_contains(table, 'tr', age_group)
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

    @singledaystat
    def _get_total_cases_by_region(self, href, html):
        """
        # TODO: TRANSITION TO https://data.nsw.gov.au/nsw-covid-19-data !! =============================================
        """
        # Why on earth are there zero width spaces!?
        html = html.replace(chr(8203), '')

        c_html = '<table class="moh-rteTable-6"' + \
                 html.partition(' class="moh-rteTable-6"')[-1]

        r = []
        if href == self.NSW_LGA_STATS_URL:
            # Get LGA stats only at the LGA url
            table = self._pq_contains(c_html, 'table', 'Local Government Area',
                                      ignore_case=True)
            datatype = DT_CASES_BY_REGION
        else:
            table = (
                self._pq_contains(c_html, 'table', '<span>LHD</span>',
                                  ignore_case=True) or
                # Earliest stats used a different classifier for region!!!
                # Might need to use a different graph..
                #self._pq_contains(c_html, 'table', 'Local Government Area',
                #                  ignore_case=True) or
                self._pq_contains(c_html, 'table', 'Local health district',
                                  ignore_case=True) or
                self._pq_contains(c_html, 'table', 'LHD',
                                  ignore_case=True) or
                # omg..why are there zero-width spaces??
                self._pq_contains(c_html, 'table', 'LH​D​',
                                  ignore_case=True)
            )
            datatype = DT_CASES_BY_LHA

        trs = pq(table)(
            'tr.moh-rteTableEvenRow-6, '
              'tr.moh-rteTableOddRow-6',
        )

        for tr in trs:
            lhd = pq(tr[0]).text().strip()

            if not tr or not lhd or 'total' in lhd.lower().split():
                print("NOT TR:", pq(tr).html())
                continue
            print("FOUND TR:", lhd)

            c_icu = pq(tr[1]).text().replace(',', '').strip()
            c_icu = int(c_icu) if c_icu not in ('1-4', '1-') else 4     # WARNING: Currently the backend doesn't support ranges!!! ====================================

            r.append(DataPoint(
                name=lhd,
                datatype=datatype,
                value=c_icu,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match=None
            ))
        return r or None

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    def _get_total_source_of_infection(self, url, html):
        # TODO: TRANSITION TO https://data.nsw.gov.au/nsw-covid-19-data !! =============================================

        r = []

        c_html = html.replace('  ', ' ').replace('\u200b', '')  # HACK!
        c_html = self._pq_contains(c_html, 'table', 'Source')

        old_type_map = {
            # NOTE: The descriptions stopped being used 21/3
            'Epi link (contact of confirmed case)':
                'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Unknown': 'Locally acquired – contact not identified',

            # These were used only 24/1
            'Locally acquired - contact of a confirmed case':
                'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Local acquired – contact not identified':
                'Locally acquired – contact not identified'
        }

        for k in (
            'Overseas acquired',
            'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Locally acquired – contact not identified',
            'Under investigation',

            'Epi link (contact of confirmed case)',
            'Unknown',

            # Misspelt on 24/1
            'Locally acquired - contact of a confirmed case',
            'Local acquired – contact not identified',
        ):
            # TODO: MAKE WORD WITH ALL THE CASES!!
            # not sure why this doesn't always work! ==================================================================
            tr = self._pq_contains(c_html, 'tr', k)
            if not tr:
                continue

            tr = tr[0]
            c_icu = int(pq(tr[1]).text().replace(',', '').strip())

            r.append(DataPoint(
                name=old_type_map.get(k, k),
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

        hospitalized = self._extract_number_using_regex(
            compile(
                r'([0-9,]+)[^0-9<.]*(?:</strong>)?[^0-9<.]*COVID-19[^0-9<.]+'
                r'cases[^0-9<.]+being[^0-9<.]+treated[^0-9<.]+NSW',
                IGNORECASE
            ),
            c_html,
            name='Hospitalized',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
            date_updated=self._get_date(href, html)
        )
        if hospitalized:
            r.append(hospitalized)

        icu = self._extract_number_using_regex(
            compile(
                r'([0-9,]+)[^0-9<.]*(?:</strong>)?[^0-9<.]*'
                r'(?:COVID-19[^0-9<.]+)?cases?[^0-9<.]+'
                r'Intensive[^0-9<.]+Care[^0-9<.]+Units?',
                IGNORECASE
            ),
            c_html,
            name='ICU',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
            date_updated=self._get_date(href, html)
        )
        if icu:
            r.append(icu)

        ventilators = self._extract_number_using_regex(
            compile(
                r'([0-9,]+)[^0-9<.]*(?:</strong>)?[^0-9<.]*'
                r'require[^0-9<.]+ventilators',
                IGNORECASE
            ),
            c_html,
            name='ICU needing ventilators',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
            date_updated=self._get_date(href, html)
        )
        if ventilators:
            r.append(ventilators)

        deaths = self._extract_number_using_regex(
            (
                # Prefer from the table if possible, as that's
                # more guaranteed to not give false positives
                compile(r'Deaths[^0-9<]+in[^0-9<]+NSW[^0-9<]+from[^0-9<]+'
                        r'confirmed[^0-9<]+cases[^0-9<]*</td>[^0-9>]*<td[^>]*>([0-9,]+)',
                        MULTILINE | DOTALL | IGNORECASE),
                compile(r'([0-9,]+)[^0-9<]+death[^0-9<]+in[^0-9<]+NSW',
                        IGNORECASE),
                compile(r'have been ([0-9,]+) deaths?',
                        IGNORECASE),
                compile(r'total[^0-9<]+deaths[^0-9<]+'
                        r'COVID-19[^0-9<]+cases[^0-9<]+(?:<strong>)?([0-9,]+)',
                        IGNORECASE),
                compile(r'total[^0-9<]+deaths[^0-9<]+(?:<strong>)?([0-9]+)',
                        IGNORECASE),
                compile(r'([0-9,]+)[^0-9<]+deaths[^0-9<]+in[^0-9<]+NSW',
                        IGNORECASE),
            ),
            c_html,
            name='Deaths',
            source_url=href,
            datatype=DT_PATIENT_STATUS,
            date_updated=self._get_date(href, html)
        )
        if deaths:
            r.append(deaths)
        return r


if __name__ == '__main__':
    from pprint import pprint
    nn = NSWNews()
    pprint(nn.get_data())
