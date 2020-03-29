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

    @abstractmethod
    def get_data(self):
        # -> {'DD-MM-YY': [DataPoint(...), ...], ...}
        pass

    def _get_listing_urls(self, url, selector):
        """
        Most (all?) of the state pages are of a very similar
        format with listings of hyperlinks to news articles
        """
        listing_urls = []

        print(f"{self.STATE_NAME}: Getting listing for URL {url}...")
        q = pq(url=url, parser='html')

        for href_elm in q(selector):
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
                    parsed = urlparse(url)
                    href = f'{parsed.scheme}://{parsed.netloc}/{href[1:]}'

                print(f'{self.STATE_NAME}: Trying href with text "{href_elm.text()}"')

                # Get the date
                date_str = self._get_date(href, FIXME)

                listing_urls.append((href, date_str))
        return listing_urls

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

    def _extract_date_using_format(self, s, format='%d %B %Y'):
        pass

    #===============================================================#
    #                Methods that must be overridden                #
    #===============================================================#

    @abstractmethod
    def _get_date(self, href, html):
        """
        Get the date when the page was updated
        """
        pass

    #===============================================================#
    #                Methods that must be overridden                #
    #===============================================================#

    @abstractmethod
    def _get_total_new_cases(self, href, html):
        """
        Get the total number of new cases for the day
        Probably not critical info, but useful for
        checking tallies etc
        """
        pass

    @abstractmethod
    def _get_total_cases(self, href, html):
        """

        """
        pass

    @abstractmethod
    def _get_total_cases_tested(self, href, html):
        """
        Get the total number of cases tested to date
        """
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    @abstractmethod
    def _get_new_cases_by_region(self, href, html):
        pass

    @abstractmethod
    def _get_total_cases_by_region(self, href, html):
        """
        A lot of states aren't recording the precise
        locations any more, only a general region
        including NSW, QLD and VIC as of 25/3
        """
        pass

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    @abstractmethod
    def _get_new_male_female_breakdown(self, url, html):
        pass

    @abstractmethod
    def _get_total_male_female_breakdown(self, url, html):
        pass

    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    @abstractmethod
    def _get_new_source_of_infection(self, url, html):
        pass

    @abstractmethod
    def _get_total_source_of_infection(self, url, html):
        pass

