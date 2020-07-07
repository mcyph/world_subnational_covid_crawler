from covid_19_au_grab.overseas.GithubRepo import (
    GithubRepo
)
from covid_19_au_grab.get_package_dir import (
    get_overseas_dir
)


# https://github.com/LintangWisesa/Indonesia-Covid19-Maps

# https://data.humdata.org/dataset/indonesia-covid-19-cases-recoveries-and-deaths-per-province
# has daily data, but is only a single day's snapshot

# https://github.com/erlange/INACOVID/blob/master/data/csv/basic.csv
# Date,Location,Confirmed,Cured,Deaths
# "2020/05/14","National",16006,3518,1043
# "2020/05/13","National",15438,3287,1028
# "2020/05/12","National",14749,3063,1007


class IDGoogleDocsData(GithubRepo):
    def __init__(self):
        # Only raw_data4.json is currently being updated,
        # so won't download the others every day
        GithubRepo.__init__(self,
             output_dir=get_overseas_dir() / 'id' / 'INACOVID',
             github_url='https://github.com/erlange/INACOVID'
        )
        self.update()

    def get_datapoints(self):
        pass

