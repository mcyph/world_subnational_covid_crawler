import json
import requests
import xmltodict
from urllib.request import urlopen


def get_boundaries(relation_items):
    for item in relation_items:
        pass


def _get_labels_from_relation_id(relation_id):
    """

    """
    xml = urlopen(
        f'https://www.openstreetmap.org/api/0.6/relation/{relation_id}'
    ).read()
    data = xmltodict.parse(xml)


def _get_geojson_from_relation_id(relation_id, properties=None):
    """

    """
    geometry_collection = json.loads(urlopen(
        f'http://polygons.openstreetmap.fr/get_geojson.py?id={relation_id}&params=0'
    ).read())

    r = []

    for geometry in geometry_collection['geometries']:
        assert geometry['type'] == 'MultiPolygon'

        r.extend({
            'type': 'Polygon',
            'coordinates': geometry['coordinates'],
            'properties': properties or {}
        } for geometry in geometry)

    return {
        'type': 'FeatureCollection',
        'features': r
    }


if __name__ == '__main__':
    pass

