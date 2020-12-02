import ssl
import json
import datetime
from os import listdir

from covid_crawlers._base_classes.URLBase import URL, URLBase
from covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.get_package_dir import get_overseas_dir

place_map = dict([i.split('\t')[::-1] for i in """
OM-DA	AL DAKHLIYAH
OM-BS	NORTH BATINAH
OM-BJ	SOUTH BATINAH
OM-WU	AL WUSTA
OM-SS	NORTH ASH SHARQIYAH
OM-SJ	SOUTH ASH SHARQIYAH
OM-ZA	ADH DHAHIRAH
OM-BU	AL BURAYMI
OM-MA	MUSCAT
OM-MU	MUSANDAM
OM-ZU	DHOFAR 
""".strip().split('\n')])


class OMData(URLBase):
    SOURCE_URL = 'https://covid19.moh.gov.om/'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'om_gov'

    def __init__(self):
        # Disable ssl, only for this crawler!
        old_create = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context
        self.sdpf = StrictDataPointsFactory()

        try:
            URLBase.__init__(self,
                output_dir=get_overseas_dir() / 'om' / 'data',
                urls_dict={
                    'region_walayat_summary.json':
                        URL('https://covid19.moh.gov.om/ens/outbreak/getRegionWalayatSummary',
                            static_file=False)
                }
            )
            self.update()
        finally:
            ssl._create_default_https_context = old_create

    def get_datapoints(self):
        r = []
        r.extend(self._get_recovered_sum())
        return r

    def _get_recovered_sum(self):
        r = self.sdpf()
        base_dir = self.get_path_in_dir('')

        for date in self.iter_nonempty_dirs(base_dir):
            path = f'{base_dir}/{date}/region_walayat_summary.json'
            with open(path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for region_dict in data['result']:
                # quarantined	2
                # suspected	0
                # infected	8
                # death	0
                # recovered	6
                # currentlySick	2
                # quarantinedNls	"٢"
                # suspectedNls	"١٩"
                # infectedNls	"٨"
                # deathNls	"٠"
                # recoveredNls	"٦"
                # currentlySickNls	"٢"
                # regionCode	50009
                # regionName	"MUSANDAM"
                # regionNameNls	"مسندم"
                # nationCode	268
                # latitude	26.16444
                # longitude	56.24264
                # publishedTime	"02-Jun-2020 16:38"
                # publishedTimeEpoch	1591101522000
                # onsetDate	"02-Jun-2020 00:00"
                region = place_map[region_dict['regionName']]
                date = datetime.datetime.fromtimestamp(
                    region_dict['publishedTimeEpoch']/1000.0
                ).strftime('%Y_%m_%d')

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='OM',
                    region_child=region,
                    datatype=DataTypes.TOTAL,
                    value=int(region_dict['infected']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='OM',
                    region_child=region,
                    datatype=DataTypes.STATUS_DEATHS,
                    value=int(region_dict['death']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='OM',
                    region_child=region,
                    datatype=DataTypes.STATUS_RECOVERED,
                    value=int(region_dict['recovered']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                r.append(
                    region_schema=Schemas.ADMIN_1,
                    region_parent='OM',
                    region_child=region,
                    datatype=DataTypes.STATUS_ACTIVE,
                    value=int(region_dict['currentlySick']),
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

                for walayat_dict in region_dict['walayat']:
                    # Provinces
                    #
                    # quarantined	2
                    # suspected	0
                    # infected	6
                    # death	0
                    # recovered	4
                    # currentlySick	2
                    # quarantinedNls	"٢"
                    # suspectedNls	"١٣"
                    # infectedNls	"٦"
                    # deathNls	"٠"
                    # recoveredNls	"٤"
                    # currentlySickNls	"٢"
                    # walayatCode	50152
                    # walayatName	"Khasab"
                    # walayatNameNls	"خصب"
                    # latitude	25.9406
                    # longitude	56.425
                    # publishedTime	"02-Jun-2020 16:38"
                    # publishedTimeEpoch	1591101522000
                    # onsetDate	"02-Jun-2020 00:00"

                    pass

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(OMData().get_datapoints())
