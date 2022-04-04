import asyncio
from telethon import TelegramClient
from settings import config
from pyrogram import Client


def login_session():
    app = Client(
        "pyrogram",
        api_id=config['api_id'],
        api_hash=config['api_hash']
    )
    app.start()
    me = app.get_me()
    print(me)
    app.stop()


async def main():
    client = TelegramClient(
        'telethon',
        config['api_id'],
        config['api_hash']
    )
    await client.start()
    await client.disconnect()

asyncio.run(main())

login_session()
asyncio.run(main())
