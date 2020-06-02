import sqlite3
from os.path import exists

from covid_19_au_grab.get_package_dir import get_package_dir
from covid_19_au_grab.datatypes.DataPoint import DataPoint
from covid_19_au_grab.datatypes.constants import \
    schema_to_name, constant_to_name, \
    name_to_schema, name_to_constant


class DataPointsDB:
    def __init__(self, path, migrate_from_path=None):
        already_exists = exists(path)
        self.path = path

        if not already_exists:
            self.__create_tables()

        if migrate_from_path:
            assert not already_exists
            self.__migrate_from(migrate_from_path)

        self.conn = sqlite3.connect(
            self.path, detect_types=sqlite3.PARSE_DECLTYPES
        )

    def __create_tables(self):
        sql = open(get_package_dir() / 'db' / 'datapoints.sql',
                   'r', encoding='utf-8').read()
        conn = sqlite3.connect(self.path)
        with conn:
            conn.executescript(sql)
        conn.close()

    def __migrate_from(self, path):
        conn = sqlite3.connect(self.path)

        with conn:
            conn.execute("ATTACH DATABASE ? AS other;", [path])
            conn.execute("""
                INSERT INTO sourceurls
                SELECT * FROM other.sourceurls;
            """)
            conn.execute("""
                INSERT INTO datapoints
                SELECT * FROM other.datapoints;
            """)

        conn.commit()
        conn.execute("""
            DETACH other;
        """)
        conn.close()

    def __del__(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def cursor(self):
        return self.conn.cursor()

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

    def append(self, datapoint, is_derived=False, cur=None, commit=False):

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

                datetime_confirmed, confirmed_uid,
                is_derived, date_inserted
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                NULL, NULL,
                ?, CURRENT_TIMESTAMP
            );
        """
        cur.execute(query, [
            datapoint.date_updated,
            schema_to_name(datapoint.region_schema), datapoint.region_parent, datapoint.region_child,
            datapoint.agerange, constant_to_name(datapoint.datatype), datapoint.value,
            source_url_map[datapoint.source_url], datapoint.text_match,

            int(is_derived)
        ])

        if commit:
            self.conn.commit()
            cur.close()

    def extend(self, datapoints, is_derived=False):
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
            """, source_urls)
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

                datetime_confirmed, confirmed_uid,
                is_derived, date_inserted
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                NULL, NULL,
                ?, CURRENT_TIMESTAMP
            );
        """

        insert = []
        for datapoint in datapoints:
            insert.append([
                datapoint.date_updated,
                schema_to_name(datapoint.region_schema), datapoint.region_parent, datapoint.region_child,
                datapoint.agerange, constant_to_name(datapoint.datatype), datapoint.value,
                source_url_map[datapoint.source_url_id], datapoint.text_match,

                int(is_derived),
            ])
        cur.executemany(query, insert)
        self.conn.commit()

    #================================================================#
    #                         Select DataPoints                      #
    #================================================================#

    def select_one(self, date_updated=None,
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
                datatype=name_to_constant(datatype),
                value=value,
                source_url=str(source_url)
            ))

        if _fetch_one:
            return r[0]
        else:
            return r

    def select_many(self, date_updated=None,
                   region_schema=None, region_parent=None, region_child=None,
                   agerange=None, datatype=None, value=None,
                   is_derived=None,

                   order_by='date_updated ASC', add_source_url=False,
                   limit=None, offset=None):

        return self.select_one(
            date_updated=date_updated,
            region_schema=region_schema, region_parent=region_parent, region_child=region_child,
            agerange=agerange, datatype=datatype, value=value,
            is_derived=is_derived,

            order_by=order_by, add_source_url=add_source_url,
            limit=limit, offset=offset,

            _fetch_one=False
        )


if __name__ == '__main__':
    from covid_19_au_grab.web_interface.CSVDataRevisions import CSVDataRevisions
    from covid_19_au_grab.web_interface.CSVDataRevision import CSVDataRevision

    rev_date, rev_subid, dt = CSVDataRevisions().get_revisions()[0]
    dr = CSVDataRevision(rev_date, rev_subid)
    dpdb = DataPointsDB('test2.sqlite',
                        migrate_from_path='test.sqlite'
                        )
    cursor = dpdb.conn.cursor()

    for i in dr:
        dd, mm, yyyy = i['date_updated'].split('/')
        i = DataPoint(
            region_schema=name_to_schema(i['region_schema']),
            region_parent=i['region_parent'],
            region_child=i['region_child'],
            datatype=name_to_constant(i['datatype']),
            agerange=i['agerange'],
            value=int(i['value']),
            date_updated=f'{yyyy}_{mm}_{dd}',
            source_url=i['source_url'],
            text_match=i['text_match']
        )
        dpdb.append(i, cur=cursor, commit=False)

    dpdb.commit()
    cursor.close()

    for i in dpdb.select_many(
        date_updated=['>= ?', ['2020_06_01']]
    ):
        print(i)
