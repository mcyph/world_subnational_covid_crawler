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
#from covid_19_au_grab.overseas.fi_data.FIData import FIData
from covid_19_au_grab.overseas.fr_data.FRData import FRData
#from covid_19_au_grab.overseas.gh_data.GHData import GHData
from covid_19_au_grab.overseas.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.overseas.in_data.INData import INData
from covid_19_au_grab.overseas.is_data.ISData import ISData
from covid_19_au_grab.overseas.it_data.ITData import ITData
from covid_19_au_grab.overseas.jp_data.JPData import JPData
from covid_19_au_grab.overseas.jp_city_data.JPCityData import JPCityData
from covid_19_au_grab.overseas.kg_data.KGData import KGData
from covid_19_au_grab.overseas.kr_data.KRData import KRData
from covid_19_au_grab.overseas.kz_data.KZData import KZData
#from covid_19_au_grab.overseas.lk_data.LKData import LKData
#from covid_19_au_grab.overseas.mm_data.MMData import MMData
from covid_19_au_grab.overseas.my_data.MYData import MYData
#from covid_19_au_grab.overseas.np_data.NPData import NPData
from covid_19_au_grab.overseas.nz_data.NZData import NZData
from covid_19_au_grab.overseas.om_data.OMData import OMData
#from covid_19_au_grab.overseas.ph_data.PHData import PHData
from covid_19_au_grab.overseas.ps_data.PSData import PSData
from covid_19_au_grab.overseas.sa_data.SAData import SAData
#from covid_19_au_grab.overseas.th_data.THData import THData
from covid_19_au_grab.overseas.uk_data.UKData import UKData
from covid_19_au_grab.overseas.us_nyt_data.USNYTData import USNYTData
#from covid_19_au_grab.overseas.uz_data.UZData import UZData
from covid_19_au_grab.overseas.tw_data.TWData import TWData
from covid_19_au_grab.overseas.vn_data.VNData import VNData
from covid_19_au_grab.overseas.west_africa_data.WestAfricaData import WestAfricaData
from covid_19_au_grab.overseas.world_bing_data.WorldBingData import WorldBingData
from covid_19_au_grab.overseas.world_jhu_data.WorldJHUData import WorldJHUData
#from covid_19_au_grab.overseas.ye_data.YEData import YEData
#from covid_19_au_grab.overseas.za_data.ZAData import ZAData


class OverseasDataSources:
    def __init__(self):
        self._status = {}

    def iter_data_sources(self):
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
            ISData,
            ITData,
            JPData,
            JPCityData,
            KGData,
            KRData,
            KZData,
            LYData,
            #MLData,
            #MMData,
            MYData,
            NZData,
            OMData,
            #PHData,
            PSData,
            SAData,
            SNData,
            SOData,
            #THData,
            TWData,
            UKData,
            WorldBingData,
            USNYTData,
            VEData,
            VNData,
        ]:
            # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
            print("Getting using class:", i)


            try:
                inst = i()
                yield inst.SOURCE_ID, inst.SOURCE_URL, inst.SOURCE_DESCRIPTION, inst.get_datapoints()

                self._status[i.SOURCE_ID] = {
                    'status': 'OK',
                    'message': None,
                }

            except:
                import traceback
                traceback.print_exc()

                self._status[i.SOURCE_ID] = {
                    'status': 'ERROR',
                    'message': traceback.format_exc()
                }

    def get_status_dict(self):
        return self._status
