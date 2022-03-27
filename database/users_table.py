from database.db import *
import time
import datetime


STATUS_NOT_VERIFY = 0
STATUS_VERIFY = 1
STATUS_ERROR = 2


def create_user(conn, data):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data["status"] = STATUS_NOT_VERIFY
    data["created_at"] = timestamp
    data["updated_at"] = timestamp
    commit(conn, """
            INSERT INTO joined_users
            ( name, chat_id, code, status, created_at, updated_at )
            VALUES (?,?,?,?,?,?)
            """, tuple(data.values()))


def update_user_status(conn, id, status):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    commit(conn, """
            UPDATE joined_users
            SET status = ?, updated_at = ?
            WHERE id = ?
            """, (status, timestamp, id))


def update_user_code(conn, id, code):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    commit(conn, """
            UPDATE joined_users
            SET code = ?, updated_at = ?
            WHERE id = ?
            """, (code, timestamp, id))


def get_new_users(conn):
    return fetch_all_with_params(conn, """
        SELECT *
        FROM joined_users
        WHERE status=:status
            """, {"status": STATUS_NOT_VERIFY})


def get_user(conn, chat_id):
    return fetch_one(conn, """
        SELECT *
        FROM joined_users
        WHERE chat_id=:chat_id
            """, {"chat_id": chat_id})


def delete_user(conn, id):
    commit(conn, """
            DELETE FROM joined_users
            WHERE id=?
            """, (id, ))