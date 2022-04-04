from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.types import ChannelAdminLogEventsFilter
from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import datetime
from storage import get_ban_list, write_row_to_ban_list
from settings import config
from captcha.image import ImageCaptcha
from storage import update_user_status, get_user
import asyncio
import datetime
import time
import os
import random


def get_name(user):
    name = ""
    try:
        if user.first_name: name += user.first_name
        if user.last_name: name += " " + user.last_name
        return name.strip()
    except: pass

    return name


def get_captcha():
    # Create an image instance of the given size
    image = ImageCaptcha(width=250, height=90)

    # Image captcha text
    captcha_text = str(random.randint(1000, 9999))

    image.generate(captcha_text)

    captcha_image_path = "images/" + captcha_text + '.png'

    # write the image on the given file and save it
    image.write(captcha_text, captcha_image_path)

    return (captcha_image_path, captcha_text)


async def check_user_status():
    for user in get_ban_list():
        created_at = datetime.datetime.strptime(user[1], '%Y-%m-%d %H:%M:%S')
        status = int(user[4])
        delta = datetime.datetime.now() - created_at
        dif_seconds = int(abs(delta.total_seconds()))

        if dif_seconds > 180 and status == 0:
            try:
                client = TelegramClient('telethon', config['api_id'], config['api_hash'])
                await client.start()
                rights = ChatBannedRights(
                    until_date=None,
                    view_messages=True,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    embed_links=True
                )
                target_chat = None
                target_user = None
                async for dialog in client.iter_dialogs():
                    if int(dialog.id) == int(config["group_id"]):
                        target_chat = dialog
                    if int(dialog.id) == int(user[0]):
                        target_user = dialog

                if target_chat and target_user: await client(EditBannedRequest(target_chat, target_user, rights))

                update_user_status(str(user[0]).strip(), 2)
                await client.disconnect()
            except Exception as e:
                print(e)


async def run():
    print("Run")
    client = TelegramClient('telethon', config['api_id'], config['api_hash'])
    await client.start()

    try:
        target_chat = None
        async for dialog in client.iter_dialogs():
            if int(dialog.id) == int(config["group_id"]):
                target_chat = dialog

        filter_results = ChannelAdminLogEventsFilter(
            join=True,
            leave=False,
            invite=False,
            ban=False,
            unban=False,
            kick=False,
            unkick=False,
            promote=False,
            demote=False,
            info=False,
            settings=False,
            pinned=False,
            edit=False,
            delete=False
        )
        log_request = GetAdminLogRequest(
            channel=target_chat,
            q='',
            max_id=0,
            min_id=0,
            limit=10,
            events_filter=filter_results
        )

        result = await client(log_request)

        for tg_user in result.users:
            is_new = True
            for event in result.events:
                print(event.date)
                print()
                delta = datetime.datetime.now(datetime.timezone.utc) - event.date

                if event.user_id == tg_user.id and int(abs(delta.total_seconds())) > 100:
                    is_new = False
                    break
            if is_new:
                user_from_db = get_user(str(tg_user.id))
                if user_from_db is None:
                    rights = ChatBannedRights(
                        until_date=None,
                        view_messages=None,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        embed_links=True
                    )

                    await client(EditBannedRequest(target_chat, tg_user, rights))

                    text = "Hello {}, welcome to {}. " \
                           "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                           "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                        str(get_name(tg_user)), str(target_chat.title), "3")

                    captcha = get_captcha()

                    await client.send_file(entity=tg_user, file=os.path.abspath(captcha[0]), caption=text)

                    data = [
                        str(tg_user.id),
                        datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                        get_name(tg_user),
                        str(captcha[1]),
                        0
                    ]
                    write_row_to_ban_list(data)
    except Exception as e: print(e)

    await client.disconnect()


async def main():
    while True:
        asyncio.ensure_future(run())
        await asyncio.sleep(1)
        asyncio.ensure_future(check_user_status())
        await asyncio.sleep(1)

asyncio.run(main())