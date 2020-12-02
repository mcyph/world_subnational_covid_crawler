import json
from polylabel import polylabel
from os.path import basename
from abc import ABC, abstractmethod
from covid_db.datatypes.schema_types import schema_types
from _utility.get_package_dir import get_package_dir


OUTPUT_DIR = get_package_dir() / 'world_geodata' / 'output'
DATA_DIR = get_package_dir() / 'world_geodata' / 'data'


class ProcessGeoJSONBase(ABC):
    def __init__(self, schema_name):
        self.schema_name = schema_name

    def output_json(self, in_paths, out_dir, pretty_print=False):
        r = {}

        for in_path in in_paths:
            fnam = basename(in_path)
            with open(in_path, 'r', encoding='utf-8') as f:
                geojson = json.loads(
                    f.read(),
                    # Limit the float precision to 3 digits
                    # after the decimal place to save space
                    parse_float=lambda x: round(float(x), 3)
                )

            # Convert MultiPolygon's to single Polygon's
            features = []
            for feature in geojson['features']:
                if feature['geometry'] is None:
                    continue
                elif feature['geometry']['type'] == 'MultiPolygon':
                    features.extend(self._multi_polygon_to_polygons(feature))
                elif feature['geometry']['type'] == 'Polygon':
                    features.append(feature)
                else:
                    raise Exception(f"Unsupported feature type: {feature}")

            for feature in features:
                if not feature['geometry'] or not feature['properties'] or not feature['geometry']['coordinates']:
                    continue
                elif (
                    'unincorporated' in str(feature).lower() and
                    not 'pastoral' in str(feature).lower()
                ):
                    print("**IGNORE:", feature)
                    continue

                parent = self.get_region_parent(fnam, feature['properties'])
                child = self.get_region_child(fnam, feature['properties'])
                printable_name = self.get_region_printable(fnam, feature['properties'])
                print(parent, child)#printable_name)

                if not isinstance(printable_name, dict):
                    printable_name = {'en': printable_name}

                # TODO: Also add underlay data(+maybe add listings for point data)!!! ======================================================================
                i_dict = r.setdefault(self.schema_name.lower(), {}) \
                          .setdefault(parent.lower(), {}) \
                          .setdefault(child.lower(), {
                              # [[area,
                              #   x1,y1,x2,y2 bounding coords,
                              #   center coords,
                              #   points], ...]
                              'geodata': [],
                              'label': printable_name
                          })

                #print(feature)

                for coords in feature['geometry']['coordinates']:
                    # HACK: Remove z extent!!
                    coords[:] = [i[:2] for i in coords]

                    for lng, lat in coords:
                        # Make sure coords using correct ranges!
                        assert -180 <= lng <= 180, lng
                        assert -90 <= lat <= 90, lat

                i_dict['geodata'].append([
                    self._get_area(feature['geometry']['coordinates']),
                    self._get_bounding_coords(feature['geometry']['coordinates']),
                    self._get_center(feature['geometry']['coordinates']),
                    feature['geometry']['coordinates']
                ])

        # Make it so largest polygons come first
        # (if there's multiple polygons for a given region)
        for schema_name, schema_dict in r.items():
            for parent_name, parent_dict in schema_dict.items():
                for child_name, child_dict in parent_dict.items():
                    child_dict['geodata'].sort(key=lambda x: -x[0])

        def output(out_path, r):
            if pretty_print:
                encoded = json.dumps(r, indent=4, ensure_ascii=False)
            else:
                encoded = json.dumps(r, separators=(',', ':'), ensure_ascii=False)

            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(encoded)

        if schema_types['schemas'][self.schema_name]['split_by_parent_region']:
            # TODO: Split into '{schema_name}_{parent_region}'
            for schema_name, schema_dict in r.items():
                for parent_name, parent_dict in schema_dict.items():
                    output(f'{out_dir}/{self.schema_name}_{parent_name.lower()}.json', {
                        self.schema_name: {parent_name: parent_dict}
                    })
        else:
            output(f'{out_dir}/{self.schema_name}.json', r)

    #===========================================================#
    #                  Methods to be overridden                 #
    #===========================================================#

    @abstractmethod
    def get_region_parent(self, fnam, feature):
        pass

    @abstractmethod
    def get_region_child(self, fnam, feature):
        # Should call normalize_locality_name(child_key(i))
        # if a unique ID (such as ISO 3166-2 etc) isn't
        # available, but unique IDs should be preferred
        pass

    @abstractmethod
    def get_region_printable(self, fnam, feature):
        pass

    def get_population(self, fnam, feature):
        # Optional: will not be able to obtain this from all sources
        # TODO: get a rough value using Facebook population density data!!! ========================================================
        pass

    #===========================================================#
    #                  Multi-Polygon to Polygons                #
    #===========================================================#

    def _multi_polygon_to_polygons(self, feature):
        out = []
        #print(feature['geometry'])
        for polygon in feature['geometry']['coordinates']:
            out.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': polygon
                },
                'properties': feature['properties']
            })
        return out

    #===========================================================#
    #                  Find Center Point-Related                #
    #===========================================================#

    def _get_center_point_features(self, features):
        center_points = []
        for feature in features:
            center_points.append({
                'type': 'Point',
                'geometry': polylabel(feature['geometry'],
                                      precision=1.0),
                'properties': feature['properties']
            })
        return center_points

    def _get_area(self, coordinates):
        min_x = 999999999999
        min_y = 999999999999
        max_x = -999999999999
        max_y = -999999999999

        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                x = coordinates[i][j][0]
                y = coordinates[i][j][1]

                if x > max_x: max_x = x;
                if x < min_x: min_x = x;
                if y > max_y: max_y = y;
                if y < min_y: min_y = y;

        return (
            (max_x - min_x) *
            (max_y - min_y)
        )

    def _get_bounding_coords(self, coordinates):
        min_x = 999999999999
        min_y = 999999999999
        max_x = -999999999999
        max_y = -999999999999

        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                x = coordinates[i][j][0]
                y = coordinates[i][j][1]

                if x > max_x: max_x = x;
                if x < min_x: min_x = x;
                if y > max_y: max_y = y;
                if y < min_y: min_y = y;

        return min_x, min_y, max_x, max_y

    def _get_center(self, coordinates):
        min_x = 999999999999
        min_y = 999999999999
        max_x = -999999999999
        max_y = -999999999999

        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                x = coordinates[i][j][0]
                y = coordinates[i][j][1]

                if x > max_x: max_x = x;
                if x < min_x: min_x = x;
                if y > max_y: max_y = y;
                if y < min_y: min_y = y;

        centerX = min_x + (max_x - min_x) / 2.0
        centerY = min_y + (max_y - min_y) / 2.0
        return [centerX, centerY]

