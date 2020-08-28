import os
import json
from os import listdir

from covid_19_au_grab.db.SQLiteDataRevision import SQLiteDataRevision
from covid_19_au_grab.db.SQLiteDataRevisions import SQLiteDataRevisions
from covid_19_au_grab.get_package_dir import \
    get_output_dir, get_global_subnational_covid_data_dir, get_package_dir


def output_tsv_data(time_format, latest_revision_id):
    sqlite_data_revision = SQLiteDataRevision(time_format, latest_revision_id)

    for source_id in sqlite_data_revision.get_source_ids():
        print(f"* {source_id}")

        for datatype in sqlite_data_revision.get_datatypes_by_source_id(source_id):
            print(f"** {source_id} -> {datatype}")
            path = get_global_subnational_covid_data_dir() / 'casedata' / source_id.split('_')[0] / source_id.partition('_')[2] / f'{datatype}.csv'
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                # NOTE: I'm using "thin_datapoints" to reduce the amount of data output on the git repo!
                f.write(sqlite_data_revision.get_tsv_data(source_id, datatype, thin_out=False))


def output_source_info(source_info):
    # Output the source info into a .tsv (tab-separated) file
    with open(get_global_subnational_covid_data_dir() / 'source_info_table.tsv', 'w', encoding='utf-8') as f:
        f.write('source_id\tsource_url\tsource_desc\n')
        for source_id, source_url, source_desc in sorted(source_info):
            f.write(f'{source_id}\t{source_url}\t{source_desc}\n')

    # Output the source info into a .md (markdown) file
    with open(get_global_subnational_covid_data_dir() / 'source_info_table.md', 'w', encoding='utf-8') as f:
        f.write('| source_id | source_url | source_desc |\n')
        f.write('| --- | --- | --- |\n')
        for source_id, source_url, source_desc in sorted(source_info):
            f.write(f'| {source_id} | {source_url} | {source_desc} |\n')


GEOJSON_DIR = get_package_dir() / 'geojson_data' / 'output'


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
                            'labels': region_child_dict['label']
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


def push_to_github():
    repo_dir = str(get_global_subnational_covid_data_dir()).rstrip('/')
    old_dir = os.getcwd()
    os.chdir(repo_dir)

    try:
        os.system('git add .')
        os.system('git commit -m "update data"')
        os.system('git push')
    finally:
        os.chdir(old_dir)


if __name__ == '__main__':
    #sqlite_data_revisions = SQLiteDataRevisions().get_revisions()
    #output_tsv_data(sqlite_data_revisions[0][0], sqlite_data_revisions[0][1])
    output_geojson()
