import asyncio
import shutil

from telethon import TelegramClient
from pyrogram import Client

from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH


def login_session(session):
    app = Client(session, api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
    app.start()
    me = app.get_me()
    print(me)
    app.stop()

    # shutil.copy("pyrogram.session", "pyrogram_second_session.session")


# async def main():
#     client = TelegramClient(
#         'telethon',
#         TELEGRAM_API_ID,
#         TELEGRAM_API_HASH
#     )
#     await client.start()
#     await client.disconnect()

# asyncio.run(main())
login_session("pyrogram")
login_session("pyrogram_second")
