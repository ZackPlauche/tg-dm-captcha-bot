import asyncio
from datetime import datetime, timezone

from telethon import TelegramClient
from telethon.tl.functions.channels import GetAdminLogRequest, EditBannedRequest
from telethon.tl.types import ChannelAdminLogEventsFilter, ChatBannedRights

from database import get_all_users, update_user, get_user, add_user, User
from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_GROUP_SUPERGROUP_ID, MINUTES_UNTIL_KICK, CAPTCHA_MESSAGE_TEMPLATE
from utils import get_image_captcha, get_name_from_tg_user


async def check_user_status():
    for user in get_all_users():
        if user.is_invalid():
            try:
                client = TelegramClient('telethon', TELEGRAM_API_ID, TELEGRAM_API_HASH)
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
                    if int(dialog.id) == int(TELEGRAM_GROUP_SUPERGROUP_ID):
                        target_chat = dialog
                    if int(dialog.id) == user.chat_id:
                        target_user = dialog
                if target_chat and target_user: await client(EditBannedRequest(target_chat, target_user, rights))
                update_user(user.chat_id, status=2)
                await client.disconnect()
            except Exception as e:
                print(e)


async def run():
    print("Run")
    client = TelegramClient('telethon', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()

    try:
        target_chat = None
        async for dialog in client.iter_dialogs():
            if int(dialog.id) == int(TELEGRAM_GROUP_SUPERGROUP_ID):
                target_chat = dialog
        filter_results = ChannelAdminLogEventsFilter(join=True,
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
                                                     delete=False)
        log_request = GetAdminLogRequest(channel=target_chat,
                                         q='',
                                         max_id=0,
                                         min_id=0,
                                         limit=10,
                                         events_filter=filter_results)
        result = await client(log_request)

        for tg_user in result.users:
            tg_user_name = get_name_from_tg_user(tg_user)
            is_new = True
            for event in result.events:
                print(event.date, end='\n\n')
                seconds = (datetime.now(timezone.utc) - event.date).seconds
                if event.user_id == tg_user.id and seconds > 100:
                    is_new = False
                    break
            if is_new:
                user_from_db = get_user(tg_user.id)
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
                    image_captcha_path, image_captcha_text = get_image_captcha()
                    caption = CAPTCHA_MESSAGE_TEMPLATE.format(user_name=tg_user_name, group_name=target_chat.title, minutes=MINUTES_UNTIL_KICK)
                    await client.send_file(entity=tg_user, file=image_captcha_path, caption=caption)
                    new_user = User(chat_id=tg_user.id,
                                    timestamp=datetime.now(),
                                    name=get_name_from_tg_user(tg_user),
                                    code=image_captcha_text,
                                    status=0)
                    add_user(new_user)
    except Exception as e: 
        print(e)
    await client.disconnect()


async def main():
    while True:
        asyncio.ensure_future(run())
        await asyncio.sleep(1)
        asyncio.ensure_future(check_user_status())
        await asyncio.sleep(1)

asyncio.run(main())