import json
from polylabel import polylabel
from os import listdir
from abc import ABC, abstractmethod
from covid_19_au_grab.normalize_locality_name import normalize_locality_name


class ProcessGeoJSONBase(ABC):
    def __init__(self, path, schema_name, parent_key, child_key,
                 name_key=None, center_point_key=None):
        self.path = path

        # Ideally, this should be set by the client,
        # but for convenience I'll add it for now
        self.schema_name = schema_name

        self.parent_key = parent_key

        if child_key is None:
            child_key = lambda i: \
                normalize_locality_name(child_key(i))
        self.child_key = child_key

        self.name_key = name_key

        if center_point_key is None:
            pass

    def process_geojson(self, in_paths, out_path):
        name_map = {}
        new_features = []

        for in_path in in_paths:
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
                if feature['type'] == 'MultiPolygon':
                    features.extend(self._multi_polygon_to_polygons(feature))
                elif feature['type'] == 'Polygon':
                    features.append(feature)
                else:
                    raise Exception(f"Unsupported feature type: {feature}")

            for feature in features:
                if not feature['geometry']:
                    continue
                elif (
                    'unincorporated' in str(feature).lower() and
                    not 'pastoral' in str(feature).lower()
                ):
                    continue

                parent = self.parent_key(feature['properties'])
                child = self.child_key(feature['properties'])

                # Get the printable name
                printable_name = self.name_key(
                    self.schema_name, parent, child
                )

                new_features.append({
                    'type': feature['type'],
                    'geometry': feature['geometry'],
                    'properties': {
                        'schema': self.schema_name,
                        'parent': parent,
                        'child': child,
                        'name': printable_name,
                        'area': self._get_area(feature['geometry']),
                        'coords': self._get_coordinates(feature['geometry'])
                    }
                })

        # Get just the center points as individual features
        center_point_features = \
            self._get_center_point_features(new_features)

        encoded = json.dumps({
            'polygons': {'features': new_features},
            'points': {'features': center_point_features}
        }, separators=(',', ':'))

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(encoded)

    def _largest_only(self, features):
        r = {}

        for feature in features:
            pass

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
            for j in range(len(coordinates)):
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

    def _get_coordinates(self, coordinates):
        min_x = 999999999999
        min_y = 999999999999
        max_x = -999999999999
        max_y = -999999999999

        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                x = coordinates[i][j][0]
                y = coordinates[i][j][1]

                if x > max_x: max_x = x;
                if x < min_x: min_x = x;
                if y > max_y: max_y = y;
                if y < min_y: min_y = y;

        return min_x, min_y, max_x, max_y

    def _find_center(self, coordinates):
        min_x = 999999999999
        min_y = 999999999999
        max_x = -999999999999
        max_y = -999999999999

        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                x = coordinates[i][j][0]
                y = coordinates[i][j][1]

                if x > max_x: max_x = x;
                if x < min_x: min_x = x;
                if y > max_y: max_y = y;
                if y < min_y: min_y = y;

        centerX = min_x + (max_x - min_x) / 2.0
        centerY = min_y + (max_y - min_y) / 2.0
        return [centerX, centerY]

    def _multi_polygon_to_polygons(self, feature):
        out = []
        for polygon in feature['geometry']:
            out.append({
                'type': 'Polygon',
                'geometry': polygon,
                'properties': feature['properties']
            })
        return out


for fnam in listdir('.'):
    if not fnam.endswith('.geojson'):
        continue
    print(fnam)
    get_minified(fnam)
