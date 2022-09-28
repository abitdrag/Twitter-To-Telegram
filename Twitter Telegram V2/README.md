# Installation
Install telethon  
`pip install telethon`  
If you already have telethon then update it  
`pip install -U telethon`  
Install twitter API for python  
`pip install tweepy`  
Install configparser for configuration files. Install it if you don't have it already  
`pip install configparser`

# Configuration
1. Configure telegramapis.py
Fill the *telegramapis.py* with telegram phone number, api_id and api_hash. 
Follow this link to get api_id and api_hash on Telegram: https://core.telegram.org/api/obtaining_api_id   
OTP will be sent to official telegram client or as SMS to phone number registered with the client. Login using OTP.   
Once logged in, details will be stored in session file. Further login details will be picked up from that session file.   

2. Configure forwarder.ini   
**telegram_channel:** If the channel is public, use the username of channel. If the channel is private, use its ID. Use telegram API to find ID. You can also forward a message from the channel to \@username_to_id_bot, it will give the id.   
**twitter_source_username:** Add full URL or just the username of Twitter.   

3. API limit   
The API limit is 900 requests per 15 minutes. This application has 2 seconds sleep to make requests. You can prefer to use websocket over REST API if this is a problem.   

# Run   
If you are running from local computer, then keep a separate terminal or CMD and run in that.   
If you are running on a remote server without GUI then run it as a daemon or process.   
For linux servers, screen can be used as:

Create a screen as: 
`screen -S twitter2telegram`   

Run script in screen: 
`python3 twitterforwarder.py`    
Press CTRL+A+D to detach the screen and it will keep running :)   

Reattach by: `screen -r twitter2telegram`

