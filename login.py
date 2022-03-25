import os

from configparser import ConfigParser, ExtendedInterpolation, os
from pyrogram import Client

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


login_session()