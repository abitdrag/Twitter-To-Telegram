==============
 Installation
==============

pip install telethon
pip install -U telethon # to upgrade, sometimes pip seems to install older version first time
pip install tweepy # twitter api
pip install configparser # only if it is not already present. python3 probably has a default configparser already.

==========
 Settings
==========

Fill telegramapis.py with telegram phone number, api_id and api_hash. OTP will be sent to official telegram client. If there is none, it may be sent as SMS. Better to already have TG on the number so OTP can be received. Once logged in, details are stored in session file. Further login will be pickedup from the session file. Works on linux and windows.

Fill the forwarder.ini
1. telegram_channel: If it is public channel, just use the username of the channel. If it is private, need its id. ID can be found out using telegram api. Another method is to forward a message from the channel to @username_to_id_bot . It will give the id.

2. twitter_source_username: Can be full url or just the username

API limit: 900 requests per 15 minutes. So, 2 second sleep has been put. Prefer to use websocket over REST api if this is a problem.

=====
 RUN
=====

RUN:
If you're running from local computer, just keep a separate terminal or cmd and run in that.

If you're running on a remote server without GUI, run it as a daemon or process.
For linux can use screen also.
screen -S twitter2telegram
python3 twitterforwarder.py
Press CTRL + A + D to detach the screen. It will keep running.
Reattach by "screen -r twitter2telegram"
screen --list will show all screens