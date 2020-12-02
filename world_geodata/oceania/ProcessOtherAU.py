from _utility.normalize_locality_name import normalize_locality_name
from world_geodata.oceania.get_postcodes_map import (
    get_postcodes_map
)
from world_geodata.ProcessGeoJSONBase import (
    ProcessGeoJSONBase, DATA_DIR, OUTPUT_DIR
)


class ProcessACTSA3(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'sa3')

    def get_region_parent(self, fnam, feature):
        return 'AU-ACT'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(self.get_region_printable(fnam, feature))

    def get_region_printable(self, fnam, feature):
        return feature['name']  # ACT SA3


class ProcessQLDHHS(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'hhs')

    def get_region_parent(self, fnam, feature):
        return 'AU-QLD'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(self.get_region_printable(fnam, feature))

    def get_region_printable(self, fnam, feature):
        return feature['HHS']


class ProcessNSWLHD(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'lhd')

    def get_region_parent(self, fnam, feature):
        return 'AU-NSW'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(self.get_region_printable(fnam, feature))

    def get_region_printable(self, fnam, feature):
        return feature['name']  # NSW LHD


class ProcessTasTHS(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'ths')

    def get_region_parent(self, fnam, feature):
        return 'AU-TAS'

    def get_region_child(self, fnam, feature):
        return normalize_locality_name(self.get_region_printable(fnam, feature))

    def get_region_printable(self, fnam, feature):
        return feature['tas_ths'].title()


postcodes_dict = get_postcodes_map()


class ProcessNSWPostcode(ProcessGeoJSONBase):
    def __init__(self):
        ProcessGeoJSONBase.__init__(self, 'postcode')

    def get_region_parent(self, fnam, feature):
        if feature['POA_CODE16'][0] == '3':
            return 'AU-VIC'
        elif feature['POA_CODE16'][0] == '2':
            return 'AU-NSW'
        else:
            raise Exception(feature)

    def get_region_child(self, fnam, feature):
        # NSW postcode ID
        return feature['POA_CODE16']

    def get_region_printable(self, fnam, feature):
        # NSW postcode name
        if feature['POA_CODE16'] in postcodes_dict and True:
            return '%s: %s, ...' % (
                feature['POA_CODE16'],
                postcodes_dict[feature['POA_CODE16']][0]
            )
        else:
            return feature['POA_CODE16']


if __name__ == '__main__':
    ProcessACTSA3().output_json([DATA_DIR / 'au' / 'sa3' / 'sa3_act.geojson'], OUTPUT_DIR, pretty_print=False)
    ProcessQLDHHS().output_json([DATA_DIR / 'au' / 'hhs' / 'hhs_qld.geojson'], OUTPUT_DIR, pretty_print=False)
    ProcessNSWLHD().output_json([DATA_DIR / 'au' / 'lhd' / 'lhd_nsw.geojson'], OUTPUT_DIR, pretty_print=False)
    ProcessTasTHS().output_json([DATA_DIR / 'au' / 'ths' / 'ths_tas.geojson'], OUTPUT_DIR, pretty_print=False)
    ProcessNSWPostcode().output_json([
        DATA_DIR / 'au' / 'postcode' / 'suburb_nsw.json',
        DATA_DIR / 'au' / 'postcode' / 'postcode_vic.json'
    ], OUTPUT_DIR, pretty_print=False)
