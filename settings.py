from pathlib import Path

# Build paths like this: BASE_DIR / 'myfile.txt'
BASE_DIR = Path(__file__).resolve().parent

TELEGRAM_API_ID = 286189

TELEGRAM_API_HASH = "5706e205c80a9f21c6f9edccb640dd5c"

# Must be a public group. You can get this by using the IDBot (@myidbot) and running the /getgroupid@myidbot command
TELEGRAM_GROUP_SUPERGROUP_ID = -1001675133744

USER_STORAGE_CSV_PATH = BASE_DIR / 'ban_list.csv'

MINUTES_UNTIL_KICK = 3

# Must contain the "user_name", "group_name", and "minutes" names in brackets.
CAPTCHA_MESSAGE_TEMPLATE = """\
Hello {user_name}, welcome to {group_name}. \
Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. \
If you don't solve this captcha in {minutes} minutes, you will be automatically kicked out of the group. \
"""