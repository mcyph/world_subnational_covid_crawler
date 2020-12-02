import multiprocessing

from covid_19_au_grab.datatypes.DataPoint import _DataPoint

#from covid_19_au_grab.overseas.ml_data.MLData import MLData
#from covid_19_au_grab.overseas.fi_data.FIData import FIData
#from covid_19_au_grab.overseas.ph_data.PHData import PHData
#from covid_19_au_grab.overseas.uz_data.UZData import UZData

#==================================================================#
# Africa
#==================================================================#

from covid_19_au_grab.overseas.africa.et_data.ETData import ETData
from covid_19_au_grab.overseas.africa.sn_data.SNData import SNData
from covid_19_au_grab.overseas.africa.so_data.SOData import SOData
from covid_19_au_grab.overseas.africa.bw_data.BWData import BWData
from covid_19_au_grab.overseas.africa.gh_data.GHDataDash import GHDataDash
from covid_19_au_grab.overseas.africa.ma_data.MAData import MAData
from covid_19_au_grab.overseas.africa.mw_data.MWData import MWData
from covid_19_au_grab.overseas.africa.na_data.NAData import NAData
from covid_19_au_grab.overseas.africa.ng_data.NGData import NGData
from covid_19_au_grab.overseas.africa.sd_data.SDData import SDData
from covid_19_au_grab.overseas.africa.west_africa_data.WestAfricaData import WestAfricaData
from covid_19_au_grab.overseas.africa.za_data.ZAData import ZAData

AFRICA_SOURCES = (
    WestAfricaData, BWData, ETData, GHDataDash, MAData, MWData,
    NAData, NGData, SDData, SNData, SOData, ZAData
)

#==================================================================#
# Americas
#==================================================================#

from covid_19_au_grab.overseas.americas.co_data.COData import COData
from covid_19_au_grab.overseas.americas.ht_data.HTData import HTData
from covid_19_au_grab.overseas.americas.br_data.BRData import BRData
from covid_19_au_grab.overseas.americas.ca_data.CACovid19Canada import CACovid19Canada
from covid_19_au_grab.overseas.americas.cu_data.CUData import CUData
from covid_19_au_grab.overseas.americas.ve_data.VEData import VEData as VEDataNonHumData
from covid_19_au_grab.overseas.humdata.ve_data.VEData import VEData
from covid_19_au_grab.overseas.americas.us_nyt_data.USNYTData import USNYTData

AMERICAS_SOURCES = (
    BRData, CACovid19Canada, COData, CUData, HTData, VEData,
    VEDataNonHumData, USNYTData
)

#==================================================================#
# Asia/Oceania
#==================================================================#

from covid_19_au_grab.overseas.se_asia.cn_data.CNData import CNData
from covid_19_au_grab.overseas.se_asia.cn_data.CNQQData import CNQQData
from covid_19_au_grab.overseas.se_asia.id_data.IDGoogleDocsData import IDGoogleDocsData
from covid_19_au_grab.overseas.se_asia.jp_data.JPData import JPData
from covid_19_au_grab.overseas.se_asia.jp_city_data.JPCityData import JPCityData
from covid_19_au_grab.overseas.se_asia.jp_tokyo_data.JPTokyoCityPDFs import JPTokyoCityPDFs
from covid_19_au_grab.overseas.se_asia.kr_data.KRData import KRData
from covid_19_au_grab.overseas.se_asia.mm_data.MMData import MMData
from covid_19_au_grab.overseas.se_asia.my_data.MYData import MYData
from covid_19_au_grab.overseas.se_asia.my_data.MYESRIDashData import MYESRIDashData
from covid_19_au_grab.overseas.se_asia.th_data.THData import THData
from covid_19_au_grab.overseas.se_asia.tw_data.TWData import TWData
from covid_19_au_grab.overseas.se_asia.vn_data.VNData import VNData
from covid_19_au_grab.overseas.se_asia.hk_data.HKData import HKData
from covid_19_au_grab.overseas.se_asia.kh_data.KHData import KHData

from covid_19_au_grab.overseas.s_asia.bd_data.BDData import BDData
from covid_19_au_grab.overseas.s_asia.lk_data.LKData import LKData
from covid_19_au_grab.overseas.s_asia.np_data.NPData import NPData

from covid_19_au_grab.overseas.oceania.nz_data.NZData import NZData

#INData, # Will use Bing data for India

ASIA_SOURCES = (
    BDData, CNQQData, CNData, IDGoogleDocsData, JPData, JPCityData,
    KRData, LKData, MMData, MYData, NPData, NZData, THData, TWData,
    VNData, HKData, KHData, MYESRIDashData, JPTokyoCityPDFs
)

#==================================================================#
# Europe
#==================================================================#

from covid_19_au_grab.overseas.world.eu_subnational_data.EUSubNationalData import EUSubNationalData

from covid_19_au_grab.overseas.e_europe.kg_data.KGData import KGData
from covid_19_au_grab.overseas.e_europe.kz_data.KZData import KZData
from covid_19_au_grab.overseas.e_europe.mk_data.MKData import MKData
from covid_19_au_grab.overseas.e_europe.rs_data.RSData import RSData

from covid_19_au_grab.overseas.w_europe.be_data.BEData import BEData
from covid_19_au_grab.overseas.w_europe.ch_data.CHData import CHData
from covid_19_au_grab.overseas.w_europe.cz_data.CZData import CZData
from covid_19_au_grab.overseas.w_europe.de_data.DEData import DEData
from covid_19_au_grab.overseas.w_europe.de_data.DERKIData import DERKIData
from covid_19_au_grab.overseas.w_europe.es_data.ESData import ESData
from covid_19_au_grab.overseas.w_europe.es_data.ESISCIIIData import ESISCIIIData
from covid_19_au_grab.overseas.w_europe.fr_data.FRData import FRData
from covid_19_au_grab.overseas.w_europe.fr_data.FRGovData import FRGovData
from covid_19_au_grab.overseas.w_europe.fr_data.FRESRIData import FRESRIData
from covid_19_au_grab.overseas.w_europe.gr_data.GRCovid19Greece import GRCovid19Greece
from covid_19_au_grab.overseas.w_europe.hr_data.HRData import HRData
from covid_19_au_grab.overseas.w_europe.ie_data.IEData import IEData
from covid_19_au_grab.overseas.w_europe.is_data.ISData import ISData
from covid_19_au_grab.overseas.w_europe.it_data.ITData import ITData
from covid_19_au_grab.overseas.w_europe.lt_data.LTData import LTData
from covid_19_au_grab.overseas.w_europe.lv_data.LVData import LVData
from covid_19_au_grab.overseas.w_europe.lv_data.LVDataArcGIS import LVDataArcGIS
from covid_19_au_grab.overseas.w_europe.pt_data.PTData import PTData
from covid_19_au_grab.overseas.w_europe.si_data.SIData import SIData
from covid_19_au_grab.overseas.w_europe.uk_data.UKData import UKData
from covid_19_au_grab.overseas.w_europe.uk_data.UKGovData import UKGovData

EUROPE_DATA = (
    BEData, CHData, CZData, DEData, DERKIData, ESData, ESISCIIIData,
    EUSubNationalData, FRData, FRESRIData, FRGovData, GRCovid19Greece,
    HRData, IEData, ISData, ITData, KGData, KZData,
    MKData, PTData, RSData, SIData, UKData, UKGovData, LVData,
    LTData, LVDataArcGIS
)

#==================================================================#
# Middle East/Central Asia
#==================================================================#

from covid_19_au_grab.overseas.c_asia.af_data.AFData import AFData
from covid_19_au_grab.overseas.humdata.iq_data.IQData import IQData
from covid_19_au_grab.overseas.humdata.ly_data.LYData import LYData

from covid_19_au_grab.overseas.mid_east.il_data.ILWikiData import ILWikiData
from covid_19_au_grab.overseas.mid_east.iq_data.IQWikiData import IQWikiData
from covid_19_au_grab.overseas.mid_east.om_data.OMData import OMData
from covid_19_au_grab.overseas.mid_east.ps_data.PSData import PSData
from covid_19_au_grab.overseas.mid_east.sa_data.SAData import SAData
from covid_19_au_grab.overseas.mid_east.tr_data.TRData import TRData
from covid_19_au_grab.overseas.mid_east.tr_data.TRWikiData import TRWikiData
from covid_19_au_grab.overseas.mid_east.ye_data.YEData import YEData
#from covid_19_au_grab.overseas.ye_data.YEData import YEData

MIDDLE_EAST_DATA = (
    AFData, IQData, LYData, OMData, PSData, SAData,
    TRData, TRWikiData, YEData, ILWikiData, IQWikiData
)

#==================================================================#
# World
#==================================================================#

from covid_19_au_grab.overseas.world.world_bing_data.WorldBingData import WorldBingData
from covid_19_au_grab.overseas.world.world_jhu_data.WorldJHUData import \
    WorldJHUDataAdmin0, WorldJHUDataAdmin1, WorldJHUDataAdmin2
from covid_19_au_grab.overseas.world.world_um_data.WorldUMData import WorldUMData
from covid_19_au_grab.overseas.world.world_google_mobility.WorldGoogleMobility import WorldGoogleMobility
from covid_19_au_grab.overseas.world.world_eu_cdc_data.WorldEUCDCData import WorldEUCDCData
from covid_19_au_grab.overseas.world.world_owid_data.WorldOWIDData import WorldOWIDData
from covid_19_au_grab.overseas.world.world_who.WorldWHO import WorldWHO
from covid_19_au_grab.overseas.world.world_gender_disaggregated.WorldGenderDisaggregated import WorldGenderDisaggregated

WORLD_DATA = (
    WorldUMData,
    WorldJHUDataAdmin0,
    WorldJHUDataAdmin1,
    WorldJHUDataAdmin2,
    WorldBingData,
    WorldGoogleMobility,
    WorldEUCDCData,
    WorldOWIDData,
    WorldWHO,
    WorldGenderDisaggregated
)


class OverseasDataSources:
    def __init__(self):
        self._status = {}

    def iter_data_sources(self):
        processes = []
        all_source_ids = []
        send_q = multiprocessing.Queue()

        for classes in (
            AFRICA_SOURCES,
            AMERICAS_SOURCES,
            ASIA_SOURCES,
            EUROPE_DATA,
            MIDDLE_EAST_DATA,
            WORLD_DATA
        ):
            all_source_ids.extend([i.SOURCE_ID for i in classes])
            process = multiprocessing.Process(target=_get_datapoints, args=(classes, send_q))
            #process = threading.Thread(target=_get_datapoints, args=(classes, send_q))
            processes.append(process)

        for process in processes:
            process.start()

        num_done = 0
        while num_done != len(processes):
            while True:
                print("OVERSEAS GETTING FROM QUEUE!!", num_done, len(processes))
                try:
                    q_item = send_q.get(timeout=60*3)
                    break
                except:
                    found = False
                    for i in all_source_ids:
                        if i not in self._status:
                            print('NOT COMPLETED:', i)
                            found = True
                    if not found:
                        print("ALL DONE(??)")

            if q_item is None:
                num_done += 1
                continue

            source_id, source_url, source_description, new_datapoints, status_dict = q_item
            self._status[source_id] = status_dict

            if new_datapoints is not None:
                new_datapoints = [_DataPoint(*i) for i in new_datapoints]
                yield source_id, source_url, source_description, new_datapoints

        print("All processes done - waiting for join")
        for process in processes:
            try:
                process.join(timeout=10)
            except:
                import traceback
                traceback.print_exc()
        print("Process join end")

    def get_status_dict(self):
        return self._status


def _get_datapoints(classes, send_q):
    for i in classes:
        # TODO: OUTPUT AS CSV OR SOMETHING, with state info added?? ====================================================
        print("Getting using class:", i)

        try:
            inst = i()
            new_datapoints = []

            for datapoint in inst.get_datapoints():
                # We won't use Australian data from international sources,
                # as it comes from the dept of Health, which doesn't always
                # match with state data
                #if datapoint.region_schema == Schemas.ADMIN_1 and datapoint.region_parent == 'au':
                #    continue
                new_datapoints.append(tuple(datapoint))

            print("Class done:", i)
            send_q.put((inst.SOURCE_ID, inst.SOURCE_URL, inst.SOURCE_DESCRIPTION, new_datapoints, {
                'status': 'OK',
                'message': None,
            }))

        except:
            print("Class done with exception:", i)
            import traceback
            traceback.print_exc()

            send_q.put((i.SOURCE_ID, i.SOURCE_URL, i.SOURCE_DESCRIPTION, None, {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }))

    print("End of worker:", classes)
    send_q.put(None)


if __name__ == '__main__':
    for i in OverseasDataSources().iter_data_sources():
        print(i[:3])
