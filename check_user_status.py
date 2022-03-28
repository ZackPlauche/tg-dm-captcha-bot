from time import sleep
from pyrogram import Client
from settings import config
from datetime import datetime
from storage import get_ban_list, rm_from_ban_list


def run():
    for user in get_ban_list():
        print(user)
        delta = datetime.now() - datetime.strptime(user[1], '%Y-%m-%d %H:%M:%S')
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
                    app.get_chat_members(chat_id=int(config["group_id"]), filter="all", query=user[2].strip())
                except Exception as e:
                    print(e)

                app.ban_chat_member(int(config["group_id"]), int(user[0].strip()))

                rm_from_ban_list(user[0].strip())
            except Exception as e:
                print(e)

        app.stop()


while True:
    run()
    sleep(10)