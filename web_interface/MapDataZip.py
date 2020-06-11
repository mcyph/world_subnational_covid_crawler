class MapDataZip:
    def __init__(self):
        self.schema_types = FIXME

    def get_zip_data(self):
        self.output_geojson()
        self.output_cases()
        self.output_underlay()

    def output_base_listing(self):
        """
        TODO: Output schema types json, combined with:
          * which geojson files are available to download (a listing)
          * possible types (e.g. total, new etc) for each outputted "cases" file
          * different kinds of underlay keys for different schemas
          * a description of different case constants, schemas, 
            overlays, datasources (lower priority but should factor in)
          * a map from ISO 3166-a2 and 3166-2 to bounding coordinates
            to allow the JS to know whether a schema is in view+
            should be downloaded
        """
        pass

    def output_geojson(self):
        for region_schema, schema_dict in self.schema_types.items():
            # TODO: Get map from {id: {lang: printable, ...}, ...}
            #   (if applicable, will be null if not available) 
            geojson_fnam = schema_dict['geojson_file']

        self.schema_types['geojson'] = FIXME

    def output_cases(self):
        for region_schema, schema_dict in self.schema_types.items():
            data_fnam = schema_dict['data_file']

        self.schema_types['cases'] = FIXME

    def output_underlay(self):
        for region_schema, schema_dict in self.schema_types.items():
            underlay_fnam = schema_dict['underlay_file']

        self.schema_types['underlay'] = FIXME

