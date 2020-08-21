import datetime
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from abc import ABC, abstractmethod

from covid_19_au_grab.datatypes.DataPoint import \
    DataPoint, _DataPoint
from covid_19_au_grab.URLArchiver import \
    URLArchiver
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes


ALWAYS_DOWNLOAD_LISTING = True

if not ALWAYS_DOWNLOAD_LISTING:
    import warnings
    warnings.warn("Using cached copy!")


METHOD_TYPE_BOTH = 0
METHOD_TYPE_SINGLE_DAY_STATS = 1
METHOD_TYPE_FROM_LISTING = 2


# Decorators

def fromlisting(fn):
    fn.typ = METHOD_TYPE_FROM_LISTING
    return fn


def singledaystat(fn):
    fn.typ = METHOD_TYPE_SINGLE_DAY_STATS
    return fn


def bothlistingandstat(fn):
    fn.typ = METHOD_TYPE_BOTH
    return fn


class StateNewsBase(ABC):
    # A short name for the state (e.g. "sa")
    STATE_NAME = None
    # Where the news listing page is
    LISTING_URL = None
    # Where to find the COVID-19 news link in the page
    LISTING_HREF_SELECTOR = None
    # URL if the grabber has a "stats by region_child"
    # page which is separate to the main news article.
    # Some such as NSW don't keep an archive of this
    # information.
    STATS_BY_REGION_URL = None

    def __init__(self):
        assert self.STATE_NAME
        #assert self.LISTING_URL
        #assert self.LISTING_HREF_SELECTOR

        # "Press release listing" archiver
        self.listing_ua = URLArchiver(f'{self.STATE_NAME}/listing')
        # Press release archiver
        self.pr_ua = URLArchiver(f'{self.STATE_NAME}/pr')
        # "Current stats" archiver
        self.current_status_ua = URLArchiver(f'{self.STATE_NAME}/current_status')

    def _pq_contains(self, html, selector, text, ignore_case=False):
        """
        For some reason, the :contains() selector doesn't
        always work for e.g. the NSW news infection reasons

        I'm not sure why this is, but for now...
        """
        text = text.replace('\u200b', '')
        if ignore_case:
            text = text.lower()

        try:
            # HTML fragments doesn't enclose e.g.
            # <td> in a <div> element but doesn't always work.
            # both "html" and "html_fragments" use lxml
            html = pq(html, parser='html_fragments')
        except AssertionError:
            html = pq(html, parser='html')

        #print("USING HTML:", html)

        out = []
        for i in html(selector):
            o = i
            try:
                i = pq(i, parser='html_fragments')
            except AssertionError:
                i = pq(i, parser='html')

            i_text = i.text() or ''
            i_html = i.html() or ''

            if ignore_case:
                i_html = i_html.lower().replace('\u200b', '')
                i_text = i_text.lower().replace('\u200b', '')

            #print("ITEM:", [i_text, text], text in i_text)

            if text in i_text or text in i_html:
                out.append(o)

        #print("OUT:", out)
        return pq(out, parser='html_fragments')

    def get_data(self):
        """
        -> [DataPoint(...), ...]
        """
        # Download from the stats by region_child URL,
        # even if I don't use the stats for now, daily!!
        # TODO: WHAT IF THERE ARE MULTIPLE UPDATES IN A DAY?? ==========================================================
        output = []

        if self.STATS_BY_REGION_URL:
            # Make sure the latest is in the cache!
            self.current_status_ua.get_url_data(
                self.STATS_BY_REGION_URL,
                cache=False if ALWAYS_DOWNLOAD_LISTING else True
            )

            for period in self.current_status_ua.iter_periods():
                for subperiod_id, subdir in self.current_status_ua.iter_paths_for_period(period):
                    path = self.current_status_ua.get_path(subdir)

                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        html = self.current_status_ua.unicode_fix(
                            f.read()
                        )
                        self._add_to_output(
                            self.STATS_BY_REGION_URL, html, output
                        )

        if self.LISTING_URL:
            for href, date_str, html in self._get_listing_urls(
                self.LISTING_URL,
                self.LISTING_HREF_SELECTOR
            ):
                self._add_to_output(href, html, output)

        return output

    def _add_to_output(self, href, html, output):
        # Add tested data
        # print('get_data for:', href, date_str, html)

        def do_call(fn, href, html):
            def check(v):
                # Make sure the correct kinds of types are returned!
                if isinstance(v, _DataPoint):
                    return v
                elif isinstance(v, (list, tuple)):
                    for i in v:
                        assert (isinstance(i, _DataPoint) or i is None), (fn, i)
                    return v
                elif v is None:
                    return v
                else:
                    raise Exception(v)

            if not hasattr(fn, 'typ') and href != self.STATS_BY_REGION_URL:
                # Functions default to for listing pages only!
                return check(fn(href, html))
            elif hasattr(fn, 'typ'):
                typ = fn.typ
                if typ == METHOD_TYPE_BOTH:
                    return check(fn(href, html))
                elif typ == METHOD_TYPE_FROM_LISTING and href != self.STATS_BY_REGION_URL:
                    return check(fn(href, html))
                elif typ == METHOD_TYPE_SINGLE_DAY_STATS and href == self.STATS_BY_REGION_URL:
                    return check(fn(href, html))
                else:
                    return None
            return None

        tested = do_call(self._get_total_cases_tested, href, html)
        if tested is not None:
            # print('** TESTED DATA OK!')
            output.append(tested)
        # else:
        # print("** TESTED NO DATA!")

        # Add total/new cases
        total_cases = do_call(self._get_total_cases, href, html)
        if total_cases:
            output.append(total_cases)
        new_cases = do_call(self._get_total_new_cases, href, html)
        if new_cases:
            output.append(new_cases)

        # Add total/new cases by region_child
        tcbr = do_call(self._get_total_cases_by_region, href, html)
        if tcbr:
            output.extend(tcbr)
        ncbr = do_call(self._get_new_cases_by_region, href, html)
        if ncbr:
            output.extend(ncbr)

        # Add new/total age breakdown
        nab = do_call(self._get_new_age_breakdown, href, html)
        if nab:
            output.extend(nab)
        tab = do_call(self._get_total_age_breakdown, href, html)
        if tab:
            output.extend(tab)

        # Add new/total source of infection
        nsoi = do_call(self._get_new_source_of_infection, href, html)
        if nsoi:
            output.extend(nsoi)
        tsoi = do_call(self._get_total_source_of_infection, href, html)
        if tsoi:
            output.extend(tsoi)

        # Add male/female breakdown
        nmfb = do_call(self._get_new_male_female_breakdown, href, html)
        if nmfb:
            output.extend(nmfb)
        tmfb = do_call(self._get_total_male_female_breakdown, href, html)
        if tmfb:
            output.extend(tmfb)

        dhr = do_call(self._get_total_dhr, href, html)
        if dhr:
            output.extend(dhr)

    def _get_listing_urls(self, url, selector, _processed=None):
        """
        Most (all?) of the state pages are of a very similar
        format with listings of hyperlinks to news articles
        """
        
        if isinstance(url, (list, tuple)):
            # TODO: MAKE SURE THE SAME CACHED FILES AREN'T PROCESSED MORE THAN ONCE!!!! ================================
            added = set()
            listing_urls = []

            for i_url in url:
                for (href, date_str, html) in self._get_listing_urls(
                    i_url, selector
                ):
                    if href in added:
                        # Don't add href's twice!
                        continue
                    added.add(href)
                    listing_urls.append((href, date_str, html))

            return listing_urls

        print(f"{self.STATE_NAME}: Getting listing for URL {url}...")

        # Download the latest listing
        self.listing_ua.get_url_data(
            url,
            cache=False if ALWAYS_DOWNLOAD_LISTING else True
        )

        # Go thru every listing so far, as some of the press
        # release listings don't go all the way back (e.g. SA)
        out_set = set()
        tried_urls_set = set()

        for period in self.listing_ua.iter_periods(
            newest_first=False
        ):
            for subperiod_id, dir_ in self.listing_ua.iter_paths_for_period(
                period, newest_first=False
            ):
                with open(self.listing_ua.get_path(dir_), 'r',
                          encoding='utf-8',
                          errors='replace') as f:

                    listing_html = self.listing_ua.unicode_fix(
                        f.read()
                    )
                    for i in self.__get_listing_urls(
                        url, selector, listing_html, tried_urls_set
                    ):
                        out_set.add(i)

        return list(sorted(out_set, key=lambda x: x[1], reverse=True))

    def __get_listing_urls(self, url, selector, listing_html, tried_urls_set):
        listing_urls = []
        q = pq(listing_html, parser='html')

        for href_elm in q(selector):
            href_elm = pq(href_elm, parser='html')

            if any([
                (i in href_elm.text().upper())
                for i in ('COVID-19', 'COVID–19',
                          'COVID 19',
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
                    'premier.vic' in href or
                    '2020/expressions_of_interest_covid-19_staffing' in href or
                    '2020/prime_minister_update_on_coronavirus_measures' in href or
                    href.endswith('news/2020/coronavirus_update') or
                    'https://www.worksafe.vic.gov.au' in href or
                    'https://www.fairwork.gov.au' in href or
                    'https://www.foodstandards.gov.au' in href or
                    'coronavirus-tasmania-snapshot' in href or
                    'covid-19+testing+for+transport+workers+begins' in href
                ):
                    continue  # HACK!

                if href in tried_urls_set:
                    continue
                tried_urls_set.add(href)

                # Get the date
                # Note that when downloading the data,
                # I'm assuming the press releases won't change.
                # This may or may not be the case!! ====================================================================
                print(f'{self.STATE_NAME}: Trying href with text "{href_elm.text()}" href {href}')
                import urllib.error
                try:
                    html = self.pr_ua.get_url_data(
                        href,
                        period=self._get_date
                    )
                except urllib.error.HTTPError:
                    if self.STATE_NAME == 'act':
                        # e.g. covid-19-update-17-april-2020
                        # gave a 403 as wasn't properly released
                        import traceback
                        traceback.print_exc()
                        continue
                    else:
                        raise

                date_str = self._get_date(href, html)
                listing_urls.append((href, date_str, html))

        return listing_urls

    def _extract_number_using_regex(self, regex, s, source_url, datatype,
                                    date_updated, agerange=None, region_child=None,
                                    region_schema=Schemas.ADMIN_1):
        """
        Convenience function for removing numeral grouping X,XXX
        and returning a number based on a match from re.compile()
        instance `regex`

        Multiple regexes can be specified for `regex`, in which
        case the first match will be returned
        """
        #
        if isinstance(regex, (list, tuple)):
            for i_regex in regex:
                dp = self._extract_number_using_regex(
                    i_regex, s, source_url, datatype,
                    date_updated, agerange, region_child, region_schema
                )
                if dp:
                    return dp
            return None

        match = regex.search(s)
        # print(regex, match)
        if match:
            num = match.group(1)
            num = num.replace(',', '')

            if num.isdecimal():
                #print(f"    Found Match: {match.group()}")
                num = int(num)
                if date_updated is None:
                    date_updated = self._todays_date()

                return DataPoint(
                    region_schema=region_schema,
                    datatype=datatype,
                    region_child=region_child,
                    agerange=agerange,
                    value=num,
                    date_updated=date_updated,
                    source_url=source_url,
                    text_match=s[
                        max(0, match.start(1)-40):
                        min(len(s), match.end(1)+40)
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
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    @abstractmethod
    def _get_total_dhr(self, href, html):
        """
        Return total deaths/hospitalized/intensive care/recovered
        I'll only record absolute values for now, as relative
        values can be unreliable
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
        locations any more, only a general region_child
        including NSW, QLD and VIC as of 25/3
        """
        pass

    #============================================================#
    #                      Age Breakdown                         #
    #============================================================#

    @abstractmethod
    def _get_new_age_breakdown(self, href, html):
        pass

    @abstractmethod
    def _get_total_age_breakdown(self, href, html):
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

