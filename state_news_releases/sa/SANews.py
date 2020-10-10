import json
import datetime
from os import listdir
from re import compile
from pyquery import PyQuery as pq

from covid_19_au_grab.state_news_releases.StateNewsBase import (
    StateNewsBase, bothlistingandstat, singledaystat
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.word_to_number import word_to_number
from covid_19_au_grab.get_package_dir import get_package_dir, get_data_dir
from covid_19_au_grab.URLArchiver import URLArchiver
from covid_19_au_grab.datatypes.DatapointMerger import DataPointMerger


OUTPUT_DIR = get_package_dir() / 'state_news_releases' / 'sa' / 'output'
SA_MAP_DIR = get_data_dir() / 'sa' / 'custom_map'


# https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/about+us/news+and+media/all+media+releases/media+releases?mr-sort=date-desc&mr-pg=1
class SANews(StateNewsBase):
    STATE_NAME = 'sa'
    SOURCE_ISO_3166_2 = 'AU-SA'
    SOURCE_ID = 'au_sa_press_releases'
    SOURCE_ID_DASH = 'au_sa_dash'
    SOURCE_URL = 'https://www.covid-19.sa.gov.au'
    SOURCE_DESCRIPTION = ''

    #LISTING_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/'  \
    #              'SA+Health+Internet/About+us/News+and+media/all+media+releases/'
    LISTING_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/Public+Content/SA+Health+Internet/About+us/News+and+media/all+media+releases/?mr-sort=date-desc&mr-pg=1'

    LISTING_HREF_SELECTOR = '.news a, .article-list-item a.arrow-link'
    # SA actually has two URLS - the below and 'https://www.sa.gov.au/covid-19/
    #                                          latest-updates/daily-update/current' - SHOULD SUPPORT BOTH!!
    #STATS_BY_REGION_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/' \
    #                      'sa+health+internet/health+topics/health+topics+a+-+z/covid+2019/' \
    #                      'latest+updates/' \
    #                      'confirmed+and+suspected+cases+of+covid-19+in+south+australia'

    # Changed as of 23/4/2020!
    STATS_BY_REGION_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/conditions/infectious+diseases/covid+2019/latest+updates/covid-19+cases+in+south+australia'

    SA_CUSTOM_MAP_URL = 'https://www.covid-19.sa.gov.au/home/dashboard'

    # https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/conditions/infectious+diseases/covid+2019/latest+updates/covid-19+cases+in+south+australia
    def _get_date(self, href, html):
        #print("HREF:", href)
        try:
            # New format of updated SA website as of 23/4/2020
            date = pq(html)('.main-content p')[0]
            if '2020' in pq(date).text():
                return self._extract_date_using_format(
                    pq(date).text().split(',')[-1].strip()
                )
        except (ValueError, IndexError):
            pass

        if href == self.STATS_BY_REGION_URL:
            # Latest statistics – as of 4pm, 1 April 2020
            date = self._pq_contains(html, 'h2,h1,h3', 'Latest statistics',
                                     ignore_case=True).text().split(',')[-1].strip()
        else:
            try:
                # Fix for date at
                # http://emergencydepartments.sa.gov.au/wps/wcm/connect/public+content/
                # sa+health+internet/about+us/news+and+media/all+media+releases/
                # covid-19+update+17+april+2020
                date = pq(html)('div.wysiwyg h1, h1.page-heading').text().split('Update')[-1].strip()
                if date.count(' ') != 2:
                    date += ' 2020'
                return self._extract_date_using_format(
                    date
                )
            except (ValueError, IndexError):
                date = pq(pq(html)('div.middle-column div.wysiwyg p')[0]) \
                                   .text().strip().split(',')[-1].strip()

        try:
            # e.g. Monday, 30 March 2020
            return self._extract_date_using_format(date)
        except:
            # e.g. Sunday 22 March 2020
            return self._extract_date_using_format(date.partition(' ')[-1])

    def get_data(self):
        r = []

        SA_DASH_JSON_URL = 'https://www.covid-19.sa.gov.au/__data/assets/' \
                      'file/0004/145849/covid_19_daily.json'
        SA_DASH_URL = 'https://www.sahealth.sa.gov.au/wps/wcm/connect/' \
                      'public+content/sa+health+internet/conditions/' \
                      'infectious+diseases/covid+2019/covid-19+dashboard'
        ua = URLArchiver(f'sa/dashboard')
        ua.get_url_data(SA_DASH_JSON_URL, cache=False)

        i_r = DataPointMerger()
        for period in ua.iter_periods():
            for subperiod_id, subdir in ua.iter_paths_for_period(period):
                path = ua.get_path(subdir)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                i_r.extend(self._get_from_json(SA_DASH_URL, data))
        r.extend(i_r)

        i_r = DataPointMerger()
        for sub_dir in sorted(listdir(SA_MAP_DIR)):
            # OPEN ISSUE: only add the most recent?? ==========================================================================
            joined_dir = f'{SA_MAP_DIR}/{sub_dir}'
            for fnam in listdir(joined_dir):
                with open(f'{joined_dir}/{fnam}', 'r', encoding='utf-8') as f:
                    r.extend(self._get_total_cases_by_region(
                        self.SA_CUSTOM_MAP_URL, f.read()
                    ))
        r.extend(i_r)

        r.extend(StateNewsBase.get_data(self))
        return r

    def _get_from_json(self, url, data):
        # Additional time series data is also available:
        # 'laboratory_char'
        # 'newcase_sa_char'
        # travellers/expiations/compliance not currently used

        def parse_date(s):
            return datetime.datetime.strptime(
                ' '.join(s.split()[-3:]), '%d %B %Y'
            ).strftime('%Y_%m_%d')

        r = []
        base_data_date = parse_date(data['hp_date'])

        r.append(DataPoint(
            datatype=DataTypes.NEW,
            value=int(data['newcase_sa']),
            date_updated=base_data_date,
            source_url=url,
            source_id=self.SOURCE_ID_DASH
        ))
        r.append(DataPoint(
            datatype=DataTypes.TOTAL,
            value=int(data['todaycase_sa']),
            date_updated=base_data_date,
            source_url=url,
            source_id=self.SOURCE_ID_DASH
        ))
        r.append(DataPoint(
            datatype=DataTypes.STATUS_ICU,
            value=int(data['icu_sa']),
            date_updated=base_data_date,
            source_url=url,
            source_id=self.SOURCE_ID_DASH
        ))
        r.append(DataPoint(
            datatype=DataTypes.STATUS_DEATHS,
            value=int(data['deaths_sa']),
            date_updated=base_data_date,
            source_url=url,
            source_id=self.SOURCE_ID_DASH
        ))
        r.append(DataPoint(
            datatype=DataTypes.STATUS_RECOVERED,
            value=int(data['recovered_sa']),
            date_updated=base_data_date,
            source_url=url,
            source_id=self.SOURCE_ID_DASH
        ))

        for agerange, value in zip(
            data['age_char']['field_order'],
            data['age_char']['data']
        ):
            agerange = agerange.replace(' - ', '-')
            r.append(DataPoint(
                datatype=DataTypes.TOTAL,
                agerange=agerange,
                value=int(value),
                date_updated=parse_date(data['age_char']['datetime']),
                source_url=url,
                source_id=self.SOURCE_ID_DASH
            ))

        for gender, value in zip(
            data['gender_char']['field_order'],
            data['gender_char']['data']
        ):
            datatype = {
                'male': DataTypes.TOTAL_MALE,
                'female': DataTypes.TOTAL_FEMALE
            }[gender.lower()]

            r.append(DataPoint(
                datatype=datatype,
                value=int(value),
                date_updated=parse_date(data['gender_char']['datetime']),
                source_url=url,
                source_id=self.SOURCE_ID_DASH
            ))

        for source, value in zip(
            data['infection_char']['field_order'],
            data['infection_char']['data']
        ):
            datatype = {
                'overseas acquired': DataTypes.SOURCE_OVERSEAS,
                'contact confirmed': DataTypes.SOURCE_CONFIRMED,
                'interstate travel': DataTypes.SOURCE_INTERSTATE,
                'under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION,
                'locally acquired': DataTypes.SOURCE_COMMUNITY
            }[source.lower()]

            r.append(DataPoint(
                datatype=datatype,
                value=int(value),
                date_updated=parse_date(data['infection_char']['datetime']),
                source_url=url,
                source_id=self.SOURCE_ID_DASH
            ))
        return r

    #============================================================#
    #                      General Totals                        #
    #============================================================#

    def _get_total_new_cases(self, href, html):
        # FIXME!!!! ==================================================================================================
        'Eighteen people in South Australia have today tested positive'
        c_html = word_to_number(html)

        return self._extract_number_using_regex(
            (
                compile('([0-9,]+) (?:people|person)[^0-9<.]+?(?:have|has)(?: today)? tested positive'),
                compile('([0-9,]+) new (?:people have|person has)(?: today)? tested positive'),
                compile('([0-9,]+) new cases of COVID-19'),
            ),
            c_html,
            source_url=href,
            datatype=DataTypes.NEW,
            date_updated=self._get_date(href, html)
        )

    @bothlistingandstat
    def _get_total_cases(self, href, html):
        if href == self.STATS_BY_REGION_URL:
            #print(href, html)
            tr = self._pq_contains(html, 'tr', 'Confirmed cases',
                                   ignore_case=True)
            if not tr:
                return None
            tr = tr[0]

            cc = int(pq(tr[1]).text().strip())
            if cc is not None:
                return DataPoint(
                    datatype=DataTypes.TOTAL,
                    value=cc,
                    date_updated=self._get_date(href, html),
                    source_url=href
                )
            return None
        else:
            # 'There have now been a total of 385 confirmed cases in South Australia'
            c_html = word_to_number(html)

            return self._extract_number_using_regex(
                (
                    compile('total of ([0-9,]+) (?:confirmed|cases)'),
                    compile('total number of cases notified in SA remains at ([0-9,]+)')
                ),
                c_html,
                datatype=DataTypes.TOTAL,
                source_url=href,
                date_updated=self._get_date(href, html)
            )

    def _get_total_cases_tested(self, href, html):
        # This is only a rough value - is currently displayed as "> (value)"!
        return self._extract_number_using_regex(
            (
                compile(r'SA Pathology has conducted ([0-9,]+) COVID-19 laboratory tests'),
                compile(r'(?:undertaken (?:almost|more than) )?([0-9,]+)(?: COVID-19)? tests'),
            ),
            html,
            datatype=DataTypes.TESTS_TOTAL,
            source_url=href,
            date_updated=self._get_date(href, html)
        )

    #============================================================#
    #                      Age Breakdown                         #
    #============================================================#

    def _get_new_age_breakdown(self, href, html):
        pass

    @singledaystat
    def _get_total_age_breakdown(self, href, html):
        """
        Age Group	Female	Male	Total
        0-9	0	3	3
        10-19	6	4	10
        20-29	31	30	61
        30-39	25	20	45
        40-49	16	21	37
        50-59	40	37	77
        60-69	34	48	82
        70-79	22	24	46
        80-89	2	4	6
        90-100	0	0	0
        >100	0	0	0
        Grand Total	176	191	367
        """

        r = []
        #print("URL:", href)
        #print(html)
        table = self._pq_contains(
            html, 'table', 'Age Group',
            ignore_case=True
        )
        if not table:
            return None
        table = table[0]
        du = self._get_date(href, html)

        for age_group in (
            '0-9',
            '10-19',
            '20-29',
            '30-39',
            '40-49',
            '50-59',
            '60-69',
            '70-79',
            '80-89',
            '90-100',
            '>100'
        ):
            tds = self._pq_contains(table, 'tr', age_group)
            if not tds:
                continue

            tds = tds[0]
            if len(tds) < 4:
                # Earliest didn't have male/female breakdown
                male = None
                female = None
                total = int(pq(tds[1]).text())
            else:
                female = int(pq(tds[1]).text())
                male = int(pq(tds[2]).text())
                total = int(pq(tds[3]).text())

            for datatype, value in (
                (DataTypes.TOTAL_FEMALE, female),
                (DataTypes.TOTAL_MALE, male),
                (DataTypes.TOTAL, total)
            ):
                if value is None:
                    continue
                elif datatype in (DataTypes.TOTAL_FEMALE, DataTypes.TOTAL_MALE):
                    continue   # HACK: SA has stopped providing these values, so will stop providing them fullstop for now!!! ===========================================================

                r.append(DataPoint(
                    datatype=datatype,
                    agerange=age_group,
                    value=value,
                    date_updated=du,
                    source_url=href
                ))

        return r

    #============================================================#
    #                  Male/Female Breakdown                     #
    #============================================================#

    def _get_new_male_female_breakdown(self, url, html):
        pass

    @singledaystat
    def _get_total_male_female_breakdown(self, url, html):
        # We need the "Grand Total
        pass

    #============================================================#
    #                     Totals by Region                       #
    #============================================================#

    def _get_new_cases_by_region(self, href, html):
        pass

    def _get_total_cases_by_region(self, href, html):
        if href != self.SA_CUSTOM_MAP_URL:
            return None

        from json import loads
        data = loads(html)  # Not actually html

        r = []
        for feature_dict in data.get('features', []):
            """
            {
                {
                  "exceededTransferLimit": false,
                  "features": [
                    {
                      "attributes": {
                        "objectid": 52,
                        "lga_code18": "49399",
                        "lga_name18": "Unincorporated SA",
                        "ste_code16": "4",
                        "ste_name16": "South Australia",
                        "areasqkm18": 622489.4848,
                        "lga": 49399.0,
                        "lga_name": "Unincorporated SA",
                        "lga_code": 49399,
                        "date_time_20200401_1000": "1/4/2020 @ 10:00 am",
                        "positive_20200401_1000": 0,
                        "active_20200401_1000": 0,
                        "date_time_20200402_0000": "2/4/2020",
                        "positive_20200402_0000": 0,
                        "active_20200402_0000": 0,
                        ...
                      },
                      "geometry": {
                        "rings": [
                          [
                            }
            """

            #print(feature_dict)
            attributes = feature_dict['attributes']
            if attributes.get('exceedslimit'):
                continue

            for k, v in attributes.items():
                if k.startswith('positive'):
                    du = datetime.datetime.strptime(
                        k.split('_')[1], '%Y%m%d'
                    ).strftime('%Y_%m_%d')
                    if du == '2020_04_12':
                        # HACK: Ignore this unreliable datapoint!
                        continue
                    elif v is None:
                        continue

                    num = DataPoint(
                        region_schema=Schemas.LGA,
                        datatype=DataTypes.TOTAL,
                        region_child=attributes['lga_name'].split('(')[0].strip(),
                        value=int(v),
                        date_updated=du,
                        source_url=href,
                        source_id=self.SOURCE_ID_DASH
                    )
                    r.append(num)
                elif k.startswith('active'):
                    du = datetime.datetime.strptime(
                        k.split('_')[1], '%Y%m%d'
                    ).strftime('%Y_%m_%d')
                    if du == '2020_04_12':
                        # HACK: Ignore this unreliable datapoint!
                        continue
                    elif du <= '2020_04_15' and not int(v):
                        # HACK: early datapoints were of very low quality!
                        continue
                    elif v is None:
                        continue

                    num = DataPoint(
                        region_schema=Schemas.LGA,
                        datatype=DataTypes.STATUS_ACTIVE,
                        region_child=attributes['lga_name'].split('(')[0].strip(),
                        value=int(v),
                        date_updated=du,
                        source_url=href,
                        source_id=self.SOURCE_ID_DASH
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
        """
        Source 	Cases
        Overseas acquired 252
        Locally acquired (close contact of a confirmed case) 78
        Locally acquired (Interstate travel) 7
        Locally acquired (contact not identified) 3
        Under investigation 27
        TOTAL 367
        """
        html = html.replace('&nbsp;', ' ')
        r = []
        du = None

        # Normalise it with other states
        sa_norm_map = {
            'Overseas acquired': DataTypes.SOURCE_OVERSEAS,
            'Locally acquired (Interstate travel)': DataTypes.SOURCE_INTERSTATE,
            'Locally acquired (close contact of a confirmed case)': DataTypes.SOURCE_CONFIRMED,
            'Locally acquired (contact not identified)': DataTypes.SOURCE_COMMUNITY,
            'Under investigation': DataTypes.SOURCE_UNDER_INVESTIGATION
        }

        for k in (
            'Overseas acquired',
            'Locally acquired (close contact of a confirmed case)',
            'Locally acquired (Interstate travel)',
            'Locally acquired (contact not identified)',
            'Under investigation'
        ):
            tr = self._pq_contains(html, 'tr', k,
                                   ignore_case=True)
            if not tr:
                continue
            if du is None:
                du = self._get_date(url, html)

            tr = tr[0]
            c_icu = int(pq(tr[1]).text().strip())

            r.append(DataPoint(
                datatype=sa_norm_map[k],
                value=c_icu,
                date_updated=du,
                source_url=url
            ))
        return r or None

    #============================================================#
    #               Deaths/Hospitalized/Recovered                #
    #============================================================#

    @bothlistingandstat
    def _get_total_dhr(self, href, html):
        # TODO: Also support updates!
        # e.g. https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/about+us/news+and+media/all+media+releases/covid-19+update+15+april+2020

        if href == self.STATS_BY_REGION_URL:
            r = []
            #print(href)
            tr = self._pq_contains(html, 'tr', 'Cases in ICU',
                                   ignore_case=True)
            if not tr:
                return []

            tr = tr[0]
            du = self._get_date(href, html)

            c_icu = int(pq(tr[1]).text().strip())
            #print(c_icu)

            if c_icu is not None:
                r.append(DataPoint(
                    datatype=DataTypes.STATUS_ICU,
                    value=c_icu,
                    date_updated=du,
                    source_url=href
                ))

            tr = self._pq_contains(html, 'tr', 'Total deaths reported',
                                   ignore_case=True)[0]
            t_d = int(pq(tr[1]).text().strip())
            if t_d is not None:
                r.append(DataPoint(
                    datatype=DataTypes.STATUS_DEATHS,
                    value=t_d,
                    date_updated=du,
                    source_url=href
                ))

            tr = self._pq_contains(html, 'tr', 'Cases cleared of COVID-19',
                                   ignore_case=True)
            if tr:
                tr = tr[0]
                t_d = int(pq(tr[1]).text().strip())

                if t_d is not None:
                    r.append(DataPoint(
                        datatype=DataTypes.STATUS_RECOVERED,
                        value=t_d,
                        date_updated=du,
                        source_url=href
                    ))
            return r
        else:
            r = []
            c_html = word_to_number(html)
            du = self._get_date(href, html)

            active = self._extract_number_using_regex(
                compile('([0-9,]+) active cases? in SA'),
                c_html, href,
                datatype=DataTypes.STATUS_ACTIVE,
                date_updated=du
            )
            if active:
                r.append(active)

            recovered = self._extract_number_using_regex(
                compile('([0-9,]+) people have been cleared'),
                c_html, href,
                datatype=DataTypes.STATUS_RECOVERED,
                date_updated=du
            )
            if recovered:
                r.append(recovered)

            deaths = self._extract_number_using_regex(
                compile('([0-9,]+) reported deaths'),
                c_html, href,
                datatype=DataTypes.STATUS_DEATHS,
                date_updated=du
            )
            if deaths:
                r.append(deaths)

            hospital = self._extract_number_using_regex(
                compile('([0-9,]+) (?:person|people) remains? in hospital'),
                c_html, href,
                datatype=DataTypes.STATUS_HOSPITALIZED,
                date_updated=du
            )
            if hospital:
                r.append(hospital)

            return r


if __name__ == '__main__':
    from pprint import pprint
    sn = SANews()
    pprint(sn.get_data())
