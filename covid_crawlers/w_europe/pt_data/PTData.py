NATIONAL_URL = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_view/FeatureServer/0/query?f=json&where=casosconfirmados IS NOT NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=datarelatorio asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true'
#MUNICIPALITY_URL = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID_Concelhos_ConcelhosDetalhes/FeatureServer/0/query?f=json&where=ConfirmadosAcumulado_Conc>0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=ConfirmadosAcumulado_Conc desc&resultOffset=0&resultRecordCount=318&resultType=standard&cacheHint=true'
MUNICIPALITY_URL = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/IncidenciaCOVIDporConc100k_view/FeatureServer/0/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Valorincid desc&outSR=102100&resultOffset=0&resultRecordCount=310&resultType=standard&cacheHint=true'.replace(' ', '%20')

# might be useful
# https://miguelrofer.carto.com/tables/portugal_municipios/public

import json
import datetime
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir
from covid_db.datatypes.DatapointMerger import DataPointMerger


'''
PT-01 	Aveiro
PT-02 	Beja
PT-03 	Braga
PT-04 	Bragança
PT-05 	Castelo Branco
PT-06 	Coimbra
PT-07 	Évora
PT-08 	Faro
PT-09 	Guarda
PT-10 	Leiria
PT-11 	Lisboa
PT-12 	Portalegre
PT-13 	Porto
PT-14 	Santarém
PT-15 	Setúbal
PT-16 	Viana do Castelo
PT-17 	Vila Real
PT-18 	Viseu
PT-20	Região Autónoma dos Açores
PT-30	Região Autónoma da Madeira
'''


class PTData(URLBase):
    SOURCE_URL = 'https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'pt_dash'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'pt' / 'data',
            urls_dict={
                'national_data.json': URL(NATIONAL_URL.replace(' ', '%20'), static_file=False),
                'municipality_data.json': URL(MUNICIPALITY_URL.replace(' ', '%20'), static_file=False)
            }
        )
        self.sdpf = StrictDataPointsFactory(
            region_mappings={
                ('pt_municipality', 'pt', 'guimarães'): None,
                ('pt_municipality', 'pt', 'tavira'): None,
                ('pt_municipality', 'pt', 'lagoa (faro)'): None,
                ('pt_municipality', 'pt', 'vila da praia da vitória'): None,
                ('pt_municipality', 'pt', 'ponte de sor'): None,
                ('pt_municipality', 'pt', 'calheta (açores)'): None,
                ('pt_municipality', 'pt', 'calheta [r.a. açores]'): None,
                ('pt_municipality', 'pt', 'lagoa [r.a. açores]'): None,
                ('pt_municipality', 'pt', 'calheta de são jorge'): None,
                ('pt_municipality', 'pt', 'calheta [r.a. madeira]'): None,
            },
            mode=MODE_STRICT
        )
        self.update()

    def get_datapoints(self):
        r = []
        #r.extend(self._get_municipality_data())
        r.extend(self._get_national_data())
        return r

    def _get_municipality_data(self):
        out = DataPointMerger()
        base_dir = self.get_path_in_dir('')

        for date in self.iter_nonempty_dirs(base_dir):
            r = self.sdpf()
            path = f'{base_dir}/{date}/municipality_data.json'
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
            except UnicodeDecodeError:
                import brotli
                with open(path, 'rb') as f:
                    data = json.loads(brotli.decompress(f.read()).decode('utf-8'))

            if not 'features' in data and date <= '2020_12_21':
                continue

            for feature in data['features']:
                attributes = feature['attributes']

                if date >= '2020_12_22':
                    #print(attributes)

                    # formula is incidence = (cases / population) * 100000
                    # incidence / 100000 = cases / population
                    # incidence / 100000 * population = cases
                    confirmed = round(attributes['Incidência']/100000*attributes['Total']) if attributes['Incidência'] else 0

                    if confirmed is not None:
                        r.append(
                            region_schema=Schemas.PT_MUNICIPALITY,
                            region_parent='PT',  # 'Distrito' -> district??
                            region_child=attributes['Concelho'],
                            datatype=DataTypes.TOTAL,
                            value=confirmed,
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )
                else:
                    if attributes['Data_Conc'] is None:
                        continue

                    # Only confirmed and deaths are shown in the dashboard
                    date = datetime.datetime.fromtimestamp(attributes['Data_Conc']/1000.0).strftime('%Y_%m_%d')
                    confirmed = attributes['ConfirmadosAcumulado_Conc']

                    if confirmed is not None:
                        r.append(
                            region_schema=Schemas.PT_MUNICIPALITY,
                            region_parent='PT', # 'Distrito' -> district??
                            region_child=attributes['Concelho'],
                            datatype=DataTypes.TOTAL,
                            value=int(confirmed),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        )

            out.extend(r)
        return out

    def _get_national_data(self):
        r = []
        base_dir = self.get_path_in_dir('')

        for date in sorted(listdir(base_dir)):
            path = f'{base_dir}/{date}/national_data.json'
            #with open(path, 'r', encoding='utf-8') as f:
            #    data = json.loads(f.read())

        return r


if __name__ == '__main__':
    from pprint import pprint
    dp = PTData().get_datapoints()
    pprint(dp)
