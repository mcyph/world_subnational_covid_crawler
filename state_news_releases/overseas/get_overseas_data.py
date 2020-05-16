import unicodedata
from covid_19_au_grab.state_news_releases.constants import constant_to_name, schema_to_name

from covid_19_au_grab.state_news_releases.overseas.af_data.AFData import AFData
from covid_19_au_grab.state_news_releases.overseas.br_data.BRData import BRData
#from covid_19_au_grab.state_news_releases.overseas.ch_data.CHData import CHData
from covid_19_au_grab.state_news_releases.overseas.co_data.COData import COData
from covid_19_au_grab.state_news_releases.overseas.de_data.DEData import DEData
#from covid_19_au_grab.state_news_releases.overseas.et_data.ETData import ETData
from covid_19_au_grab.state_news_releases.overseas.eu_subnational_data.EUSubNationalData import EUSubNationalData
from covid_19_au_grab.state_news_releases.overseas.fr_data.FRData import FRData
from covid_19_au_grab.state_news_releases.overseas.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.state_news_releases.overseas.in_data.INData import INData
#from covid_19_au_grab.state_news_releases.overseas.iq_data.IQData import IQData
from covid_19_au_grab.state_news_releases.overseas.it_data.ITData import ITData
from covid_19_au_grab.state_news_releases.overseas.jp_data.JPData import JPData
#from covid_19_au_grab.state_news_releases.overseas.ko_data.KOData import KOData
#from covid_19_au_grab.state_news_releases.overseas.kz_data.KZData import KZData
#from covid_19_au_grab.state_news_releases.overseas.ly_data.LYData import LYData
#from covid_19_au_grab.state_news_releases.overseas.mm_data.MMData import MMData
#from covid_19_au_grab.state_news_releases.overseas.my_data.MYData import MYData
from covid_19_au_grab.state_news_releases.overseas.nz_data.NZData import NZData
#from covid_19_au_grab.state_news_releases.overseas.ph_data.PHData import PHData
#from covid_19_au_grab.state_news_releases.overseas.sg_data.SGData import SGData
#from covid_19_au_grab.state_news_releases.overseas.so_data.SOData import SOData
from covid_19_au_grab.state_news_releases.overseas.th_data.THData import THData
from covid_19_au_grab.state_news_releases.overseas.uk_data.UKData import UKData
from covid_19_au_grab.state_news_releases.overseas.us_nyt_data.USNYTData import USNYTData
#from covid_19_au_grab.state_news_releases.overseas.world_eu_data.EUData import EUData


def get_overseas_data():
    r = []
    for i in [
        AFData,
        #BRData,
        #CHData,
        #COData,
        #DEData,
        EUSubNationalData,
        FRData,
        IDGoogleDocsData,
        INData,
        ITData,
        JPData,
        #KOData,
        #KZData,
        #MYData,
        NZData,
        #PHData,
        #SGData,
        #THData,
        UKData,
        USNYTData,
    ]:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        print("Getting using class:", i)
        inst = i()
        r.extend(inst.get_datapoints())

    return r


def remove_control_characters(s):
    return "".join(
        ch for ch in s
        if unicodedata.category(ch)[0] != "C"
    )


if __name__ == '__main__':
    overseas_data = get_overseas_data()

    with open('output.tsv', 'w', encoding='utf-8') as f:
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
                    str(datapoint.text_match).replace("\t", " ").replace('\n', ' ').replace('\r', ' ')
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
