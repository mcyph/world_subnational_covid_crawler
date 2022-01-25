import csv
import codecs
from io import BytesIO, StringIO
from _utility.get_package_dir import get_global_subnational_covid_data_dir
from covid_db.SQLiteDataRevision import SQLiteDataRevision
from data_export.split_csv_into_chunks import split_csv_into_chunks, FIVE_MB


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

            seek_data_dict, data_dict = get_csv_data_for_source_id(sqlite_data_revision, source_id, datatype)

            for schema, seek_data in seek_data_dict.items():
                seek_path = path_parent / 'seek_pos' / f'{country}.{schema}.{source_name}.{datatype}.seek_pos.txt'
                seek_path.parent.mkdir(parents=False, exist_ok=True)

                with open(seek_path, 'w', encoding='utf-8') as f:
                    f.write(seek_data)

            for schema, data in data_dict.items():
                path = path_parent / f'{country}.{schema}.{source_name}.{datatype}.txt'
                with open(path, 'wb') as f:
                    f.write(data)

                if len(data) > FIVE_MB:
                    split_csv_into_chunks(path, chunk_size=FIVE_MB)


class _CSVWriter:
    def __init__(self):
        StreamWriter = codecs.getwriter('utf-8')
        self._csvfile = BytesIO()
        self.csvfile = StreamWriter(self._csvfile)

        self.writer = csv.DictWriter(
            self.csvfile,
            fieldnames=['date', 'region_schema', 'region_parent', 'region_child', 'agerange', 'value']
        )
        self.writer.writeheader()

        self.seek_csvfile = StringIO()
        self.seek_writer = csv.DictWriter(
            self.seek_csvfile,
            fieldnames=['month', 'seek']
        )
        self.seek_writer.writeheader()


def get_csv_data_for_source_id(sqlite_data_revision, source_id, datatype):
    out_dicts_by_schema = {}
    for group_dict, values_by_date in sqlite_data_revision.iter_rows(source_id, datatype):
        for date, value in values_by_date:
            out_dicts_by_schema.setdefault(group_dict['region_schema'], []).append({
                'date': date,
                'region_schema': group_dict['region_schema'],
                'region_parent': group_dict['region_parent'],
                'region_child': group_dict['region_child'],
                'agerange': group_dict['agerange'],
                'value': value
            })

    csv_writers = {}
    for region_schema, out_dicts in out_dicts_by_schema.items():
        writer = csv_writers[region_schema] = _CSVWriter()

        prev_month = None
        for out_dict in sorted(out_dicts, key=lambda x: (x['date'],
                                                         x['region_schema'],
                                                         x['region_parent'],
                                                         x['region_child'],
                                                         x['agerange'])):

            month = out_dict['date'].rpartition('-')[0]
            if not prev_month or month != prev_month:
                writer.seek_writer.writerow({'month': month,
                                             'seek': writer._csvfile.tell()})
                prev_month = month
            writer.writer.writerow(out_dict)

        writer._csvfile.seek(0)
        writer.seek_csvfile.seek(0)

    return (
        {k: writer.seek_csvfile.read() for k, writer in csv_writers.items()},
        {k: writer._csvfile.read() for k, writer in csv_writers.items()}
    )
