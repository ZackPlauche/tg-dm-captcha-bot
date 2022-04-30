from pathlib import Path

# Build paths like this: BASE_DIR / 'myfile.txt'
BASE_DIR = Path(__file__).resolve().parent

DEBUG = False

# Telegram Settings

TELEGRAM_API_ID = 286189

TELEGRAM_API_HASH = "5706e205c80a9f21c6f9edccb640dd5c"

# Must be a public group. You can get this by using the IDBot (@myidbot) and running the /getgroupid@myidbot command
TELEGRAM_GROUP_SUPERGROUP_ID = -1001675133744

# Minutes until the bot kicks and unverified user from the group after join.
MINUTES_UNTIL_KICK = 3

# Must contain the "user_name", "group_name", and "minutes" names in brackets.
CAPTCHA_MESSAGE_TEMPLATE = """\
Hello {user_name}, welcome to {group_name}. \
Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. \
If you don't solve this captcha in {minutes} minutes, you will be automatically kicked out of the group. \
"""

# Database Settings

GOOGLE_CLOUD_INFO = {
    'dbname': 'test_database',
    'projectid': 'telegram-project-347815',
    'instancename': 'tg-dm-captcha-bot',
    'user': 'root',
    'host': '34.121.116.37',
    'port': '3306',
    'password': '3o9L0klt3PNH8tNF',
}


try: 
    from local_settings import * 
except ImportError:
    pass

print('DEBUG:', DEBUG)