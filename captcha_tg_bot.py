from telethon import TelegramClient
from telethon import events
from telethon.tl.functions.messages import AddChatUserRequest
from settings import config
from captcha.image import ImageCaptcha
from database.users_table import create_user, get_user, update_user_status, update_user_code, STATUS_VERIFY, STATUS_NOT_VERIFY
from database.db import get_connection
import os
import random


def get_name(user):
    name = ""
    try:
        if user.first_name: name += user.first_name
        if user.last_name: name += " " + user.last_name
        return name.strip()
    except Exception as e:
        print(e)

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


async def joined_users_handler(event):
    if event.user_joined:
        chat = await event.get_chat()
        joined_users = await event.get_users()

        for j_user in joined_users:
            try:
                conn = get_connection()
                db_user = get_user(conn, str(j_user.id))
                if db_user == None or db_user["status"] == STATUS_NOT_VERIFY:

                    await client.kick_participant(chat, j_user)
                    text = "Hello {}, welcome to {}. " \
                           "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                           "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                        str(get_name(j_user)), str(chat.title), "3")

                    captcha = get_captcha()

                    await client.send_file(entity=j_user, file=os.path.abspath(captcha[0]), caption=text)

                    data = {
                        "name": get_name(j_user.id),
                        "chat_id": str(j_user.id),
                        "code": str(captcha[1]),
                    }
                    create_user(conn, data)

                conn.close()
            except Exception as e:
                print(e)


async def private_message_handler(event):
    if event.is_private:
        tg_user = await event.get_chat()

        conn = get_connection()
        user = get_user(conn, tg_user.id)

        try:
            if user and str(user["code"]).strip() == str(event.text).strip():
                await client.send_message(tg_user, "Done! Now you have access to the group")
                await client(AddChatUserRequest(
                    int(config["group_id"]),
                    tg_user,
                    fwd_limit=100
                ))
                update_user_status(conn, user["id"], STATUS_VERIFY)
            elif user["status"] == STATUS_NOT_VERIFY:
                text = "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                       "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                    "3")

                captcha = get_captcha()
                await client.send_file(entity=tg_user, file=os.path.abspath(captcha[0]), caption=text)
                update_user_code(conn, user["id"], captcha[1])
        except Exception as e:
            print(e)

        conn.close()

with TelegramClient("captcha_bot", api_id=config['api_id'], api_hash=config['api_hash']) as client:
    client.add_event_handler(private_message_handler, events.NewMessage)
    client.add_event_handler(joined_users_handler, events.ChatAction)
    client.run_until_disconnected()