import re
import unicodedata
from covid_19_au_grab.datatypes.constants import SCHEMA_ADMIN_1, datatype_to_name, schema_to_name

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
from covid_19_au_grab.overseas.bw_data.BWData import BWData
from covid_19_au_grab.overseas.ca_data.CACovid19Canada import CACovid19Canada
from covid_19_au_grab.overseas.ch_data.CHData import CHData
from covid_19_au_grab.overseas.cu_data.CUData import CUData
from covid_19_au_grab.overseas.de_data.DEData import DEData
from covid_19_au_grab.overseas.es_data.ESData import ESData
from covid_19_au_grab.overseas.eu_subnational_data.EUSubNationalData import EUSubNationalData
#from covid_19_au_grab.overseas.fi_data.FIData import FIData
from covid_19_au_grab.overseas.fr_data.FRData import FRData
#from covid_19_au_grab.overseas.gh_data.GHData import GHData
from covid_19_au_grab.overseas.gh_data.GHDataDash import GHDataDash
from covid_19_au_grab.overseas.gr_data.GRCovid19Greece import GRCovid19Greece
from covid_19_au_grab.overseas.hr_data.HRData import HRData
from covid_19_au_grab.overseas.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.overseas.ie_data.IEData import IEData
from covid_19_au_grab.overseas.in_data.INData import INData
from covid_19_au_grab.overseas.is_data.ISData import ISData
from covid_19_au_grab.overseas.it_data.ITData import ITData
from covid_19_au_grab.overseas.jp_data.JPData import JPData
from covid_19_au_grab.overseas.jp_city_data.JPCityData import JPCityData
from covid_19_au_grab.overseas.kg_data.KGData import KGData
from covid_19_au_grab.overseas.kh_data.KHData import KHData
from covid_19_au_grab.overseas.kr_data.KRData import KRData
from covid_19_au_grab.overseas.kz_data.KZData import KZData
from covid_19_au_grab.overseas.lk_data.LKData import LKData
from covid_19_au_grab.overseas.mm_data.MMData import MMData
from covid_19_au_grab.overseas.mw_data.MWData import MWData
from covid_19_au_grab.overseas.my_data.MYData import MYData
from covid_19_au_grab.overseas.na_data.NAData import NAData
from covid_19_au_grab.overseas.np_data.NPData import NPData
from covid_19_au_grab.overseas.nz_data.NZData import NZData
from covid_19_au_grab.overseas.om_data.OMData import OMData
#from covid_19_au_grab.overseas.ph_data.PHData import PHData
from covid_19_au_grab.overseas.ps_data.PSData import PSData
from covid_19_au_grab.overseas.sa_data.SAData import SAData
from covid_19_au_grab.overseas.sd_data.SDData import SDData
#from covid_19_au_grab.overseas.th_data.THData import THData
from covid_19_au_grab.overseas.uk_data.UKData import UKData
from covid_19_au_grab.overseas.us_nyt_data.USNYTData import USNYTData
#from covid_19_au_grab.overseas.uz_data.UZData import UZData
from covid_19_au_grab.overseas.th_data.THData import THData
from covid_19_au_grab.overseas.tr_data.TRData import TRData
from covid_19_au_grab.overseas.tw_data.TWData import TWData
from covid_19_au_grab.overseas.ve_data.VEData import VEData as VEDataNonHumData
from covid_19_au_grab.overseas.vn_data.VNData import VNData
from covid_19_au_grab.overseas.ye_data.YEData import YEData
from covid_19_au_grab.overseas.west_africa_data.WestAfricaData import WestAfricaData
from covid_19_au_grab.overseas.world_bing_data.WorldBingData import WorldBingData
from covid_19_au_grab.overseas.world_jhu_data.WorldJHUData import \
    WorldJHUDataAdmin0, WorldJHUDataAdmin1, WorldJHUDataAdmin2
#from covid_19_au_grab.overseas.ye_data.YEData import YEData
#from covid_19_au_grab.overseas.za_data.ZAData import ZAData


class OverseasDataSources:
    def __init__(self):
        self._status = {}

    def iter_data_sources(self):
        for i in [
            WestAfricaData,
            WorldJHUDataAdmin0,
            WorldJHUDataAdmin1,
            WorldJHUDataAdmin2,
            AFData,
            BDData,
            BRData,
            BWData,
            CACovid19Canada,
            CHData,
            COData,
            CUData,
            DEData,
            ESData,
            ETData,
            EUSubNationalData,
            FRData,
            GHDataDash,
            GRCovid19Greece,
            HRData,
            HTData,
            IDGoogleDocsData,
            IEData,
            #INData, # Will use Bing data for India
            IQData,
            ISData,
            ITData,
            JPData,
            JPCityData,
            KGData,
            KHData,
            KRData,
            KZData,
            LKData,
            LYData,
            #MLData,
            MMData,
            MWData,
            MYData,
            NAData,
            NPData,
            NZData,
            OMData,
            #PHData,
            PSData,
            SAData,
            SDData,
            SNData,
            SOData,
            THData,
            TRData,
            TWData,
            UKData,
            WorldBingData,
            #USNYTData,
            VEData,
            VEDataNonHumData,
            VNData,
            YEData,
        ]:
            # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
            print("Getting using class:", i)

            try:
                inst = i()
                new_datapoints = []

                for datapoint in inst.get_datapoints():
                    # We won't use Australian data from international sources,
                    # as it comes from the dept of Health, which doesn't always
                    # match with state data
                    if datapoint.region_schema == SCHEMA_ADMIN_1 and datapoint.region_parent == 'au':
                        continue
                    new_datapoints.append(datapoint)

                yield inst.SOURCE_ID, inst.SOURCE_URL, inst.SOURCE_DESCRIPTION, new_datapoints

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
