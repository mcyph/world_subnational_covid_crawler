from covid_19_au_grab.datatypes.constants import SCHEMA_ADMIN_1

from covid_19_au_grab.overseas.c_asia.af_data.AFData import AFData
from covid_19_au_grab.overseas.americas.co_data.COData import COData
from covid_19_au_grab.overseas.africa.et_data.ETData import ETData
from covid_19_au_grab.overseas.americas.ht_data.HTData import HTData
from covid_19_au_grab.overseas.humdata.iq_data.IQData import IQData
#from covid_19_au_grab.overseas.kz_data.KZData import KZData
from covid_19_au_grab.overseas.humdata.ly_data.LYData import LYData
#from covid_19_au_grab.overseas.ml_data.MLData import MLData
from covid_19_au_grab.overseas.africa.sn_data.SNData import SNData
from covid_19_au_grab.overseas.africa.so_data.SOData import SOData
from covid_19_au_grab.overseas.humdata.ve_data.VEData import VEData

from covid_19_au_grab.overseas.s_asia.bd_data.BDData import BDData
from covid_19_au_grab.overseas.americas.br_data.BRData import BRData
from covid_19_au_grab.overseas.africa.bw_data.BWData import BWData
from covid_19_au_grab.overseas.americas.ca_data.CACovid19Canada import CACovid19Canada
from covid_19_au_grab.overseas.w_europe.ch_data.CHData import CHData
from covid_19_au_grab.overseas.americas.cu_data.CUData import CUData
from covid_19_au_grab.overseas.w_europe.de_data.DEData import DEData
from covid_19_au_grab.overseas.w_europe.es_data.ESData import ESData
from covid_19_au_grab.overseas.eu_subnational_data.EUSubNationalData import EUSubNationalData
#from covid_19_au_grab.overseas.fi_data.FIData import FIData
from covid_19_au_grab.overseas.w_europe.fr_data.FRData import FRData
#from covid_19_au_grab.overseas.gh_data.GHData import GHData
from covid_19_au_grab.overseas.africa.gh_data.GHDataDash import GHDataDash
from covid_19_au_grab.overseas.w_europe.gr_data.GRCovid19Greece import GRCovid19Greece
from covid_19_au_grab.overseas.w_europe.hr_data.HRData import HRData
from covid_19_au_grab.overseas.se_asia.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.overseas.w_europe.ie_data.IEData import IEData
from covid_19_au_grab.overseas.w_europe.is_data.ISData import ISData
from covid_19_au_grab.overseas.w_europe.it_data.ITData import ITData
from covid_19_au_grab.overseas.se_asia.jp_data.JPData import JPData
from covid_19_au_grab.overseas.se_asia.jp_city_data.JPCityData import JPCityData
from covid_19_au_grab.overseas.e_europe.kg_data.KGData import KGData
from covid_19_au_grab.overseas.e_europe.kh_data.KHData import KHData
from covid_19_au_grab.overseas.se_asia.kr_data.KRData import KRData
from covid_19_au_grab.overseas.e_europe.kz_data.KZData import KZData
from covid_19_au_grab.overseas.s_asia.lk_data.LKData import LKData
from covid_19_au_grab.overseas.se_asia.mm_data.MMData import MMData
from covid_19_au_grab.overseas.africa.mw_data.MWData import MWData
from covid_19_au_grab.overseas.se_asia.my_data.MYData import MYData
from covid_19_au_grab.overseas.africa.na_data.NAData import NAData
from covid_19_au_grab.overseas.s_asia.np_data.NPData import NPData
from covid_19_au_grab.overseas.oceania.nz_data.NZData import NZData
from covid_19_au_grab.overseas.mid_east.om_data.OMData import OMData
#from covid_19_au_grab.overseas.ph_data.PHData import PHData
from covid_19_au_grab.overseas.mid_east.ps_data.PSData import PSData
from covid_19_au_grab.overseas.mid_east.sa_data.SAData import SAData
from covid_19_au_grab.overseas.africa.sd_data.SDData import SDData
#from covid_19_au_grab.overseas.th_data.THData import THData
from covid_19_au_grab.overseas.w_europe.uk_data.UKData import UKData
#from covid_19_au_grab.overseas.uz_data.UZData import UZData
from covid_19_au_grab.overseas.se_asia.th_data.THData import THData
from covid_19_au_grab.overseas.mid_east.tr_data.TRData import TRData
from covid_19_au_grab.overseas.se_asia.tw_data.TWData import TWData
from covid_19_au_grab.overseas.americas.ve_data.VEData import VEData as VEDataNonHumData
from covid_19_au_grab.overseas.se_asia.vn_data.VNData import VNData
from covid_19_au_grab.overseas.mid_east.ye_data.YEData import YEData
from covid_19_au_grab.overseas.africa.west_africa_data.WestAfricaData import WestAfricaData
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
