from settings import config
from database.tables import list_tables
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_connection():
    con = sqlite3.connect(str(config["db_name"])+".db")

    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(tables)
    if len(tables) == 0:
        for table in list_tables:
            try:
                con.cursor().execute(table)
            except Exception as e:
                print(e)
    return con


def fetch_all_with_params(conn, query, params):
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def fetch_one(conn, query, params):
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchone()


def commit(conn, query, params):
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return cursor.lastrowid