import json
import datetime
from os import listdir
from collections import Counter

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)


_provinces = '''
ES-C	GA	Bizkaia
ES-C	GA	Coruña, A
ES-VI	PV	Álava
ES-VI	PV	araba/álava
ES-AB	CM	Albacete
ES-A	VC	Alicante Alacan
ES-A	VC	alicante/alacant
ES-AL	AN	Almería
ES-O	AS	Asturias
ES-AV	CL	Ávila
ES-BA	EX	Badajoz
ES-PM	IB	Balears
ES-PM	IB	balears, illes
ES-B	CT	Barcelona
ES-BI	PV	Bizkaia
ES-BU	CL	Burgos 
ES-CC	EX	Cáceres 
ES-CA	AN	Cádiz 
ES-S	CB	Cantabria 
ES-CS	VC	Castellón Castell
ES-CS	VC	castellón/castelló
ES-CR	CM	Ciudad Real 
ES-CO	AN	Córdoba 
ES-CU	CM	Cuenca 
ES-SS	PV	Gipuzkoa
ES-GI	CT	Girona
ES-GR	AN	Granada 
ES-GU	CM	Guadalajara 
ES-H	AN	Huelva 
ES-HU	AR	Huesca 
ES-J	AN	Jaén 
ES-LO	RI	La Rioja 
ES-LO	RI	rioja, la 
ES-GC	CN	Las Palmas 
ES-GC	CN	palmas, las 
ES-LE	CL	León 
ES-L	CT	Lleida
ES-LU	GA	Lugo
ES-M	MD	Madrid 
ES-MA	AN	Málaga 
ES-MU	MC	Murcia 
ES-NA	NC	Navarra
ES-OR	GA	Ourense
ES-P	CL	Palencia 
ES-PO	GA	Pontevedra
ES-SA	CL	Salamanca 
ES-TF	CN	Santa Cruz de Tenerife
ES-SG	CL	Segovia
ES-SE	AN	Sevilla
ES-SO	CL	Soria
ES-T	CT	Tarragona
ES-TE	AR	Teruel
ES-TO	CM	Toledo
ES-V	VC	Valencia
ES-V	VC	valencia/valència
ES-VA	CL	Valladolid
ES-ZA	CL	Zamora
ES-Z	AR	Zaragoza
'''.strip()


def _get_provinces_map():
    province_map = {}
    for province_code, ac_code, province_name in [
        i.split('\t') for i in _provinces.split('\n')
    ]:
        province_map[province_name.lower().strip()] = (
            province_code, 'ES-'+ac_code
        )
    return province_map


_provinces_map = _get_provinces_map()

START = '<h3>Curva epidémica</h3>'
END = '</script>'


class ESISCIIIData(URLBase):
    SOURCE_URL = 'https://cnecovid.isciii.es/covid19/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'es_iscii'

    def __init__(self):
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / 'es' / 'isciii_data',
            urls_dict={
                'index.html': URL('https://cnecovid.isciii.es/covid19/',
                                   static_file=False),
            }
        )
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_datapoints())
        return r

    def _get_datapoints(self):
        r = []
        text = self.get_text('index.html', include_revision=True)
        text = text.split(START)[-1]
        text = text.split('<script type="application/json"')[1]
        text = text.split('">')[1]
        text = text.split(END)[0]
        data = json.loads(text)

        for label_item, data_item in zip(data['x']['layout']['updatemenus'][0]['buttons'], data['x']['data']):
            print(label_item)
            print(data_item)

            region = label_item['label']
            if region in ('España', 'Ceuta', 'Melilla'):
                continue

            region = _provinces_map[region.lower()][0]
            dates = data_item['x']
            values = data_item['y']
            print(region, dates, values)

            running_total = 0
            for date, value in zip(dates, values):
                date = self.convert_date(date)
                running_total += value

                r.append(DataPoint(
                    region_schema=Schemas.ES_PROVINCE,
                    region_parent='ES',
                    region_child=region,
                    datatype=DataTypes.NEW,
                    value=int(value),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))
                r.append(DataPoint(
                    region_schema=Schemas.ES_PROVINCE,
                    region_parent='ES',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    value=int(running_total),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(ESISCIIIData().get_datapoints())
