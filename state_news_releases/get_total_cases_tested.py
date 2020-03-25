from pyquery import PyQuery as pq
from urllib.parse import urlparse
from urllib.request import urlopen
from collections import namedtuple
from re import compile, MULTILINE, DOTALL


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
                print(f"    Found Match: {match.group()}")
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
