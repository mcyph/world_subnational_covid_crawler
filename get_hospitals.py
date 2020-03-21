from re import compile
from collections import namedtuple
from pyquery import PyQuery as pq


Hospital = namedtuple('Hospital', [
    'name', 'location', 'message', 'phone', 'opening_hours'
])


def get_hospitals():
    return _GetHospitals().get_hospitals()


class _GetHospitals:
    def __init__(self):
        self._states = {
            'VIC': self._get_for_vic,
            'NSW': self._get_for_nsw,
            'WA': self._get_for_wa,
        }

    def get_hospitals(self):
        r = {}
        for state_name, fn in self._states.items():
            r[state_name] = fn()
        return r

    def _get_for_wa(self):
        html = pq(
            url='https://pathwest.health.wa.gov.au/'
                'COVID-19/Pages/default.aspx',
            parser='html'
        )
        section = html('p:contains("Where can I be tested?")') \
                       .next_all()
        ul = pq(section('ul')[0])
        hospitals = []

        for li in ul('li'):
            li = pq(li)
            text = li.text()
            name, _, address = text.partition('-')
            name = name.strip()
            address = address.strip()
            hospitals.append(Hospital(
                name=name,
                location=address,
                message=None,
                phone=None,
                opening_hours=None
            ))
        return hospitals

    def _get_for_nsw(self):
        html = pq(
            url='https://www.health.nsw.gov.au/Infectious/diseases/'
                'Pages/coronavirus-clinics.aspx',
            parser='html'
        )

        table = html('table.moh-rteTable-6')
        hospitals = []

        for x, tr in enumerate(table('tr')):
            if not x: continue
            tr = pq(tr)
            name = pq(tr('th')[0]).text().strip()
            address, opening_hours = tr('td')[0], tr('td')[1]
            address = pq(address).text().strip()
            opening_hours = pq(opening_hours).text().strip()
            hospitals.append(Hospital(
                name=name,
                location=address,
                message=None,
                phone=None,
                opening_hours=opening_hours
            ))
        return hospitals

    def _get_for_vic(self):
        html = pq(
            url='https://www.dhhs.vic.gov.au/'
                'victorian-public-coronavirus-disease-covid-19',
            parser='html'
        )
        next_ul = html("div.field section ul")[0]

        hospitals = []
        VIC_RE = compile(r'^(.*?)(-.*)?(\(.*?\))?$')

        for li in pq(next_ul)('li'):
            li = pq(li)
            text = li.text().strip().replace('–', '-')
            match = VIC_RE.match(text)

            name, location, message = match.groups()
            if location is not None:
                location = location.strip(' -')
            if message is not None:
                message = message.strip().strip('()').strip()

            hospitals.append(Hospital(
                name=name.strip(),
                location=location,
                message=message,
                phone=None,  # TODO!
                opening_hours=None
            ))
        return hospitals


if __name__ == '__main__':
    print(_GetHospitals()._get_for_wa())
    #print(_GetHospitals()._get_for_vic())
    #print(_GetHospitals()._get_for_nsw())
