# http://www.epid.gov.lk/web/index.php?option=com_content&view=article&id=225&lang=en

# https://github.com/arimacdev/covid19-srilankan-data/commits/master/Districts/districts_lk.csv
# https://stackoverflow.com/questions/28803626/get-all-revisions-for-a-specific-file-in-gitpython

# https://covid19-sl-report.netlify.app/

import git
import csv
from io import StringIO
from collections import Counter

from covid_19_au_grab.covid_db.datatypes.StrictDataPointsFactory import StrictDataPointsFactory, MODE_STRICT
from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes
from covid_19_au_grab.covid_crawlers._base_classes.GithubRepo import GithubRepo
from covid_19_au_grab._utility.get_package_dir import get_overseas_dir
from covid_19_au_grab.world_geodata.LabelsToRegionChild import LabelsToRegionChild

_ltrc = LabelsToRegionChild()


_districts = """
LK-11	Colombo	LK-1
LK-12	Gampaha	LK-1
LK-13	Kalutara	LK-1
LK-21	Kandy	LK-2
LK-22	Matale	LK-2
LK-23	Nuwara Eliya	LK-2
LK-31	Galle	LK-3
LK-32	Matara	LK-3
LK-33	Hambantota	LK-3
LK-41	Jaffna	LK-4
LK-42	Kilinochchi	LK-4
LK-43	Mannar	LK-4
LK-44	Vavuniya	LK-4
LK-45	Mullaittivu	LK-4
LK-45	mullaitivu	LK-4
LK-51	Batticaloa	LK-5
LK-52	Ampara	LK-5
LK-52	kalmunai	LK-5
LK-53	Trincomalee	LK-5
LK-61	Kurunegala	LK-6
LK-62	Puttalam	LK-6
LK-71	Anuradhapura	LK-7
LK-72	Polonnaruwa	LK-7
LK-81	Badulla	LK-8
LK-82	Monaragala	LK-8
LK-91	Ratnapura	LK-9
LK-92	Kegalla	LK-9
LK-92	Kegalle	LK-9
""".strip()


def _get_district_map():
    r = {}
    for district_code, district, province_code in [
        i.split('\t') for i in _districts.split('\n')
    ]:
        r[district.lower()] = (province_code, district_code)
    return r


_district_map = _get_district_map()


class LKData(GithubRepo):
    SOURCE_URL = 'https://github.com/arimacdev/covid19-srilankan-data'
    SOURCE_DESCRIPTION = ''
    SOURCE_ID = 'lk_arimacdev'

    def __init__(self):
        GithubRepo.__init__(self,
                            output_dir=get_overseas_dir() / 'lk' / 'covid19-srilankan-data',
                            github_url='https://github.com/arimacdev/covid19-srilankan-data')
        self.sdpf = StrictDataPointsFactory(mode=MODE_STRICT)
        self.update()

    def get_datapoints(self):
        r = []
        r.extend(self._get_cases_by_district())
        return r

    def _get_cases_by_district(self):
        repo = git.Repo(self.output_dir)

        path="Districts/districts_lk.csv"
        revlist = (
            (commit, (commit.tree / path).data_stream.read())
            for commit in repo.iter_commits(paths=path)
        )

        r = self.sdpf()
        for commit, file_contents in revlist:
            #print(dir(commit))
            #print(commit.committed_date)
            #print(commit.committed_datetime)

            date = commit.committed_datetime.strftime('%Y_%m_%d')
            f = StringIO(file_contents.decode('utf-8'))

            by_district = Counter()
            by_province = Counter()

            for i in csv.reader(f):
                #print(i)
                try:
                    district, latitude, longitude, cases = i
                except ValueError:
                    district, latitude, longitude, cases, __date = i

                if district.lower() == 'district':
                    continue
                elif latitude == '0' and longitude == '0':
                    continue

                #date = self.convert_date(__date.split()[0])
                province_code, district_code = _district_map[district.lower()]
                cases = int(cases)
                by_district[province_code, district_code] += cases
                by_province[province_code] += cases

            #cumulative = Counter()
            #for province, value in sorted(by_province.items()):
            #    cumulative[province] += value
            #    r.append(DataPoint(
            #        region_schema=Schemas.ADMIN_1,
            #        region_parent='LK',
            #        region_child=province,
            #        datatype=DataTypes.TOTAL,
            #        value=cumulative[province],
            #        date_updated=date,
            #        source_url=self.SOURCE_URL
            #    ))

            cumulative = Counter()
            for (province, district), value in sorted(by_district.items()):
                cumulative[province, district] += value
                r.append(
                    region_schema=Schemas.ADMIN_1,
                    #region_schema=Schemas.LK_DISTRICT,
                    region_parent='LK',
                    region_child=district,
                    datatype=DataTypes.TOTAL,
                    value=cumulative[province, district],
                    date_updated=date,
                    source_url=self.SOURCE_URL
                )

        return r


if __name__ == '__main__':
    from pprint import pprint
    pprint(LKData().get_datapoints())
