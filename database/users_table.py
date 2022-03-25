import time
import datetime

from database.db import *

STATUS_NOT_VERIFY = 0
STATUS_VERIFY = 1
STATUS_ERROR = 2


def create_user(conn, data):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data["created_at"] = timestamp
    data["updated_at"] = timestamp
    data["status"] = STATUS_NOT_VERIFY
    commit(conn, """
            INSERT INTO joined_users
            ( chat_id, name, code, status, created_at, updated_at )
            VALUES ( %(chat_id)s, %(name)s, %(code)s, %(status)s, %(created_at)s, %(updated_at)s)
            """, data)


def update_user_status(conn, id, status):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    commit(conn, """
            UPDATE joined_users
            SET status = %s, updated_at = %s
            WHERE id = %s
            """, (status, timestamp, id))


def update_user_code(conn, id, code):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    commit(conn, """
            UPDATE joined_users
            SET code = %s, updated_at = %s
            WHERE id = %s
            """, (code, timestamp, id))


def get_new_users(conn):
    return fetch_all_with_params(conn, """
        SELECT *
        FROM joined_users
        WHERE status = %s
            """, (STATUS_NOT_VERIFY,))


def get_user(conn, chat_id):
    return fetch_one(conn, """
        SELECT *
        FROM joined_users
        WHERE chat_id = %s
            """, (chat_id,))


def delete_user(conn, id):
    commit(conn, """
            DELETE FROM joined_users
            WHERE id = %s
            """, (id, ))