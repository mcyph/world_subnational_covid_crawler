import re
import unicodedata
from covid_19_au_grab.state_news_releases.constants import constant_to_name, schema_to_name

from covid_19_au_grab.state_news_releases.overseas.humdata.af_data.AFData import AFData
from covid_19_au_grab.state_news_releases.overseas.br_data.BRData import BRData
from covid_19_au_grab.state_news_releases.overseas.ch_data.CHData import CHData
from covid_19_au_grab.state_news_releases.overseas.de_data.DEData import DEData
from covid_19_au_grab.state_news_releases.overseas.es_data.ESData import ESData
from covid_19_au_grab.state_news_releases.overseas.humdata.et_data.ETData import ETData
from covid_19_au_grab.state_news_releases.overseas.eu_subnational_data.EUSubNationalData import EUSubNationalData
from covid_19_au_grab.state_news_releases.overseas.fr_data.FRData import FRData
from covid_19_au_grab.state_news_releases.overseas.humdata.ht_data.HTData import HTData
from covid_19_au_grab.state_news_releases.overseas.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.state_news_releases.overseas.in_data.INData import INData
from covid_19_au_grab.state_news_releases.overseas.humdata.iq_data.IQData import IQData
from covid_19_au_grab.state_news_releases.overseas.it_data.ITData import ITData
from covid_19_au_grab.state_news_releases.overseas.jp_data.JPData import JPData
from covid_19_au_grab.state_news_releases.overseas.jp_city_data.JPCityData import JPCityData
from covid_19_au_grab.state_news_releases.overseas.kr_data.KRData import KRData
#from covid_19_au_grab.state_news_releases.overseas.kz_data.KZData import KZData
from covid_19_au_grab.state_news_releases.overseas.humdata.ly_data.LYData import LYData
#from covid_19_au_grab.state_news_releases.overseas.mm_data.MMData import MMData
#from covid_19_au_grab.state_news_releases.overseas.ml_data.MLData import MLData
from covid_19_au_grab.state_news_releases.overseas.my_data.MYData import MYData
from covid_19_au_grab.state_news_releases.overseas.nz_data.NZData import NZData
#from covid_19_au_grab.state_news_releases.overseas.ph_data.PHData import PHData
#from covid_19_au_grab.state_news_releases.overseas.ps_data.PSData import PSData
#from covid_19_au_grab.state_news_releases.overseas.sn_data.SNData import SNData
from covid_19_au_grab.state_news_releases.overseas.humdata.so_data.SOData import SOData
from covid_19_au_grab.state_news_releases.overseas.uk_data.UKData import UKData
from covid_19_au_grab.state_news_releases.overseas.us_nyt_data.USNYTData import USNYTData
#from covid_19_au_grab.state_news_releases.overseas.us_covidtracking_data.USCovidTrackingData import USCovidTrackingData
#from covid_19_au_grab.state_news_releases.overseas.west_africa_data.WestAfricaData import WestAfricaData
#from covid_19_au_grab.state_news_releases.overseas.world_eu_data.EUData import EUData
#from covid_19_au_grab.state_news_releases.overseas.world_jhu_data.WorldJHUData import WorldJHUData


def get_overseas_data():
    for i in [
        AFData,
        BRData,
        CHData,
        #COData,
        DEData,
        ESData,
        ETData,
        EUSubNationalData,
        FRData,
        HTData,
        IDGoogleDocsData,
        INData,
        IQData,
        ITData,
        JPData,
        JPCityData,
        KRData,
        #KZData,
        LYData,
        #MLData,
        MYData,
        NZData,
        #PHData,
        SOData,
        #THData,
        UKData,
        USNYTData,
    ]:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        print("Getting using class:", i)
        inst = i()
        name = i.__class__.__name__.replace('data', '_data')
        name = (
            name.partition('_')[0].lower().strip('_') +
            '_' +
            name.partition('_')[-1].strip('_')
        ).strip('_')
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        yield i.SOURCE_URL, name, inst.get_datapoints()


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
            f.write('state_name\t'
                    'schema\t'
                    'datatype\t'
                    'agerange\t'
                    'region\t'
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

                f.write(f'{datapoint.statename}\t'
                        f'{schema_to_name(datapoint.schema)[7:].lower()}\t'
                        f'{constant_to_name(datapoint.datatype)[3:].lower()}\t'
                        f'{datapoint.agerange}\t'
                        f'{datapoint.region}\t'
                        f'{datapoint.value}\t'
                        f'{backwards_date}\t'
                        f'{datapoint.source_url}\t'
                        f'{text_match}\n')

    for source_url in source_urls:
        print(f'* {source_url}')
