from covid_19_au_grab.state_news_releases.overseas.br_data.BRData import BRData
from covid_19_au_grab.state_news_releases.overseas.ch_data.CHData import CHData
from covid_19_au_grab.state_news_releases.overseas.de_data.DEData import DEData
from covid_19_au_grab.state_news_releases.overseas.fr_data.FRData import FRData
from covid_19_au_grab.state_news_releases.overseas.id_data.IDData import IDData
from covid_19_au_grab.state_news_releases.overseas.in_data.INData import INData
from covid_19_au_grab.state_news_releases.overseas.it_data.ITData import ITData
from covid_19_au_grab.state_news_releases.overseas.jp_data.JPData import JPData
from covid_19_au_grab.state_news_releases.overseas.ko_data.KOData import KOData
from covid_19_au_grab.state_news_releases.overseas.kz_data.KZData import KZData
from covid_19_au_grab.state_news_releases.overseas.my_data.MYData import MYData
from covid_19_au_grab.state_news_releases.overseas.nz_data.NZData import NZData
from covid_19_au_grab.state_news_releases.overseas.ph_data.PHData import PHData
from covid_19_au_grab.state_news_releases.overseas.sg_data.SGData import SGData
from covid_19_au_grab.state_news_releases.overseas.th_data.THData import THData
from covid_19_au_grab.state_news_releases.overseas.uk_data.UKData import UKData
from covid_19_au_grab.state_news_releases.overseas.us_data.USData import USData


def get_overseas_data():
    r = []
    for i in [
        BRData,
        CHData,
        DEData,
        FRData,
        IDData,
        INData,
        ITData,
        JPData,
        KOData,
        KZData,
        MYData,
        NZData,
        PHData,
        SGData,
        THData,
        UKData,
        USData,
    ]:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        inst = i()
        r.extend(inst.get_datapoints())

    return r


if __name__ == '__main__':
    pass
