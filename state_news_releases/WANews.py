from pyquery import PyQuery as pq
from re import compile, IGNORECASE, MULTILINE, DOTALL

from covid_19_au_grab.state_news_releases.StateNewsBase import \
    StateNewsBase, singledaystat
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_TESTED, DT_CASES, \
    DT_SOURCE_OF_INFECTION, \
    DT_NEW_CASES_BY_REGION, DT_CASES_BY_REGION, DT_NEW_CASES, \
    DT_NEW_MALE, DT_NEW_FEMALE, \
    DT_RECOVERED, DT_DEATHS
from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.word_to_number import word_to_number
from covid_19_au_grab.URLArchiver import URLArchiver


class WANews(StateNewsBase):
    STATE_NAME = 'wa'
    LISTING_URL = 'https://ww2.health.wa.gov.au/News/' \
                  'Media-releases-listing-page'
    LISTING_HREF_SELECTOR = 'div.threeCol-accordian a'
    STATS_BY_REGION_URL = 'https://ww2.health.wa.gov.au/' \
                          'Articles/A_E/Coronavirus/' \
                          'COVID19-statistics'

    # This is only used by the wa map
    WA_CUSTOM_MAP_URL = 'https://services.arcgis.com/Qxcws3oU4ypcnx4H/arcgis/rest/' \
                        'services/confirmed_cases_by_LGA/FeatureServer/0/query?' \
                        'f=json&' \
                        'where=Confirmed_cases%20%3C%3E%200&' \
                        'returnGeometry=false&' \
                        'spatialRel=esriSpatialRelIntersects&' \
                        'geometryType=esriGeometryEnvelope&' \
                        'inSR=102100&outFields=*&' \
                        'outSR=102100&resultType=tile'

    def get_data(self):
        r = []

        # WA-specific maps archiver
        wa_custom_map_ua = URLArchiver(f'{self.STATE_NAME}/custom_map')
        wa_custom_map_ua.get_url_data(self.WA_CUSTOM_MAP_URL, cache=True)   #  TODO: Should this be cached?? ===

        for period in wa_custom_map_ua.iter_periods():
            for subperiod_id, subdir in wa_custom_map_ua.iter_paths_for_period(period):
                path = wa_custom_map_ua.get_path(subdir)

                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    json_text = f.read()

                print("JSON:", json_text)
                cbr = self._get_total_cases_by_region(
                    self.WA_CUSTOM_MAP_URL,
                    (json_text, subdir.split('-')[0])
                )
                if cbr:
                    r.extend(cbr)

        r.extend(
            StateNewsBase.get_data(self)
        )
        return r

    def _get_date(self, url, html):
        # e.g. "24 March 2020"
        if url == self.STATS_BY_REGION_URL:
            regex = compile(
                '<strong>As of ([^<]+?)</strong>',
                IGNORECASE
            )
            match = regex.search(html)
            date = match.group(1)
        else:
            try:
                date = pq((
                    pq(html)('.newsCreatedDate') or
                    self._pq_contains(
                        html, 'div p strong p', 'As of',
                        ignore_case=True
                    )
                )[0]).text().strip()

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
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            compile('reported ([0-9,]+) new cases'),
            c_html,
            source_url=url,
            datatype=DT_NEW_CASES,
            date_updated=self._get_date(url, html)
        ) or self._extract_number_using_regex(
            compile('([0-9,]+) Western Australians who have tested positive'),
            c_html,
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

        c_html = word_to_number(html)

        r = []

        # Get male breakdown
        male = self._extract_number_using_regex(
            compile('[^0-9.]+([0-9,]+) male(?:s)?'),
            c_html,
            source_url=url,
            datatype=DT_NEW_MALE,
            date_updated=self._get_date(url, html)
        )
        if male:
            r.append(male)

        # Get female breakdown
        female = self._extract_number_using_regex(
            compile('[^0-9.]+([0-9,]+) female(?:s)?'),
            c_html,
            source_url=url,
            datatype=DT_NEW_FEMALE,
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
        if url != self.WA_CUSTOM_MAP_URL:
            return None

        json_text, period = html
        from json import loads
        data = loads(json_text)  # Not actually html

        r = []
        for feature_dict in data['features']:
            """
            {
                "attributes":{
                    "OBJECTID":145,
                    "LGA_CODE19":"50080",
                    "LGA_NAME19":"Albany (C)",
                    "AREASQKM19":4310.8905,
                    "Metro_WACHS":"WACHS",
                    "Pop65_plus":7781,
                    "Pop_total_18":37826,
                    "Confirmed_cases":6,
                    "Classification":"6 - 10",
                    "Shape__Area":6399054898.15234,
                    "Shape__Length":910942.011045383,
                    "LGA_Name_Full":"City of Albany  "
                }, ...
            }
            """
            attributes = feature_dict['attributes']

            num = DataPoint(
                name=attributes['LGA_NAME19'].split('(')[0].strip(),
                datatype=DT_CASES_BY_REGION,
                value=attributes['Confirmed_cases'],
                date_updated=period,
                source_url='https://ww2.health.wa.gov.au/Articles/A_E/Coronavirus/COVID19-statistics',
                text_match=None
            )
            r.append(num)
        return r


    #============================================================#
    #                     Totals by Source                       #
    #============================================================#

    def _get_new_source_of_infection(self, url, html):
        pass

    @singledaystat
    def _get_total_source_of_infection(self, url, html):
        c_html = word_to_number(html)

        unknown_source = self._extract_number_using_regex(
            compile(
                '<td[^>]*?>Unknown source</td>[^<]*?'
                '<td[^>]*?>([0-9,]+)</td>',
                MULTILINE | DOTALL
            ),
            c_html,
            source_url=url,
            datatype=DT_SOURCE_OF_INFECTION,
            date_updated=self._get_date(url, html)
        )
        if unknown_source:
            return (unknown_source,)
        return None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    @singledaystat
    def _get_total_dhr(self, href, html):
        r = []
        c_html = word_to_number(html)

        recovered = self._extract_number_using_regex(
            compile(
                '<td[^>]*?>Recovered</td>[^<]*?'
                '<td[^>]*?>([0-9,]+)</td>',
                MULTILINE | DOTALL
            ),
            c_html,
            source_url=href,
            datatype=DT_RECOVERED,
            date_updated=self._get_date(href, html)
        )
        if recovered:
            r.append(recovered)

        deaths = self._extract_number_using_regex(
            compile(
                '<td[^>]*?>Deaths</td>[^<]*?'
                '<td[^>]*?>([0-9,]+)</td>',
                MULTILINE | DOTALL
            ),
            c_html,
            source_url=href,
            datatype=DT_DEATHS,
            date_updated=self._get_date(href, html)
        )
        if deaths:
            r.append(deaths)
        return r


if __name__ == '__main__':
    from pprint import pprint
    wn = WANews()
    pprint(wn.get_data())
