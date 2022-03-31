import asyncio
from telethon import TelegramClient
from settings import config


async def main():
    client = TelegramClient('captcha_bot', config['api_id'], config['api_hash'])
    await client.start()

asyncio.run(main())