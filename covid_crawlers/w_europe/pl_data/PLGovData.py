import csv
from pyquery import PyQuery as pq

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir


class PLGovData(URLBase):
    SOURCE_URL = 'https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'pl_gov'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'pl' / 'govdata',
            urls_dict=self.__get_urls_dict()
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('admin_1', 'pl', 'pl-02'): ('admin_1', 'pl', 'pl-ds'),
                ('admin_1', 'pl', 'pl-04'): ('admin_1', 'pl', 'pl-kp'),
                ('admin_1', 'pl', 'pl-06'): ('admin_1', 'pl', 'pl-lu'),
                ('admin_1', 'pl', 'pl-08'): ('admin_1', 'pl', 'pl-lb'),
                ('admin_1', 'pl', 'pl-14'): ('admin_1', 'pl', 'pl-mz'),
                ('admin_1', 'pl', 'pl-12'): ('admin_1', 'pl', 'pl-ma'),
                ('admin_1', 'pl', 'pl-16'): ('admin_1', 'pl', 'pl-op'),
                ('admin_1', 'pl', 'pl-18'): ('admin_1', 'pl', 'pl-pk'),
                ('admin_1', 'pl', 'pl-20'): ('admin_1', 'pl', 'pl-pd'),
                ('admin_1', 'pl', 'pl-22'): ('admin_1', 'pl', 'pl-pm'),
                ('admin_1', 'pl', 'pl-28'): ('admin_1', 'pl', 'pl-wn'),
                ('admin_1', 'pl', 'pl-30'): ('admin_1', 'pl', 'pl-wp'),
                ('admin_1', 'pl', 'pl-32'): ('admin_1', 'pl', 'pl-zp'),
                ('admin_1', 'pl', 'pl-10'): ('admin_1', 'pl', 'pl-ld'),
                ('admin_1', 'pl', 'pl-24'): ('admin_1', 'pl', 'pl-sl'),
                ('admin_1', 'pl', 'pl-26'): ('admin_1', 'pl', 'pl-sk'),
            },
            mode=MODE_STRICT
        )
        self.update()

    def __get_urls_dict(self):
        r = {}
        for listing_url, typ, key in (
            (
                'https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2',
                'Taux de positivité - quotidien - département',
                'admin1.csv'
            ),
            (
                'https://www.gov.pl/web/koronawirus/mapa-zarazen-koronawirusem-sars-cov-2-powiaty',
                'Taux de positivité - quotidien - région',
                'powiat.csv'
            ),
        ):
            html = pq(listing_url)
            r[key] = URL(html(f'a:contains("rejestr.csv")').attr('href'), static_file=False)
        return r

    def get_datapoints(self):
        r = []
        #r.extend(self._get_admin1())
        #r.extend(self._get_powiat())
        return r

    def _get_admin1(self):
        # wojewodztwo	liczba_przypadkow	liczba_na_10_tys_mieszkancow
        # zgony	zgony_w_wyniku_covid_bez_chorob_wspolistniejacych
        # zgony_w_wyniku_covid_i_chorob_wspolistniejacych	teryt
        # voivodeship
        # number of cases
        # number per 10,000 inhabitants
        # deaths
        # deaths as a result of covid without comorbidities
        # deaths as a result of covid and comorbidities
        # terit
        # Cały kraj	6945	1	81	102	18	84	t00

        r = self.sdpf()

        for date in self.iter_nonempty_dirs(self.output_dir):
            with open(self.output_dir / date / 'admin1.csv', 'r',
                      encoding='iso-8859-2') as f:

                for item in csv.DictReader(f, delimiter=';'):
                    values = {
                        DataTypes.TOTAL: item['liczba_przypadkow'],
                        DataTypes.STATUS_DEATHS: item['zgony']
                    }

                    for datatype, value in values.items():
                        if item['wojewodztwo'].lower() == 'cały kraj':
                            r.append(
                                region_schema=Schemas.ADMIN_0,
                                region_parent='',
                                region_child='PL',
                                datatype=datatype,
                                value=value,
                                date_updated=date,
                                source_url=self.SOURCE_URL
                            )
                        else:
                            r.append(
                                region_schema=Schemas.ADMIN_1,
                                region_parent='PL',
                                region_child='PL-%s' % item['teryt'].lstrip('t'),
                                datatype=datatype,
                                value=value,
                                date_updated=date,
                                source_url=self.SOURCE_URL
                            )

        return r

    def _get_powiat(self):
        # TODO!
        r = self.sdpf()
        f = self.get_file('powiat.csv',
                          encoding='iso-8859-2',
                          include_revision=True)

        for item in csv.DictReader(f):
            date = self.convert_date(item['jour'])

            r.append(
                region_schema=Schemas.PL_POWIAT,
                region_parent='FR',
                region_child=region_child,
                agerange=agerange,
                datatype=DataTypes.TESTS_TOTAL,
                value=tests_totals_by_age[agerange, region_child],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(PLGovData().get_datapoints())
