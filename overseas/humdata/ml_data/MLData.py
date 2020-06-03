import csv

from covid_19_au_grab.overseas.URLBase import (
    URL, URLBase
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


class MLData(URLBase):
    SOURCE_URL = 'https://data.humdata.org/dataset/mali-coronavirus-covid-19-subnational-cases'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'ml_ocha_mali_humdata'

    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        URLBase.__init__(self,
             output_dir=get_overseas_dir() / '' / 'data',
             urls_dict={
                 'ml_data.csv': URL(
                     'https://docs.google.com/spreadsheets/d/e/'
                     '2PACX-1vQLsd3rT6OXsSaC6Skla3WHkfRvNSbLHxhUcZaGwi3Ox6Ipa3LOLFAuINKQqEINhw/'
                     'pub?gid=314833870&single=true&output=csv',
                     static_file=False
                 )
             }
        )
        self.update()

    def get_datapoints(self):
        r = []

        f = self.get_file('ml_data.csv',
                          include_revision=True)
        first_item = True

        for item in csv.DictReader(f):
            # Date,Région,Cercle,Sum of Cas confirmés,Sum of Décès,Sum of Cas guéris,Sum of Cas suspects,Sum of Nombre contact
            # #date,#adm1 +name,#adm2 +name,#affected +infected,#affected +killed,#affected +recovered,,
            # 25-mars,Bamako,Bamako,1,0,0,,
            # 25-mars,Kayes,Kayes,1,0,0,,
            # 26-mars,Bamako,Bamako,2,0,0,,
            # 27-mars,Bamako,Bamako,8,1,0,,
            # 27-mars,Kayes,Yelimane,1,0,0,,
            # 28-mars,Bamako,Bamako,6,0,0,,
            # 28-mars,Kayes,Kayes,1,0,0,,
            # 29-mars,Kayes,Kayes,0,1,0,,
            # 30-mars,Bamako,Bamako,4,0,0,,
            pass

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(MLData().get_datapoints())
