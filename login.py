from configparser import ConfigParser, ExtendedInterpolation, os
from pyrogram import Client
import shutil

parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.read(os.path.abspath("config.ini"))


def login_session():
    app = Client(
        "captcha_bot",
        api_id=parser["pyrogram"]['api_id'],
        api_hash=parser["pyrogram"]['api_hash']
    )
    app.start()
    me = app.get_me()
    print(me)
    app.stop()

    shutil.copy("captcha_bot.session", "captcha_kick_user_bot.session")


login_session()