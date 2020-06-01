import re
import unicodedata
from covid_19_au_grab.datatypes.constants import constant_to_name, schema_to_name

from covid_19_au_grab.overseas.humdata.af_data.AFData import AFData
from covid_19_au_grab.overseas.humdata.co_data.COData import COData
from covid_19_au_grab.overseas.humdata.et_data.ETData import ETData
from covid_19_au_grab.overseas.humdata.ht_data.HTData import HTData
from covid_19_au_grab.overseas.humdata.iq_data.IQData import IQData
#from covid_19_au_grab.overseas.kz_data.KZData import KZData
from covid_19_au_grab.overseas.humdata.ly_data.LYData import LYData
#from covid_19_au_grab.overseas.ml_data.MLData import MLData
from covid_19_au_grab.overseas.humdata.sn_data.SNData import SNData
from covid_19_au_grab.overseas.humdata.so_data.SOData import SOData
from covid_19_au_grab.overseas.humdata.ve_data.VEData import VEData

from covid_19_au_grab.overseas.bd_data.BDData import BDData
from covid_19_au_grab.overseas.br_data.BRData import BRData
from covid_19_au_grab.overseas.ch_data.CHData import CHData
from covid_19_au_grab.overseas.de_data.DEData import DEData
from covid_19_au_grab.overseas.es_data.ESData import ESData
from covid_19_au_grab.overseas.eu_subnational_data.EUSubNationalData import EUSubNationalData
from covid_19_au_grab.overseas.fr_data.FRData import FRData
#from covid_19_au_grab.overseas.gh_data.GHData import GHData
from covid_19_au_grab.overseas.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.overseas.in_data.INData import INData
from covid_19_au_grab.overseas.it_data.ITData import ITData
from covid_19_au_grab.overseas.jp_data.JPData import JPData
from covid_19_au_grab.overseas.jp_city_data.JPCityData import JPCityData
from covid_19_au_grab.overseas.kr_data.KRData import KRData
from covid_19_au_grab.overseas.kz_data.KZData import KZData
#from covid_19_au_grab.overseas.mm_data.MMData import MMData
from covid_19_au_grab.overseas.my_data.MYData import MYData
from covid_19_au_grab.overseas.nz_data.NZData import NZData
#from covid_19_au_grab.overseas.ph_data.PHData import PHData
from covid_19_au_grab.overseas.ps_data.PSData import PSData
from covid_19_au_grab.overseas.sa_data.SAData import SAData
from covid_19_au_grab.overseas.uk_data.UKData import UKData
from covid_19_au_grab.overseas.us_nyt_data.USNYTData import USNYTData
from covid_19_au_grab.overseas.vn_data.VNData import VNData
#from covid_19_au_grab.overseas.us_covidtracking_data.USCovidTrackingData import USCovidTrackingData
#from covid_19_au_grab.overseas.world_eu_data.EUData import EUData
from covid_19_au_grab.overseas.west_africa_data.WestAfricaData import WestAfricaData
from covid_19_au_grab.overseas.world_bing_data.WorldBingData import WorldBingData
from covid_19_au_grab.overseas.world_jhu_data.WorldJHUData import WorldJHUData


def get_overseas_data():
    for i in [
        WestAfricaData,
        WorldJHUData,
        AFData,
        BDData,
        BRData,
        CHData,
        COData,
        DEData,
        ESData,
        ETData,
        EUSubNationalData,
        FRData,
        #GHData,
        HTData,
        IDGoogleDocsData,
        INData,
        IQData,
        ITData,
        JPData,
        JPCityData,
        KRData,
        KZData,
        LYData,
        #MLData,
        #MMData,
        MYData,
        NZData,
        #PHData,
        PSData,
        SAData,
        SNData,
        SOData,
        #THData,
        UKData,
        WorldBingData,
        USNYTData,
        VEData,
        VNData,
    ]:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        print("Getting using class:", i)
        inst = i()
        name = inst.__class__.__name__.replace('data', '_data')
        name = (
            name.partition('_')[0].lower().strip('_') +
            '_' +
            name.partition('_')[-1].strip('_')
        ).strip('_')
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        yield inst.SOURCE_URL, name, inst.get_datapoints()


def remove_control_characters(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C"
    )


if __name__ == '__main__':
    source_urls = []

    for source_url, overseas_name, overseas_data in get_overseas_data():
        source_urls.append(source_url)

        with open(f'covid_{overseas_name}.tsv', 'w', encoding='utf-8') as f:
            print("WRITING:", f'covid_{overseas_name}.tsv')
            f.write('region_parent\t'
                    'region_schema\t'
                    'region_child\t'
                    'datatype\t'
                    'agerange\t'
                    'value\t'
                    'date_updated\t'
                    'source_url\t'
                    'text_match\n')

            added = set()
            for datapoint in overseas_data:
                if datapoint in added:
                    continue
                added.add(datapoint)

                try:
                    text_match = repr(remove_control_characters(
                        str(datapoint.text_match).replace("\t", " ")
                                                 .replace('\n', ' ')
                                                 .replace('\r', ' ')
                    ))
                except:
                    print("ERROR:", datapoint)
                    raise

                yyyy, mm, dd = datapoint.date_updated.split('_')
                backwards_date = f'{dd}/{mm}/{yyyy}'

                f.write(f'{schema_to_name(datapoint.region_schema)[7:].lower()}\t'
                        f'{datapoint.region_parent}\t'
                        f'{datapoint.region_child}\t'
                        f'{constant_to_name(datapoint.datatype)[3:].lower()}\t'
                        f'{datapoint.agerange}\t'
                        f'{datapoint.value}\t'
                        f'{backwards_date}\t'
                        f'{datapoint.source_url}\t'
                        f'{text_match}\n')

    for source_url in source_urls:
        print(f'* {source_url}')
