from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.request import urlopen
from collections import namedtuple
from re import compile, MULTILINE, DOTALL

CaseURL = namedtuple('CaseURL', [
    # Where the news listing page is
    'url',
    # Where to find the COVID-19 news link in the page
    'href',
    # The regular expression instance, which
    # grabs the number from the news article
    'regex',
    # Whether the number is exact
    'rough_only'
])

urls_dict = {
    'NSW': CaseURL(
        'https://www.health.nsw.gov.au/news/Pages/default.aspx',
        href='.dfwp-item a',
        regex=compile(
            # Total (including tested and excluded)
            r'<td width="208" class="moh-rteTableFooterOddCol-6">.*?([0-9,]+).*?</td>',
            MULTILINE|DOTALL
        ),
        rough_only=False
    ),
    'VIC': CaseURL(
        'https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19',
        href='.field--item a',
        regex=compile(r'([0-9,]+) Victorians have been tested'),
        rough_only=False
    ),
    'QLD': CaseURL(
        'https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status',
        href='#qg-primary-content a',
        regex=compile(r'<strong>Total</strong></td><td headers="table.*?"><strong>([0-9,]+)</strong>'),
        rough_only=False
    ),
    'WA': CaseURL(
        'https://ww2.health.wa.gov.au/News/Media-releases-listing-page',
        href='div.threeCol-accordian a',
        regex=(
            # Seems the WA website's wording can change day-to-day
            compile(r'([0-9]+[0-9,]*)(.*?negative COVID-19 tests|.*?tested negative|.*?negative)'),
            compile(r'total to ([0-9,]+)')
        ),
        rough_only=False
    ),
    'SA': CaseURL(
        'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/'
            'SA+Health+Internet/About+us/News+and+media/all+media+releases/',
        href='.news a',
        regex=compile(r'undertaken more than ([0-9,]+) tests'),
        rough_only=True
    ),
    'ACT': CaseURL(
        'https://www.health.act.gov.au/about-our-health-system/'
            'novel-coronavirus-covid-19',
        href='.latestnewsinner a',
        regex=(
            compile(r'tested negative is now ([0-9,]+)'),
            compile(r'confirmed cases in the ACT is now ([0-9,]+)')
        ),
        rough_only=False
    ),
    #'nt': CaseURL(
    #    'https://securent.nt.gov.au/alerts/coronavirus-covid-19-updates'
    #),
    'TAS': CaseURL(
        'https://www.dhhs.tas.gov.au/news/2020',
        href='table.dhhs a',
        regex=compile('([0-9,]+) coronavirus tests had been completed'),
        rough_only=False
    )
}


def get_total_cases_tested():
    total_cases_dict = {}

    for state_name, case_url in urls_dict.items():
        print(f"{state_name}: Getting listing for URL {case_url.url}...")
        q = pq(url=case_url.url, parser='html')

        for href_elm in q(case_url.href):
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
                    parsed = urlparse(case_url.url)
                    href = f'{parsed.scheme}://{parsed.netloc}/{href[1:]}'

                print(f'{state_name}: Trying href with text "{href_elm.text()}"')
                total_cases = get_from_subpage(
                    href,
                    case_url.regex
                )
                if total_cases is None:
                    print(f"{state_name}: Warning: not found, trying next URL")
                else:
                    print(f"{state_name}: Found ")
                    if case_url.rough_only:
                        total_cases_dict[state_name] = "> " + str(total_cases)
                    else:
                        total_cases_dict[state_name] = str(total_cases)
                    break

        print()

    total_cases_dict['NT'] = 'N/A' # HACK! =================================
    return total_cases_dict


def get_from_subpage(url, regex):
    print(f"    Getting from subpage {url}...")

    def do_search(regex):
        # Remove numeral grouping X,XXX
        match = regex.search(html)
        # print(regex, match)
        if match:
            num = match.group(1)
            num = num.replace(',', '')
            if num.isdecimal():
                return int(num)
        return None

    with urlopen(url) as req:
        html = req.read().decode('utf-8', 'replace')

        if isinstance(regex, (tuple, list)):
            # Two regexes: (negative, positive
            neg = do_search(regex[0])
            pos = do_search(regex[1])
            if neg and pos:
                return pos+neg
            else:
                return None
        else:
            return do_search(regex)


if __name__ == '__main__':
    import json
    import datetime

    r = get_total_cases_tested()
    print()

    today = datetime.date.today()
    print('"'+today.strftime('%Y-%m-%d')+'"', end=": ")
    print(json.dumps(r, indent=4))
