import os
import random

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from configparser import ConfigParser, ExtendedInterpolation

from database.users_table import create_user, get_user, update_user_status, update_user_code, STATUS_VERIFY, STATUS_NOT_VERIFY
from database.db import get_connection
from captcha.image import ImageCaptcha


conf_parser = ConfigParser(interpolation=ExtendedInterpolation())
conf_parser.read(os.path.abspath("config.ini"))

app = Client(
                "captcha_bot",
                api_id=conf_parser["pyrogram"]['api_id'],
                api_hash=conf_parser["pyrogram"]['api_hash']
            )


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
    captcha_text = str(random.randint(1000, 99999))

    image.generate(captcha_text)

    captcha_image_path = "images/" + captcha_text + '.png'

    # write the image on the given file and save it
    image.write(captcha_text, captcha_image_path)

    return (captcha_image_path, captcha_text)


@app.on_message(filters.chat(chats=[conf_parser["telegram"]["group_id"]]))
def new_users_handler(client, message):
    if message.service and message.new_chat_members:
        for user in message.new_chat_members:
            try:
                client.restrict_chat_member(
                    chat_id=int(message.chat.id),
                    user_id=int(user.id),
                    permissions=ChatPermissions(can_send_messages=False)
                )
                text = "Hello {}, welcome to {}. " \
                       "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                       "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                    str(get_name(user)), str(message.chat.title), "3")

                captcha = get_captcha()

                client.send_photo(chat_id=user.id, photo=os.path.abspath(captcha[0]), caption=text)
                conn = get_connection()
                data = {
                    "name": get_name(user),
                    "chat_id": str(user.id),
                    "code": str(captcha[1]),
                }

                if get_user(conn, str(user.id)) == None:
                    create_user(conn, data)

                conn.close()
            except Exception as e:
                print(e)


@app.on_message(filters.private)
def handle_captcha(client, message):
    conn = get_connection()
    user = get_user(conn, message.chat.id)
    if user and str(user["code"]).strip() == str(message.text).strip():
        client.send_message(chat_id=int(message.from_user.id), text="Done! Now you have access to the group")
        client.restrict_chat_member(
            chat_id=conf_parser["telegram"]["group_id"],
            user_id=int(message.from_user.id),
            permissions=ChatPermissions(can_send_messages=True)
        )
        update_user_status(conn, user["id"], STATUS_VERIFY)
    elif user["status"] == STATUS_NOT_VERIFY:
        text = "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
               "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
            "3")

        captcha = get_captcha()
        client.send_photo(chat_id=message.chat.id, photo=os.path.abspath(captcha[0]), caption=text)
        update_user_code(conn, user["id"], captcha[1])

    conn.close()


app.run()