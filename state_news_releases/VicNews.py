from re import compile, IGNORECASE
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class VicNews(StateNewsBase):
    STATE_NAME = 'vic'
    LISTING_URL = 'https://www.dhhs.vic.gov.au/' \
                  'media-hub-coronavirus-disease-covid-19'
    LISTING_HREF_SELECTOR = '.field--item a'

    def _get_date(self, href, html):
        selector = (
            # New page format
            '.first-line field field--name-field-general-first-line '
                'field--type-string-long field--label-hidden field--item, '
            # Old page format
            '.page-date',
        )
        s = pq(html)(selector).text()
        self._extract_date_using_format(
            s.strip().split('\n')[-1]
        )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        pass

    def _get_total_cases(self, href, html):
        pass

    def _get_total_cases_tested(self, href, html):
        # Victoria's seems to follow a formula (for now), so will hardcode
        vic_test = self._extract_number_using_regex(
            compile(
                r'([0-9,]+) (?:Victorians have been tested|'
                r'tests have been conducted',
                IGNORECASE
            ),
            html
        )
        if vic_test:
            return vic_test
        elif 'thousand casual contacts have been tested' in html:
            return 1000
        else:
            return None

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, url, html):
        pass

    def _get_total_male_female_breakdown(self, url, html):
        men = self._extract_number_using_regex(
            compile('([0-9,]+) men'),
            html
        )
        women = self._extract_number_using_regex(
            compile('([0-9,]+) women'),
            html
        )
        if men is not None and women is not None:
            return (men, women)
        return None

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_total_new_cases_by_region(self, href, html):
        return None

    def _get_total_cases_by_region(self, href, html):
        """
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
        regions = {}

        if 'regional local government areas of' in html:
            multi_region_info = html.split(
                'regional local government areas of '
            )[1].split('.')[0].replace(' and ', ', ')

            for region in multi_region_info.split(', '):
                region_name, num_cases = region.split('(')
                num_cases = num_cases.strip('( ')
                regions[region_name] = int(num_cases)

        if 'have all recorded one case' in html:
            single_region_info = html.split(
                ' have all recorded one case'
            )[0].split('.')[1].replace(' and ', ', ')

            for region_name in single_region_info.split(', '):
                regions[region_name.strip()] = 1

        return regions

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        return None

    def _get_total_source_of_infection(self, url, html):
        num_comm_trans = self._extract_number_using_regex(
            compile('([0-9,]+) confirmed cases of COVID-19 in '
                    'Victoria that may have been acquired '
                    'through community transmission'),
            html
        )
        total_cases = self._get_total_cases(url, html)

        if num_comm_trans is not None and total_cases is not None:
            return {
                'Community Transmission': num_comm_trans,
                'Other': total_cases - num_comm_trans
            }
        return None
