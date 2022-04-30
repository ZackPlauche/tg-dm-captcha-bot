from pyrogram import Client

from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH


def login_session(session):
    app = Client(session, api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
    app.start()
    me = app.get_me()
    print(me)
    app.stop()


if __name__ == '__main__':
    login_session("pyrogram")
    login_session("pyrogram_second")
