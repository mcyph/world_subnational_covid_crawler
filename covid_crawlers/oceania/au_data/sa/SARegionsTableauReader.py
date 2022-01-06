import pprint
import json
from _utility.get_package_dir import get_data_dir
from covid_db.datatypes.DatapointMerger import DataPointMerger
from covid_db.datatypes.DataPoint import DataPoint
from covid_db.datatypes.enums import Schemas, DataTypes
from _utility.normalize_locality_name import normalize_locality_name


SA_TABLEAU_MAP_DIR = get_data_dir() / 'sa' / 'custom_map_tableau'


class SARegionsTableauReader:
    SOURCE_ID = 'au_sa_dashmap'
    SOURCE_URL = 'https://www.covid-19.sa.gov.au/home/dashboard'
    SOURCE_DESCRIPTION = ''

    def __init__(self):
        pass

    def get_datapoints(self):
        r = DataPointMerger()
        for path in SA_TABLEAU_MAP_DIR.iterdir():
            r.extend(self._get_datapoints(path))
        return r

    def _get_datapoints(self, path):
        date = path.name.split('-')[0]

        for path in path.iterdir():
            with open(path / '', 'r', encoding='utf-8') as f:
                r = []

                text = json.loads(f.read())
                data = self.get_from_multipart(text, 'dataColumns')

                values_by_idx = self.get_recursively(data, 'dataColumns')[0]['dataValues']
                lga_by_idx = self.get_recursively(data, 'dataColumns')[2]['dataValues']

                active_idx = self.get_recursively(data, 'paneColumnsList')[0]['vizPaneColumns'][3]['aliasIndices']
                total_idx = self.get_recursively(data, 'paneColumnsList')[0]['vizPaneColumns'][4]['aliasIndices']

                for _active, lga in zip(active_idx, lga_by_idx[1:]):
                    if _active in (-44, -70, -71):
                        continue
                    elif _active < 0:
                        continue
                        raise Exception(_active)

                    r.append(DataPoint(
                        region_schema=Schemas.LGA,
                        region_parent='AU-SA',
                        region_child=normalize_locality_name(lga),
                        datatype=DataTypes.STATUS_ACTIVE,
                        value=int(values_by_idx[_active]),
                        date_updated=date,
                        source_url=self.SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))

                for _total, lga in zip(total_idx, lga_by_idx[1:]):
                    if _total == -44:
                        continue
                    elif _total < 0:
                        raise Exception(_total)

                    r.append(DataPoint(
                        region_schema=Schemas.LGA,
                        region_parent='AU-SA',
                        region_child=normalize_locality_name(lga),
                        datatype=DataTypes.TOTAL,
                        value=int(values_by_idx[_total]),
                        date_updated=date,
                        source_url=self.SOURCE_URL,
                        source_id=self.SOURCE_ID
                    ))

                #print(values_by_idx)
                #print(lga_by_idx)
                #pprint(total_idx)

                return r

    def get_recursively(self, search_dict, field):
        if isinstance(search_dict, dict):
            if field in search_dict:
                return search_dict[field]
            for key in search_dict:
                item = self.get_recursively(search_dict[key], field)
                if item is not None:
                    return item
        elif isinstance(search_dict, list):
            for element in search_dict:
                item = self.get_recursively(element, field)
                if item is not None:
                    return item
        return None

    def get_from_multipart(self, s, contains):
        #print(s)

        while s:
            num_chars, _, s = s.partition(';')
            num_chars = int(num_chars)

            i_s = s[:num_chars]
            #print(i_s)
            s = s[num_chars:]

            if contains in i_s:
                # print("FOUND:", contains, i_s)
                return json.loads(i_s)


if __name__ == '__main__':
    from pprint import pprint
    sr = SARegionsTableauReader()
    pprint(sr.get_datapoints())

