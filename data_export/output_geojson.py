import json
from os import listdir

from _utility.get_package_dir import get_global_subnational_covid_data_dir, get_package_dir
from world_geodata.get_population_map import get_population_map


GEOJSON_DIR = get_package_dir() / 'world_geodata' / 'output'


def output_geojson():
    for k, (poly_geojson, point_geojson) in _OutputGeoJSON().get_geojson_data().items():
        path_poly = get_global_subnational_covid_data_dir() / 'geojson' / 'poly' / f'{k}.json'
        path_poly.parent.mkdir(parents=True, exist_ok=True)
        with open(path_poly, 'w', encoding='utf-8') as f:
            f.write(json.dumps(poly_geojson, indent=2, ensure_ascii=False))

        path_point = get_global_subnational_covid_data_dir() / 'geojson' / 'point' / f'{k}.json'
        path_point.parent.mkdir(parents=True, exist_ok=True)
        with open(path_point, 'w', encoding='utf-8') as f:
            f.write(json.dumps(point_geojson, indent=2, ensure_ascii=False))


class _OutputGeoJSON:
    def __init__(self):
        self._population_map = get_population_map()

    def get_geojson_data(self):
        r = {}
        for fnam in listdir(GEOJSON_DIR):
            if fnam.endswith('.json'):
                with open(GEOJSON_DIR / fnam, 'r', encoding='utf-8') as f:
                    geojson = json.loads(f.read())
                    out_poly_geojson, out_point_geojson = self.__get_geojson(geojson)
                    r[fnam.replace('.json', '')] = (out_poly_geojson, out_point_geojson)
        return r

    def __get_geojson(self, geojson):
        out_poly_features = []
        out_poly_geojson = {
            'type': 'FeatureCollection',
            'features': out_poly_features
        }

        out_point_features = []
        out_point_geojson = {
            'type': 'FeatureCollection',
            'features': out_point_features
        }

        for region_schema, region_schema_dict in geojson.items():
            for region_parent, region_parent_dict in region_schema_dict.items():
                for region_child, region_child_dict in region_parent_dict.items():
                    for feature in region_child_dict['geodata']:
                        # Convert e.g. [[144.543, -33.5], ...] to
                        # [144543, ...], [-33500, ...] to reduce bandwidth

                        properties = {
                            'region_schema': region_schema,
                            'region_parent': region_parent,
                            'region_child': region_child,
                            'area': feature[0],
                            'bounding_box': feature[1],
                            'point': feature[2],
                            'labels': region_child_dict['label'],
                            'population': self._population_map.get(
                                (region_schema, region_parent, region_child)
                            )
                        }
                        out_poly_features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Polygon',
                                'coordinates': feature[3]
                            },
                            'properties': properties
                        })
                        out_point_features.append({
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Point',
                                'coordinates': feature[2]
                            },
                            'properties': properties
                        })

        return out_poly_geojson, out_point_geojson


