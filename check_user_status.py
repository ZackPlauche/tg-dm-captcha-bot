from time import sleep
from pyrogram import Client
from configparser import ConfigParser, ExtendedInterpolation
from database.users_table import get_new_users, delete_user
from database.db import get_connection
from datetime import datetime
import os


conf_parser = ConfigParser(interpolation=ExtendedInterpolation())
conf_parser.read(os.path.abspath("config.ini"))


def run():
    conn = get_connection()
    not_verified_users = get_new_users(conn)

    for user in not_verified_users:
        delta = datetime.now() - user["created_at"]
        dif_seconds = int(abs(delta.total_seconds()))

        app = Client(
            "captcha_bot",
            api_id=conf_parser["pyrogram"]['api_id'],
            api_hash=conf_parser["pyrogram"]['api_hash']
        )
        app.start()

        if dif_seconds > 180:
            try:
                app.ban_chat_member(conf_parser["telegram"]["group_id"], user["chat_id"])

                delete_user(conn, user["id"])
            except Exception as e:
                print(e)

        app.stop()


while True:
    run()
    sleep(5)