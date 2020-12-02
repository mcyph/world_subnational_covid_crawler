import csv
from collections import Counter

from covid_19_au_grab.covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir


region_map = dict([i.split('\t')[::-1] for i in """
BE-BRU	Brussels
BE-VLG	Vlaams
BE-WAL	Waals
BE-VAN	Antwerpen
BE-WBR	Brabantwallon
BE-WHT	Hainaut
BE-WLG	Liège
BE-VLI	Limburg
BE-WLX	Luxembourg
BE-WNA	Namur
BE-VOV	Oostvlaanderen
BE-VBR	Vlaamsbrabant
BE-VWV	Westvlaanderen
Unknown	na
""".lower().strip().split('\n')])


class BEData(URLBase):
    SOURCE_URL = 'https://epistat.wiv-isp.be/covid/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'be_epistat'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'be' / 'data',
            urls_dict={
                'cases_age_sex.csv': URL('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv', static_file=False),
                'cases_municipality_cumulative.csv': URL('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.csv', static_file=False),
                'cases_municipality.csv': URL('https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv', static_file=False),
                'cases_hospital.csv': URL('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv', static_file=False),
                'cases_mortality.csv': URL('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv', static_file=False),
                'cases_tests.csv': URL('https://epistat.sciensano.be/Data/COVID19BE_tests.csv', static_file=False),
            }
        )
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self.get_cases_age_sex())
        r.extend(self.get_cases_municipality_cumulative())
        r.extend(self.get_cases_municipality())
        return r

    def get_cases_age_sex(self):
        # DATE	PROVINCE	REGION	AGEGROUP	SEX	CASES
        # 2020-03-01	Antwerpen	Flanders	40-49	M	1
        # 2020-03-01	Brussels	Brussels	10-19	M	1
        # 2020-03-01	Brussels	Brussels	10-19	F	1
        r = self.sdpf()

        by_total = Counter()
        by_province = Counter()
        by_agerange = Counter()
        by_gender = Counter()

        for item in csv.DictReader(self.get_file('cases_age_sex.csv', include_revision=True)):
            if item['DATE'] == 'NA':
                continue
            date = self.convert_date(item['DATE'])
            region_child = region_map[item['PROVINCE'].lower()]
            agerange = item['AGEGROUP']
            num_cases = int(item['CASES'])

            by_total[date] += num_cases
            by_province[date, region_child] += num_cases
            by_agerange[date, agerange] += num_cases

            if item['SEX'] != 'NA':
                gender = {
                    'M': DataTypes.TOTAL_MALE,
                    'F': DataTypes.TOTAL_FEMALE
                }[item['SEX']]
                by_gender[date, gender] += num_cases

        cumulative = 0
        for date, value in sorted(by_total.items()):
            cumulative += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='BE',
                datatype=DataTypes.TOTAL,
                value=cumulative,
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (date, province), value in sorted(by_province.items()):
            cumulative[province] += value
            r.append(
                region_schema=Schemas.ADMIN_1,
                region_parent='BE',
                region_child=province,
                datatype=DataTypes.TOTAL,
                value=cumulative[province],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (date, agerange), value in sorted(by_agerange.items()):
            cumulative[agerange] += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='BE',
                datatype=DataTypes.TOTAL,
                agerange=agerange,
                value=cumulative[agerange],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        cumulative = Counter()
        for (date, gender), value in sorted(by_gender.items()):
            cumulative[gender] += value
            r.append(
                region_schema=Schemas.ADMIN_0,
                region_parent=None,
                region_child='BE',
                datatype=gender,
                value=cumulative[gender],
                date_updated=date,
                source_url=self.SOURCE_URL
            )

        return r

    def get_cases_municipality_cumulative(self):
        # NIS5	TX_DESCR_NL	TX_DESCR_FR	TX_ADM_DSTR_DESCR_NL	TX_ADM_DSTR_DESCR_FR	TX_PROV_DESCR_NL	TX_PROV_DESCR_FR	TX_RGN_DESCR_NL	TX_RGN_DESCR_FR	CASES
        # 11001	Aartselaar	Aartselaar	Arrondissement Antwerpen	Arrondissement d’Anvers	Provincie Antwerpen	Province d’Anvers	Vlaams Gewest	Région flamande	134
        # 11002	Antwerpen	Anvers	Arrondissement Antwerpen	Arrondissement d’Anvers	Provincie Antwerpen	Province d’Anvers	Vlaams Gewest	Région flamande	2746
        r = []
        return r

    def get_cases_municipality(self):
        # DATE	NIS5	TX_DESCR_NL	TX_DESCR_FR	TX_ADM_DSTR_DESCR_NL	TX_ADM_DSTR_DESCR_FR	TX_PROV_DESCR_NL	TX_PROV_DESCR_FR	TX_RGN_DESCR_NL	TX_RGN_DESCR_FR	CASES
        # 2020-03-01	11002	Antwerpen	Anvers	Arrondissement Antwerpen	Arrondissement d’Anvers	Provincie Antwerpen	Province d’Anvers	Vlaams Gewest	Région flamande	<5
        # 2020-03-01	21004	Brussel	Bruxelles	Arrondissement Brussel-Hoofdstad	Arrondissement de Bruxelles-Capitale	NA	NA	Brussels Hoofdstedelijk Gewest	Région de Bruxelles-Capitale	<5
        r = []
        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(BEData().get_datapoints())
