from time import sleep
from pyrogram import Client
from settings import config
from database.users_table import get_new_users, delete_user
from database.db import get_connection
from datetime import datetime


def run():
    conn = get_connection()
    not_verified_users = get_new_users(conn)

    for user in not_verified_users:
        print(user)
        # delta = datetime.now() - user["created_at"]
        delta = datetime.now() - datetime.strptime(user["created_at"], '%Y-%m-%d %H:%M:%S')
        dif_seconds = int(abs(delta.total_seconds()))

        app = Client(
            "captcha_kick_user_bot",
            api_id=config['api_id'],
            api_hash=config['api_hash']
        )
        app.start()

        if dif_seconds > 180:
            try:
                try:
                    app.get_chat_members(chat_id=int(config["group_id"]), filter="all", query=user["name"])
                except Exception as e:
                    print(e)

                app.ban_chat_member(int(config["group_id"]), int(user["chat_id"]))

                delete_user(conn, user["id"])
            except Exception as e:
                print(e)

        app.stop()


while True:
    run()
    sleep(5)