import mysql.connector
from configparser import ConfigParser, ExtendedInterpolation

parser = ConfigParser(interpolation=ExtendedInterpolation())
# parser.read(os.path.abspath("config.ini"))
script_path = __file__
cwd = str(script_path).replace("database/db.py", "")
parser.read(cwd + "config.ini")

db_conf = {
        'host': parser['db']['host'],
        'user': parser['db']['user'],
        'passwd': parser['db']['passwd'],
        'database': parser['db']['database'],
        "use_unicode": True,
    }


def get_connection(db=None):
    if db:
        db_conf["database"] = db
    return mysql.connector.connect(**db_conf)


def fetch_all_with_params(conn, query, params):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute(query, params)
    return cursor.fetchall()


def fetch_all(conn, query):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute(query)
    return cursor.fetchall()


def fetch_one(conn, query, params):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute(query, params)
    return cursor.fetchone()


def commit(conn, query, params):
    cursor = conn.cursor(buffered=True, dictionary=True)
    cursor.execute(query, params)
    conn.commit()
    return cursor.lastrowid