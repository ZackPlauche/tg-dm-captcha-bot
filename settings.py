TELEGRAM_API_ID = 286189

TELEGRAM_API_HASH = "5706e205c80a9f21c6f9edccb640dd5c"

TELEGRAM_GROUP_SUPERGROUP_ID = -1001675133744  # Must be a public group. You can get this by using the IDBot (@myidbot) and running the /getgroupid@myidbot command

MINUTES_UNTIL_KICK = 3  # Minutes until the bot kicks and unverified user from the group after join.

CAPTCHA_MESSAGE_TEMPLATE = (
    # Can contain dynamic_variables "user_name", "group_name", and "minutes". Format: "Hello, {user_name}!"
    'Hello {user_name}, welcome to {group_name}. ' 
    'Please write a message with the numbers and/or letters that appear in this image to verify that you are a human. ' 
    'If you don\'t solve this captcha in {minutes} minutes, you will be automatically kicked out of the group.'
)


DATABASE_INFO = {
    'user': 'root',
    'password': '3o9L0klt3PNH8tNF',
    'host': '34.121.116.37',
    'port': '3306',
    'dbname': 'user_database',
}