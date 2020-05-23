# https://data.humdata.org/dataset/west-and-central-africa-coronavirus-covid-19-situation

# https://data.humdata.org/dataset/2ec81cad-04a3-4bfe-b127-c36658947427/resource/22bb4232-897b-4e7a-8e35-bbe030fca37c/download/wca_covid19_data_admin1_master.xlsx


from covid_19_au_grab.state_news_releases.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir, get_package_dir
)
from covid_19_au_grab.state_news_releases.overseas.humdata.west_africa_data.west_africa_powerbi import (
    get_powerbi_data
)
from covid_19_au_grab.state_news_releases.overseas.humdata.west_africa_data.WestAfricaPowerBI import (
    WestAfricaPowerBI
)


class WestAfricaData(URLBase):
    SOURCE_URL = WestAfricaPowerBI.POWERBI_URL
    SOURCE_LICENSE = ''

    GEO_DIR = ''
    GEO_URL = ''
    GEO_LICENSE = ''

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
            output_dir=get_overseas_dir() / '' / '',
            urls_dict={
                '': URL(
                    '',
                    static_file=False
                )
            }
        )
        #wapb = WestAfricaPowerBI()
        #wapb.run_powerbi_grabber()

    def get_datapoints(self):
        return get_powerbi_data()


if __name__ == '__main__':
    from pprint import pprint
    pprint(WestAfricaData().get_datapoints())
