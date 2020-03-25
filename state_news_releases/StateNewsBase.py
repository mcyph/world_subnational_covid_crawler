from urllib.parse import urlparse
from abc import ABC, abstractmethod
from pyquery import PyQuery as pq
from collections import namedtuple, defaultdict


class StateNewsBase(ABC):
    # A short name for the state (e.g. "sa")
    STATE_NAME = None
    # Where the news listing page is
    LISTING_URL = None
    # Where to find the COVID-19 news link in the page
    LISTING_HREF_SELECTOR = None
    # URL if the grabber has a "stats by region"
    # page which is separate to the main news article.
    # Some such as NSW don't keep an archive of this
    # information.
    STATS_BY_REGION_URL = None

    def __init__(self, force_no_cache=False):
        assert self.STATE_NAME
        assert self.LISTING_URL
        assert self.LISTING_HREF_SELECTOR

        self.url_archiver = URLArchiver(
            self.STATE_NAME, force_no_cache
        )

    def get_data_by_date_dict(self):
        # -> {'DD-MM-YY': [DataPoint(...), ...], ...}
        data_by_date = defaultdict([])

        print(f"{self.STATE_NAME}: Getting listing for URL {self.LISTING_URL}...")
        q = pq(url=self.LISTING_URL, parser='html')

        for href_elm in q(self.LISTING_HREF_SELECTOR):
            href_elm = pq(href_elm, parser='html')

            if any([
                (i in href_elm.text().upper())
                for i in ('COVID-19', 'COVID–19',
                          'CURRENT STATUS', 'CORONAVIRUS')
            ]):
                # If the link says it's about COVID-19, it's a
                # reasonable bet it'll contain the latest total cases
                href = href_elm.attr('href')
                if href.startswith('/'):
                    parsed = urlparse(self.LISTING_URL)
                    href = f'{parsed.scheme}://{parsed.netloc}/{href[1:]}'

                print(f'{self.STATE_NAME}: Trying href with text "{href_elm.text()}"')

                # Get the date
                date_str = self._get_date(href)

                # Get total number tested
                total_tested = self._get_total_cases_tested(href)
                if total_tested is not None:
                    data_by_date[date_str] = total_tested

                # Get new cases
                new_cases = self._get_total_new_cases(href)

                # Get total cases
                self._get_total_cases(href)

                # Get cases by region
                # FIXME: This often only has the current day of data - caching etc will need to be adjusted!!!!
                self._get_total_cases_by_region(href)

                # Get fatalities
                self._get_total_fatalities(href)

                # Get hospitalized/recovered
                self._get_total_hospitalized_recovered(href)

                # Get new cases
                self._get_total_new_cases(href)

        print()

    def _extract_number_using_regex(self, regex, s):
        """
        Convenience function for removing numeral grouping X,XXX
        and returning a number based on a match from re.compile()
        instance `regex`
        """
        #
        match = regex.search(s)
        # print(regex, match)
        if match:
            num = match.group(1)
            num = num.replace(',', '')
            if num.isdecimal():
                print(f"    Found Match: {match.group()}")
                return int(num)
        return None

    #===============================================================#
    #                Methods that must be overridden                #
    #===============================================================#

    @abstractmethod
    def _get_date(self, href, html):
        """
        Get the date when the page was updated
        """
        pass

    @abstractmethod
    def _get_total_cases_tested(self, href, html):
        """
        Get the total number of cases tested to date
        """
        pass

    @abstractmethod
    def _get_total_new_cases(self, href, html):
        """
        Get the total number of new cases for the day
        Probably not critical info, but useful for
        checking tallies etc
        """
        pass

    @abstractmethod
    def _get_total_cases_by_region(self, href, html):
        """
        A lot of states aren't recording the precise
        locations any more, only a general region
        including NSW, QLD and VIC as of 25/3
        """
        pass

    @abstractmethod
    def _get_total_cases(self, href, html):
        """

        """
        pass

    @abstractmethod
    def _get_total_fatalities(self, href, html):
        """

        """
        pass

    @abstractmethod
    def _get_total_hospitalized_recovered(self, href, html):
        """

        """
        pass
