from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from storage import update_user_code, update_user_status, get_user
from captcha.image import ImageCaptcha
from settings import config
import os
import random


app = Client(
                "pyrogram",
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
def handle_captcha(client, message):
    try:
        user = get_user(str(message.from_user.id).strip())

        if user and str(user["code"]).strip() == str(message.text).strip():
            if int(user["status"]) == 0:
                client.send_message(chat_id=int(message.from_user.id), text="Done! Now you have access to the group")
                client.restrict_chat_member(
                    chat_id=config["group_id"],
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

                update_user_status(user["chat_id"], 1)
            elif int(user["status"]) == 2:
                client.send_message(chat_id=int(message.from_user.id), text="Time is left. Try to contact with admins")
        elif int(user["status"]) == 0:
            text = "Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. " \
                   "If you don't solve this captcha in {} minutes, you will be automatically kicked out of the group.".format(
                "3")

            captcha = get_captcha()
            client.send_photo(chat_id=message.chat.id, photo=os.path.abspath(captcha[0]), caption=text)
            update_user_code(user["chat_id"], captcha[1])
    except: pass


app.run()