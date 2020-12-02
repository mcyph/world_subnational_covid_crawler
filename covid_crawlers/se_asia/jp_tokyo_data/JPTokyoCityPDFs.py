from covid_crawlers._base_classes.URLBase import URLBase
from _utility.get_package_dir import get_overseas_dir
from world_geodata.LabelsToRegionChild import LabelsToRegionChild
from covid_crawlers.se_asia.jp_tokyo_data.extract_from_tokyo_pdf import ExtractFromTokyoPDF


class JPTokyoCityPDFs(URLBase):
    SOURCE_URL = 'https://www.metro.tokyo.lg.jp'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'jp_tokyo_city'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
                         # TODO: SUPPORT TOKYO DATA AS WELL from !!!
                         output_dir=get_overseas_dir() / 'jp_city_data' / 'data',
                         urls_dict={})
        self.update()

        self._labels_to_region_child = LabelsToRegionChild()

    def update(self, force=False):
        ExtractFromTokyoPDF().download_pdfs(only_most_recent=True)
        URLBase.update(self, force)

    def get_datapoints(self):
        r = []
        r.extend(ExtractFromTokyoPDF().get_from_pdfs())
        return r


if __name__ == '__main__':
    for i in JPTokyoCityPDFs().get_datapoints():
        if i.region_child == 'jp-13':
            print(i)
