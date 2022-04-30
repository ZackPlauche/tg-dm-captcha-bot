from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

from database import get_user, update_user
from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_GROUP_SUPERGROUP_ID, MINUTES_UNTIL_KICK
from utils import get_image_captcha

app = Client("pyrogram", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)


@app.on_message(filters.private)
async def handle_captcha(client, message):
    try:
        user = get_user(chat_id=message.from_user.id)
        if user and str(user.code).strip() == str(message.text).strip():
            if user.status == 0:
                await client.send_message(chat_id=int(message.from_user.id), text="Done! Now you have access to the group")
                await client.restrict_chat_member(
                    chat_id=TELEGRAM_GROUP_SUPERGROUP_ID,
                    user_id=int(message.from_user.id),
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True
                    )
                )
                update_user(user, status=1)
            elif user.status == 2:
                await client.send_message(chat_id=int(message.from_user.id), text="Time is left. Try to contact with admins")
        elif user.status == 0:
            text = "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                   "If you don't solve this captcha in {minutes} minutes, you will be automatically kicked out of the group.".format(minutes=MINUTES_UNTIL_KICK)
            image_captcha_path, image_captcha_text = get_image_captcha()
            await client.send_photo(chat_id=message.chat.id, photo=image_captcha_path, caption=text)
            update_user(user, code=image_captcha_text)
    except: 
        pass


if __name__ == '__main__':
    app.run()