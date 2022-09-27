from telethon.sync import TelegramClient, events
import re 
import time 
import datetime
import sys
import os
import telethon
import tweepy
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'forwarder.ini'

try:
	configParser.read(configFilePath)

	tg_api_id = int(configParser.get('telegram-settings', 'tg_api_id'))
	tg_api_hash = configParser.get('telegram-settings', 'tg_api_hash')
	telegram_channel = configParser.get('telegram-settings', 'telegram_channel')

	twitter_key = configParser.get('twitter-settings', 'twitter_key')
	twitter_secret = configParser.get('twitter-settings', 'twitter_secret')
	twitter_access_token = configParser.get('twitter-settings', 'twitter_access_token')
	twitter_access_token_secret = configParser.get('twitter-settings', 'twitter_access_token_secret')
	twitter_username = configParser.get('twitter-settings', 'twitter_source_username')

except Exception as e:
	print ('Fill up the forwarder.ini properly:', e)
	input(' Press ENTER to exit...')
	sys.exit()

print ('Initializing TG...')
# get platform/machine
phone = '+91xxxxxxxxxx' # main client
platform = str(os.name)
sessionfilename = phone[3:] + '_' + platform + '_tg'
print ('Will use', sessionfilename)
print ('')
clienttg = TelegramClient(sessionfilename, tg_api_id, tg_api_hash)
clienttg.start(phone)
print ('TG account connected!')
print ('')
try:
	telegram_channel = int(telegram_channel)
except:
	telegram_channel = clienttg.get_entity(telegram_channel)
	telegram_channel = telegram_channel.id
dialogs = clienttg.get_dialogs()
name = clienttg.get_entity(int(telegram_channel))
print ('Will forward messages from twitter to telegram: ', name.title)
print ('')

tweepy_auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
tweepy_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(tweepy_auth)


twitter_username = twitter_username.split('/')[-1]
twitter_link = 'https://twitter.com/' + twitter_username
tweets_found_old = twitter_api.user_timeline(screen_name=twitter_username, count=1000, tweet_mode='extended')
print ('Started monitoring twitter constantly: ', twitter_link)
print ('Number of tweets found: ', len(tweets_found_old))
print ('')

tweets_found_old = twitter_api.user_timeline(screen_name=twitter_username, count=1, tweet_mode='extended')
while True: # sometimes there is error with tweepy
	now = datetime.datetime.now()
	time.sleep(2) # 900 requests in 15 mins which is 900 seconds (currently checking 450 times per 15 minutes)
	try:
		tweets_found = twitter_api.user_timeline(screen_name=twitter_username, count=1, tweet_mode='extended')
		if tweets_found != tweets_found_old:
			print ('\r ', now.hour, now.minute, now.second, 'New tweet found! ', sep = ' ', end='')
			message_posted = tweets_found[0].full_text
			twitter_urls = tweets_found[0].entities['urls']
			for url in twitter_urls:
				message_posted = message_posted.replace(url['url'], url['expanded_url'])
			print (message_posted)
			clienttg.send_message(telegram_channel,message_posted)
			print ('\n ', now.hour, now.minute, now.second, 'Sent new message to TG',)
			print ()
			tweets_found_old = tweets_found
		else:
			print ('\r ', now.hour, now.minute, now.second, 'No new tweet found yet! ', sep = ' ', end='')
	except Exception as e:
		print ('Error: ', e, 'try again!')



