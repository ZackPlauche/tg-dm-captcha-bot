import asyncio

from telethon import TelegramClient
from pyrogram import Client

from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH


def login_session():
    app = Client("pyrogram", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
    app.start()
    me = app.get_me()
    print(me)
    app.stop()


async def main():
    client = TelegramClient(
        'telethon',
        TELEGRAM_API_ID,
        TELEGRAM_API_HASH
    )
    await client.start()
    await client.disconnect()

asyncio.run(main())
login_session()
asyncio.run(main())
