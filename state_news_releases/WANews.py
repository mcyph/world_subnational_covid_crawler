from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint


class WANews(StateNewsBase):
    STATE_NAME = 'wa'
    LISTING_URL = 'https://ww2.health.wa.gov.au/News/' \
                  'Media-releases-listing-page'
    LISTING_HREF_SELECTOR = 'div.threeCol-accordian a'

    """
    def get_data(self):
        date_dict = defaultdict([])

        for date_str, url, href_text, html in self._get_listing_urls(
            self.LISTING_URL,
            self.LISTING_HREF_SELECTOR
        ):
            date_dict[date_str].append(
                self._get_total_cases(url, html)
            )
    """

    def _get_date(self, url, html):
        # e.g. "24 March 2020"
        print(url)
        try:
            date = pq(pq(html)('.newsCreatedDate')[0]).text().strip()
            if not date:
                raise IndexError
        except IndexError:
            date = pq(pq(html)('#contentArea h3')[0]).text().strip()

        if ', ' in date:
            date = date.split(', ')[-1]

        try:
            return self._extract_date_using_format(date)
        except ValueError:
            return self._extract_date_using_format(
                date.split()[0], format='%d/%m/%Y'
            )

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_cases(self, url, html):
        return self._extract_number_using_regex(
            compile(r'total to ([0-9,]+)'),
            html,
            source_url=url,
            datatype=DT_CASES,
            date_updated=self._get_date(url, html)
        )

    def _get_total_cases_tested(self, url, html):
        neg_cases = self._extract_number_using_regex(
            # Seems the WA website's wording can change day-to-day
            compile(r'([0-9]+[0-9,]*?)'
                    r'([^0-9]*?negative COVID-19 tests|'
                    r'[^0-9]*?tested negative|'
                    r'[^0-9]*?negative)'),
            html,
            source_url=url,
            datatype=DT_CASES_TESTED,
            date_updated=self._get_date(url, html)
        )
        pos_cases = self._get_total_cases(url, html)

        if neg_cases and pos_cases:
            return DataPoint(
                datatype=neg_cases.datatype,
                value=neg_cases.value+pos_cases.value,
                date_updated=neg_cases.date_updated,
                source_url=neg_cases.source_url,
                text_match=(
                    neg_cases.text_match,
                    pos_cases.text_match
                )
            )
        return None

    def _get_total_new_cases(self, url, html):
        regex = compile(
            "new.*?([0-9,]+) males? and ([0-9,]+) females?",
            IGNORECASE
        )
        match = regex.match(html)
        if match:
            return int(match.group(1).replace(',', '')) + \
                   int(match.group(2).replace(',', ''))
        return None

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, url, html):
        # Get male breakdown
        m_regex = compile('new[^.]+([0-9,]+) males?')
        m_match = m_regex.match(html)
        if m_match:
            m = int(m_match.group(1).strip().replace(',', ''))
        else:
            m = None

        # Get female breakdown
        f_regex = compile('new[^.]+([0-9,]+) females?')
        f_match = f_regex.match(html)
        if f_match:
            f = int(f_match.group(1).strip().replace(',', ''))
        else:
            f = None
        return m, f

    def _get_total_male_female_breakdown(self, url, html):
        return None

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, url, html):
        # AFAIK, this information currently isn't
        # available in an easily readable format

        # It might be worth indicating whether regional or metropolitan, e.g.:
        # To date, 9,948 Western Australians have tested negative
        # for COVID-19 – 1,283 of these are from regional WA.

        num_regional = self._extract_number_using_regex(
            compile('([0-9,]) [^0-9.]*'
                    'cases were from regional WA',
                    IGNORECASE),
            html
        )
        total_new = self._get_total_new_cases(url, html)

        if (
            num_regional is not None and
            total_new is not None
        ):
            return {
                'Regional WA': num_regional,
                'Other': -num_regional
            }
        return None

    def _get_total_cases_by_region(self, url, html):
        return None

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        # https://ww2.health.wa.gov.au/Media-releases/2020/Children-among-35-new-cases-of--COVID19
        # Ruby princess
        # ... princess
        # Ovation of the Seas
        # overseas travel
        num_overseas = self._extract_number_using_regex(
            compile("([0-9]+) cases [^0-9.]*"
                    "overseas",
                    IGNORECASE),
            html
        )
        num_cruise_ship = self._extract_number_using_regex(
            compile("([0-9]+) cases [^0-9.]*"
                    "(?:Ruby Princess|Ovation of the Seas|Diamond Princess|Cruise)",
                    IGNORECASE),
            html
        )
        total_new = self._get_total_new_cases(url, html)

        if (
            num_overseas is not None or
            num_cruise_ship is not None
        ) and total_new is not None:
            return {
                'Overseas': num_overseas or 0,
                'Cruise Ship': num_cruise_ship or 0,
                'Other': total_new -
                         (num_overseas or 0) -
                         (num_cruise_ship or 0)
            }
        return None

    def _get_total_source_of_infection(self, url, html):
        pass


if __name__ == '__main__':
    from pprint import pprint
    wn = WANews()
    pprint(wn.get_data())
