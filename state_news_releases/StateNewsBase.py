import datetime
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from abc import ABC, abstractmethod

from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.URLArchiver import URLArchiver


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

    def __init__(self):
        assert self.STATE_NAME
        assert self.LISTING_URL
        assert self.LISTING_HREF_SELECTOR

        # "Press release listing" archiver
        self.listing_ua = URLArchiver(f'{self.STATE_NAME}/listing')
        # Press release archiver
        self.pr_ua = URLArchiver(f'{self.STATE_NAME}/pr')
        # "Current stats" archiver
        self.current_status_ua = URLArchiver(f'{self.STATE_NAME}/current_status')

    def get_data(self):
        """
        -> [DataPoint(...), ...]
        """
        output = []
        for href, date_str, html in self._get_listing_urls(
            self.LISTING_URL,
            self.LISTING_HREF_SELECTOR
        ):
            print('get_data for:', href, date_str, html)
            tested = self._get_total_cases_tested(href, html)
            if tested is not None:
                print('** TESTED DATA OK!')
                output.append(tested)
            else:
                print("** TESTED NO DATA!")
        return output

    def _get_listing_urls(self, url, selector):
        """
        Most (all?) of the state pages are of a very similar
        format with listings of hyperlinks to news articles
        """
        listing_urls = []

        print(f"{self.STATE_NAME}: Getting listing for URL {url}...")
        listing_html = self.listing_ua.get_url_data(url)
        q = pq(listing_html, parser='html')

        for href_elm in q(selector):
            href_elm = pq(href_elm, parser='html')

            if any([
                (i in href_elm.text().upper())
                for i in ('COVID-19', 'COVID–19',
                          'CURRENT STATUS',
                          'CORONAVIRUS', 'CORONA')
            ]):
                # If the link says it's about COVID-19, it's a
                # reasonable bet it'll contain the latest total cases
                href = href_elm.attr('href')
                if href.startswith('/'):
                    parsed = urlparse(url)
                    href = f'{parsed.scheme}://{parsed.netloc}/{href[1:]}'

                if (
                    'soundcloud' in href or
                    'coronavirus-stage-1-statement-premier' in href or
                    'youtube.com' in href or
                    'premier.vic' in href
                ):
                    continue  # HACK!

                # Get the date
                print(f'{self.STATE_NAME}: Trying href with text "{href_elm.text()}"')
                html = self.pr_ua.get_url_data(href)
                date_str = self._get_date(href, html)

                listing_urls.append((href, date_str, html))
        return listing_urls

    def _extract_number_using_regex(self, regex, s, source_url, datatype,
                                    date_updated=None):
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
                num = int(num)
                if date_updated is None:
                    date_updated = self._todays_date()

                return DataPoint(
                    datatype=datatype,
                    value=num,
                    date_updated=date_updated,
                    source_url=source_url,
                    text_match=s[
                        max(0, match.start(1)-5):
                        min(len(s), match.end(1)+5)
                    ]
                )
        return None

    def _extract_date_using_format(self, s,
                                   format='%d %B %Y'):
        """
        Parses a date as strptime format "format"
        and outputs it as format 'YYYY_MM_DD'
        """
        print("INPUT:", s, "OUTPUT:", datetime.datetime.strptime(s, format) \
               .strftime('%Y_%m_%d'))
        return datetime.datetime.strptime(s, format) \
               .strftime('%Y_%m_%d')

    def _todays_date(self):
        return datetime.datetime.now() \
            .strftime('%Y_%m_%d')

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

