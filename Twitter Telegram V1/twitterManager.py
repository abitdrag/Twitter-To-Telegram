import re
import configparser
from twython import Twython
import sys
import os

configParser = configparser.RawConfigParser()
configFilePath = r'config.config'
configParser.read(configFilePath)

APP_KEY = configParser.get('api-settings', 'APP_KEY')
APP_SECRET = configParser.get('api-settings', 'APP_SECRET')
OAUTH_TOKEN = configParser.get('api-settings', 'OAUTH_TOKEN') # Access Token here
OAUTH_TOKEN_SECRET = configParser.get('api-settings', 'OAUTH_TOKEN_SECRET')

twitter = Twython(app_key=APP_KEY,
app_secret=APP_SECRET,
oauth_token=OAUTH_TOKEN,
oauth_token_secret=OAUTH_TOKEN_SECRET)

# returns ID of the username
def lookup_id(username):
    try:
        output = twitter.lookup_user(screen_name = username)
        return output[0]['id_str']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))


# returns usernames of the ids as dict
def lookup_usernames(userids):
    try:
        output = twitter.lookup_user(user_id = userids)
        usernames = []
        for i in range(0,len(output)):
            usernames.append(output[i]['screen_name'])
        return usernames
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))


# get tweets of user from oldest to recent order
def get_user_timeline(userid, lastid=None):
    try:
        user_timeline = twitter.get_user_timeline(user_id=userid, since_id=lastid, tweet_mode='extended')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))

    tweetlist = []
    for tweets in user_timeline:
        # create list of tweets
        tweetlist.append(tweets)
    # reverse the tweetlist to get oldest to recent order
    tweetlist = list(reversed(tweetlist))
    return tweetlist

# get last post id 
def get_last_post_id(userid):
    return get_user_timeline(userid)[-1]['id_str']
