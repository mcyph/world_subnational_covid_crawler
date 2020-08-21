import csv
import json

from covid_19_au_grab.datatypes.DataPoint import (
    DataPoint
)
from covid_19_au_grab.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


state_to_name = dict([i.split() for i in """
DE-BW Baden-Württemberg
DE-BY Bayern
DE-BE Berlin
DE-BB Brandenburg
DE-HB Bremen
DE-HH Hamburg
DE-HE Hessen
DE-MV Mecklenburg-Vorpommern
DE-NI Niedersachsen
DE-NW Nordrhein-Westfalen
DE-RP Rheinland-Pfalz
DE-SL Saarland
DE-SN Sachsen
DE-ST Sachsen-Anhalt
DE-SH Schleswig-Holstein
DE-TH Thüringen
""".strip().split('\n')])


class DEData(GithubRepo):
    SOURCE_URL = 'https://github.com/jgehrcke/covid-19-germany-gae'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'de_unofficial'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'de' / 'covid-19-germany-gae',
                            github_url='https://github.com/jgehrcke/covid-19-germany-gae')
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_national_data())
        #r.extend(self._get_cases_by_ags())   # TODO: Find geojson data+re-enable me!!!! ==================================
        r.extend(self._get_cases_by_state())
        #r.extend(self._get_deaths_by_ags())
        r.extend(self._get_deaths_by_state())
        return r

    def _get_ags_id_to_name(self):
        return json.loads(self.get_text('ags.json'))

    def _get_national_data(self):
        r = []

        # time_iso8601,source,DE-BW_cases,DE-BW_deaths,DE-BY_cases,DE-BY_deaths,DE-BE_cases,DE-BE_deaths,DE-BB_cases,DE-BB_deaths,DE-HB_cases,DE-HB_deaths,DE-HH_cases,DE-HH_deaths,DE-HE_cases,DE-HE_deaths,DE-MV_cases,DE-MV_deaths,DE-NI_cases,DE-NI_deaths,DE-NW_cases,DE-NW_deaths,DE-RP_cases,DE-RP_deaths,DE-SL_cases,DE-SL_deaths,DE-SN_cases,DE-SN_deaths,DE-SH_cases,DE-SH_deaths,DE-ST_cases,DE-ST_deaths,DE-TH_cases,DE-TH_deaths,sum_cases,sum_deaths
        # 2020-03-10T12:00:00+01:00,RKI PDF,237,0,314,0,48,0,9,0,4,0,29,0,35,0,13,0,49,0,484,0,25,0,7,0,22,0,9,0,7,0,4,0,1296,0
        # 2020-03-11T12:00:00+01:00,RKI PDF,277,0,366,0,90,0,24,0,21,0,48,0,48,0,17,0,75,0,484,0,25,0,14,0,26,0,27,0,15,0,10,0,1567,0
        # 2020-03-12T12:00:00+01:00,RKI PDF,454,0,500,0,137,0,30,0,38,0,88,0,99,0,23,0,129,0,688,0,52,0,14,0,45,0,31,0,27,0,14,0,2369,0
        # 2020-03-13T12:00:00+01:00,RKI PDF,454,0,558,0,174,0,44,0,42,0,99,0,148,0,33,0,230,0,936,0,102,0,40,0,83,0,48,0,42,0,29,0,3062,0

        with open(self.get_path_in_dir('data.csv'),
                  'r', encoding='utf-8') as f:
            for item in csv.DictReader(f):
                date = self.convert_date(item['time_iso8601'].split('T')[0])
                del item['time_iso8601']
                source = item['source']
                del item['source']

                for key, value in item.items():
                    if key == 'sum_cases':
                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_0,
                            region_child='Germany',
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=source
                        ))
                    elif key == 'sum_deaths':
                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_0,
                            region_child='Germany',
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(value),
                            date_updated=date,
                            source_url=source
                        ))
                    elif key.endswith('_cases'):
                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='Germany',
                            region_child=state_to_name[key.split('_')[0]],
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=source
                        ))
                    elif key.endswith('_deaths'):
                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='Germany',
                            region_child=state_to_name[key.split('_')[0]],
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(value),
                            date_updated=date,
                            source_url=source
                        ))
                    else:
                        raise Exception(key)

        return r

    def _get_cases_by_ags(self):
        r = []
        ags_id_to_name = self._get_ags_id_to_name()
        
        # time_iso8601,1001,1002,1003,1004,1051,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,2000,3101,3102,3103,3151,3153,3154,3155,3157,3158,3159,3241,3251,3252,3254,3255,3256,3257,3351,3352,3353,3354,3355,3356,3357,3358,3359,3360,3361,3401,3402,3403,3404,3405,3451,3452,3453,3454,3455,3456,3457,3458,3459,3460,3461,3462,4011,4012,5111,5112,5113,5114,5116,5117,5119,5120,5122,5124,5154,5158,5162,5166,5170,5314,5315,5316,5334,5358,5362,5366,5370,5374,5378,5382,5512,5513,5515,5554,5558,5562,5566,5570,5711,5754,5758,5762,5766,5770,5774,5911,5913,5914,5915,5916,5954,5958,5962,5966,5970,5974,5978,6411,6412,6413,6414,6431,6432,6433,6434,6435,6436,6437,6438,6439,6440,6531,6532,6533,6534,6535,6611,6631,6632,6633,6634,6635,6636,7111,7131,7132,7133,7134,7135,7137,7138,7140,7141,7143,7211,7231,7232,7233,7235,7311,7312,7313,7314,7315,7316,7317,7318,7319,7320,7331,7332,7333,7334,7335,7336,7337,7338,7339,7340,8111,8115,8116,8117,8118,8119,8121,8125,8126,8127,8128,8135,8136,8211,8212,8215,8216,8221,8222,8225,8226,8231,8235,8236,8237,8311,8315,8316,8317,8325,8326,8327,8335,8336,8337,8415,8416,8417,8421,8425,8426,8435,8436,8437,9161,9162,9163,9171,9172,9173,9174,9175,9176,9177,9178,9179,9180,9181,9182,9183,9184,9185,9186,9187,9188,9189,9190,9261,9262,9263,9271,9272,9273,9274,9275,9276,9277,9278,9279,9361,9362,9363,9371,9372,9373,9374,9375,9376,9377,9461,9462,9463,9464,9471,9472,9473,9474,9475,9476,9477,9478,9479,9561,9562,9563,9564,9565,9571,9572,9573,9574,9575,9576,9577,9661,9662,9663,9671,9672,9673,9674,9675,9676,9677,9678,9679,9761,9762,9763,9764,9771,9772,9773,9774,9775,9776,9777,9778,9779,9780,10041,10042,10043,10044,10045,10046,12051,12052,12053,12054,12060,12061,12062,12063,12064,12065,12066,12067,12068,12069,12070,12071,12072,12073,13003,13004,13071,13072,13073,13074,13075,13076,14511,14521,14522,14523,14524,14612,14625,14626,14627,14628,14713,14729,14730,15001,15002,15003,15081,15082,15083,15084,15085,15086,15087,15088,15089,15090,15091,16051,16052,16053,16054,16055,16056,16061,16062,16063,16064,16065,16066,16067,16068,16069,16070,16071,16072,16073,16074,16075,16076,16077,11000,sum_cases
        # 2020-03-02T17:00:00+0000,0,0,1,0,0,1,0,0,0,0,0,0,1,0,2,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,1,1,8,0,9,2,0,0,84,0,1,0,0,2,1,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,3,0,0,0,0,1,1,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,3,0,1,6,0,0,0,0,1,0,0,0,0,0,2,0,1,0,0,0,0,3,3,0,0,1,0,0,0,0,0,0,2,1,0,1,0,0,1,0,0,9,0,0,0,0,0,1,0,0,2,3,0,1,0,0,1,0,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,203
        # 2020-03-03T17:00:00+0000,0,0,1,0,0,1,0,0,1,0,0,0,1,0,2,4,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,4,0,0,0,0,2,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,4,0,0,1,0,0,1,0,0,0,0,0,0,0,2,2,1,1,14,0,9,2,0,0,101,1,3,2,0,2,1,1,0,0,0,0,0,0,0,0,4,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,3,0,0,3,0,1,1,1,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,4,2,3,5,2,6,0,0,0,0,2,0,0,1,0,0,2,0,1,0,0,0,0,3,6,0,0,1,0,0,0,1,0,0,2,3,2,1,0,0,2,0,0,10,0,0,0,0,0,2,0,0,2,3,0,1,0,0,3,0,0,1,3,4,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,5,288
        # 2020-03-04T17:00:00+0000,0,0,1,0,0,1,0,0,1,0,0,0,1,0,2,7,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,4,0,0,0,0,2,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,4,0,2,2,0,0,3,0,0,0,0,0,0,0,5,2,1,1,16,0,25,4,0,0,146,1,3,3,0,2,3,1,10,0,0,0,0,0,0,0,6,0,0,2,0,0,0,0,0,0,3,0,0,0,0,0,4,0,0,3,0,1,2,1,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,10,3,5,5,2,10,0,0,1,0,4,0,0,1,0,2,4,0,1,0,0,0,0,3,7,1,0,1,0,0,0,1,0,0,2,12,3,4,0,1,2,1,0,13,0,0,0,0,0,2,0,0,3,3,0,1,0,0,3,0,0,1,3,4,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,4,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,8,445

        with open(self.get_path_in_dir('cases-rki-by-ags.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                date = self.convert_date(item['time_iso8601'].split('T')[0])
                del item['time_iso8601']

                for ags_id, value in item.items():
                    if ags_id == 'sum_cases':
                        pass
                    else:
                        ags_dict = ags_id_to_name[ags_id]

                        r.append(DataPoint(
                            region_schema=Schemas.DE_AGS,
                            region_parent=ags_dict['state'],
                            region_child=ags_dict['name'],
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))

        return r

    def _get_cases_by_state(self):
        r = []

        with open(self.get_path_in_dir('cases-rki-by-state.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                date = self.convert_date(item['time_iso8601'].split('T')[0])
                del item['time_iso8601']

                for region_child, value in item.items():
                    if region_child == 'sum_cases':
                        pass
                    else:
                        state = state_to_name[region_child]

                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='Germany',
                            region_child=state,
                            datatype=DataTypes.TOTAL,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))

        return r

    def _get_deaths_by_ags(self):
        r = []
        ags_id_to_name = self._get_ags_id_to_name()

        with open(self.get_path_in_dir('deaths-rki-by-ags.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                date = self.convert_date(item['time_iso8601'].split('T')[0])
                del item['time_iso8601']

                for ags_id, value in item.items():
                    if ags_id == 'sum_deaths':
                        pass
                    else:
                        ags_dict = ags_id_to_name[ags_id]

                        r.append(DataPoint(
                            region_schema=Schemas.DE_AGS,
                            region_parent=ags_dict['state'],
                            region_child=ags_dict['name'],
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))

        return r

    def _get_deaths_by_state(self):
        r = []

        with open(self.get_path_in_dir('deaths-rki-by-state.csv'),
                  'r', encoding='utf-8') as f:

            for item in csv.DictReader(f):
                date = self.convert_date(item['time_iso8601'].split('T')[0])
                del item['time_iso8601']

                for region_child, value in item.items():
                    if region_child == 'sum_deaths':
                        pass
                    else:
                        state = state_to_name[region_child]

                        r.append(DataPoint(
                            region_schema=Schemas.ADMIN_1,
                            region_parent='Germany',
                            region_child=state,
                            datatype=DataTypes.STATUS_DEATHS,
                            value=int(value),
                            date_updated=date,
                            source_url=self.SOURCE_URL
                        ))

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(DEData().get_datapoints())
