import sqlite3
from os.path import exists

from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.constants import \
    schema_to_name, datatype_to_name, \
    name_to_schema, name_to_datatype


class DataPointsDB:
    def __init__(self, path):
        path = str(path)
        already_exists = exists(path)
        self.path = path

        if not already_exists:
            self.__create_tables()

        self.conn = sqlite3.connect(
            self.path, detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.conn.execute('PRAGMA journal_mode = WAL;')
        self.conn.execute('PRAGMA cache_size = -512000;')  # 512MB
        self.conn.execute('PRAGMA SYNCHRONOUS = 0;')

    def __create_tables(self):
        sql = open(get_package_dir() / 'db' / 'datapoints.sql',
                   'r', encoding='utf-8').read()
        conn = sqlite3.connect(self.path)
        with conn:
            conn.executescript(sql)
        conn.close()

    def migrate_source_ids(self, path, source_ids):
        """
        Copy across non-derived datapoints from one DB to the other
        """
        other_inst = DataPointsDB(path)
        for source_id in source_ids:
            datapoints = other_inst.select_many(
                source_id=['=?', [source_id]],
                is_derived=['=?', [0]],
                add_source_url=True
            )
            self.extend(source_id, datapoints)
        other_inst.close()

    def __del__(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def cursor(self):
        return self.conn.cursor()

    def get_source_ids(self):
        r = []
        cur = self.conn.cursor()
        cur.execute('SELECT MIN(source_id) FROM datapoints;')
        value = cur.fetchone()[0]
        if value:
            r.append(value)

        while value:
            cur.execute("""
                SELECT MIN(source_id) 
                FROM datapoints 
                WHERE source_id > ? 
                ORDER BY source_id 
                LIMIT 1;
            """, [value])
            value = cur.fetchone()[0]
            if value:
                r.append(value)

        cur.close()
        return sorted(set(r))

    def get_region_schemas(self):
        r = []
        cur = self.conn.cursor()
        cur.execute('SELECT MIN(region_schema) FROM datapoints;')
        value = cur.fetchone()[0]
        if value:
            r.append(name_to_schema(value))

        while value:
            cur.execute("""
                SELECT MIN(region_schema) 
                FROM datapoints 
                WHERE region_schema > ? 
                ORDER BY region_schema 
                LIMIT 1;
            """, [value])
            value = cur.fetchone()[0]
            if value:
                r.append(name_to_schema(value))

        cur.close()
        return sorted(set(r))

    def get_datatypes_by_region_schema(self, region_schema):
        if isinstance(region_schema, int):
            region_schema = schema_to_name(region_schema)
        region_schema = region_schema.lower()

        cur = self.conn.cursor()
        cur.execute("""
            SELECT DISTINCT datatype 
            FROM datapoints 
            WHERE region_schema = ?;
        """, [region_schema])
        r = [name_to_datatype(i[0]) for i in cur.fetchall()]
        cur.close()
        return sorted(set(r))

    def get_region_parents(self, region_schema):
        if isinstance(region_schema, int):
            region_schema = schema_to_name(region_schema)
        region_schema = region_schema.lower()

        cur = self.conn.cursor()
        cur.execute("""
            SELECT DISTINCT region_parent 
            FROM datapoints 
            WHERE region_schema = ?;
        """, [region_schema])
        r = [i[0] for i in cur.fetchall()]
        cur.close()
        return sorted(set(r))

    #================================================================#
    #                         Delete DataPoints                      #
    #================================================================#

    def delete(self, date_updated=None,
               region_schema=None, region_parent=None, region_child=None,
               agerange=None, datatype=None, value=None,
               is_derived='!= 1'):

        where = []
        values = []

        def _append(col, i):
            if isinstance(i, (list, tuple)):
                where.append('%s %s' % (col, i[0]))

                if col == 'region_schema':
                    values.extend([self.__convert_region_schema(x) for x in i[1]])
                elif col == 'datatype':
                    values.extend([self.__convert_datatype(x) for x in i[1]])
                else:
                    values.extend(i[1])
            else:
                where.append('%s %s' % (col, i))

        if date_updated is not None: _append('date_updated', date_updated)
        if region_schema is not None: _append('region_schema', region_schema)
        if region_parent is not None: _append('region_parent', region_parent)
        if region_child is not None: _append('region_child', region_child)
        if agerange is not None: _append('agerange', agerange)
        if datatype is not None: _append('datatype', datatype)
        if value is not None: _append('date_updated', date_updated)
        if is_derived is not None: _append('is_derived', is_derived)

        query = f"""
            DELETE FROM datapoints 
            WHERE {' AND '.join(where)}
            ;
        """
        cur = self.conn.cursor()
        cur.execute(query, values)
        self.conn.commit()
        cur.close()

    #================================================================#
    #                         Insert DataPoints                      #
    #================================================================#

    def append(self, source_id, datapoint, is_derived=False, cur=None, commit=False):

        cur = cur or self.conn.cursor()

        for x in range(2):
            cur.execute(f"""
                SELECT
                    source_url, source_url_id
                FROM
                    sourceurls
                WHERE
                    source_url = ?
                ;
            """, [datapoint.source_url])
            source_url_map = dict(cur.fetchall())

            if source_url_map:
                break
            else:
                cur.execute(f"""
                    INSERT INTO sourceurls (
                        source_url, source_url_id
                    )
                    VALUES (
                        ?, 
                        coalesce((SELECT MAX(source_url_id)+1 FROM sourceurls), 0)
                    );
                """, [datapoint.source_url])

        query = """
            INSERT INTO datapoints (
                date_updated, region_schema, region_parent, region_child,
                agerange, datatype, `value`, source_url_id, text_match,

                is_derived, date_inserted,
                source_id
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                ?, CURRENT_TIMESTAMP,
                ?
            );
        """
        cur.execute(query, [
            datapoint.date_updated,
            schema_to_name(datapoint.region_schema), datapoint.region_parent, datapoint.region_child,
            datapoint.agerange, datatype_to_name(datapoint.datatype), datapoint.value,
            source_url_map[datapoint.source_url], datapoint.text_match,

            int(is_derived),
            source_id
        ])

        if commit:
            self.conn.commit()
            cur.close()

    def extend(self, source_id, datapoints, is_derived=False):
        cur = self.conn.cursor()

        for x in range(2):
            source_urls = set(str(datapoint.source_url)
                              for datapoint in datapoints)
            cur.execute(f"""
                SELECT
                    source_url, source_url_id
                FROM
                    sourceurls
                WHERE
                    source_url IN ({','.join('?' for _ in source_urls)})
                ;
            """, list(source_urls))
            source_url_map = dict(cur.fetchall())

            for source_url in [i for i in source_urls
                               if i not in source_url_map]:

                if len(source_url_map) == len(source_urls):
                    break
                else:
                    cur.execute(f"""
                        INSERT INTO sourceurls (
                            source_url, source_url_id
                        )
                        VALUES (
                            ?, 
                            coalesce((SELECT MAX(source_url_id)+1 FROM sourceurls), 0)
                        );
                    """, [source_url])

        query = """
            INSERT INTO datapoints (
                date_updated, region_schema, region_parent, region_child,
                agerange, datatype, `value`, source_url_id, text_match,

                is_derived, date_inserted,
                source_id
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, CURRENT_TIMESTAMP,
                ?
            );
        """

        insert = []
        for datapoint in datapoints:
            insert.append([
                datapoint.date_updated,
                schema_to_name(datapoint.region_schema), datapoint.region_parent, datapoint.region_child,
                datapoint.agerange, datatype_to_name(datapoint.datatype), datapoint.value,
                source_url_map[datapoint.source_url], datapoint.text_match,

                int(is_derived),
                source_id
            ])
        cur.executemany(query, insert)
        self.conn.commit()

    #================================================================#
    #                         Select DataPoints                      #
    #================================================================#

    def select_one(self, source_id=None, date_updated=None,
                   region_schema=None, region_parent=None, region_child=None,
                   agerange=None, datatype=None, value=None,
                   is_derived=None,

                   order_by='date_updated ASC', add_source_url=False,
                   _fetch_one=True, limit=None, offset=None):

        where = []
        values = []

        def _append(col, i):
            if isinstance(i, (list, tuple)):
                where.append('%s %s' % (col, i[0]))

                if col == 'region_schema':
                    values.extend([self.__convert_region_schema(x) for x in i[1]])
                elif col == 'datatype':
                    values.extend([self.__convert_datatype(x) for x in i[1]])
                else:
                    values.extend(i[1])
            else:
                where.append('%s %s' % (col, i))

        if source_id is not None: _append('source_id', source_id)
        if date_updated is not None: _append('date_updated', date_updated)
        if region_schema is not None: _append('region_schema', region_schema)
        if region_parent is not None: _append('region_parent', region_parent)
        if region_child is not None: _append('region_child', region_child)
        if agerange is not None: _append('agerange', agerange)
        if datatype is not None: _append('datatype', datatype)
        if value is not None: _append('date_updated', date_updated)
        if is_derived is not None: _append('is_derived', is_derived)

        if order_by:
            order_by = f'ORDER BY {order_by}'
        else:
            order_by = ''

        if _fetch_one:
            assert not limit
            assert not offset
            limit = 'LIMIT 1'
            offset = ''
        else:
            if limit:
                limit = 'LIMIT %s' % int(limit)
            if offset:
                offset = 'OFFSET %s' % int(offset)

        query = f"""
            SELECT 
                date_updated, 
                region_schema, region_parent, region_child,
                agerange, datatype, `value`,
                source_url_id
            FROM
                datapoints
            WHERE
                { ' AND '.join(where) }
            
            {order_by or ''}
            {limit or ''} {offset or ''}
            ;
        """

        cur = self.conn.cursor()
        cur.execute(query, values)
        results = cur.fetchall()
        source_url_ids = set([i[-1] for i in results])

        if add_source_url:
            source_ids = set(str(source_url_id)
                             for source_url_id in source_url_ids)

            cur.execute(f"""
                SELECT
                    source_url_id, source_url
                FROM
                    sourceurls
                WHERE
                    source_url_id IN ({','.join(source_ids)})
                ;
            """)
            source_url_map = dict(cur.fetchall())

        r = []
        for (
            date_updated,
            region_schema, region_parent, region_child,
            agerange, datatype, value,
            source_url_id
        ) in results:
            if add_source_url:
                source_url = source_url_map[source_url_id]
            else:
                source_url = source_url_id

            r.append(DataPoint(
                date_updated=date_updated,
                region_schema=name_to_schema(region_schema),
                region_parent=region_parent,
                region_child=region_child,
                agerange=agerange,
                datatype=name_to_datatype(datatype),
                value=value,
                source_url=str(source_url)
            ))

        if _fetch_one:
            return r[0]
        else:
            return r

    def __convert_region_schema(self, s):
        if isinstance(s, str):
            return s
        else:
            return schema_to_name(s)

    def __convert_datatype(self, s):
        if isinstance(s, str):
            return s
        else:
            return datatype_to_name(s)

    def select_many(self, source_id=None, date_updated=None,
                   region_schema=None, region_parent=None, region_child=None,
                   agerange=None, datatype=None, value=None,
                   is_derived=None,

                   order_by='date_updated ASC', add_source_url=False,
                   limit=None, offset=None):

        return self.select_one(
            source_id=source_id,
            date_updated=date_updated,
            region_schema=region_schema, region_parent=region_parent, region_child=region_child,
            agerange=agerange, datatype=datatype, value=value,
            is_derived=is_derived,

            order_by=order_by, add_source_url=add_source_url,
            limit=limit, offset=offset,

            _fetch_one=False
        )

    def get_datapoints_by_source_id(self, source_id):
        query = f"""
            SELECT 
                date_updated, 
                region_schema, region_parent, region_child,
                agerange, datatype, `value`,
                source_url_id
            FROM
                datapoints
            WHERE
                source_id = ?
            ORDER BY 
                date_updated ASC
            ;
        """
        cur = self.conn.cursor()
        cur.execute(query, [source_id])
        results = cur.fetchall()

        source_url_ids = set([i[-1] for i in results])
        source_url_ids = set(str(source_url_id)
                         for source_url_id in source_url_ids)

        cur.execute(f"""
            SELECT
                source_url_id, source_url
            FROM
                sourceurls
            WHERE
                source_url_id IN ({','.join(source_url_ids)})
            ;
        """)
        source_url_map = dict(cur.fetchall())

        r = []
        for (
            date_updated,
            region_schema, region_parent, region_child,
            agerange, datatype, value,
            source_url_id
        ) in results:
            source_url = source_url_map[source_url_id]

            r.append(DataPoint(
                date_updated=date_updated,
                region_schema=name_to_schema(region_schema),
                region_parent=region_parent,
                region_child=region_child,
                agerange=agerange,
                datatype=name_to_datatype(datatype),
                value=value,
                source_url=str(source_url)
            ))

        return r


if __name__ == '__main__':
    from covid_19_au_grab.db.SQLiteDataRevisions import SQLiteDataRevisions
    from covid_19_au_grab.db.SQLiteDataRevision import SQLiteDataRevision

    rev_date, rev_subid, dt = SQLiteDataRevisions().get_revisions()[0]
    dr = SQLiteDataRevision(rev_date, rev_subid)
    dpdb = DataPointsDB('test.sqlite',
                        #migrate_from_path='test.sqlite'
                        )
    cursor = dpdb.conn.cursor()

    for i in dr:
        dd, mm, yyyy = i['date_updated'].split('/')
        i = DataPoint(
            region_schema=name_to_schema(i['region_schema']),
            region_parent=i['region_parent'],
            region_child=i['region_child'],
            datatype=name_to_datatype(i['datatype']),
            agerange=i['agerange'],
            value=int(i['value']),
            date_updated=f'{yyyy}_{mm}_{dd}',
            source_url=i['source_url'],
            text_match=i['text_match']
        )
        dpdb.append('TEST', i, cur=cursor, commit=False)

    dpdb.commit()
    cursor.close()

    for i in dpdb.select_many(
        date_updated=['>= ?', ['2020_06_01']]
    ):
        print(i)
