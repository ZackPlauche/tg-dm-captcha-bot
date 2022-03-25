from database.tables import list_tables
from database.db import get_connection

conn = get_connection()


def execute(conn, query_list):
    for table in query_list:
        print(table)
        try:
            conn.cursor().execute(table)
        except Exception as e:
            print(e)


execute(conn, list_tables)

conn.close()