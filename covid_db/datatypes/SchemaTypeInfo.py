import json
import unidecode

from _utility.get_package_dir import get_package_dir
from misc_data_scripts.other_data.iso_3166_1 import iso_3166_data
from misc_data_scripts.other_data.iso_3166_2 import iso_3166_2_data
from covid_db.datatypes.enums import Schemas
from world_geodata.LabelsToRegionChild import LabelsToRegionChild


with open(get_package_dir() / 'covid_db' / 'datatypes' / 'schema_types.json',
          'r', encoding='utf-8') as _f:
    _schema_types = json.loads(_f.read())


def get_schema_type_info(schema):
    if isinstance(schema, int):
        schema = Schemas(schema)
    schema = schema.lower().replace('schema_', '')
    return SchemaTypeInfo(schema, _schema_types['schemas'][schema])


class SchemaTypeInfo:
    def __init__(self, schema, schema_dict):
        self.schema = schema
        self.schema_dict = schema_dict
        self.ltrc = LabelsToRegionChild()

        #self._possible_regions = set(self.get_possible_parent_child_regions())

    def get_iso_3166(self):
        """

        """
        return self.schema_dict['iso_3166']

    def get_data_file(self, iso_3166_1, iso_3166_2):
        """

        """
        return self.schema_dict['data_file'] \
                   .replace('${', '%(') \
                   .replace('}', ')s') % {
            'iso_3166_1': iso_3166_1,
            'iso_3166_2': iso_3166_2
        }

    def get_geojson_file(self, iso_3166_1, iso_3166_2):
        """

        """
        return self.schema_dict['geojson_file'] \
                   .replace('${', '%(') \
                   .replace('}', ')s') % {
            'iso_3166_1': iso_3166_1,
            'iso_3166_2': iso_3166_2
        }

    def get_underlay_file(self, iso_3166_1, iso_3166_2):
        """

        """
        return self.schema_dict['underlay_file'] \
                   .replace('${', '%(') \
                   .replace('}', ')s') % {
            'iso_3166_1': iso_3166_1,
            'iso_3166_2': iso_3166_2
        }

    def convert_parent_child(self, region_parent, region_child):
        """

        """
        iso_3166 = self.get_iso_3166()

        if self.schema in ('admin_0', 'admin_1'):
            if self.schema == 'admin_1' and region_parent and region_child:
                # Convert names to ISO codes
                region_parent, region_child = self.__convert_admin_1(
                    region_parent, region_child
                )
            elif self.schema == 'admin_0' and region_child:
                region_parent, region_child = self.__convert_admin_0(
                    region_parent, region_child
                )
        elif iso_3166:
            # Convert e.g. "AU"/"Victoria" to "AU-VIC"
            _, region_parent = self.__convert_admin_1(
                iso_3166, region_parent
            )

        return region_parent, region_child

    def __convert_admin_0(self, region_parent, region_child):
        assert not region_parent, region_parent
        try:
            item = iso_3166_data.get_data_item_by_name(
                region_child
            )
            region_child = item.iso3166.a2
        except KeyError:
            pass
        return region_parent, region_child

    def __convert_admin_1(self, region_parent, region_child):
        try:
            item = iso_3166_2_data.get_data_item_by_name(
                unidecode.unidecode(region_child), region_parent
            )
            region_parent = item.country_code
            region_child = item.code
        except KeyError:
            pass
        return region_parent, region_child
