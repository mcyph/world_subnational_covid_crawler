from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES, DT_NEW_CASES, \
    DT_CASES_BY_REGION, DT_NEW_CASES_BY_REGION, \
    DT_MALE, DT_FEMALE, \
    DT_SOURCE_OF_INFECTION, \
    DT_DEATHS, DT_HOSPITALIZED, DT_ICU, DT_RECOVERED
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.word_to_number import word_to_number


class VicNews(StateNewsBase):
    STATE_NAME = 'vic'
    LISTING_URL = 'https://www.dhhs.vic.gov.au/' \
                  'media-hub-coronavirus-disease-covid-19'
    LISTING_HREF_SELECTOR = '.field--item a'

    def _get_date(self, href, html):
        selector = (
            # New page format
            '.first-line.field.field--name-field-general-first-line.'
                'field--type-string-long.field--label-hidden.field--item, '
            # Old page format
            '.page-date'
        )
        s = pq(html)(selector).text()
        s = s.strip().split('\n')[-1]

        if ', ' in s:
            s = s.split(', ')[-1]

        try:
            return self._extract_date_using_format(s)
        except ValueError:
            return self._extract_date_using_format(
                s, format='%d %b %Y'
            )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            compile('an increase of ([0-9,]+)'),
            c_html,
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        ) or self._extract_number_using_regex(
            compile('([0-9,]+) new cases'),
            c_html,
            source_url=href,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(href, html)
        )

    def _get_total_cases(self, href, html):
        vic_total_cases = self._extract_number_using_regex(
            compile(
                '(?:cases in Victoria is|'
                   'total number of cases in Victoria to) '
                '([0-9,]+)'
            ),
            html,
            source_url=href,
            datatype=DT_CASES,
            date_updated=self._get_date(href, html)
        )
        return vic_total_cases

    def _get_total_cases_tested(self, href, html):
        # Victoria's seems to follow a formula (for now), so will hardcode
        print("TT DATE UPDATE:", self._get_date(href, html))
        vic_test = self._extract_number_using_regex(
            compile(
                r'([0-9,]+) (?:Victorians have been tested|'
                r'tests have been conducted)',
                IGNORECASE
            ),
            html,
            source_url=href,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(href, html)
        )

        if vic_test:
            return vic_test
        elif 'thousand casual contacts have been tested' in html:
            return DataPoint(
                name=None,
                value=1000,
                datatype=DT_CASES_TESTED,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match='thousand casual contacts have been tested'
            )
        else:
            return None

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

    def _get_new_male_female_breakdown(self, url, html):
        pass

    def _get_total_male_female_breakdown(self, url, html):
        men = self._extract_number_using_regex(
            compile('total[^0-9.]+([0-9,]+) men'),
            html,
            source_url=url,
            datatype=DT_MALE,
            date_updated=self._get_date(url, html)
        )
        women = self._extract_number_using_regex(
            compile('total[^0-9.]+([0-9,]+) women'),
            html,
            source_url=url,
            datatype=DT_FEMALE,
            date_updated=self._get_date(url, html)
        )
        if men is not None and women is not None:
            return (men, women)
        return None

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, href, html):
        return None

    def _get_total_cases_by_region(self, href, html):
        """
        TODO: Get from PowerBI data!!! =================================================================================

        https://www.dhhs.vic.gov.au/coronavirus-update-victoria-25-march-2020

        Multiple cases have occurred in the regional local
        government areas of Greater Geelong (11), Ballarat (5),
        Baw Baw (2), Greater Shepparton (2), Surf Coast (2),
        Warrnambool (2), Latrobe (2), Macedon Ranges (2),
        Mitchell (4) and Mount Alexander (3). Bass Coast,
        East Gippsland, Gannawarra, Hepburn, Mildura, Moira,
        Moyne, Moorabool, Northern Grampians, South Gippsland,
        Wellington and Yarriambiack have all recorded one case.
        """
        regions = []

        if 'regional local government areas of' in html:
            multi_region_info = html.split(
                'regional local government areas of '
            )[1].split('.')[0].replace(' and ', ', ').replace(') ', '), ')

            for region in multi_region_info.split(', '):
                print(region)
                if '(' in region:
                    region_name, num_cases = region.split('(')
                    region_name = region_name.strip()
                    num_cases = num_cases.strip('() ')
                else:
                    region_name = region.strip()
                    num_cases = 1

                if region_name == 'org/rss/1':
                    continue

                regions.append(DataPoint(
                    datatype=DT_CASES_BY_REGION,
                    name=region_name,
                    value=int(num_cases),
                    date_updated=self._get_date(href, html),
                    source_url=href,
                    text_match=None
                ))

        if 'have all recorded one case' in html:
            single_region_info = html.split(
                ' have all recorded one case'
            )[0].split('.')[1].replace(' and ', ', ')

            for region_name in single_region_info.split(', '):
                if region_name == 'org/rss/1':
                    continue

                regions.append(DataPoint(
                    datatype=DT_CASES_BY_REGION,
                    name=region_name,
                    value=1,
                    date_updated=self._get_date(href, html),
                    source_url=href,
                    text_match=None
                ))

        return regions

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        return None

    def _get_total_source_of_infection(self, url, html):
        return None  # FIXME!!! =======================================================================================

        num_comm_trans = self._extract_number_using_regex(
            compile('([0-9,]+) confirmed cases of COVID-19 in '
                    'Victoria that may have been acquired '
                    'through community transmission'),
            html,
            source_url=url,
            datatype=DT_SOURCE_OF_INFECTION,
            date_updated=self._get_date(url, html)
        )
        total_cases = self._get_total_cases(url, html)

        if num_comm_trans is not None and total_cases is not None:
            return {
                'Community Transmission': num_comm_trans,
                'Other': total_cases - num_comm_trans
            }
        return None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        """
        "Currently 26 people are in hospital, including four patients in intensive care, 193 people have recovered. "
        """
        r = []
        c_html = word_to_number(html)

        deaths = self._extract_number_using_regex(
            compile('([0-9,]+) (?:deaths|people have(?: already)? died)'),
            c_html,
            source_url=href,
            datatype=DT_DEATHS,
            date_updated=self._get_date(href, html)
        )
        if deaths:
            r.append(deaths)

        in_hospital = self._extract_number_using_regex(
            compile('([0-9,]+) people are in hospital'),
            c_html,
            source_url=href,
            datatype=DT_HOSPITALIZED,
            date_updated=self._get_date(href, html)
        )
        if in_hospital:
            r.append(in_hospital)

        in_icu = self._extract_number_using_regex(
            compile('([0-9,]+) patients? in intensive care'),
            c_html,
            source_url=href,
            datatype=DT_ICU,
            date_updated=self._get_date(href, html)
        )
        if in_icu:
            r.append(in_icu)

        recovered = self._extract_number_using_regex(
            compile('([0-9,]+) people have recovered'),
            c_html,
            source_url=href,
            datatype=DT_RECOVERED,
            date_updated=self._get_date(href, html)
        )
        if recovered:
            r.append(recovered)
        return r


if __name__ == '__main__':
    from pprint import pprint
    vn = VicNews()
    pprint(vn.get_data())
