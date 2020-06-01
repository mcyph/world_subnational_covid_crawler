from pyquery import PyQuery as pq
from re import compile, MULTILINE, DOTALL, IGNORECASE

from covid_19_au_grab.state_news_releases.StateNewsBase import (
    StateNewsBase, singledaystat, ALWAYS_DOWNLOAD_LISTING, bothlistingandstat
)
from covid_19_au_grab.state_news_releases.nsw.get_nsw_cases_data import (
    get_nsw_cases_data
)
from covid_19_au_grab.state_news_releases.nsw.get_nsw_tests_data import (
    get_nsw_tests_data
)
from covid_19_au_grab.state_news_releases.nsw.get_nsw_postcode_data import (
    get_nsw_postcode_data
)
from covid_19_au_grab.datatypes.constants import (
    SCHEMA_LGA, SCHEMA_LHD,
    DT_TOTAL, DT_TOTAL_FEMALE, DT_TOTAL_MALE,
    DT_NEW,
    DT_TESTS_TOTAL,
    DT_SOURCE_UNDER_INVESTIGATION, DT_SOURCE_COMMUNITY,
    DT_SOURCE_CONFIRMED, DT_SOURCE_INTERSTATE,
    DT_SOURCE_OVERSEAS,
    DT_STATUS_DEATHS, DT_STATUS_HOSPITALIZED, DT_STATUS_ICU,
    DT_STATUS_ICU_VENTILATORS,
    DT_STATUS_ACTIVE, DT_STATUS_RECOVERED
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.word_to_number import (
    word_to_number
)
from covid_19_au_grab.URLArchiver import (
    URLArchiver
)


class NSWNews(StateNewsBase):
    STATE_NAME = 'nsw'
    #LISTING_URL = 'https://www.health.nsw.gov.au/news/Pages/default.aspx'
    LISTING_URL = 'https://www.health.nsw.gov.au/news/pages/2020-nsw-health.aspx'
    LISTING_HREF_SELECTOR = '.dfwp-item a'

    #STATS_BY_REGION_URL = 'https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-latest.aspx'
    #NSW_LHD_STATS_URL = 'https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-lhd.aspx'
    #NSW_LGA_STATS_URL = 'https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-lga.aspx'

    # URLs changed around 23rd April
    STATS_BY_REGION_URL = 'https://www.health.nsw.gov.au/Infectious/covid-19/Pages/stats-nsw.aspx'
    #NSW_LHD_STATS_URL = 'https://www.health.nsw.gov.au/Infectious/covid-19/Pages/stats-lhd.aspx'
    NSW_LHD_STATS_URL = STATS_BY_REGION_URL # HACK: LHD stats have moved here as of 28/5
    NSW_LGA_STATS_URL = 'https://www.health.nsw.gov.au/Infectious/covid-19/Pages/stats-lga.aspx'

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
                    #print("NSW News:", typ, subperiod_id, subdir, url, path)

                    with open(path, 'r',
                              encoding='utf-8',
                              errors='ignore') as f:
                        html = f.read()

                    cbr = self._get_total_cases_by_region(url, html)
                    if cbr:
                        r.extend(cbr)

        r.extend(StateNewsBase.get_data(self))

        unique_keys = set()
        for datapoint in r:
            k = (
                datapoint.region_schema,
                datapoint.region_parent,
                datapoint.region_child,
                datapoint.agerange,
                datapoint.datatype,
                datapoint.date_updated
            )
            unique_keys.add(k)

        # Combine+make sure the postcode mappings to LGA are
        # consistent between the two datasets (regression check)
        postcode_to_lga_1, nsw_cases_data = get_nsw_cases_data()
        postcode_to_lga_2, nsw_tests_data = get_nsw_tests_data()
        r.extend(nsw_tests_data)

        for k, v in postcode_to_lga_1.items():
            assert postcode_to_lga_2.get(k, v) == v, v
        for k, v in postcode_to_lga_2.items():
            assert postcode_to_lga_1.get(k, v) == v, v
        postcode_to_lga_1.update(postcode_to_lga_2)

        for datapoint in get_nsw_postcode_data(postcode_to_lga_1)+nsw_cases_data:
            # Prefer website over csv data
            import datetime
            yyyy, mm, dd = datapoint.date_updated.split('_')
            date = datetime.datetime(year=int(yyyy),
                                     month=int(mm),
                                     day=int(dd))

            found = False
            for i_delta in (
                datetime.timedelta(days=-1),
                datetime.timedelta(days=0),
                datetime.timedelta(days=1),
            ):
                # Only add if haven't got data for some
                # time (as last resort) to reduce anomalies!
                k = (
                    datapoint.region_schema,
                    datapoint.region_parent,
                    datapoint.region_child,
                    datapoint.agerange,
                    datapoint.datatype,
                    (date+i_delta).strftime('%Y_%m_%d')
                )

                if k in unique_keys:
                    found = True
                    break

            if not found:
                r.append(datapoint)

        return r

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    @bothlistingandstat
    def _get_total_new_cases(self, href, html):
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile('([0-9,]+) additional cases? of COVID-19'),
                compile(
                    'additional[^0-9<>.]+(?:COVID-19[^0-9<>.]+)?'
                    '(?:<strong>)?([0-9,]+)[^0-9<>.]*(?:</strong>)?'
                    '[^0-9<>.]+cases?',
                    IGNORECASE
                )
            ),
            c_html.replace('\n', ' '),
            datatype=DT_NEW,
            source_url=href,
            date_updated=self._get_date(href, html)
        )
    
    @bothlistingandstat
    def _get_total_cases(self, href, html):
        total = self._extract_number_using_regex(
            compile('bringing the total to ([0-9,]+)'),
            html,
            datatype=DT_TOTAL,
            source_url=href
        )
        if total:
            return total

        tr = self._pq_contains(
            html, 'tr', 'Confirmed cases',
            ignore_case=True
        )
        if not tr:
            return None
        tr = tr[0]

        return DataPoint(
            datatype=DT_TOTAL,
            value=int(pq(tr[1]).html().split('<')[0]
                                      .strip()
                                      .replace(',', '')
                                      .replace('*', '')
                                      .replace('&#8203;', '')
                                      .replace('\u200b', '')),
            date_updated=self._get_date(href, html),
            source_url=href
        )

    @bothlistingandstat
    def _get_total_cases_tested(self, href, html):
        # TODO: Also support from https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-latest.aspx !!
        tests = self._extract_number_using_regex(
            compile(
                'More than ([0-9,]+) people have now been tested for COVID-19',
                IGNORECASE
            ),
            html,
            datatype=DT_TESTS_TOTAL,
            source_url=href
        )
        if tests:
            return tests

        table = self._pq_contains(
            html, 'table', 'Total persons tested',
            ignore_case=True
        ) or self._pq_contains(
            html, 'table', 'Total',
            ignore_case=True
        )
        if not table:
            return

        return self._extract_number_using_regex(
            (
                compile(
                    # Total (including tested and excluded)
                    r'<td[^>]*?>(?:<[^</>]+>)?'
                        r'Total[^0-9<>.]+persons[^0-9<>.]+tested[^0-9<>.]*'
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
            table.html(),
            datatype=DT_TESTS_TOTAL,
            source_url=href,
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
        du = self._get_date(href, html)

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
                (DT_TOTAL_FEMALE, female),
                (DT_TOTAL_MALE, male),
                (DT_TOTAL, total)
            ):
                if value is None:
                    continue
                r.append(DataPoint(
                    datatype=datatype,
                    agerange=age_group,
                    value=value,
                    date_updated=du,
                    source_url=href
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
        date = self._get_date(href, html)

        # Why on earth are there zero width spaces!?
        html = html.replace(chr(8203), '')

        #c_html = '<table class="moh-rteTable-6"' + \
        #         html.partition(' class="moh-rteTable-6"')[-1]

        r = []
        du = self._get_date(href, html)

        if href == self.NSW_LGA_STATS_URL:
            for datatype, text in (
                (DT_TOTAL, 'Confirmed cases'),
                (DT_SOURCE_COMMUNITY, 'Cases locally acquired - Contact not identified')
            ):
                # Get LGA stats only at the LGA url
                table = self._pq_contains(html, 'table', text,
                                          ignore_case=False)
                #print("LGA STATS:", table.text())
                #print(html)
                r.extend(self.__get_datapoints_from_table(
                    href, html, table,
                    region_schema=SCHEMA_LGA,
                    datatype=datatype,
                    du=du
                ))
            return r or None
        else:
            table = (
                self._pq_contains(html, 'table', '<span>LHD</span>',
                                  ignore_case=True) or
                # Earliest stats used a different classifier for region_child!!!
                # Might need to use a different graph..
                #self._pq_contains(c_html, 'table', 'Local Government Area',
                #                  ignore_case=True) or
                self._pq_contains(html, 'table', 'Local health district',
                                  ignore_case=True) or
                self._pq_contains(html, 'table', 'LHD',
                                  ignore_case=True)
            )
            return self.__get_datapoints_from_table(
                href, html, table,
                region_schema=SCHEMA_LHD,
                datatype=DT_TOTAL,
                du=du
            ) or None

    def __get_datapoints_from_table(self,
                                    href, html, table,
                                    region_schema, datatype, du):

        # TODO: Support testing data for LHA, etc!!! ============================================================================================================
        r = []
        trs = pq(table)(
            'tr.moh-rteTableEvenRow-6, '
              'tr.moh-rteTableOddRow-6',
        )

        for tr in trs:
            lhd = pq(tr[0]).text().strip().split('(')[0].strip()

            if not pq(tr) or not pq(lhd) or 'total' in lhd.lower().split():
                print("NOT TR:", pq(tr).html())
                continue
            print("FOUND TR:", lhd)

            c_icu = pq(tr[1]).text().replace(',', '').strip()

            if c_icu in ('1-4', '1-', '<5'):
                # WARNING: Currently the backend doesn't support ranges!!! ====================================
                if True:
                    # I think best not add for now, deferring to open data?
                    continue
                else:
                    c_icu = 0
            else:
                c_icu = int(c_icu)

            r.append(DataPoint(
                region_schema=region_schema,
                datatype=datatype,
                region_child=lhd,
                value=c_icu,
                date_updated=du,
                source_url=href
            ))
        return r

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    def _get_total_source_of_infection(self, url, html):
        # TODO: TRANSITION TO https://data.nsw.gov.au/nsw-covid-19-data !! =============================================

        r = []

        c_html = html.replace('  ', ' ').replace('&#8203;', '').replace('\u200b', '')  # HACK!
        c_html = self._pq_contains(c_html, 'table', 'Source')
        du = self._get_date(url, html)

        # Normalise it with other states
        nsw_norm_map = {
            'Overseas acquired': DT_SOURCE_OVERSEAS,
            'Locally acquired – contact of a confirmed case and/or in a known cluster': DT_SOURCE_CONFIRMED,
            'Locally acquired – contact not identified': DT_SOURCE_COMMUNITY,
            'Under investigation': DT_SOURCE_UNDER_INVESTIGATION,
            'Interstate acquired': DT_SOURCE_INTERSTATE
        }

        # Wording has changed in NSW reports -
        # normalise them to be consistent in-state
        old_type_map = {
            # NOTE: The descriptions stopped being used 21/3
            'Epi link (contact of confirmed case)':
                'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Unknown': 'Locally acquired – contact not identified',

            # These were used only 24/1
            'Locally acquired - contact of a confirmed case':
                'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Local acquired – contact not identified':
                'Locally acquired – contact not identified',

        }

        for k in (
            'Overseas acquired',
            'Locally acquired – contact of a confirmed case and/or in a known cluster',
            'Locally acquired – contact not identified',
            'Under investigation',
            'Interstate acquired',

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

            # I'm using index -1, as there's now an added
            # "Change in past 24 hours" column as of 20/4/2020
            c_value = int(pq(tr[-1]).text().replace(',', '').strip())

            r.append(DataPoint(
                datatype=nsw_norm_map[old_type_map.get(k, k)],
                value=c_value,
                date_updated=du,
                source_url=url
            ))
        return r or None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    @bothlistingandstat
    def _get_total_dhr(self, href, html):
        r = []
        html = html.replace('&#8203;', '').replace('\u200b', '')
        c_html = word_to_number(html)
        du = self._get_date(href, html)

        if href == self.STATS_BY_REGION_URL:
            # Support recovered numbers by LHD at
            # https://www.health.nsw.gov.au/Infectious/covid-19/Pages/stats-nsw.aspx

            recovered_map = {
                'Recovered': DT_STATUS_RECOVERED,
                'Lives lost': DT_STATUS_DEATHS,
                'Total cases': DT_TOTAL
            }

            table_recovered = [
                i for i in self._pq_contains(
                    html, 'table', 'Local health district​', ignore_case=True
                ) if 'recovered' in pq(i).html().lower()
            ] + [
                i for i in self._pq_contains(
                    html, 'table', 'LHD', ignore_case=True
                ) if 'recovered' in pq(i).html().lower()
            ]

            #print("**RECOVERED TABLE:", table_recovered.html())
            if table_recovered:
                table_recovered = table_recovered[0] # table
                first_tr = table_recovered[0][0] # tbody -> tr
                keys = [pq(first_tr[x+1]).text().strip() for x in range(len(first_tr)-1)]
                #print("NSW KEYS:", keys)

                for tr in table_recovered[0][1:]:
                    lhd = pq(tr[0]).text().strip().split('(')[0].strip()
                    values = [int(pq(tr[x+1]).text().replace(',', '').strip()) for x in range(len(tr)-1)]

                    values_dict = {}
                    for x, value in enumerate(values):
                        datatype = recovered_map[keys[x]]
                        values_dict[datatype] = value
                    #print("NSW VALUES:", values_dict)

                    r.append(DataPoint(
                        region_schema=SCHEMA_LHD,
                        datatype=DT_STATUS_ACTIVE,
                        region_child=lhd,
                        value=values_dict[DT_TOTAL]-values_dict[DT_STATUS_RECOVERED],
                        date_updated=du,
                        source_url=href
                    ))
                    for datatype, value in values_dict.items():
                        r.append(DataPoint(
                            region_schema=SCHEMA_LHD,
                            datatype=datatype,
                            region_child=lhd,
                            value=value,
                            date_updated=du,
                            source_url=href
                        ))

            table_ar = self._pq_contains(
                html, 'table', 'active cases', ignore_case=True
            )
            #print("TABLE AR:", table_ar.html())

            if table_ar:
                tr_active = self._pq_contains(
                    table_ar[0],
                    'tr', 'active cases',
                    ignore_case=True
                )
                tr_recovered = self._pq_contains(
                    table_ar[0],
                    'tr', 'recovered',
                    ignore_case=True
                )
                #print("TRAR:", [tr_active.html()], [tr_recovered.html()])

                if tr_active and tr_recovered:
                    # why do I need to coerce to html then reparse with html_fragments!?
                    # I have no idea, but couldn't get it working otherwise..
                    active = int(
                        pq(pq(tr_active.html(),
                           parser='html_fragments')[1]).text().replace(',', '').strip()
                    )
                    recovered = int(
                        pq(pq(tr_recovered.html(),
                           parser='html_fragments')[1]).text().replace(',', '').strip()
                    )

                    r.append(DataPoint(
                        datatype=DT_STATUS_ACTIVE,
                        value=active,
                        date_updated=du,
                        source_url=href
                    ))
                    r.append(DataPoint(
                        datatype=DT_STATUS_RECOVERED,
                        value=recovered,
                        date_updated=du,
                        source_url=href
                    ))

            return r

        else:

            hospitalized = self._extract_number_using_regex(
                compile(
                    r'([0-9,]+)[^0-9<>.]*(?:</strong>)?[^0-9<>.]*COVID-19[^0-9<>.]+'
                    r'cases?[^0-9<>.]+being[^0-9<>.]+treated[^0-9<>.]+NSW',
                    IGNORECASE
                ),
                c_html,
                datatype=DT_STATUS_HOSPITALIZED,
                source_url=href,
                date_updated=du
            )
            if hospitalized:
                r.append(hospitalized)

            icu = self._extract_number_using_regex(
                (
                    compile(
                        r'([0-9,]+)[^0-9<>.]*(?:</strong>)?[^0-9<>.]*'
                        r'(?:COVID-19[^0-9<>.]+)?cases?[^0-9<>.]+'
                        r'Intensive[^0-9<>.]+Care[^0-9<>.]+Units?',
                        IGNORECASE
                    ),
                    compile(
                        r'([0-9,]+)[^0-9<>.]*(?:</strong>)?[^0-9<>.]*'
                        r'people[^0-9<>.]+being[^0-9<>.]+treated[^0-9<>.]+in[^0-9<>.]+'
                        r'Intensive[^0-9<>.]+Care[^0-9<>.]+Units?',
                        IGNORECASE
                    )
                ),
                c_html,
                datatype=DT_STATUS_ICU,
                source_url=href,
                date_updated=du
            )
            if icu:
                r.append(icu)

            ventilators = self._extract_number_using_regex(
                compile(
                    r'([0-9,]+)[^0-9<>.]*(?:</strong>)?[^0-9<>.]*'
                    r'require[^0-9<>.]+ventilators',
                    IGNORECASE
                ),
                c_html,
                datatype=DT_STATUS_ICU_VENTILATORS,
                source_url=href,
                date_updated=du
            )
            if ventilators:
                r.append(ventilators)

            deaths = self._extract_number_using_regex(
                (
                    # Prefer from the table if possible, as that's
                    # more guaranteed to not give false positives
                    compile(r'Deaths[^0-9<>.]+in[^0-9<>.]+NSW[^0-9<>.]+from[^0-9<>.]+'
                            r'confirmed[^0-9<>.]+cases?[^0-9<>.]*</td>[^0-9<>.]*<td[^>]*>([0-9,]+)',
                            MULTILINE | DOTALL | IGNORECASE),
                    compile(r'([0-9,]+)[^0-9<>.]+death[^0-9<>.]+in[^0-9<>.]+NSW',
                            IGNORECASE),
                    compile(r'have been ([0-9,]+) deaths?',
                            IGNORECASE),
                    compile(r'total[^0-9<>.]+deaths[^0-9<>.]+'
                            r'COVID-19[^0-9<>.]+cases?[^0-9<>.]+(?:<strong>)?([0-9,]+)',
                            IGNORECASE),
                    compile(r'total[^0-9<>.]+deaths[^0-9<>.]+(?:<strong>)?([0-9]+)',
                            IGNORECASE),
                    compile(r'([0-9,]+)[^0-9<>.]+deaths[^0-9<>.]+in[^0-9<>.]+NSW',
                            IGNORECASE),
                ),
                c_html,
                datatype=DT_STATUS_DEATHS,
                source_url=href,
                date_updated=du
            )
            if deaths:
                r.append(deaths)
            return r


if __name__ == '__main__':
    from pprint import pprint
    nn = NSWNews()
    #print(pq('<td class="moh-rteTableEvenCol-6" rowspan="1">Recovered</td><td align="right" class="moh-rteTableOddCol-6" rowspan="1">2,306</td>', parser='html_fragments')[1])
    pprint(nn.get_data())
