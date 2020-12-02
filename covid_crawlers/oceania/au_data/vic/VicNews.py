from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_db.datatypes.enums import Schemas, DataTypes
from covid_db.datatypes.DataPoint import DataPoint
from _utility.word_to_number import word_to_number

from covid_crawlers.oceania.au_data.StateNewsBase import StateNewsBase, bothlistingandstat


class VicNews(StateNewsBase):
    STATE_NAME = 'vic'

    SOURCE_ID = 'au_vic_press_releases'
    SOURCE_URL = 'https://www.dhhs.vic.gov.au/coronavirus'
    SOURCE_DESCRIPTION = ''

    LISTING_URL = (
        'https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19',
        'https://www.dhhs.vic.gov.au/coronavirus'
    )
    LISTING_HREF_SELECTOR = (
        # A very broad selector, unfortunately to
        # prevent going into other irrelevant links
        '.field.field--name-field-dhhs-rich-text-text'
            '.field--type-text-long.field--label-hidden.field--item a , '
        '.field--name-field-more-updates .field--item a'
    )
    STATS_BY_REGION_URL = (
        # https://www.dhhs.vic.gov.au/coronavirus-testing-data-local-government-area
        # https://www.dhhs.vic.gov.au/case-locations-and-outbreaks
        'https://www.dhhs.vic.gov.au/coronavirus-covid-19-daily-update'
    )

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

        if '-' in s:
            s = s.split('-')[-1].strip()
        if ', ' in s:
            s = s.split(', ')[-1]

        if not s or 'and' in s:
            # Exception to the rule..
            # https://www.dhhs.vic.gov.au/media-release-coronavirus-update-cho-victoria-2-april-2020
            s = pq(html)('.page-banner-content h1').text().split('-')[-1].strip()
        #print('S:', s)

        if not '2020' in s and '/' in s:
            s = s.strip()+'/2020'
        elif not '2020' in s:
            s = s.strip()+' 2020'

        try:
            return self._extract_date_using_format(s)
        except ValueError:
            try:
                return self._extract_date_using_format(s, format='%d %b %Y')
            except ValueError:
                try:
                    return self._extract_date_using_format(pq(html)('.purple-pullout').text().strip(), format='%d/%m/%Y')
                except ValueError:
                    # https://www.dhhs.vic.gov.au/victorias-coronavirus-covid-19-modelling-confirms-staying-home-saves-lives
                    return self._extract_date_using_format(pq(html)('.page-updated').text().split(' on ')[-1].strip(), format='%d/%m/%Y')

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    @bothlistingandstat
    def _get_total_new_cases(self, href, html):
        c_html = word_to_number(html)

        if 'same total number as yesterday' in html:
            # https://www.dhhs.vic.gov.au/coronavirus-update-victoria-27-april-2020
            return DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-VIC',
                datatype=DataTypes.NEW,
                value=0,
                date_updated=self._get_date(href, html),
                source_url=href,
                text_match='same total number as yesterday'
            )

        return self._extract_number_using_regex(
            compile('increase of ([0-9,]+)'),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.NEW,
            source_url=href,
            date_updated=self._get_date(href, html)
        ) or self._extract_number_using_regex(
            compile('([0-9,]+) new cases'),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.NEW,
            source_url=href,
            date_updated=self._get_date(href, html)
        )

    @bothlistingandstat
    def _get_total_cases(self, href, html):
        vic_total_cases = self._extract_number_using_regex(
            compile(
                '(?:cases in Victoria is|'
                   'total number of cases in Victoria to) '
                '([0-9,]+)'
            ),
            html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.TOTAL,
            source_url=href,
            date_updated=self._get_date(href, html)
        )
        return vic_total_cases

    @bothlistingandstat
    def _get_total_cases_tested(self, href, html):
        # Victoria's seems to follow a formula (for now), so will hardcode
        #print("TT DATE UPDATE:", self._get_date(href, html))

        if 'have been completed with many more samples still being ' \
           'processed as part of Victoria’s testing blitz' in html:
            return None

        vic_test = self._extract_number_using_regex(
            compile(
                r'([0-9,]+) (?:Victorians have been tested|'
                r'tests have been conducted|'
                r'tests have been completed|'
                r'tests have been performed|'
                r'tests have been processed)',
                IGNORECASE
            ),
            html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.TESTS_TOTAL,
            source_url=href,
            date_updated=self._get_date(href, html)
        )

        if vic_test:
            return vic_test
        elif 'thousand casual contacts have been tested' in html:
            return DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-VIC',
                datatype=DataTypes.TESTS_TOTAL,
                value=1000,
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

    @bothlistingandstat
    def _get_total_male_female_breakdown(self, url, html):
        du = self._get_date(url, html)

        regex = compile(r'Total cases include ([0-9,]+) men and ([0-9,]+) women')
        match = regex.search(html)
        if match:
            men = int(match.group(1).replace(',', ''))
            women = int(match.group(2).replace(',', ''))

            men = DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='au',
                region_child='au-vic',
                date_updated=du,
                datatype=DataTypes.TOTAL_MALE,
                value=men,
                source_url=url
            )
            women = DataPoint(
                region_schema=Schemas.ADMIN_1,
                region_parent='au',
                region_child='au-vic',
                date_updated=du,
                datatype=DataTypes.TOTAL_FEMALE,
                value=women,
                source_url=url
            )
            return men, women

        else:
            men = self._extract_number_using_regex(
                compile('total[^0-9.]+?([0-9,]+) men'),
                html,
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-VIC',
                source_url=url,
                datatype=DataTypes.TOTAL_MALE,
                date_updated=du
            )
            women = self._extract_number_using_regex(
                compile('total[^0-9.]+?([0-9,]+) women'),
                html,
                region_schema=Schemas.ADMIN_1,
                region_parent='AU',
                region_child='AU-VIC',
                source_url=url,
                datatype=DataTypes.TOTAL_FEMALE,
                date_updated=du
            )
            if men is not None and women is not None:
                return men, women
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

        regional_table = pq(html)('table:contains("LGA")')

        if regional_table and len(regional_table):
            datatype_map = {
                'confirmed cases': DataTypes.TOTAL,
                'confirmed cases (ever)': DataTypes.TOTAL,
                'confirmed cases\n(ever)': DataTypes.TOTAL,
                'total confirmed cases (ever)': DataTypes.TOTAL,
                'total confirmed cases\n(ever)': DataTypes.TOTAL,
                'active cases (current)': DataTypes.STATUS_ACTIVE,
                'active cases\n(current)': DataTypes.STATUS_ACTIVE,
                'currently active cases': DataTypes.STATUS_ACTIVE,
            }
            datatypes = [
                datatype_map[pq(th).text().strip().lower()]
                for th in pq(regional_table)('thead th')[1:]
            ]
            date = self._get_date(href, html)

            for tr in pq(regional_table)('tbody tr'):
                if not tr or not len(tr):
                    continue # ???
                region = pq(tr[0]).text().strip().lower()
                tr = pq(tr)('td')

                if region == 'total':
                    for value, datatype in zip(tr[1:], datatypes):
                        value = pq(value).text().strip().strip('*-').replace(',', '')
                        if value:
                            value = int(value)
                            regions.append(DataPoint(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='AU',
                                region_child='AU-VIC',
                                datatype=datatype,
                                value=value,
                                date_updated=date,
                                source_url=href
                            ))
                else:
                    for value, datatype in zip(tr[1:], datatypes):
                        value = pq(value).text().strip().strip('*-').replace(',', '')
                        if value:
                            value = int(value)
                            regions.append(DataPoint(
                                region_schema=Schemas.LGA,
                                region_parent='AU-VIC',
                                region_child=region,
                                datatype=datatype,
                                value=value,
                                date_updated=date,
                                source_url=href
                            ))

        if 'regional local government areas of' in html:
            multi_region_info = html.split(
                'regional local government areas of '
            )[1].split('.')[0].replace(' and ', ', ').replace(') ', '), ')

            for region_child in multi_region_info.split(', '):
                #print(region_child)
                if '(' in region_child:
                    region_name, num_cases = region_child.split('(')
                    region_name = region_name.strip()
                    num_cases = num_cases.strip('() ')
                else:
                    region_name = region_child.strip()
                    num_cases = 1

                if region_name == 'org/rss/1':
                    continue

                regions.append(DataPoint(
                    region_schema=Schemas.LGA,
                    region_parent='au-vic',
                    region_child=region_name.replace('have all recorded one case', '').strip(),
                    datatype=DataTypes.TOTAL,
                    value=int(num_cases),
                    date_updated=self._get_date(href, html),
                    source_url=href
                ))

        if 'have all recorded one case' in html:
            single_region_info = html.split(
                ' have all recorded one case'
            )[0].split('.')[1].replace(' and ', ', ')

            for region_name in single_region_info.split(', '):
                if region_name == 'org/rss/1':
                    continue

                regions.append(DataPoint(
                    region_schema=Schemas.LGA,
                    region_parent='au-vic',
                    region_child=region_name,
                    datatype=DataTypes.TOTAL,
                    value=1,
                    date_updated=self._get_date(href, html),
                    source_url=href
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
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            source_url=url,
            datatype=DataTypes.SOURCE_OF_INFECTION,
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

    @bothlistingandstat
    def _get_total_dhr(self, href, html):
        """
        "Currently 26 people are in hospital, including four
        patients in intensive care, 193 people have recovered. "
        """
        r = []
        c_html = word_to_number(html)
        du = self._get_date(href, html)

        deaths = self._extract_number_using_regex(
            (
                compile(
                    'died in Victoria from '
                    '(?:coronavirus|COVID-19) '
                    '(?:is|to) ([0-9,]+)',
                    IGNORECASE
                ),
                compile(
                    '([0-9,]+) (?:people have(?: already)? died)' # deaths| generates a lot of false positives after a certain date!!
                ) if du >= '2020_07_07' else compile(
                    '([0-9,]+) (?:deaths|people have(?: already)? died)'
                ),
            ),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.STATUS_DEATHS,
            source_url=href,
            date_updated=du
        )
        if deaths:
            if du >= '2020_07_29' and deaths.value < 50:
                raise Exception((du, href, deaths))
            r.append(deaths)

        in_hospital = self._extract_number_using_regex(
            compile('([0-9,]+) people are in hospital'),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.STATUS_HOSPITALIZED,
            source_url=href,
            date_updated=du
        )
        if in_hospital:
            r.append(in_hospital)

        in_icu = self._extract_number_using_regex(
            compile('([0-9,]+) (?:patients?|person|people) in intensive care'),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.STATUS_ICU,
            source_url=href,
            date_updated=du
        )
        if in_icu:
            r.append(in_icu)

        active = self._extract_number_using_regex(
            compile('([0-9,]+) active cases'),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.STATUS_ACTIVE,
            source_url=href,
            date_updated=du
        )
        if active:
            r.append(active)

        recovered = self._extract_number_using_regex(
            compile('([0-9,]+) people have recovered'),
            c_html,
            region_schema=Schemas.ADMIN_1,
            region_parent='AU',
            region_child='AU-VIC',
            datatype=DataTypes.STATUS_RECOVERED,
            source_url=href,
            date_updated=du
        )
        if recovered:
            r.append(recovered)
        return r


if __name__ == '__main__':
    from pprint import pprint
    vn = VicNews()
    pprint(vn.get_datapoints())
