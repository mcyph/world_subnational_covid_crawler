from re import compile
from pyquery import PyQuery as pq
from collections import namedtuple


Hospital = namedtuple('Hospital', [
    'name', 'location', 'message', 'phone', 'opening_hours'
])


def get_hospitals_dict():
    return _GetHospitals().get_hospitals_dict()


class _GetHospitals:
    def __init__(self):
        self._states = {
            'VIC': self._get_for_vic,
            'NSW': self._get_for_nsw,
            'WA': self._get_for_wa,
            'SA': self._get_for_sa,
            'TAS': self._get_for_tas,
        }

    def get_hospitals_dict(self):
        r = {}
        for state_name, fn in self._states.items():
            r[state_name] = fn()
        return r

    _SA_DEDICATED_CLINIC = 0
    _SA_DRIVE_THRU_CLINIC = 1

    def _get_for_sa(self):
        html = pq(
            url='http://emergencydepartments.sa.gov.au/wps/wcm/connect/'
                'public+content/sa+health+internet/health+topics/'
                'health+topics+a+-+z/covid+2019/covid-19+response'
        )

        sections = (
            (
                ':contains("Dedicated COVID-19 clinics are open '
                'across metropolitan and regional South Australia.")',
                self._SA_DEDICATED_CLINIC
            ),
            (
                ':contains("Drive-through COVID-19 collection")',
                self._SA_DRIVE_THRU_CLINIC
            )
        )

        hospitals = []
        for selector, typ in sections:
            #print(selector, typ)
            p = html(selector)
            ul = pq(pq(p).next_all('ul')[0])

            for a in ul('a'):
                a = pq(a)
                name = a.text()
                href = a.attr('href')

                if 'PDF' in name:
                    hospitals.append(Hospital(
                        # FIXME!
                        name=name.split('(')[0].strip(),
                        location=None,
                        message=None,
                        phone=None,
                        opening_hours=None
                    ))
                elif href.startswith('http'):
                    hospitals.append(Hospital(
                        # FIXME! - royal adelaide hospital
                        # https://www.rah.sa.gov.au/news/coronavirus-novel-coronavirus-2019-ncov
                        name=name.split('(')[0].strip(),
                        location=None,
                        message=None,
                        phone=None,
                        opening_hours=None
                    ))
                else:
                    href = 'http://emergencydepartments.sa.gov.au' + href
                    hospitals.append(
                        self.__get_for_sa_clinic_testing_centre(name, href, typ)
                    )
        return hospitals

    def __get_for_sa_clinic_testing_centre(self, name, href, typ):
        #print(name, href, typ)
        html = pq(url=href)

        try:
            phone_p = pq(html('p:contains("Telephone:")')[0])
            #print("Phone:", phone_p.text())
            phone = phone_p.text() \
                           .strip() \
                           .split('\n')[0] \
                           .strip() \
                           .partition(':')[-1] \
                           .strip()
        except IndexError:
            phone = None

        try:
            address_p = pq((
                html('p:contains("address:")') or
                html('p:contains("Address:")')
            )[0])
            #print("Address:", address_p.text())
            address = pq(address_p[0]).text() \
                                      .strip() \
                                      .partition(':')[-1] \
                                      .strip() \
                                      .split('\n')[0] \
                                      .strip()
        except IndexError:
            address = None

        if typ == self._SA_DEDICATED_CLINIC:
            message = 'These clinics are for people who have COVID-19 symptoms ' \
                      '(especially fever or cough) AND have recently returned ' \
                      'from overseas  OR have had contact with a known COVID-19 ' \
                      'case.'
        elif typ == self._SA_DRIVE_THRU_CLINIC:
            message = 'Patients need a referral from their GP to access this service.'
        else:
            raise Exception()

        return Hospital(
            name=name,
            location=address,
            message=message,
            phone=phone,
            opening_hours=None  # ??? is this provided for some of them?
        )

    def _get_for_tas(self):
        html = pq(
            url='https://health.act.gov.au/about-our-health-system/'
                'novel-coronavirus-covid-19/getting-tested',
            parser='html'
        )
        TAS_RE = compile(
            r'^(?P<name>.*?)'
            r'(?P<location>\(.*?\))'
            r'(?P<opening_hours>Open.*?\.)?'
            r'(?P<message>.*?)?$'
        )
        p = html(
            ':contains("The ACT Respiratory Assessment Clinics are located at:")'
        )
        ul = pq(pq(p).next_all('ul')[0])

        # Example:
        # "Weston Creek Walk-in Centre (24 Parkinson St, Weston). " \
        # "Open 7:30 am – 10:00 pm daily, including public holidays. " \
        # "Please ensure you use a mask and hand sanitiser available at the front door."

        hospitals = []
        for li in ul('li'):
            match = TAS_RE.match(pq(li).text())
            hospital_dict = match.groupdict()

            for k, v in hospital_dict.items():
                if v:
                    hospital_dict[k] = v.strip('().').strip()

            hospital_dict['phone'] = None
            hospitals.append(Hospital(**hospital_dict))
        return hospitals

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
    #print(_GetHospitals()._get_for_wa())
    #print(_GetHospitals()._get_for_vic())
    #print(_GetHospitals()._get_for_nsw())
    #print(_GetHospitals()._get_for_tas())
    print(_GetHospitals()._get_for_sa())
