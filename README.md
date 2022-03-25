# Telegram DM Captcha Bot

## Requirements
- Python 3.6+
- Must have a MySQL Database
- **A telegram user account to use as the bot.**
- **A telegram group with the account you're using as the bot as an Admin.**
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

### 2. Create an empty MySQL Database

### 3. Configure the settings

First, make a copy of the `config.ini.dist` file and rename it to `config.ini`.

For Windows command line:
```cmd
type config.ini.dist > config.ini
```
For Mac / Linux console:
```console
cp config.ini.dist config.ini
```

Then, edit the contents of `config.ini` with your telegram and database credentials.

You can skip the `[pyrogram]` part (those are already taken care of).

```ini
[telegram]
group_id=group_id

[pyrogram]
api_id=...
api_hash=...

[db]
host=localhost
user=root
passwd=pass
database=db_name
```
You might've noticed that so far there's no setting to specify which telegram account is being used. This happens in [Step 5](#5-create-a-telegram-session), but you'll need to do [Step 4](#4-create-the-database-tables) first.

### 4. Create the database tables.

Create the database tables by running the `create_db.py` file after you've added your database credentials to `config.ini`.

### 5. Create a Telegram Session
Create a telegram session by logging into your bot account by running the `login.py` file.

It will prompt you to enter your bot token or phone number, then ask you to enter the code that telegram sent you.

When you're done, the script will end and a `captcha_bot.session` file will be created in your directory.

### 6. Run The Bot

To run the bot fully, the `captcha_tg_bot.py` and `check_user_status.py` files need to be running simultaneously.

How this is done depends on the environment the bot is setup, but a simple version is it can be done in 2 terminal instances (for example, a split window terminal in VSCode).