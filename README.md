# Telegram DM Captcha Bot

## Requirements
- Python 3.6+
- A telegram user account to use as the bot.
- A **Public** telegram group with the account you're using as the bot as an Admin in that group.
- A telegram core api account (only needed for developers)

## Setup Guide

### 1. Setup Your Python Environment

Your Python environment should be using minimum Python 3.6, then run the following command to install the required packages.

Windows
```cmd
pip install -r requirements.txt
```

Mac / Linux
```console
pip3 install -r requirements.txt
```


### 2. Configure the settings in settings.py

The main setting to edit here is the `TELEGRAM_SUPERGROUP_ID` setting.

To ensure you have the right Supergroup ID, you can add the IDBot (@myidbot) to your public group and run the `/getgroupid@myidbot` command in telegram.

### 3. Create a Telegram Session

Create a telegram session by logging into your bot account by running the `login.py` file.

It will prompt you to enter your bot token or phone number, then ask you to enter the code that telegram sent you.

When you're done, the script will end and a `telethon.session` file and a `pyrogram.session` file will be created in your directory.

### 4. Run The Bot

To run the bot fully, the `pygrogram_handler.py` and `check_user_status.py` files need to be running simultaneously.

Probably in 2 terminal instances.