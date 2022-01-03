import csv
import codecs
from io import BytesIO
from _utility.get_package_dir import get_global_subnational_covid_data_dir
from covid_db.SQLiteDataRevision import SQLiteDataRevision


def output_csv_data(time_format, latest_revision_id):
    sqlite_data_revision = SQLiteDataRevision(time_format, latest_revision_id)

    for source_id in sqlite_data_revision.get_source_ids():
        print(f"* {source_id}")

        for datatype in sqlite_data_revision.get_datatypes_by_source_id(source_id):
            print(f"** {source_id} -> {datatype}")
            path_parent = get_global_subnational_covid_data_dir() / 'casedata' / source_id.split('_')[0]
            country = source_id.split('_')[0]
            source_name = source_id.partition('_')[2]
            path_parent.mkdir(parents=True, exist_ok=True)

            with open(path_parent / f'{country}_{source_name}_{datatype}_seek_pos.csv', 'w',
                      encoding='utf-8') as seek_f:
                writer = csv.DictWriter(seek_f, ['month', 'seek'])
                writer.writeheader()

                def on_month_change(month, file_obj):
                    writer.writerow({'month': month,
                                     'seek': file_obj.tell()})

                with open(path_parent / f'{country}_{source_name}_{datatype}.csv', 'wb') as f:
                    f.write(get_csv_data_for_source_id(sqlite_data_revision, source_id, datatype,
                                                       on_month_change=on_month_change))


def get_csv_data_for_source_id(sqlite_data_revision, source_id, datatype,
                               on_month_change=None):
    StreamWriter = codecs.getwriter('utf-8')
    _csvfile = BytesIO()
    csvfile = StreamWriter(_csvfile)

    writer = csv.DictWriter(
        csvfile,
        fieldnames=['date', 'region_schema', 'region_parent', 'region_child', 'agerange', 'value']
    )
    writer.writeheader()

    out_dicts = []
    for group_dict, values_by_date in sqlite_data_revision.iter_rows(source_id, datatype):
        for date, value in values_by_date:
            out_dicts.append({'date': date,
                              'region_schema': group_dict['region_schema'],
                              'region_parent': group_dict['region_parent'],
                              'region_child': group_dict['region_child'],
                              'agerange': group_dict['agerange'],
                              'value': value})

    prev_month = None
    for out_dict in sorted(out_dicts, key=lambda x: (x['date'],
                                                     x['region_schema'],
                                                     x['region_parent'],
                                                     x['region_child'],
                                                     x['agerange'])):

        month = out_dict['date'].rpartition('-')[0]
        if not prev_month or month != prev_month:
            if on_month_change:
                on_month_change(month, _csvfile)
            prev_month = month
        writer.writerow(out_dict)

    _csvfile.seek(0)
    return _csvfile.read()
