import json
from os import listdir
from _utility.get_package_dir import get_package_dir
from covid_db.datatypes.enums import Schemas
from _utility.normalize_locality_name import normalize_locality_name


_labels_to_region_child = [None]


def LabelsToRegionChild():
    if not _labels_to_region_child[0]:
        _labels_to_region_child[0] = __LabelsToRegionChild()
    return _labels_to_region_child[0]


class __LabelsToRegionChild:
    def __init__(self):
        """

        """
        self.__english, self.__non_english, self.__all_possible = self.__get_labels_to_admin_1()

    def region_child_in_geojson(self, region_schema, region_parent, region_child):
        return (
            region_schema,
            (region_parent or '').lower(),
            (region_child or '').lower()
        ) in self.__all_possible

    def get_by_label(self, region_schema, region_parent, label, default=KeyError):
        """

        """
        label = label.strip().lower()
        region_parent = region_parent or None
        if region_parent:
            region_parent = region_parent.lower()

        for i in self.__iter_alternatives(label):
            try:
                return self.__english[region_schema, region_parent, i]
            except KeyError:
                pass

        for i in self.__iter_alternatives(label):
            try:
                return self.__non_english[region_schema, region_parent, i]
            except KeyError:
                pass

        if default == KeyError:
            raise KeyError((region_schema, region_parent, label))
        else:
            return default

    def __get_labels_to_admin_1(self):
        english = {}
        non_english = {}
        all_possible = set()

        dir_ = get_package_dir() / 'world_geodata' / 'output'

        for fnam in listdir(dir_):
            with open(dir_ / fnam, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for region_schema, schema_dict in data.items():
                if region_schema.upper() in ('FR_DEPARTMENT', 'LK_DISTRICT', 'ES_MADRID_MUNICIPALITY'):
                    continue  # HACK!
                region_schema = Schemas(region_schema)

                for region_parent, region_parent_dict in schema_dict.items():
                    for region_child, region_child_item in region_parent_dict.items():
                        if region_child_item['label']['en'] is not None:
                            english[
                                region_schema,
                                region_parent or None,
                                region_child_item['label']['en'].strip().lower()
                            ] = region_child

                        for label in self.__iter_non_english_labels(region_child_item['label']):
                            non_english[
                                region_schema,
                                region_parent or None,
                                label
                            ] = region_child

                        all_possible.add((
                            region_schema,
                            region_parent.lower(),
                            region_child.lower()
                        ))

        return english, non_english, all_possible

    def __iter_non_english_labels(self, labels):
        for k, label in labels.items():
            if k == 'en':
                continue
            elif not label or not isinstance(label, str):
                continue

            label = label.strip().lower()
            for i_label in self.__iter_alternatives(label):
                yield i_label

            yield label

    def __iter_alternatives(self, label):
        yield label

        for c in '区町村市島':
            if label.endswith(c):
                yield label[:-1]

        normalized = normalize_locality_name(label)
        if normalized:
            yield normalized


if __name__ == '__main__':
    ltrc = LabelsToRegionChild()
    print(ltrc.get_by_label(Schemas.ADMIN_1, 'au', 'Victoria'))
    print(ltrc.get_by_label(Schemas.JP_CITY, 'JP-13', '武蔵野'))
    print(ltrc.get_by_label(Schemas.ADMIN_1, 'cn', 'guangdong'))
    print(ltrc.get_by_label(Schemas.ADMIN_0, '', 'China'))
    print(ltrc.get_by_label(Schemas.ADMIN_0, '', 'Japan'))
    print(ltrc.region_child_in_geojson(Schemas.ADMIN_0, '', 'jp'))
