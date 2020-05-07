import json


def get_key(data, j, k, l, m):
    return data[0][13][0][j][3][k][0][l][0][m][0][::-1]


def get_from_data(data):
    r = []

    j = k = l = m = 0
    while True:
        try:
            name = data[0][13][0][j][5][0][1][0]
            #print(name)
            polygons = []
            polygon = []
        except IndexError:
            break

        while True:
            try:
                get_key(data, j, k, 0, 0)
            except IndexError:
                j += 1
                k = l = m = 0
                break

            while True:
                try:
                    get_key(data, j, k, l, 0)
                except IndexError:
                    k += 1
                    l = m = 0
                    break

                while True:
                    #print(j, k, l, m)
                    try:
                        polygon.append(get_key(data, j, k, l, m))
                        m += 1
                    except IndexError:
                        polygons.append(polygon)
                        polygon = []
                        l += 1
                        m = 0
                        break

        r.append((name, polygons))

    return r


def get_geojson(data):
    from copy import deepcopy

    feature_collection_template = {
        "type": "FeatureCollection",
        "features": []
    }

    for division, polygons in data:
        feature_template = {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": polygons},
            "properties": {"name": division},
            "id": division
        }
        feature_collection_template['features'].append(
            feature_template
        )

    return feature_collection_template


if __name__ == '__main__':
    out = []

    with open('lhd_metro.json', 'r', encoding='utf-8') as f:
        out.extend(get_from_data(json.loads(f.read())))

    with open('lhd_regional.json', 'r', encoding='utf-8') as f:
        out.extend(get_from_data(json.loads(f.read())))

    with open('lhd_nsw.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(get_geojson(out)))
