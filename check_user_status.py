import asyncio
from datetime import datetime

from pyrogram import Client
from pyrogram.types import ChatPermissions, ChatEventFilter

from database import get_all_users, update_user, get_user, add_user, User
from settings import (
    TELEGRAM_API_ID, 
    TELEGRAM_API_HASH, 
    TELEGRAM_GROUP_SUPERGROUP_ID, 
    MINUTES_UNTIL_KICK, 
    CAPTCHA_VERIFY_INSTRUCTIONS_MESSAGE
)
from utils import get_image_captcha, get_name_from_tg_user


async def check_user_status():
    for user in get_all_users():
        if user.is_invalid():
            try:
                client = Client("pyrogram_second", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
                await client.start()
                await client.restrict_chat_member(
                    chat_id=int(TELEGRAM_GROUP_SUPERGROUP_ID),
                    user_id=int(user.chat_id),
                    permissions=ChatPermissions(can_send_messages=False)
                )

                await client.stop()

                update_user(user.chat_id, status=2)
            except Exception as e:
                print(e)


async def check_new_users():
    print("check_new_users")
    client = Client(
        "pyrogram_second",
        api_id=TELEGRAM_API_ID,
        api_hash=TELEGRAM_API_HASH
    )

    await client.start()

    try:
        target_chat = await client.get_chat(int(TELEGRAM_GROUP_SUPERGROUP_ID))

        result = client.get_chat_event_log(
            chat_id=int(TELEGRAM_GROUP_SUPERGROUP_ID),
            query='',
            limit=10,
            filters=ChatEventFilter(new_members=True)
        )

        async for event in result:
            if event.action == "member_joined":
                tg_user = event.user
                tg_user_name = get_name_from_tg_user(tg_user)
                seconds_since_join = (datetime.now() - datetime.fromtimestamp(event.date)).seconds
                user_is_new = not seconds_since_join > 2000
                if user_is_new:
                    user_from_db = get_user(tg_user.id)
                    if not user_from_db:

                        await client.restrict_chat_member(chat_id=int(TELEGRAM_GROUP_SUPERGROUP_ID),
                                                          user_id=int(tg_user.id),
                                                          permissions=ChatPermissions(can_send_messages=False))

                        # Send initial captcha
                        image_captcha_path, image_captcha_text = get_image_captcha()
                        caption = CAPTCHA_VERIFY_INSTRUCTIONS_MESSAGE.format(user_name=tg_user_name, 
                                                                             group_name=target_chat.title, 
                                                                             minutes=MINUTES_UNTIL_KICK)
                        await client.send_photo(tg_user.id, image_captcha_path, caption=caption)

                        # Add new user to the database
                        new_user = User(
                            chat_id=tg_user.id,
                            timestamp=datetime.now(),
                            name=get_name_from_tg_user(tg_user),
                            code=image_captcha_text,
                            status=0
                        )
                        add_user(new_user)
    except Exception as e:
        print(e)
    await client.stop()

async def main():
    while True:
        asyncio.ensure_future(check_new_users())
        await asyncio.sleep(1)
        asyncio.ensure_future(check_user_status())
        await asyncio.sleep(1)

asyncio.run(main())