from re import compile
from pyquery import PyQuery as pq
from covid_19_au_grab.state_news_releases.StateNewsBase import StateNewsBase


class VicNews(StateNewsBase):
    STATE_NAME = 'vic'
    LISTING_URL = 'https://www.dhhs.vic.gov.au/' \
                  'media-hub-coronavirus-disease-covid-19'
    LISTING_HREF_SELECTOR = '.field--item a'

    def _get_total_cases(self, href, html):
        pass

    def _get_date(self, href, html):
        selector = (
            # New page format
            '.first-line field field--name-field-general-first-line '
                'field--type-string-long field--label-hidden field--item, '
            # Old page format
            '.page-date',
        )

        lambda s: strptime('%d %B %Y',
                           s.strip().split('\n')[-1])

    def _get_total_cases_tested(self, href, html):
        # Victoria's seems to follow a formula (for now), so will hardcode
        lambda s: (
            (compile(r'([0-9,]+) Victorians have been tested').match(s)) or
            (1000 if 'thousand casual contacts have been tested' in s else None)
        )

    def _get_total_cases_by_region(self, href, html):
        pass

    def _get_total_fatalities(self, href, html):
        pass

    def _get_total_hospitalized_recovered(self, href, html):
        pass

