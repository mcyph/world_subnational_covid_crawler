import csv
import json
import visvalingamwyatt as vw


def get_id_to_city_names():
    # 国コード	第二行政区画コード	日本語表記	英語表記
    r = {}
    with open('japan_cities.csv',
              'r', encoding='utf-8') as f:
        for item in csv.DictReader(f, delimiter='\t'):
            r[item['第二行政区画コード']] = (item['日本語表記'], item['英語表記'])
    return r


id_to_city_names = get_id_to_city_names()


def process_json(path):
    print(path)

    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    out = []
    for feature in data['features']:
        if not feature['geometry']['coordinates']:
            continue
        #print(feature)

        admin2_code = feature['id']
        try:
            ja, en = id_to_city_names[admin2_code]
        except KeyError:
            import traceback
            traceback.print_exc()
            continue

        coordinates_out = []
        for i_coords in feature['geometry']['coordinates']:
            simplifier = vw.Simplifier(i_coords)
            simplified = (
                [list(i) for i in simplifier.simplify(ratio=0.02)]# or
                #[list(i) for i in simplifier.simplify(number=4)]
            )

            if len(simplified) < 3:
                # Probably can ignore
                continue
            coordinates_out.append(simplified)

        out.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates_out
            },
            "properties": {
                'admin2_code': admin2_code,
                'ja': ja,
                'en': en
            }
        })
    return out


if __name__ == '__main__':
    from os import listdir
    BASE_DIR = '/home/david/Downloads/JapanCityGeoJson-master_/geojson'

    for subdir in listdir(BASE_DIR):
        try:
            int(subdir)
        except ValueError:
            continue

        out_city = []
        dir_ = f'{BASE_DIR}/{subdir}'
        for fnam in listdir(dir_):
            path = f'{dir_}/{fnam}'
            if fnam.endswith('.json'):
                out_city.extend(process_json(path))

        with open(f'{subdir}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(
                {"type": "FeatureCollection", "features": out_city},
                ensure_ascii=False
            ))
