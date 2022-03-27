from configparser import ConfigParser, ExtendedInterpolation, os
from pyrogram import Client
from settings import config
import shutil



def login_session():
    app = Client(
        "captcha_bot",
        api_id=config['api_id'],
        api_hash=config['api_hash']
    )
    app.start()
    me = app.get_me()
    print(me)
    app.stop()

    shutil.copy("captcha_bot.session", "captcha_kick_user_bot.session")


login_session()