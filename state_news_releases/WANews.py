from pyquery import PyQuery as pq
from re import compile, IGNORECASE

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES, \
    DT_SOURCE_OF_INFECTION, \
    DT_NEW_CASES_BY_REGION, DT_NEW_CASES, \
    DT_MALE, DT_FEMALE
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.word_to_number import word_to_number


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
        print(date)

        if ', ' in date:
            date = date.split(', ')[-1]
        print(date)

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
                name=None,
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
        html = word_to_number(html)

        return self._extract_number_using_regex(
            compile('reported ([0-9,]+) new cases'),
            html,
            source_url=url,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(url, html)
        ) or self._extract_number_using_regex(
            compile('([0-9,]+) Western Australians who have tested positive'),
            html,
            source_url=url,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(url, html)
        )

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
        #return None  # HACK: This info is likely to be too unreliable at this stage - may add back later!!

        html = word_to_number(html)

        r = []

        # Get male breakdown
        male = self._extract_number_using_regex(
            compile('[^0-9.]+([0-9,]+) male(?:s)?'),
            html,
            source_url=url,
            datatype=DT_MALE,
            date_updated=self._get_date(url, html)
        )
        if male:
            r.append(male)

        # Get female breakdown
        female = self._extract_number_using_regex(
            compile('[^0-9.]+([0-9,]+) female(?:s)?'),
            html,
            source_url=url,
            datatype=DT_FEMALE,
            date_updated=self._get_date(url, html)
        )
        if female:
            r.append(female)

        return r

    def _get_total_male_female_breakdown(self, url, html):
        return None

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, url, html):
        # AFAIK, this information currently isn't
        # available in an easily readable format

        html = html.replace(
            # HACK: This only happens once!
            'first confirmed case in regional WA',
            'new case 16 metropolitan 1 regional'
        )
        html = html.replace(
            # Same here...
            'The Department of Health has reported four new cases of '
            'COVID-19 overnight, bringing the State&rsquo;s total to 35.',
            'new case 4 metropolitan'
        )
        html = html.replace(
            'The Department of Health has reported 12 new cases of '
            'COVID-19 overnight, bringing the State&rsquo;s total to 64.',
            'new case 12 metropolitan'
        )

        grab_from = [
            i for i in html.split('.')
            if 'new case' in i and ('metropolitan' in i.lower() or 'regional' in i.lower())  # ...s are?
        ]
        if not grab_from:
            return None

        total = self._get_total_new_cases(url, html)
        if not total:
            return None

        # "all" is pretty much synonymous with "total" here
        grab_from = grab_from[0]
        grab_from = grab_from.replace('All ', ' all ')
        grab_from = grab_from.replace(' all ', ' '+str(total.value)+' ')

        # It might be worth indicating whether regional or metropolitan, e.g.:
        # To date, 9,948 Western Australians have tested negative
        # for COVID-19 – 1,283 of these are from regional WA.
        grab_from = word_to_number(grab_from)
        print("GRAB FROM:", grab_from)

        def get_num(i):
            if i: return i.value
            return 0

        num_regional = self._extract_number_using_regex(
            compile(r'([0-9,]+) [^0-9.]*regional',
                    IGNORECASE),
            grab_from,
            name='Regional WA',
            source_url=url,
            datatype=DT_NEW_CASES_BY_REGION,
            date_updated=self._get_date(url, html)
        )
        num_metro = self._extract_number_using_regex(
            compile('([0-9,]+) [^0-9.]*metropolitan', IGNORECASE),
            grab_from,
            name='Metropolitan/Other',
            source_url=url,
            datatype=DT_NEW_CASES_BY_REGION,
            date_updated=self._get_date(url, html)
        )
        num_investigation = self._extract_number_using_regex(
            compile('([0-9,]+) [^0-9.]*under investigation'),
            grab_from,
            name='Under Investigation',
            source_url=url,
            datatype=DT_NEW_CASES_BY_REGION,
            date_updated=self._get_date(url, html)
        )

        if (
            num_metro is not None or
            num_regional is not None or
            num_investigation is not None
        ):
            r = []

            other = (
                total.value -
                get_num(num_regional) -
                get_num(num_metro) -
                get_num(num_investigation)
            )
            if other:
                # Trouble is, they explicitly explain when there are
                # regional WA inhabitants, but sometimes only imply
                # that the others are metro ==========================================================================
                # At least can be sure "Metropolitan/Other" is suitably vague..
                num_metro = DataPoint(
                    name='Metropolitan/Other',
                    datatype=DT_NEW_CASES_BY_REGION,
                    value=other+get_num(num_metro),
                    date_updated=self._get_date(url, html),
                    source_url=url,
                    text_match=None
                )
                #r.append(num_other)

            if num_regional:
                r.append(num_regional)
            if num_metro:
                r.append(num_metro)
            if num_investigation:
                r.append(num_investigation)
            return r

        return None

    def _get_total_cases_by_region(self, url, html):
        return None

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        return None   # This data is really not easily machine-readable, I can't think of any better way than to go thru manually!

        # https://ww2.health.wa.gov.au/Media-releases/2020/Children-among-35-new-cases-of--COVID19
        # Ruby princess
        # ... princess
        # Ovation of the Seas
        # overseas travel
        num_overseas = self._extract_number_using_regex(
            compile("([0-9]+) cases [^0-9.]*"
                    "overseas",
                    IGNORECASE),
            html,
            name='Overseas',
            source_url=url,
            datatype=DT_SOURCE_OF_INFECTION,
            date_updated=self._get_date(url, html)
        )
        num_cruise_ship = self._extract_number_using_regex(
            compile("([0-9]+) cases [^0-9.]*"
                    "(?:Ruby Princess|Ovation of the Seas|Diamond Princess|Cruise)",
                    IGNORECASE),
            html,
            name='Cruise Ship',
            source_url=url,
            datatype=DT_SOURCE_OF_INFECTION,
            date_updated=self._get_date(url, html)
        )
        total_new = self._get_total_new_cases(url, html)

        if (
            num_overseas is not None or
            num_cruise_ship is not None
        ) and total_new is not None:
            output = []
            if num_cruise_ship:
                output.append(num_cruise_ship)
            if num_overseas:
                output.append(num_overseas)

            cruise_ship = num_cruise_ship.value \
                if num_cruise_ship else 0
            overseas = num_overseas.value \
                if num_overseas else 0

            other = DataPoint(
                name='Other',
                datatype=DT_SOURCE_OF_INFECTION,
                value=total_new.value - cruise_ship - overseas,
                date_updated=self._get_date(url, html),
                source_url=url,
                text_match=None
            )
            output.append(other)
            return output
        return None

    def _get_total_source_of_infection(self, url, html):
        pass

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    def _get_total_dhr(self, href, html):
        pass


if __name__ == '__main__':
    from pprint import pprint
    wn = WANews()
    pprint(wn.get_data())
