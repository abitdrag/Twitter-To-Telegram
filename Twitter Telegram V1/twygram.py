import time
from tweetProcessor import *
import dbManager 
import twitterManager 
import sys
import os
import telegramManager

while True:
    # get users from db 
    users = dbManager.list_all_users()
    for user in users:
        try:
            tweetlist = twitterManager.get_user_timeline(user[0], user[2])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('\n**ERROR**\n{0}, {1}, {2}\n{3}\n'.format(exc_type, fname, exc_tb.tb_lineno, str(e)))
            print('Continue with other users ...')
            continue # in case of tweet fetch issue, continue with other users
        
        print('user : ' + str(user))
        # recent_tweets, lastid = findRecents(tweetlist, user[2])
        # print('recent tweets \n' + str(recent_tweets))
        parsed_tweets, lastid = parseTweets(tweetlist)
        messages = createMessage(parsed_tweets)

        # print message
        for message in messages:
            print (message[0])
            print (message[1])
            print ()
        print()

        # then call the sendToTelegram
        # telegramManager.
        # get last post id 

        # update lastid in db
        if lastid != None:
            dbManager.update_post_id_in_userdata(user[1], lastid)
    print('sleep 15 seconds')
    time.sleep(15)