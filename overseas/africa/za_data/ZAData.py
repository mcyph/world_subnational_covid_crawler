import json
import datetime
from os import listdir
from pyquery import PyQuery as pq
from collections import Counter

from covid_19_au_grab.overseas.PressReleaseBase import PressReleaseBase
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.get_package_dir import get_overseas_dir, get_package_dir


class ZAData(PressReleaseBase):
    SOURCE_URL = 'https://sacoronavirus.co.za/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'za_gov'

    def __init__(self):
        PressReleaseBase.__init__(self,
            output_dir=get_overseas_dir() / 'za' / 'data',
            urls_dict={
                'pr_1.html': 'https://sacoronavirus.co.za/category/press-releases-and-notices/',
                'pr_2.html': 'https://sacoronavirus.co.za/category/press-releases-and-notices/page/2',
                'pr_3.html': 'https://sacoronavirus.co.za/category/press-releases-and-notices/page/3',
                'pr_4.html': 'https://sacoronavirus.co.za/category/press-releases-and-notices/page/4',
            },
            url_selector='h2 a:contains("Update on Covid-19")'
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'za', 'national'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def _get_date(self, href, html):
        date = self.convert_date(
            pq(html)('.updated.rich-snippet-hidden').text().strip().split('T')[0]
        )
        return date

    def get_datapoints(self):
        r = []
        for url, date, html in self.iter_press_releases():
            print(url, date)
            r.extend(self._get_total_datapoints(date, html))
            r.extend(self._get_recovered_death_datapoints(date, html))
        return r

    def _get_total_datapoints(self, date, html):
        r = self.sdpf()
        TRs = pq(html)('.NormalTable:contains("Total cases"):contains("New cases") tbody tr')

        if TRs:
            TRs = pq(html)('.NormalTable:contains("Total cases"):contains("New cases") tbody tr')

            for province, cases, new, percentage in TRs[1:]:
                province = self._elm_to_province(province)
                if province == 'total':
                    continue

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.TOTAL,
                    value=self._elm_to_int(cases),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.NEW,
                    value=self._elm_to_int(new),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
        else:
            TRs = pq(html)('.NormalTable:contains("Total cases") tbody tr')

            for tr in TRs[1:]:
                try:
                    province, cases, percentage = tr
                except ValueError:
                    province, cases = tr

                province = self._elm_to_province(province)
                if province == 'total':
                    continue

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.TOTAL,
                    value=self._elm_to_int(cases),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r

    def _get_recovered_death_datapoints(self, date, html):
        r = self.sdpf()

        TRsDeathsRecoveries = pq(html)('table.NormalTable:contains("Deaths"):contains("Recoveries") '
                       'tbody '
                       'tr')
        TRsDeathsRecoveriesActive = pq(html)('table.NormalTable:contains("Deaths"):contains("Recoveries"):contains("Active") '
                                       'tbody '
                                       'tr')

        if TRsDeathsRecoveriesActive:
            def append_me(province, deaths, recoveries, active):
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.STATUS_DEATHS,
                    value=self._elm_to_int(deaths),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=self._elm_to_int(recoveries),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=self._elm_to_int(active),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

            try:
                for province, deaths, recoveries, active in TRsDeathsRecoveries[1:]:
                    # print(pq(province).text(),
                    #      pq(deaths).text(),
                    #      pq(recoveries).text())
                    province = self._elm_to_province(province)
                    if province == 'total':
                        continue
                    append_me(province, deaths, recoveries, active)
            except:
                for province, deaths, recoveries, recoveries_pc, active in TRsDeathsRecoveries[1:]:
                    # print(pq(province).text(),
                    #      pq(deaths).text(),
                    #      pq(recoveries).text())
                    province = self._elm_to_province(province)
                    if province == 'total':
                        continue
                    append_me(province, deaths, recoveries, active)

        else:
            for province, deaths, recoveries in TRsDeathsRecoveries[1:]:
                #print(pq(province).text(),
                #      pq(deaths).text(),
                #      pq(recoveries).text())
                province = self._elm_to_province(province)
                if province == 'total':
                    continue

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.STATUS_DEATHS,
                    value=self._elm_to_int(deaths),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='ZA',
                    region_child=pq(province).text().strip(),
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=self._elm_to_int(recoveries),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r

    def _elm_to_int(self, elm):
        return int(pq(elm).text().replace(' ', ''))

    def _elm_to_province(self, elm):
        province = pq(elm).text().strip().lower()
        if province == 'kwazulu natal':
            province = 'ZA-KZN'
        return province


if __name__ == '__main__':
    from pprint import pprint
    pprint(ZAData().get_datapoints())
