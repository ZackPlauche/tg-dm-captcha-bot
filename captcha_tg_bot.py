from pyrogram import Client, filters
from database.users_table import create_user, get_user, update_user_status, update_user_code, STATUS_VERIFY, STATUS_NOT_VERIFY
from database.db import get_connection
from captcha.image import ImageCaptcha
from settings import config
from storage import write_row_to_ban_list, rm_from_ban_list
import datetime
import time
import os
import random

app = Client(
                "captcha_bot",
                api_id=config['api_id'],
                api_hash=config['api_hash']
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


@app.on_message(filters.private)
async def handle_captcha(client, message):
    conn = get_connection()
    user = get_user(conn, message.chat.id)
    try:
        print(message)
        if user and str(user["code"]).strip() == str(message.text).strip():
            await client.send_message(chat_id=int(message.from_user.id), text="Done! Now you have access to the group")
            await client.add_chat_members(int(config["group_id"]), int(message.from_user.id))
            update_user_status(conn, user["id"], STATUS_VERIFY)
            rm_from_ban_list(str(message.from_user.id))
        elif user["status"] == STATUS_NOT_VERIFY:
            text = "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                   "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                "3")

            captcha = get_captcha()
            await client.send_photo(chat_id=message.chat.id, photo=os.path.abspath(captcha[0]), caption=text)
            await update_user_code(conn, user["id"], captcha[1])
    except Exception as e:
        print(e)

    conn.close()


@app.on_message(filters.chat(chats=[int(config["group_id"])]))
async def new_users_handler(client, message):
    if message.service and message.new_chat_members:
        for user in message.new_chat_members:
            try:
                conn = get_connection()
                db_user = get_user(conn, str(user.id))
                if db_user == None or db_user["status"] == STATUS_NOT_VERIFY:
                    await client.ban_chat_member(int(message.chat.id), int(user.id))
                    text = "Hello {}, welcome to {}. " \
                           "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                           "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                        str(get_name(user)), str(message.chat.title), "3")

                    captcha = get_captcha()

                    await client.send_photo(chat_id=user.id, photo=os.path.abspath(captcha[0]), caption=text)

                    data = {
                        "name": get_name(user),
                        "chat_id": str(user.id),
                        "code": str(captcha[1]),
                    }
                    create_user(conn, data)

                    ts = time.time()
                    write_row_to_ban_list([str(user.id), datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), data["name"]])

                conn.close()
            except Exception as e:
                print(e)


app.run()