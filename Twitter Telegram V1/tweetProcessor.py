import urlextract

# # extract only the recent tweets
# def findRecents(tweets, lastid):
#     results = []
#     for tweet in tweets:
#         if(tweet['id_str'] > lastid):
#             results.append(tweet)
#             lastid = tweet['id_str']
#     return results, lastid

# keep only the essential data 
def parseTweets(tweets):
    results = []
    lastid = None
    for tweet in tweets : 
        # take only new tweets or self-replies
        if tweet['in_reply_to_user_id_str'] == tweet['user']['id_str'] or tweet['in_reply_to_user_id_str'] == None:
            data = {}
            data['created_at'] = tweet['created_at']
            data['id_str'] = tweet['id_str']
            data['full_text'] = tweet['full_text']
            data['in_reply_to_status_id_str'] = tweet['in_reply_to_status_id_str']
            data['name'] = tweet['user']['name']
            data['username'] = tweet['user']['screen_name']
            data['location'] = tweet['user']['location']
            data['url'] = "https://twitter.com/i/web/status/" + tweet['id_str'] # tweet url
            # is_quote_status is used to check is this is a quoted tweet
            if tweet['is_quote_status']:
                data['quoted_status_id'] = tweet['quoted_status_id']
            else :
                data['quoted_status_id'] = None
            # check for image 
            try:
                media_urls = []
                for media in tweet['extended_entities']['media'] :
                    media_urls.append(media['media_url'])
                data['media_urls'] = media_urls                
            except Exception as e:
                pass
            # check for links 
            data['links'] = {}
            for e in tweet['entities']['urls']:
                data['links'][e['url']] = e['expanded_url']
            results.append(data)
        lastid = tweet['id_str']
    return results, lastid

# create the message to be sent to telegram
def createMessage(tweets):
    all_messages = []
    for tweet in tweets:
        text = tweet['full_text']
        # replace the short urls with extended urls
        extractor = urlextract.URLExtract()
        urls = extractor.find_urls(text)
        count = len(urls)
        for url in urls:
            try:
                text = text.replace(url, tweet['links'][url], count)
            except:
                text = text.replace(url, '', count)
        # create the message
        message = ""
        name = tweet['name']
        username = tweet['username']
        tweeturl = tweet['url']
        message = name + ' (@' + username + ')\n' + tweeturl + '\n' + text
        # print (message)
        images = []
        try:
            for image in tweet['media_urls']:
                images.append(image)
                # print (image)
        except:
            pass
        message_with_images = (message, images) # (single_message, [image1, image2])
        # print ()
        all_messages.append(message_with_images) # TO DO - put image into this for telegram sender
    return all_messages
        

